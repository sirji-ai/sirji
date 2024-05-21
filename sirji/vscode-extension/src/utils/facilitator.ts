import * as vscode from 'vscode';
import { randomBytes } from 'crypto';
import path from 'path';
import os from 'os';
import * as fs from 'fs';

import { renderView } from './render_view';
import { MaintainHistory } from './maintain_history';
import { spawnAdapter } from './adapter_wrapper';
import { SecretStorage } from './secret_storage';
import { Constants, ACTOR_ENUM, ACTION_ENUM } from './constants';

import { Executor } from './executor/executor';
import { readDependencies } from './executor/extract_file_dependencies';

import { AgentStackManager } from './agent_stack_manager';
import { SessionManager } from './session_manager';

export class Facilitator {
  private context: vscode.ExtensionContext | undefined;
  private projectRootUri: any;
  private projectRootPath: any;
  private sirjiRunId: string = '';
  private chatPanel: vscode.WebviewPanel | undefined;
  private secretManager: SecretStorage | undefined;
  private envVars: any = undefined;
  private historyManager: MaintainHistory | undefined;
  private isPlannerTabShown: Boolean = false;
  private isResearcherTabShown: Boolean = false;
  private isCoderTabShown: Boolean = false;
  private isFirstUserMessage: Boolean = true;
  private stackManager: AgentStackManager = new AgentStackManager();
  private sessionManager: SessionManager | null = null;
  private agentOutputFolderPath: string = '';
  private lastMessageFrom: string = '';
  private sirjiInstallationFolderPath: string = '';
  private sirjiRunFolderPath: string = '';
  private inputFilePath: string = '';

  public constructor(context: vscode.ExtensionContext) {
    const oThis = this;

    oThis.context = context;
  }

  public async init() {
    const oThis = this;

    // Setup Project Folder
    await oThis.selectProjectFolder();

    // Setup folders for run, installed_agents, etc.
    await oThis.initializeFolders();

    // Setup secret manager
    await oThis.setupSecretManager();

    // Open Chat Panel
    await oThis.openChatViewPanel();

    return oThis.chatPanel;
  }

  private async selectProjectFolder(): Promise<void> {
    const oThis = this;

    oThis.projectRootUri = vscode.workspace.workspaceFolders ? vscode.workspace.workspaceFolders[0].uri : null;
    oThis.projectRootPath = oThis.projectRootUri ? oThis.projectRootUri.fsPath : null;

    if (!oThis.projectRootUri) {
      // Prompt user to open a folder
      const openFolderMsg = 'No project folder is open. Please open a folder to proceed.';
      await vscode.window.showErrorMessage(openFolderMsg, 'Open Folder').then(async (selection) => {
        if (selection === 'Open Folder') {
          await vscode.commands.executeCommand('workbench.action.files.openFolder');
          return; // Exit the current command execution to avoid further operations until folder is opened
        }
      });
    }
  }

  private async initializeFolders() {
    const oThis = this;

    oThis.sirjiRunId = Date.now().toString() + '_' + randomBytes(16).toString('hex');

    let rootPath = oThis.context?.globalStorageUri.path || '';

    console.log('-----rootPath------', rootPath);

    let sirjiInstallationFolderPath = path.join(rootPath, 'Sirji');
    oThis.sirjiInstallationFolderPath = sirjiInstallationFolderPath;

    let sessionFolderPath = path.join(sirjiInstallationFolderPath, Constants.SESSIONS);
    let runFolderPath = path.join(sessionFolderPath, oThis.sirjiRunId);
    oThis.sirjiRunFolderPath = runFolderPath;

    let conversationFolderPath = path.join(runFolderPath, 'conversations');
    oThis.agentOutputFolderPath = path.join(runFolderPath, 'agent_output');
    let activeRecipeFolderPath = path.join(sirjiInstallationFolderPath, 'active_recipe');

    let agentSessionsFilePath = path.join(runFolderPath, 'agent_sessions.json');
    let constantsFilePath = path.join(runFolderPath, 'constants.json');
    let recipeFilePath = path.join(activeRecipeFolderPath, 'index.json');
    let installedAgentsFolderPath = path.join(activeRecipeFolderPath, 'agents');
    let fileSummariesFolderPath = path.join(sirjiInstallationFolderPath, 'file_summaries');
    let agentOutputIndexFilePath = path.join(oThis.agentOutputFolderPath, 'index.json');

    fs.mkdirSync(runFolderPath, { recursive: true });
    fs.mkdirSync(conversationFolderPath, { recursive: true });
    fs.mkdirSync(oThis.agentOutputFolderPath, { recursive: true });
    fs.mkdirSync(activeRecipeFolderPath, { recursive: true });
    fs.mkdirSync(fileSummariesFolderPath, { recursive: true });

    fs.writeFileSync(agentOutputIndexFilePath, JSON.stringify({}), 'utf-8');
    fs.writeFileSync(constantsFilePath, JSON.stringify({ project_folder: oThis.projectRootPath }, null, 4), 'utf-8');

    fs.writeFileSync(agentSessionsFilePath, JSON.stringify({ sessions: [] }, null, 4), 'utf-8');
    oThis.sessionManager = new SessionManager(agentSessionsFilePath);

    if (!fs.existsSync(recipeFilePath)) {
      // Copy all the files from defaults folder to the active_recipe folder
      await oThis.copyDirectory(path.join(__dirname, '..', 'defaults'), activeRecipeFolderPath);

      // fs.copyFileSync(path.join(__dirname, '..', 'defaults', 'recipe.json'), recipeFilePath);
      // await oThis.copyDirectory(path.join(__dirname, '..', 'defaults', 'agents'), installedAgentsFolderPath);
      // fs.writeFileSync(path.join(sirjiInstallationFolderPath, 'active_recipe', 'config.json'), '{}', 'utf-8');
    }
  }

  // private async copyDirectory(source: string, destination: string) {
  //   if (!fs.existsSync(destination)) {
  //     fs.mkdirSync(destination, { recursive: true });
  //   }

  //   let items = fs.readdirSync(source);

  //   items.forEach((item) => {
  //     let srcPath = path.join(source, item);
  //     let destPath = path.join(destination, item);
  //     fs.copyFileSync(srcPath, destPath);
  //   });
  // }

  private async copyDirectory(source: string, destination: string) {
    try {
      if (!fs.existsSync(destination)) {
        fs.mkdirSync(destination, { recursive: true });
      }

      let items = fs.readdirSync(source);

      for (const item of items) {
        let srcPath = path.join(source, item);
        let destPath = path.join(destination, item);
        let stats = fs.statSync(srcPath);

        if (stats.isDirectory()) {
          await this.copyDirectory(srcPath, destPath);
        } else {
          fs.copyFileSync(srcPath, destPath);
        }
      }
    } catch (error) {
      console.error(`Error copying directory from ${source} to ${destination}:`, error);
      throw error;
    }
  }

  private async setupSecretManager() {
    const oThis = this;

    oThis.secretManager = new SecretStorage(oThis.context);
    await oThis.retrieveSecret();
  }

  private async openChatViewPanel() {
    const oThis = this;

    oThis.chatPanel = renderView(oThis.context, 'chat', oThis.projectRootUri, oThis.projectRootPath, oThis.sirjiRunId);

    oThis.chatPanel.webview.onDidReceiveMessage(
      async (message: any) => {
        await oThis.handleMessagesFromChatPanel(message);
      },
      undefined,
      (oThis.context || {}).subscriptions
    );
  }

  private async retrieveSecret() {
    const oThis = this;

    oThis.envVars = await oThis.secretManager?.retrieveSecret(Constants.ENV_VARS_KEY);
  }

  private async setSecretEnvVars(data: any) {
    const oThis = this;

    let responseContent;

    try {
      await oThis.secretManager?.storeSecret(Constants.ENV_VARS_KEY, JSON.stringify(data));
      responseContent = {
        success: true,
        message: 'Great! Your environment is all setup and ready to roll! What would you like me to build today?'
      };

      await oThis.retrieveSecret();
    } catch (error) {
      console.log(error);
      responseContent = {
        success: false,
        message: error
      };
    }

    oThis.chatPanel?.webview.postMessage({
      type: 'settingSaved',
      content: { message: responseContent, allowUserMessage: true }
    });
  }

  private async readCoderLogs() {
    const oThis = this;

    const coderConversationFilePath = path.join(oThis.sirjiRunFolderPath, 'logs', 'coder.log');

    let coderLogFileContent = '';

    // TODO P1: remove history manager.
    if (oThis.historyManager?.checkIfFileExists(coderConversationFilePath)) {
      coderLogFileContent = oThis.historyManager?.readFile(coderConversationFilePath);
      // return coderLogFileContent;
    }

    this.chatPanel?.webview.postMessage({
      type: 'coderLogs',
      content: coderLogFileContent
    });
  }

  private async readPlannerLogs() {
    const oThis = this;

    const plannerConversationFilePath = path.join(oThis.sirjiRunFolderPath, 'logs', 'planner.log');

    let plannerLogFileContent = '';
    if (oThis.historyManager?.checkIfFileExists(plannerConversationFilePath)) {
      plannerLogFileContent = oThis.historyManager?.readFile(plannerConversationFilePath);
      // return plannerLogFileContent;
    }

    oThis.chatPanel?.webview.postMessage({
      type: 'plannerLogs',
      content: plannerLogFileContent
    });
  }

  private async readResearcherLogs() {
    const oThis = this;

    const researcherConversationFilePath = path.join(oThis.sirjiRunFolderPath, 'logs', 'researcher.log');

    let researcherLogFileContent = '';
    if (oThis.historyManager?.checkIfFileExists(researcherConversationFilePath)) {
      researcherLogFileContent = oThis.historyManager?.readFile(researcherConversationFilePath);
      // return researcherLogFileContent;
    }

    this.chatPanel?.webview.postMessage({
      type: 'researcherLogs',
      content: researcherLogFileContent
    });
  }

  private async sendWelcomeMessage() {
    const oThis = this;

    oThis.chatPanel?.webview.postMessage({
      type: 'botMessage',
      content: {
        message: 'Hello, I am Sirji. Please wait while I am getting initialized...',
        allowUserMessage: false,
        messageInputText: 'Sirji> is getting initialized... Please wait...'
      }
    });

    try {
      await oThis.setupVirtualEnv();
    } catch (error) {
      oThis.chatPanel?.webview.postMessage({
        type: 'botMessage',
        content: {
          message: `Unable to setup python virtual environment. Error: ${error}`,
          allowUserMessage: false
        }
      });
      return;
    }

    if (!oThis.envVars) {
      oThis.chatPanel?.webview.postMessage({
        type: 'botMessage',
        content: { message: "Please configure your environment by simply tapping on the settings icon. Let's get you all set up and ready to go!", allowUserMessage: false }
      });
    } else {
      oThis.chatPanel?.webview.postMessage({
        type: 'botMessage',
        content: { message: 'I am all setup!', allowUserMessage: false }
      });
    }
  }

  private async setupVirtualEnv(): Promise<void> {
    const oThis = this;

    try {
      await spawnAdapter(oThis.context, oThis.sirjiInstallationFolderPath, oThis.sirjiRunFolderPath, oThis.projectRootPath, path.join(__dirname, '..', 'py_scripts', 'setup_virtual_env.py'), [
        '--venv',
        path.join(oThis.sirjiInstallationFolderPath, 'venv')
      ]);
    } catch (error) {
      oThis.sendErrorToChatPanel(error);
    }
  }

  private writeToFile(filePath: string, content: string, options: any = 'utf-8'): void {
    fs.writeFileSync(filePath, content, options);
  }

  private async handleMessagesFromChatPanel(message: any) {
    const oThis = this;

    switch (message.type) {
      case 'webViewReady':
        await oThis.sendWelcomeMessage();
        console.log('Starting Facilitation...');
        await oThis.initFacilitation('', {
          TO: ACTOR_ENUM.ORCHESTRATOR
        });
        break;

      case 'saveSettings':
        await oThis.setSecretEnvVars(message.content);
        break;

      case 'requestPlannerLogs':
        await oThis.readPlannerLogs();
        break;

      case 'requestResearcherLogs':
        await oThis.readResearcherLogs();
        break;

      case 'requestCoderLogs':
        await oThis.readCoderLogs();
        break;

      case 'userMessage':
        console.log('message.content--------', message.content);

        oThis.inputFilePath = path.join(oThis.sirjiRunFolderPath, 'input.txt');
        fs.writeFileSync(oThis.inputFilePath, message.content, 'utf-8');

        await oThis.initFacilitation(message.content, {
          TO: oThis.lastMessageFrom,
          FROM: ACTOR_ENUM.USER
        });

        break;

      default:
        vscode.window.showErrorMessage(`Unknown message received from chat panel: ${message}`);
    }
  }

  async initFacilitation(rawMessage: string, parsedMessage: any) {
    const oThis = this;

    let keepFacilitating: Boolean = true;
    while (keepFacilitating) {
      oThis.displayParsedMessageSummaryToChatPanel(parsedMessage);
      oThis.lastMessageFrom = parsedMessage?.FROM;
      console.log('rawMessage-------', rawMessage);
      console.log('parsedMessage------', parsedMessage);
      console.log('lastMessageFrom------', oThis.lastMessageFrom);

      const inputFilePath = path.join(oThis.sirjiRunFolderPath, 'input.txt');

      if (parsedMessage.ACTION === 'INVOKE_AGENT' || parsedMessage.ACTION === 'INVOKE_AGENT_EXISTING_SESSION') {
        let agent_id = parsedMessage.TO;

        oThis.stackManager.addAgentId(agent_id);
        let agentCallstack = oThis.stackManager.getStack();

        let sessionId = parsedMessage.ACTION === 'INVOKE_AGENT' ? oThis.sessionManager?.startNewSession(agentCallstack) : oThis.sessionManager?.reuseSession(agentCallstack);

        try {
          await spawnAdapter(oThis.context, oThis.sirjiInstallationFolderPath, oThis.sirjiRunFolderPath, oThis.projectRootPath, path.join(__dirname, '..', 'py_scripts', 'agents', 'invoke_agent.py'), [
            '--agent_id',
            agent_id,
            '--agent_callstack',
            agentCallstack,
            '--agent_session_id',
            sessionId
          ]);
        } catch (error) {
          oThis.sendErrorToChatPanel(error);
          keepFacilitating = false;
        }

        const agentConversationFilePath = path.join(oThis.sirjiRunFolderPath, 'conversations', `${agentCallstack}.${sessionId}.json`);
        console.log('agentConversationFilePath------', agentConversationFilePath);

        const conversationContent = JSON.parse(fs.readFileSync(agentConversationFilePath, 'utf-8'));
        const lastAgentMessage: any = conversationContent.conversations[conversationContent.conversations.length - 1];

        console.log('------lastAgentMessage------', lastAgentMessage);

        rawMessage = lastAgentMessage?.content;

        parsedMessage = lastAgentMessage?.parsed_content;

        fs.writeFileSync(inputFilePath, rawMessage, 'utf-8');

        if (parsedMessage.ACTION == ACTION_ENUM.RESPONSE) {
          oThis.stackManager.removeLastAgentId();
        }
      } else {
        switch (parsedMessage.TO) {
          case ACTOR_ENUM.ORCHESTRATOR:
            console.log('Orchestrator message', parsedMessage);
            try {
              await spawnAdapter(
                oThis.context,
                oThis.sirjiInstallationFolderPath,
                oThis.sirjiRunFolderPath,
                oThis.projectRootPath,
                path.join(__dirname, '..', 'py_scripts', 'agents', 'invoke_orchestator.py')
              );
            } catch (error) {
              oThis.sendErrorToChatPanel(error);
              keepFacilitating = false;
            }

            const orchestratorConversationFilePath = path.join(oThis.sirjiRunFolderPath, 'conversations', 'ORCHESTRATOR.json');
            console.log('orchestratorConversationFilePath-----', orchestratorConversationFilePath);

            let conversationContent = JSON.parse(fs.readFileSync(orchestratorConversationFilePath, 'utf-8'));

            const lastOrchestratorMessage: any = conversationContent.conversations[conversationContent.conversations.length - 1];

            console.log('lastCoderMessage', lastOrchestratorMessage);

            rawMessage = lastOrchestratorMessage?.content;

            parsedMessage = lastOrchestratorMessage?.parsed_content;

            oThis.writeToFile(inputFilePath, rawMessage);
            break;

          case ACTOR_ENUM.USER:
            if (parsedMessage.ACTION === ACTION_ENUM.SOLUTION_COMPLETE) {
              keepFacilitating = false;
              oThis.chatPanel?.webview.postMessage({
                type: 'solutionCompleted',
                content: { message: parsedMessage.BODY, allowUserMessage: true }
              });
            }

            if (parsedMessage.ACTION === ACTION_ENUM.QUESTION) {
              keepFacilitating = false;
              oThis.chatPanel?.webview.postMessage({
                type: 'botMessage',
                content: { message: parsedMessage.BODY, allowUserMessage: true }
              });
            }
            oThis.writeToFile(inputFilePath, rawMessage);
            break;

          case ACTOR_ENUM.EXECUTOR:
            try {
              const executor = new Executor(parsedMessage, oThis.projectRootPath, oThis.agentOutputFolderPath, oThis.sirjiRunFolderPath, oThis.sirjiInstallationFolderPath);
              const executorResp = await executor.perform();

              rawMessage = executorResp.rawMessage;
              parsedMessage = executorResp.parsedMessage;
              oThis.writeToFile(inputFilePath, rawMessage);
            } catch (error) {
              console.log('error------', error);
              console.log('Execution default', parsedMessage);
              oThis.chatPanel?.webview.postMessage({
                type: 'botMessage',
                content: { message: `An error occurred during the execution of the Python script: ${error}`, allowUserMessage: true }
              });
              keepFacilitating = false;
            }
            break;

          default:
            let agent_id = parsedMessage.TO;

            let agentCallstack = oThis.stackManager.getStack();
            let sessionId = oThis.sessionManager?.reuseSession(agentCallstack);

            try {
              await spawnAdapter(
                oThis.context,
                oThis.sirjiInstallationFolderPath,
                oThis.sirjiRunFolderPath,
                oThis.projectRootPath,
                path.join(__dirname, '..', 'py_scripts', 'agents', 'invoke_agent.py'),
                ['--agent_id', parsedMessage.TO, '--agent_callstack', agentCallstack, '--agent_session_id', sessionId]
              );
            } catch (error) {
              oThis.sendErrorToChatPanel(error);
              keepFacilitating = false;
            }

            const agentConversationFilePath = path.join(oThis.sirjiRunFolderPath, 'conversations', `${agentCallstack}.${sessionId}.json`);

            let genericAgentConversationContent = JSON.parse(fs.readFileSync(agentConversationFilePath, 'utf-8'));
            const lastAgentMessage: any = genericAgentConversationContent.conversations[genericAgentConversationContent.conversations.length - 1];

            console.log('------lastAgentMessage------', lastAgentMessage);

            rawMessage = lastAgentMessage?.content;

            parsedMessage = lastAgentMessage?.parsed_content;
            oThis.writeToFile(inputFilePath, rawMessage);

            if (parsedMessage.ACTION == ACTION_ENUM.RESPONSE) {
              oThis.stackManager.removeLastAgentId();
            }
            break;
        }
      }

      const totalTokensUsed = await oThis.calculateTotalTokensUsed();

      oThis.chatPanel?.webview.postMessage({
        type: 'tokenUsed',
        content: {
          message: totalTokensUsed,
          allowUserMessage: false
        }
      });
    }
  }

  private displayParsedMessageSummaryToChatPanel(parsedMessage: any) {
    const oThis = this;

    let contentMessage = null;

    if (!parsedMessage || !parsedMessage.ACTION || parsedMessage.TO == ACTOR_ENUM.USER || !parsedMessage.SUMMARY.trim() || parsedMessage.SUMMARY.trim().toLowerCase() === 'empty') {
      return;
    }

    oThis.chatPanel?.webview.postMessage({
      type: 'botMessage',
      content: {
        message: `${parsedMessage.FROM}: ${parsedMessage.SUMMARY.trim()}`,
        allowUserMessage: false
      }
    });
  }

  private toCoderRelayToChatPanel(parsedMessage: any) {
    const oThis = this;

    let contentMessage = null;

    if (!parsedMessage || !parsedMessage.ACTION) {
      return;
    }

    switch (parsedMessage.ACTION) {
      case ACTION_ENUM.STEPS:
        contentMessage = 'Steps generation done. Proceeding step by step.';
        break;

      default:
        break;
    }

    if (!contentMessage) {
      return;
    }

    oThis.chatPanel?.webview.postMessage({
      type: 'botMessage',
      content: {
        message: contentMessage,
        allowUserMessage: false
      }
    });
  }

  private async calculateTotalTokensUsed() {
    const oThis = this;

    // TODO - we need to read the conversation files of all the agents

    // const coderConversationFilePath = path.join(oThis.sirjiRunId, Constants.CODER_JSON_FILE);
    // const researcherConversationFilePath = path.join(oThis.sirjiRunId, Constants.RESEARCHER_JSON_FILE);
    // const plannerConversationFilePath = path.join(oThis.sirjiRunId, Constants.PLANNER_JSON_FILE);

    // const coderTokensUsed = await oThis.getTokensUsed(coderConversationFilePath);
    // const researcherTokensUsed = await oThis.getTokensUsed(researcherConversationFilePath);
    // const plannerTokensUsed = await oThis.getTokensUsed(plannerConversationFilePath);

    // const totalPromptTokens = coderTokensUsed.prompt_tokens + researcherTokensUsed.prompt_tokens + plannerTokensUsed.prompt_tokens;

    // const totalCompletionTokens = coderTokensUsed.completion_tokens + researcherTokensUsed.completion_tokens + plannerTokensUsed.completion_tokens;

    // const totalPromptTokensValueInDollar = (totalPromptTokens * Constants.PROMPT_TOKEN_PRICE_PER_MILLION_TOKENS) / 1000000.0;
    // const totalCompletionTokensValueInDollar = (totalCompletionTokens * Constants.COMPLETION_TOKEN_PRICE_PER_MILLION_TOKENS) / 1000000.0;

    // return {
    //   total_prompt_tokens: totalPromptTokens,
    //   total_completion_tokens: totalCompletionTokens,
    //   total_prompt_tokens_value: totalPromptTokensValueInDollar,
    //   total_completion_tokens_value: totalCompletionTokensValueInDollar
    // };

    return {
      total_prompt_tokens: 0,
      total_completion_tokens: 0,
      total_prompt_tokens_value: 0,
      total_completion_tokens_value: 0
    };
  }

  private async getTokensUsed(conversationFilePath: string): Promise<any> {
    const oThis = this;

    if (oThis.historyManager?.checkIfFileExists(conversationFilePath)) {
      const conversationContent = JSON.parse(oThis.historyManager?.readFile(conversationFilePath));
      return {
        prompt_tokens: conversationContent.prompt_tokens,
        completion_tokens: conversationContent.completion_tokens
      };
    }

    return {
      prompt_tokens: 0,
      completion_tokens: 0
    };
  }

  private sendErrorToChatPanel(error: any) {
    const oThis = this;

    const detailedErrorMessage = `An error occurred during the execution of the Python script: : ${error}`;

    oThis.chatPanel?.webview.postMessage({
      type: 'botMessage',
      content: { message: detailedErrorMessage, allowUserMessage: true }
    });
  }
}
async function getResponseFromExecutor(parsedMessage: any, oThis: any, rawMessage: string, keepFacilitating: Boolean) {}
