import * as vscode from 'vscode';
import { randomBytes } from 'crypto';
import path from 'path';
import os from 'os';

import { renderView } from './render_view';
import { MaintainHistory } from './maintain_history';
import { invokeAgent } from './invoke_agent';
import { SecretStorage } from './secret_storage';
import { Constants, ACTOR_ENUM, ACTION_ENUM } from './constants';
import { openBrowser } from './open_browser';
import { executeCommand } from './execute_command';
import { createFile } from './create_file';
import { readContent } from './read_content';
import { readDirectoryStructure } from './read_directory_structure';
import { executeTask } from './execute_task';
import { executeSpawn } from './execute_spawn';
import { appendToSharedResourcesIndex } from './append_to_shared_resources_index';
import { readSharedResourcesIndex } from './read_shared_resource_index';

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
  private sessionManager: MaintainHistory | undefined;
  private isFirstUserMessage: Boolean = true;
  private sharedResourcesFolderPath: string = '';
  private lastMessageFrom: string = '';

  public constructor(context: vscode.ExtensionContext) {
    const oThis = this;

    oThis.context = context;
  }

  public async init() {
    const oThis = this;

    // Setup workspace
    await oThis.selectWorkspace();

    // Setup Environment
    await oThis.setupEnvironment();

    // Setup secret manager
    await oThis.setupSecretManager();

    // Open Chat Panel
    oThis.openChatViewPanel();

    return oThis.chatPanel;
  }

  private async setupEnvironment() {
    const oThis = this;
    oThis.sirjiRunId = randomBytes(16).toString('hex');
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

  private async setupHistoryManager() {
    const oThis = this;
    oThis.historyManager = new MaintainHistory();

    oThis.historyManager.createHistoryFolder(oThis.workspaceRootPath, oThis.sirjiRunId);

    let sessionManager = new MaintainHistory();

    let rootPath = os.homedir();

    let sessionFolderPath = path.join(rootPath, 'Documents', 'Sirji', Constants.SESSIONS);
    let conversationFolderPath = path.join(sessionFolderPath, oThis.sirjiRunId, 'conversations');
    let inputFolderPath = path.join(sessionFolderPath, oThis.sirjiRunId, 'inputs');
    oThis.sharedResourcesFolderPath = path.join(sessionFolderPath, oThis.sirjiRunId, 'shared_resources');
    let constantsFolderPath = path.join(sessionFolderPath, oThis.sirjiRunId, 'constants.json');
    let recipeFolderPath = path.join(rootPath, 'Documents', 'Sirji', 'recipe.json');

    sessionManager.createHistoryFolder(sessionFolderPath, oThis.sirjiRunId);
    sessionManager.createHistoryFolder(conversationFolderPath, oThis.sirjiRunId);
    sessionManager.createHistoryFolder(inputFolderPath, oThis.sirjiRunId);
    sessionManager.createHistoryFolder(oThis.sharedResourcesFolderPath, oThis.sirjiRunId);
    sessionManager.createHistoryFolder(constantsFolderPath, oThis.sirjiRunId);

    sessionManager.writeFile(
      recipeFolderPath,
      JSON.stringify({
        prescribed_tasks: ['Write epics and user stories.', 'Write architecture components.', 'Implement the epic & user stories using the architecture components.'],
        tips: ['Ensure finalized epics & user stories and architecture components are consistent. Address any discrepancies with the user.']
      })
    );
  }

  private async setupSecretManager() {
    const oThis = this;

    oThis.secretManager = new SecretStorage(oThis.context);
    await oThis.retrieveSecret();
  }

  private async retrieveSecret() {
    const oThis = this;

    oThis.envVars = await oThis.secretManager?.retrieveSecret(Constants.ENV_VARS_KEY);
  }

  private async setSecretEnvVars(data: any) {
    const oThis = this;

    let responseContent;
    let rootPath = os.homedir();
    data.SIRJI_INSTALLATION_DIR = rootPath;

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

  private async readCoderLogs() {
    const oThis = this;

    const coderConversationFilePath = path.join(oThis.workspaceRootPath, Constants.HISTORY_FOLDER, oThis.sirjiRunId, 'logs', 'coder.log');

    let coderLogFileContent = '';

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

    const plannerConversationFilePath = path.join(oThis.workspaceRootPath, Constants.HISTORY_FOLDER, oThis.sirjiRunId, 'logs', 'planner.log');

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

    const researcherConversationFilePath = path.join(oThis.workspaceRootPath, Constants.HISTORY_FOLDER, oThis.sirjiRunId, 'logs', 'researcher.log');

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
      await invokeAgent(oThis.context, oThis.workspaceRootPath, oThis.sirjiRunId, path.join(__dirname, '..', 'py_scripts', 'setup_virtual_env.py'), [
        '--venv',
        path.join(oThis.workspaceRootPath, Constants.PYHTON_VENV_FOLDER)
      ]);
    } catch (error) {
      oThis.sendErrorToChatPanel(error);
    }
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
        if (!oThis.historyManager) {
          await oThis.setupHistoryManager();
        }

        if (oThis.isFirstUserMessage) {
          const sharedResourcesIndexFilePath = path.join(oThis.sharedResourcesFolderPath, 'index.json');
          const problemStatementFilePath = path.join(oThis.sharedResourcesFolderPath, 'problem_statement.txt');

          oThis.historyManager?.writeFile(problemStatementFilePath, message.content);
          oThis.historyManager?.writeFile(
            sharedResourcesIndexFilePath,
            JSON.stringify({
              'shared_resources/SIRJI/problem.txt': {
                description: 'Problem statement from the user.',
                created_by: 'SIRJI'
              }
            })
          );

          oThis.isFirstUserMessage = false;

          await oThis.initFacilitation(message.content, {
            TO: ACTOR_ENUM.ORCHESTRATOR
          });
        } else {
          await oThis.initFacilitation(message.content, {
            TO: oThis.lastMessageFrom
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
    oThis.lastMessageFrom = parsedMessage.FROM;
    while (keepFacilitating) {
      if (parsedMessage.ACTION === 'INVOKE_AGENT') {
        try {
          await invokeAgent(oThis.context, oThis.workspaceRootPath, oThis.sirjiRunId, path.join(__dirname, '..', 'py_scripts', 'agents', 'invoke_agent.py'));
        } catch (error) {}
      } else {
        switch (parsedMessage.TO) {
          case ACTOR_ENUM.ORCHESTRATOR:
            try {
              await invokeAgent(oThis.context, oThis.workspaceRootPath, oThis.sirjiRunId, path.join(__dirname, '..', 'py_scripts', 'agents', 'invoke_orchestator.py'));
            } catch (error) {
              oThis.sendErrorToChatPanel(error);
              keepFacilitating = false;
            }
            break;

          case ACTOR_ENUM.USER:
            if (parsedMessage.ACTION === ACTION_ENUM.SOLUTION_COMPLETE) {
              keepFacilitating = false;
              oThis.chatPanel?.webview.postMessage({
                type: 'solutionCompleted',
                content: { message: parsedMessage.DETAILS, allowUserMessage: true }
              });
            }

            if (parsedMessage.ACTION === ACTION_ENUM.QUESTION) {
              keepFacilitating = false;
              oThis.chatPanel?.webview.postMessage({
                type: 'botMessage',
                content: { message: parsedMessage.DETAILS, allowUserMessage: true }
              });
            }
            break;

          case ACTOR_ENUM.EXECUTOR:
            parsedMessage = {
              TO: parsedMessage.FROM
            };
            switch (parsedMessage.ACTION) {
              case ACTION_ENUM.OPEN_BROWSER:
                //TODO:Implement this
                openBrowser(parsedMessage.URL);
                console.log('Browse', parsedMessage);
                break;

              case ACTION_ENUM.EXECUTE_COMMAND:
                const executedCommandRes = await executeSpawn(parsedMessage.BODY, oThis.workspaceRootPath);
                rawMessage = executedCommandRes;
                console.log('executedCommandRes', executedCommandRes);
                break;

              case ACTION_ENUM.RUN_SERVER:
                const runServerRes = await executeTask(parsedMessage.BODY, oThis.workspaceRootPath, oThis.sirjiRunId);
                rawMessage = runServerRes;
                console.log('runServerRes', runServerRes);
                break;

              case ACTION_ENUM.CREATE_FILE:
                const createFileRes = await createFile(oThis.workspaceRootPath, parsedMessage.BODY);
                rawMessage = createFileRes;
                console.log('Create', createFileRes);
                break;

              case ACTION_ENUM.READ_DIR:
                const readDirContentRes = await readContent(oThis.workspaceRootPath, parsedMessage.BODY, true);
                rawMessage = readDirContentRes;
                break;

              case ACTION_ENUM.READ_FILES:
                const readFileContentRes = await readContent(oThis.workspaceRootPath, parsedMessage.BODY, false);
                rawMessage = readFileContentRes;
                break;

              case ACTION_ENUM.READ_DIR_STRUCTURE:
                const readDirStructureRes = await readDirectoryStructure(oThis.workspaceRootPath, parsedMessage.BODY);
                rawMessage = readDirStructureRes;
                break;

              case ACTION_ENUM.APPEND_TO_SHARED_RESOURCES_INDEX:
                const appendToSharedResourcesIndexRes = await appendToSharedResourcesIndex(oThis.workspaceRootPath, parsedMessage.BODY, parsedMessage.FROM);
                rawMessage = appendToSharedResourcesIndexRes;
                break;

              case ACTION_ENUM.READ_SHARED_RESOURCE_INDEX:
                const readSharedResourcesIndexRes = await readSharedResourcesIndex(oThis.workspaceRootPath);
                rawMessage = readSharedResourcesIndexRes;
                break;

              default:
                console.log('Execution default', parsedMessage);
                oThis.chatPanel?.webview.postMessage({
                  type: 'botMessage',
                  content: { message: `Executor called with unknown action: ${parsedMessage.ACTION}. Raw message: ${rawMessage}`, allowUserMessage: true }
                });
                keepFacilitating = false;
                break;
            }

            break;

          default:
            console.log('Actor default', parsedMessage);
            try {
              await invokeAgent(oThis.context, oThis.workspaceRootPath, oThis.sirjiRunId, path.join(__dirname, '..', 'py_scripts', 'agents', 'invoke_agent.py'));
            } catch (error) {}

            keepFacilitating = false;
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

  private fromCoderRelayToChatPanel(parsedMessage: any) {
    const oThis = this;

    let contentMessage = null;

    if (!parsedMessage || !parsedMessage.ACTION) {
      return;
    }

    switch (parsedMessage.ACTION) {
      case ACTION_ENUM.GENERATE_STEPS:
        contentMessage = 'Generating steps to solve the given problem statement.';
        break;

      case ACTION_ENUM.CREATE_FILE:
        contentMessage = `Creating File: ${parsedMessage.FILENAME}`;
        break;

      case ACTION_ENUM.EXECUTE_COMMAND:
        contentMessage = `Executing Command: ${parsedMessage.COMMAND}`;
        break;

      case ACTION_ENUM.RUN_SERVER:
        contentMessage = `Running Server: ${parsedMessage.COMMAND}`;
        break;

      case ACTION_ENUM.INSTALL_PACKAGE:
        contentMessage = `Installing Package: ${parsedMessage.COMMAND}`;
        break;

      case ACTION_ENUM.READ_FILES:
        contentMessage = `Reading Files: ${parsedMessage.FILEPATHS}`;
        break;

      case ACTION_ENUM.READ_DIR:
        contentMessage = `Reading Files in Folder (and its Sub-Folders): ${parsedMessage.DIRPATH}`;
        break;

      case ACTION_ENUM.READ_DIR_STRUCTURE:
        contentMessage = `Reading Directory Structure: ${parsedMessage.DIRPATH}`;
        break;

      case ACTION_ENUM.TRAIN_USING_URL:
        contentMessage = `Training Research Agent (RAG): Using contents from ${parsedMessage.URL}`;
        break;

      case ACTION_ENUM.INFER:
        contentMessage = 'Inferring from the Research Agent based on trained knowledge';
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

    const coderConversationFilePath = path.join(oThis.workspaceRootPath, Constants.HISTORY_FOLDER, oThis.sirjiRunId, Constants.CODER_JSON_FILE);
    const researcherConversationFilePath = path.join(oThis.workspaceRootPath, Constants.HISTORY_FOLDER, oThis.sirjiRunId, Constants.RESEARCHER_JSON_FILE);
    const plannerConversationFilePath = path.join(oThis.workspaceRootPath, Constants.HISTORY_FOLDER, oThis.sirjiRunId, Constants.PLANNER_JSON_FILE);

    const coderTokensUsed = await oThis.getTokensUsed(coderConversationFilePath);
    const researcherTokensUsed = await oThis.getTokensUsed(researcherConversationFilePath);
    const plannerTokensUsed = await oThis.getTokensUsed(plannerConversationFilePath);

    const totalPromptTokens = coderTokensUsed.prompt_tokens + researcherTokensUsed.prompt_tokens + plannerTokensUsed.prompt_tokens;

    const totalCompletionTokens = coderTokensUsed.completion_tokens + researcherTokensUsed.completion_tokens + plannerTokensUsed.completion_tokens;

    const totalPromptTokensValueInDollar = (totalPromptTokens * Constants.PROMPT_TOKEN_PRICE_PER_MILLION_TOKENS) / 1000000.0;
    const totalCompletionTokensValueInDollar = (totalCompletionTokens * Constants.COMPLETION_TOKEN_PRICE_PER_MILLION_TOKENS) / 1000000.0;

    return {
      total_prompt_tokens: totalPromptTokens,
      total_completion_tokens: totalCompletionTokens,
      total_prompt_tokens_value: totalPromptTokensValueInDollar,
      total_completion_tokens_value: totalCompletionTokensValueInDollar
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
