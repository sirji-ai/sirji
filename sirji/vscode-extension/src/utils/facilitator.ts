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
import { readDependencies } from './executor/read_file_dependencies';

import { AgentStackManager } from './agent_stack_manager';
import { SessionManager } from './session_manager';

export class Facilitator {
  private context: vscode.ExtensionContext | undefined;
  private workspaceRootUri: any;
  private workspaceRootPath: any;
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
  private sharedResourcesFolderPath: string = '';
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

    // Setup workspace
    await oThis.selectWorkspace();

    // Setup folders for run, installed_agents, etc.
    await oThis.initializeFolders();

    // Setup secret manager
    await oThis.setupSecretManager();

    // Open Chat Panel
    oThis.openChatViewPanel();

    return oThis.chatPanel;
  }

  private async selectWorkspace(): Promise<void> {
    const oThis = this;

    oThis.workspaceRootUri = vscode.workspace.workspaceFolders ? vscode.workspace.workspaceFolders[0].uri : null;
    oThis.workspaceRootPath = oThis.workspaceRootUri ? oThis.workspaceRootUri.fsPath : null;

    if (!oThis.workspaceRootUri) {
      // Prompt user to open a folder
      const openFolderMsg = 'No workspace/folder is open. Please open a folder to proceed.';
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
    oThis.sharedResourcesFolderPath = path.join(runFolderPath, 'shared_resources');
    let activeRecipeFolderPath = path.join(sirjiInstallationFolderPath, 'active_recipe');

    let agentSessionsFilePath = path.join(runFolderPath, 'agent_sessions.json');
    let constantsFilePath = path.join(runFolderPath, 'constants.json');
    let recipeFilePath = path.join(activeRecipeFolderPath, 'recipe.json');
    let installedAgentsFolderPath = path.join(activeRecipeFolderPath, 'agents');
    let fileSummariesFolderPath = path.join(sirjiInstallationFolderPath, 'file_summaries');

    fs.mkdirSync(runFolderPath, { recursive: true });
    fs.mkdirSync(conversationFolderPath, { recursive: true });
    fs.mkdirSync(oThis.sharedResourcesFolderPath, { recursive: true });
    fs.mkdirSync(activeRecipeFolderPath, { recursive: true });
    fs.mkdirSync(fileSummariesFolderPath, { recursive: true });

    fs.writeFileSync(constantsFilePath, JSON.stringify({ workspace_folder: oThis.workspaceRootPath }, null, 4), 'utf-8');
    
    fs.writeFileSync(agentSessionsFilePath, JSON.stringify({sessions: []}, null, 4), 'utf-8');
    oThis.sessionManager = new SessionManager(agentSessionsFilePath);

    if (!fs.existsSync(recipeFilePath)) {
      fs.copyFileSync(path.join(__dirname, '..', 'defaults', 'recipe.json'), recipeFilePath);
      await oThis.copyDirectory(path.join(__dirname, '..', 'defaults', 'agents'), installedAgentsFolderPath);
      fs.writeFileSync(path.join(sirjiInstallationFolderPath, 'active_recipe', 'config.json'), '{}', 'utf-8');
    }
  }

  private async copyDirectory(source: string, destination: string) {
    if (!fs.existsSync(destination)) {
      fs.mkdirSync(destination, { recursive: true });
    }

    let items = fs.readdirSync(source);

    items.forEach((item) => {
      let srcPath = path.join(source, item);
      let destPath = path.join(destination, item);
      fs.copyFileSync(srcPath, destPath);
    });
  }

  private async setupSecretManager() {
    const oThis = this;

    oThis.secretManager = new SecretStorage(oThis.context);
    await oThis.retrieveSecret();
  }

  private openChatViewPanel() {
    const oThis = this;

    oThis.chatPanel = renderView(oThis.context, 'chat', oThis.workspaceRootUri, oThis.workspaceRootPath, oThis.sirjiRunId);

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
        message: 'Hello, I am Sirji. Please wait while i am setting up the workspace...',
        allowUserMessage: false,
        messageInputText: 'Sirji> is setting up the workspace... Please wait...'
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
        content: { message: 'I am all setup! What would you like me to build today?', allowUserMessage: true }
      });
    }
  }

  private async setupVirtualEnv(): Promise<void> {
    const oThis = this;

    try {
      await spawnAdapter(oThis.context, oThis.sirjiInstallationFolderPath, oThis.sirjiRunFolderPath, oThis.workspaceRootPath, path.join(__dirname, '..', 'py_scripts', 'setup_virtual_env.py'), [
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
        if (oThis.isFirstUserMessage) {
          const sharedResourcesIndexFilePath = path.join(oThis.sharedResourcesFolderPath, 'index.json');

          let creatorAgent = 'SIRJI';
          let creatorForlderPath = path.join(oThis.sharedResourcesFolderPath, creatorAgent);
          let problemStatementFilePath = path.join(creatorForlderPath, 'problem.txt');

          let problemStatementFilePathKey = path.join(creatorAgent, 'problem.txt');

          fs.mkdirSync(creatorForlderPath, { recursive: true });
          fs.writeFileSync(problemStatementFilePath, message.content, 'utf-8');

          oThis.writeToFile(problemStatementFilePath, message.content);

          fs.writeFileSync(
            sharedResourcesIndexFilePath,
            JSON.stringify({
              [problemStatementFilePathKey]: {
                description: 'Problem statement from the SIRJI_USER.',
                created_by: creatorAgent
              }
            }),
            'utf-8'
          );

          oThis.isFirstUserMessage = false;

          await oThis.initFacilitation(message.content, {
            TO: ACTOR_ENUM.ORCHESTRATOR
          });
        } else {
          console.log('message.content--------', message.content);

          oThis.inputFilePath = path.join(oThis.sirjiRunFolderPath, 'input.txt');
          fs.writeFileSync(oThis.inputFilePath, message.content, 'utf-8');

          await oThis.initFacilitation(message.content, {
            TO: oThis.lastMessageFrom,
            FROM: ACTOR_ENUM.USER
          });
        }

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

      if (parsedMessage.ACTION === 'INVOKE_AGENT') {
        let agent_id = parsedMessage.TO;

        oThis.stackManager.addAgentId(agent_id)
        
        let agentCallstack = oThis.stackManager.getStack();
        let sessionId = oThis.sessionManager?.startNewSession(agentCallstack);

        try {
          await spawnAdapter(
            oThis.context,
            oThis.sirjiInstallationFolderPath,
            oThis.sirjiRunFolderPath,
            oThis.workspaceRootPath,
            path.join(__dirname, '..', 'py_scripts', 'agents', 'invoke_agent.py'),
            ['--agent_id', agent_id, '--agent_callstack', agentCallstack, '--agent_session_id', sessionId]
          );
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

        if(parsedMessage.ACTION == ACTION_ENUM.RESPONSE) {
          oThis.stackManager.removeLastAgentId();
        }
      } else {
        switch (parsedMessage.TO) {
          case ACTOR_ENUM.ORCHESTRATOR:
            try {
              await spawnAdapter(
                oThis.context,
                oThis.sirjiInstallationFolderPath,
                oThis.sirjiRunFolderPath,
                oThis.workspaceRootPath,
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
              const executor = new Executor(parsedMessage, oThis.workspaceRootPath, oThis.sharedResourcesFolderPath, oThis.sirjiRunFolderPath);
              const executorResp = await executor.perform();

              rawMessage = executorResp.rawMessage;
              parsedMessage = executorResp.parsedMessage;
              oThis.writeToFile(inputFilePath, rawMessage);
            } catch (error) {
              console.log('error------', error);
              console.log('Execution default', parsedMessage);
              oThis.chatPanel?.webview.postMessage({
                type: 'botMessage',
                content: { message: `Executor called with unknown action: ${parsedMessage.ACTION}. Raw message: ${rawMessage}`, allowUserMessage: true }
              });
              keepFacilitating = false;
            }
            break;

          default:
            let agent_id = parsedMessage.TO;

            if (parsedMessage.FROM === ACTOR_ENUM.SHORTLISTER) {
              const readDependenciesResponse = await readDependencies(parsedMessage.BODY, oThis.workspaceRootPath);
              console.log('readDependenciesResponse------', readDependenciesResponse);
              
              let body = parsedMessage.BODY;
              let startIndex = body.indexOf('[');
              let endIndex = body.lastIndexOf(']');
              let pathsString = body.substring(startIndex, endIndex + 1);
              let pathsArray = JSON.parse(pathsString);
              pathsArray.push(...readDependenciesResponse);
              let updatedBody = body.substring(0, startIndex) + JSON.stringify(pathsArray) + body.substring(endIndex + 1);
              parsedMessage.BODY = updatedBody;
              let rawMessageParts = rawMessage.split('BODY:');
              let updateRawMessage = rawMessageParts[0] + 'BODY:\n' + updatedBody + '\n***';
              rawMessage = updateRawMessage;
              oThis.writeToFile(inputFilePath, rawMessage);
            }

            let agentCallstack = oThis.stackManager.getStack();
            let sessionId = oThis.sessionManager?.reuseSession(agentCallstack);

            try {
              await spawnAdapter(
                oThis.context,
                oThis.sirjiInstallationFolderPath,
                oThis.sirjiRunFolderPath,
                oThis.workspaceRootPath,
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

            if(parsedMessage.ACTION == ACTION_ENUM.RESPONSE) {
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
