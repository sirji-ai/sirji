import * as vscode from 'vscode';
import { randomBytes } from 'crypto';
import path from 'path';
import * as fs from 'fs';

import { renderView } from './render_view';
import { MaintainHistory } from './maintain_history';
import { spawnAdapter } from './adapter_wrapper';
import { SecretStorage } from './secret_storage';
import { Constants, ACTOR_ENUM, ACTION_ENUM } from './constants';

import { Executor } from './executor/executor';

import { AgentStackManager } from './agent_stack_manager';
import { SessionManager } from './session_manager';
import { TokenManager } from './token_manager';
import { StepManager } from './step_manager';

export class Facilitator {
  private context: vscode.ExtensionContext | undefined;
  private projectRootUri: any;
  private projectRootPath: any;
  private sirjiRunId: string = '';
  private chatPanel: vscode.WebviewPanel | undefined;
  private secretManager: SecretStorage | undefined;
  private envVars: any = undefined;
  private historyManager: MaintainHistory | undefined;
  private stackManager: AgentStackManager = new AgentStackManager();
  private sessionManager: SessionManager | null = null;
  private agentOutputFolderPath: string = '';
  private lastMessageFrom: string = '';
  private sirjiInstallationFolderPath: string = '';
  private sirjiRunFolderPath: string = '';
  private inputFilePath: string = '';
  private tokenManager: TokenManager | undefined;
  private isDebugging: Boolean = false;
  private stepsFolderPath: string = '';
  private stepsManager: StepManager | undefined;
  private aggregateTokenFilePath: string = '';
  private asyncMessagesFolder: string = '';

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

  public getChatPanel() {
    const oThis = this;
    return oThis.chatPanel;
  }

  public revealChatPanel() {
    const oThis = this;
    if (oThis.chatPanel) {
      oThis.chatPanel.reveal(vscode.ViewColumn.One);
    }
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
    oThis.stepsFolderPath = path.join(runFolderPath, 'steps');
    oThis.asyncMessagesFolder = path.join(runFolderPath, 'async_messages');

    console.log('oThis.asyncMessagesFolder------', oThis.asyncMessagesFolder);

    fs.mkdirSync(runFolderPath, { recursive: true });
    fs.mkdirSync(conversationFolderPath, { recursive: true });
    fs.mkdirSync(oThis.agentOutputFolderPath, { recursive: true });
    fs.mkdirSync(studioFolderPath, { recursive: true });
    fs.mkdirSync(fileSummariesFolderPath, { recursive: true });
    fs.mkdirSync(oThis.stepsFolderPath, { recursive: true });

    fs.writeFileSync(agentOutputIndexFilePath, JSON.stringify({}), 'utf-8');
    fs.writeFileSync(fileSummariesIndexFilePath, JSON.stringify({}), 'utf-8');
    fs.writeFileSync(constantsFilePath, JSON.stringify({ project_folder: oThis.projectRootPath }, null, 4), 'utf-8');

    fs.writeFileSync(agentSessionsFilePath, JSON.stringify({ sessions: [] }, null, 4), 'utf-8');
    oThis.sessionManager = new SessionManager(agentSessionsFilePath);
    oThis.stepsManager = new StepManager(oThis.stepsFolderPath);
    oThis.aggregateTokenFilePath = path.join(runFolderPath, 'aggregate_tokens.json');

    oThis.tokenManager = new TokenManager(agentSessionsFilePath, conversationFolderPath, oThis.aggregateTokenFilePath);

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

    return oThis.envVars;
  }

  private async readSecretKeys() {
    const oThis = this;

    const secretKeys = await oThis.retrieveSecret();

    this.chatPanel?.webview.postMessage({
      type: 'showSecretKeys',
      content: secretKeys
    });
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

    const tokenUsedInTheConversation = await oThis.tokenManager?.readFile(oThis.aggregateTokenFilePath);

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
      try {
        console.log('Cleaning up existing runs...');
        await oThis.cleanupExistingRun();
      } catch (error) {
        console.error('Error cleaning up existing runs:', error);
      }

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

  private async requestSteps() {
    const oThis = this;
    const res = await oThis.stepsManager?.readStepsFile();

    oThis.chatPanel?.webview.postMessage({
      type: 'displaySteps',
      content: { message: res }
    });
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

      case 'requestSteps':
        await oThis.requestSteps();
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

      case 'requestSecretKeys':
        await oThis.readSecretKeys();
        break;

      default:
        vscode.window.showErrorMessage(`Unknown message received from chat panel: ${message}`);
    }
  }

  private processMessages = () => {
    const oThis = this;
    try {
      console.log('Processing async messages...');
      if (!fs.existsSync(oThis.asyncMessagesFolder)) {
        return;
      }

      const files = fs.readdirSync(oThis.asyncMessagesFolder);

      const jsonFiles = files
        .filter((file) => file.startsWith('notification_') && file.endsWith('.json'))
        .sort((a, b) => {
          const timestampA = a.match(/notification_(.*)\.json/)?.[1];
          const timestampB = b.match(/notification_(.*)\.json/)?.[1];
          return timestampA && timestampB ? timestampA.localeCompare(timestampB) : 0;
        });

      for (const file of jsonFiles) {
        const filePath = path.join(oThis.asyncMessagesFolder, file);
        try {
          const content = fs.readFileSync(filePath, 'utf-8');
          const message = JSON.parse(content);

          console.log(`Message: ${message.content.message}`);
          oThis.chatPanel?.webview.postMessage({
            type: 'botMessage',
            content: message.content
          });

          fs.unlinkSync(filePath);
        } catch (err) {
          console.error(`Error processing file ${file}:`, err);
        }
      }
    } catch (err) {
      console.error('Error reading async_messages folder:', err);
    }
  };

  async initFacilitation(rawMessage: string, parsedMessage: any) {
    const oThis = this;

    let keepFacilitating: Boolean = true;
    oThis.inputFilePath = path.join(oThis.sirjiRunFolderPath, 'input.txt');

    setInterval(oThis.processMessages, 5000);

    while (keepFacilitating) {
      oThis.displayParsedMessageSummaryToChatPanel(parsedMessage);
      // Todo: Do not call updateSteps if action == 'LOG_STEPS'
      let updateStepsRes = oThis.updateSteps(parsedMessage);

      console.log('parsedMessage +------+', parsedMessage);

      console.log('updateStepsRes------', updateStepsRes);

      if (updateStepsRes && Object.keys(updateStepsRes).length > 0 && updateStepsRes?.shouldDiscard) {
        if (updateStepsRes?.isError) {
          console.log('updateStepsRes------', updateStepsRes);

          let newParsedMessage = {
            FROM: parsedMessage.TO,
            TO: parsedMessage.FROM,
            ACTION: ACTION_ENUM.RESPONSE,
            STEP: 'Empty',
            SUMMARY: 'Empty',
            BODY: '\n' + updateStepsRes?.errorMessage
          };

          let newRawMessage = `***
            FROM: ${newParsedMessage.FROM}
            TO: ${newParsedMessage.TO}
            ACTION: ${newParsedMessage.ACTION}
            STEP: ${newParsedMessage.STEP},
            SUMMARY: ${newParsedMessage.SUMMARY}
            BODY: \n${newParsedMessage.BODY}
            ***`;

          console.log('newRawMessage------', newRawMessage);
          console.log('newParsedMessage------', newParsedMessage);

          rawMessage = newRawMessage;
          parsedMessage = newParsedMessage;

          console.log('oThis.inputFilePath', oThis.inputFilePath);

          oThis.writeToFile(oThis.inputFilePath, newRawMessage);
          console.log('Continuing with the next message...');
          continue;
        }
      }

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
            await oThis.tokenManager?.generateAggregateTokenForAgent(ACTOR_ENUM.ORCHESTRATOR);
            break;

          case ACTOR_ENUM.USER:
            if (parsedMessage.ACTION === ACTION_ENUM.SOLUTION_COMPLETE) {
              try {
                oThis.chatPanel?.webview.postMessage({
                  type: 'botMessage',
                  content: { message: 'The assistant cleanup is in progress. Please wait...', allowUserMessage: false }
                });

                await spawnAdapter(oThis.context, oThis.sirjiInstallationFolderPath, oThis.sirjiRunFolderPath, oThis.projectRootPath, path.join(__dirname, '..', 'py_scripts', 'cleanup.py'));
              } catch (error) {
                oThis.sendErrorToChatPanel(error);
                keepFacilitating = false;
              }

              oThis.chatPanel?.webview.postMessage({
                type: 'botMessage',
                content: { message: 'The cleanup is complete.', allowUserMessage: false }
              });

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
              let agentCallstack = oThis.stackManager.getStack();

              if (parsedMessage.ACTION === ACTION_ENUM.LOG_STEPS) {
                setTimeout(() => {
                  this.requestSteps();
                }, 5000);
              }

              const executor = new Executor(
                parsedMessage,
                oThis.projectRootPath,
                oThis.agentOutputFolderPath,
                oThis.sirjiRunFolderPath,
                oThis.sirjiInstallationFolderPath,
                agentCallstack,
                oThis.stepsFolderPath
              );
              const executorResp = await executor.perform();

              if (
                parsedMessage.ACTION === ACTION_ENUM.INSERT_ABOVE ||
                parsedMessage.ACTION === ACTION_ENUM.INSERT_BELOW ||
                parsedMessage.ACTION === ACTION_ENUM.FIND_AND_REPLACE ||
                parsedMessage.ACTION === ACTION_ENUM.CREATE_PROJECT_FILE
              ) {
                switch (parsedMessage.ACTION) {
                  case ACTION_ENUM.INSERT_ABOVE:
                    let filePath = parsedMessage.BODY.split('FILE_PATH:')[1].split('---')[0].trim();
                    filePath = path.join(oThis.projectRootPath, filePath);
                    await spawnAdapter(oThis.context, oThis.sirjiInstallationFolderPath, oThis.sirjiRunFolderPath, oThis.projectRootPath, path.join(__dirname, '..', 'py_scripts', 'sync_file.py'), [
                      '--file_path',
                      filePath
                    ]);
                    break;
                  case ACTION_ENUM.INSERT_BELOW:
                    let filePathBelow = parsedMessage.BODY.split('FILE_PATH:')[1].split('---')[0].trim();
                    filePathBelow = path.join(oThis.projectRootPath, filePathBelow);
                    await spawnAdapter(oThis.context, oThis.sirjiInstallationFolderPath, oThis.sirjiRunFolderPath, oThis.projectRootPath, path.join(__dirname, '..', 'py_scripts', 'sync_file.py'), [
                      '--file_path',
                      filePathBelow
                    ]);
                    break;

                  case ACTION_ENUM.FIND_AND_REPLACE:
                    let filePathFindAndReplace = parsedMessage.BODY.split('FILE_PATH:')[1].split('---')[0].trim();
                    filePathFindAndReplace = path.join(oThis.projectRootPath, filePathFindAndReplace);
                    await spawnAdapter(oThis.context, oThis.sirjiInstallationFolderPath, oThis.sirjiRunFolderPath, oThis.projectRootPath, path.join(__dirname, '..', 'py_scripts', 'sync_file.py'), [
                      '--file_path',
                      filePathFindAndReplace
                    ]);
                    break;

                  case ACTION_ENUM.CREATE_PROJECT_FILE:
                    const [filePathPart, fileContent] = parsedMessage.BODY.split('---');
                    const createFilePath = filePathPart.replace('File path:', '').trim();
                    let filePathCreate = path.join(oThis.projectRootPath, createFilePath);
                    await spawnAdapter(oThis.context, oThis.sirjiInstallationFolderPath, oThis.sirjiRunFolderPath, oThis.projectRootPath, path.join(__dirname, '..', 'py_scripts', 'sync_file.py'), [
                      '--file_path',
                      filePathCreate
                    ]);
                    break;

                  default:
                    break;
                }
              }

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

          case ACTOR_ENUM.RESEARCHER:
            console.log('Researcher message', parsedMessage);
            try {
              await spawnAdapter(
                oThis.context,
                oThis.sirjiInstallationFolderPath,
                oThis.sirjiRunFolderPath,
                oThis.projectRootPath,
                path.join(__dirname, '..', 'py_scripts', 'agents', 'research_agent.py')
              );
            } catch (error) {
              oThis.sendErrorToChatPanel(error);
              keepFacilitating = false;
            }

            const researcherConversationFilePath = path.join(oThis.sirjiRunFolderPath, 'conversations', 'RESEARCHER.json');
            console.log('researcherConversationFilePath-----', researcherConversationFilePath);

            let researcherConversationContent = JSON.parse(fs.readFileSync(researcherConversationFilePath, 'utf-8'));

            const lastResearcherMessage: any = researcherConversationContent.conversations[researcherConversationContent.conversations.length - 1];

            console.log('lastCoderMessage', lastResearcherMessage);

            rawMessage = lastResearcherMessage?.content;

            parsedMessage = lastResearcherMessage?.parsed_content;

            oThis.writeToFile(inputFilePath, rawMessage);

            await oThis.tokenManager?.generateAggregateTokenForAgent(ACTOR_ENUM.RESEARCHER);
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
              break; 
            }

            const agentConversationFilePath = path.join(oThis.sirjiRunFolderPath, 'conversations', `${agentCallstack}.${sessionId}.json`);

            let genericAgentConversationContent = JSON.parse(fs.readFileSync(agentConversationFilePath, 'utf-8'));
            const lastAgentMessage: any = genericAgentConversationContent.conversations[genericAgentConversationContent.conversations.length - 1];

            console.log('------lastAgentMessage------', lastAgentMessage);

            rawMessage = lastAgentMessage?.content;

            parsedMessage = lastAgentMessage?.parsed_content;
            oThis.writeToFile(inputFilePath, rawMessage);

            if (parsedMessage.ACTION == ACTION_ENUM.RESPONSE) {
              oThis.stepsManager?.updateAllStepsToCompleted(agentCallstack);
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
        parsedMessage.ACTION === 'READ_AGENT_OUTPUT_FILES' ||
        parsedMessage.ACTION === 'LOG_STEPS'
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

  private updateSteps(parsedMessage: any): any {
    const oThis = this;

    let agent_callstack = oThis.stackManager.getStack();
    let stepNumber = parsedMessage.STEP;

    if (!stepNumber || stepNumber === undefined || stepNumber === null) {
      return {};
    }
    stepNumber = Number(stepNumber.replace(/\D/g, ''));

    if (!stepNumber || isNaN(stepNumber)) {
      return {};
    }

    setTimeout(() => {
      oThis.requestSteps();
    }, 2000);

    return this.stepsManager?.updateStepStatus(agent_callstack, stepNumber);
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

  private async sendErrorToChatPanel(error: any) {
    const oThis = this;

    const errorLogFilePath = path.join(oThis.sirjiRunFolderPath, 'error.log');
    fs.writeFileSync(errorLogFilePath, error, 'utf-8');

    oThis.chatPanel?.webview.postMessage({
      type: 'botMessage',
      content: { message: 'An error occurred during the execution of the Python script. Working on cleanup. Please wait...', allowUserMessage: false }
    });

    await oThis.cleanup();

    const detailedErrorMessage = `Cleanup done.\nPlease check the error log file at: ${errorLogFilePath}`;

    oThis.chatPanel?.webview.postMessage({
      type: 'botMessage',
      content: { message: detailedErrorMessage, allowUserMessage: true }
    });
  }

  public async cleanup(runPath: string = this.sirjiRunFolderPath) {
    console.log('Performing cleanup tasks...');
    const oThis = this;

    try {
      await spawnAdapter(oThis.context, oThis.sirjiInstallationFolderPath, runPath, oThis.projectRootPath, path.join(__dirname, '..', 'py_scripts', 'cleanup.py'));
      console.log('Cleanup tasks completed.');
    } catch (error) {
      console.error('Error executing cleanup script:', error);
    }
  }

  public async cleanupExistingRun() {
    const oThis = this;

    console.log('Cleaning up existing run...');

    const sessionFolderPath = path.join(oThis.sirjiInstallationFolderPath, Constants.SESSIONS);
    const allRuns = fs.readdirSync(sessionFolderPath);

    allRuns.sort((a, b) => {
      const aTimestamp = parseInt(a.split('_')[0]);
      const bTimestamp = parseInt(b.split('_')[0]);

      return bTimestamp - aTimestamp;
    });

    let runsWithActiveAssistantDetails = [];

    for (let i = 0; i < allRuns.length; i++) {
      const runPath = path.join(sessionFolderPath, allRuns[i]);
      const assistantDetailsFilePath = path.join(runPath, 'assistant_details.json');
      if (fs.existsSync(assistantDetailsFilePath)) {
        const assistantDetails = JSON.parse(fs.readFileSync(assistantDetailsFilePath, 'utf-8'));
        if (assistantDetails.status === 'active') {
          runsWithActiveAssistantDetails.push(allRuns[i]);
        }
      }
    }

    console.log('Existing runs with active assistant:', runsWithActiveAssistantDetails);

    for (let i = 0; i < runsWithActiveAssistantDetails.length; i++) {
      const runPath = path.join(sessionFolderPath, runsWithActiveAssistantDetails[i]);
      console.log('Cleaning up run:', runsWithActiveAssistantDetails[i]);
      await oThis.cleanup(runPath);
      console.log('Cleanup completed for run:', runPath);
    }

    console.log('Existing runs cleanup completed.');
  }
}

async function getResponseFromExecutor(parsedMessage: any, oThis: any, rawMessage: string, keepFacilitating: Boolean) {}
