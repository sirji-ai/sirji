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
import { TokenManager } from './token_manager';

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
  private tokenManager: TokenManager | undefined;
  private isDebugging: Boolean = false;

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
    let studioFolderPath = path.join(sirjiInstallationFolderPath, 'studio');

    let agentSessionsFilePath = path.join(runFolderPath, 'agent_sessions.json');
    let constantsFilePath = path.join(runFolderPath, 'constants.json');
    let recipeFilePath = path.join(studioFolderPath, 'recipes');
    let installedAgentsFolderPath = path.join(studioFolderPath, 'agents');
    let fileSummariesFolderPath = path.join(sirjiInstallationFolderPath, 'file_summaries');
    let fileSummariesIndexFilePath = path.join(fileSummariesFolderPath, 'index.json');
    let agentOutputIndexFilePath = path.join(oThis.agentOutputFolderPath, 'index.json');

    fs.mkdirSync(runFolderPath, { recursive: true });
    fs.mkdirSync(conversationFolderPath, { recursive: true });
    fs.mkdirSync(oThis.agentOutputFolderPath, { recursive: true });
    fs.mkdirSync(studioFolderPath, { recursive: true });
    fs.mkdirSync(fileSummariesFolderPath, { recursive: true });

    fs.writeFileSync(agentOutputIndexFilePath, JSON.stringify({}), 'utf-8');
    fs.writeFileSync(fileSummariesIndexFilePath, JSON.stringify({}), 'utf-8');
    fs.writeFileSync(constantsFilePath, JSON.stringify({ project_folder: oThis.projectRootPath }, null, 4), 'utf-8');

    fs.writeFileSync(agentSessionsFilePath, JSON.stringify({ sessions: [] }, null, 4), 'utf-8');
    oThis.sessionManager = new SessionManager(agentSessionsFilePath);
    oThis.tokenManager = new TokenManager(agentSessionsFilePath, conversationFolderPath, path.join(runFolderPath, 'aggregate_tokens.json'));

    if (!fs.existsSync(recipeFilePath)) {
      // Copy all the files from defaults folder to the studio folder
      await oThis.copyDirectory(path.join(__dirname, '..', 'defaults'), studioFolderPath);

      // fs.copyFileSync(path.join(__dirname, '..', 'defaults', 'recipe.json'), recipeFilePath);
      // await oThis.copyDirectory(path.join(__dirname, '..', 'defaults', 'agents'), installedAgentsFolderPath);
      // fs.writeFileSync(path.join(sirjiInstallationFolderPath, 'studio', 'config.json'), '{}', 'utf-8');
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
        message: 'Great! Your environment is all setup and ready to roll!'
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
      content: { message: responseContent, allowUserMessage: false }
    });
  }

  private async readLogs(fileName: string) {
    const oThis = this;
    const logsFilePath = path.join(oThis.sirjiInstallationFolderPath, 'sessions', oThis.sirjiRunId, 'logs', `${fileName}.log`);
    let logFileContent = '';

    if (fs.existsSync(logsFilePath)) {
      logFileContent = fs.readFileSync(logsFilePath, 'utf-8');
    }

    oThis.chatPanel?.webview.postMessage({
      type: 'displayLogs',
      content: { fileName, logFileContent }
    });

    return logFileContent;
  }

  private async requestAvailableHeaderLogs() {
    const oThis = this;

    const logsFilePath = path.join(oThis.sirjiInstallationFolderPath, 'sessions', oThis.sirjiRunId, 'logs');
    const logsFiles = fs.readdirSync(logsFilePath);

    let availableLogs = logsFiles.map((file) => {
      return file.replace('.log', '');
    });

    oThis.chatPanel?.webview.postMessage({
      type: 'availableHeaderLogs',
      content: availableLogs
    });
  }

  private async getTokenUsedAgentWise() {
    const oThis = this;

    const tokenUsedInTheConversation = await oThis.tokenManager?.getTokenUsedInConversation();

    console.log('tokenUsedInTheConversation------', tokenUsedInTheConversation);

    oThis.chatPanel?.webview.postMessage({
      type: 'tokenUsesByAgent',
      content: {
        message: tokenUsedInTheConversation,
        allowUserMessage: false
      }
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
      console.log('Starting Facilitation...');
      await oThis.initFacilitation('', {
        TO: ACTOR_ENUM.ORCHESTRATOR
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
        break;

      case 'saveSettings':
        await oThis.setSecretEnvVars(message.content);
        console.log('Starting Facilitation...');
        await oThis.initFacilitation('', {
          TO: ACTOR_ENUM.ORCHESTRATOR
        });
        break;

      case 'requestAvailableHeaderLogs':
        await oThis.requestAvailableHeaderLogs();
        break;

      case 'requestTokenUsage':
        await oThis.getTokenUsedAgentWise();
        break;

      case 'requestLogs':
        await oThis.readLogs(message.content);
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
            await oThis.tokenManager?.generateAggregateTokenForOrchestrator();
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

      await oThis.tokenManager?.generateAggregateTokens();

      const totalTokensUsed = await oThis.calculateTotalTokensUsed();

      console.log('totalTokensUsed------', totalTokensUsed);

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

    if (!oThis.isDebugging) {
      if (
        parsedMessage.ACTION === 'INVOKE_AGENT' ||
        parsedMessage.ACTION === 'STORE_IN_AGENT_OUTPUT' ||
        parsedMessage.ACTION === 'FETCH_RECIPE_INDEX' ||
        parsedMessage.ACTION === 'FETCH_RECIPE' ||
        parsedMessage.ACTION === 'READ_AGENT_OUTPUT_FILES'
      ) {
        return;
      }
    }

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
    return await oThis.tokenManager?.getAggregateTokensUsedInConversation();
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
