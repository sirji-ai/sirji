import * as vscode from 'vscode';
import { randomBytes } from 'crypto';
import path from 'path';

import { renderView } from './render_view';
import { MaintainHistory } from './maintain_history';
import { invokeAgent } from './invoke_agent';
import { SecretStorage } from './secret_storage';
import { Constants, ACTOR_ENUM, ACTION_ENUM } from './constants';
import { openBrowser } from './open_browser';
import { executeCommand } from './execute_command';
import { createFile } from './create_file';
import { readContent } from './read_content';

export class Facilitator {
  private context: vscode.ExtensionContext | undefined;
  private workspaceRootUri: any;
  private workspaceRootPath: any;
  private sirjiRunId: string = '';
  private chatPanel: vscode.WebviewPanel | undefined;
  private secretManager: SecretStorage | undefined;
  private envVars: any = undefined;
  private historyManager: MaintainHistory | undefined;

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

    // Setup History Manager
    oThis.setupHistoryManager();

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

  private setupHistoryManager() {
    const oThis = this;
    oThis.historyManager = new MaintainHistory();

    oThis.historyManager.createHistoryFolder(oThis.workspaceRootPath, oThis.sirjiRunId);
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
      content: responseContent
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

  private async sendWelcomeMessage() {
    const oThis = this;

    oThis.chatPanel?.webview.postMessage({
      type: 'botMessage',
      content: {
        message: 'Hello, I am Sirji. Please wait while i am setting up the workspace...',
        allowUserMessage: true
      }
    });

    // Setup Python virtual env and Install dependencies

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

    await invokeAgent(oThis.context, oThis.workspaceRootPath, oThis.sirjiRunId, path.join(__dirname, '..', 'py_scripts', 'setup_virtual_env.py'), [
      '--venv',
      path.join(oThis.workspaceRootPath, Constants.PYHTON_VENV_FOLDER)
    ]);
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

      case 'userMessage':
        await oThis.initFacilitation(message.content, {
          TO: ACTOR_ENUM.CODER
        });
        break;

      default:
        vscode.window.showErrorMessage(`Unknown message received from chat panel: ${message}`);
    }
  }

  private async constructUserMessage(message: string) {
    const oThis = this;
    //write in a file
    //call coder
    // Read coder json file
    // call infinite loop function with the last message, formatted
  }

  //  private async initFacilitation(message: string) {
  //   while (true) {
  //    // add switch cases
  //    switch (message) {
  //     case 'Researcher':
  //      //write in a file
  //      //call researcher
  //      //read last message from researcher json file
  //      // set last message to message
  //      break;

  //     case 'Coder':
  //      //write in a file
  //      //call coder
  //      //read last message from coder json file
  //      // set last message to message
  //      break;

  //     case 'Planner':
  //      //write in a file
  //      //call planner
  //      //read last message from planner json file
  //      // set last message to message
  //      break;

  //     case 'User':
  //      // if
  //      // step_started step_completed
  //      // update plan for user
  //      // write sure in a file
  //      // call coder
  //      // read last message from coder json file
  //      // set the last message to message
  //      //  else
  //      // solution_completed, question, inform
  //      // show the message to end user, open user input box and break the while loop
  //      break;
  //    }
  //   }
  //  }

  private async initFacilitation(rawMessage: string, parsedMessage: any) {
    const oThis = this;

    let keepFacilitating: Boolean = true;
    while (keepFacilitating) {
      console.log('inside while loop', parsedMessage);
      const inputFilePath = path.join(oThis.workspaceRootPath, Constants.HISTORY_FOLDER, oThis.sirjiRunId, Constants.PYTHON_INPUT_FILE);
      switch (parsedMessage.TO) {
        case ACTOR_ENUM.CODER:
          if (parsedMessage.ACTION === ACTION_ENUM.STEPS) {
            oThis.chatPanel?.webview.postMessage({
              type: 'plannedSteps',
              content: parsedMessage.PARSED_STEPS
            });
          }

          oThis.historyManager?.writeFile(inputFilePath, rawMessage);

          const coderConversationFilePath = path.join(oThis.workspaceRootPath, Constants.HISTORY_FOLDER, oThis.sirjiRunId, Constants.CODER_JSON_FILE);

          const codingAgentPath = path.join(__dirname, '..', 'py_scripts', 'agents', 'coding_agent.py');

          await invokeAgent(oThis.context, oThis.workspaceRootPath, oThis.sirjiRunId, codingAgentPath, ['--input', inputFilePath, '--conversation', coderConversationFilePath]);

          const coderConversationContent = JSON.parse(oThis.historyManager?.readFile(coderConversationFilePath));

          const lastCoderMessage: any = coderConversationContent.conversations[coderConversationContent.conversations.length - 1];

          console.log('lastCoderMessage', lastCoderMessage);

          rawMessage = lastCoderMessage?.content;

          parsedMessage = lastCoderMessage?.parsed_content;

          break;

        case ACTOR_ENUM.RESEARCHER:
          oThis.historyManager?.writeFile(inputFilePath, rawMessage);

          const researcherConversationFilePath = path.join(oThis.workspaceRootPath, Constants.HISTORY_FOLDER, oThis.sirjiRunId, Constants.RESEARCHER_JSON_FILE);

          const researcherAgentPath = path.join(__dirname, '..', 'py_scripts', 'agents', 'researcher_agent.py');

          await invokeAgent(oThis.context, oThis.workspaceRootPath, oThis.sirjiRunId, researcherAgentPath, ['--input', inputFilePath, '--conversation', researcherConversationFilePath]);

          const researcherConversationContent = JSON.parse(oThis.historyManager?.readFile(researcherConversationFilePath));

          const lastResearcherMessage: any = researcherConversationContent.conversations[researcherConversationContent.conversations.length - 1];

          console.log('lastResearcherMessage', lastResearcherMessage);

          rawMessage = lastResearcherMessage?.content;

          parsedMessage = lastResearcherMessage?.parsed_content;

          break;

        case ACTOR_ENUM.PLANNER:
          oThis.chatPanel?.webview.postMessage({
            type: 'botMessage',
            content: { message: 'Generating Steps to solve the problem statement...', allowUserMessage: false }
          });

          oThis.historyManager?.writeFile(inputFilePath, rawMessage);

          const plannerConversationFilePath = path.join(oThis.workspaceRootPath, Constants.HISTORY_FOLDER, oThis.sirjiRunId, Constants.PLANNER_JSON_FILE);

          const plannerAgentPath = path.join(__dirname, '..', 'py_scripts', 'agents', 'planning_agent.py');

          await invokeAgent(oThis.context, oThis.workspaceRootPath, oThis.sirjiRunId, plannerAgentPath, ['--input', inputFilePath, '--conversation', plannerConversationFilePath]);

          const plannerConversationContent = JSON.parse(oThis.historyManager?.readFile(plannerConversationFilePath));

          const lastPlannerMessage: any = plannerConversationContent.conversations[plannerConversationContent.conversations.length - 1];

          console.log('lastPlannerMessage', lastPlannerMessage);

          rawMessage = lastPlannerMessage?.content;

          parsedMessage = lastPlannerMessage?.parsed_content;

          break;

        case ACTOR_ENUM.USER:
          if (parsedMessage.ACTION === ACTION_ENUM.STEP_STARTED) {
            oThis.chatPanel?.webview.postMessage({
              type: 'plannedStepStart',
              content: parsedMessage.DETAILS
            });

            rawMessage = 'sure';
            parsedMessage = {
              TO: ACTOR_ENUM.CODER
            };
          }

          if (parsedMessage.ACTION === ACTION_ENUM.STEP_COMPLETED) {
            oThis.chatPanel?.webview.postMessage({
              type: 'plannedStepComplete',
              content: parsedMessage.DETAILS
            });

            rawMessage = 'sure';
            parsedMessage = {
              TO: ACTOR_ENUM.CODER
            };
          }

          if (parsedMessage.ACTION === ACTION_ENUM.SOLUTION_COMPLETE || parsedMessage.ACTION === ACTION_ENUM.QUESTION || parsedMessage.ACTION === ACTION_ENUM.INFORM) {
            keepFacilitating = false;
            oThis.chatPanel?.webview.postMessage({
              type: 'botMessage',
              content: { message: parsedMessage.DETAILS, allowUserMessage: true }
            });
          }
          break;

        case ACTOR_ENUM.EXECUTOR:
          switch (parsedMessage.ACTION) {
            case ACTION_ENUM.OPEN_BROWSER:
              //TODO:Implement this
              openBrowser(parsedMessage.URL);
              console.log('Browse', parsedMessage);
              break;

            case ACTION_ENUM.INSTALL_PACKAGE:
              const installPackageLogPath = path.join(oThis.workspaceRootPath, Constants.HISTORY_FOLDER, oThis.sirjiRunId);
              const installPackageCommandRes = await executeCommand(parsedMessage.COMMAND, installPackageLogPath);
              rawMessage = installPackageCommandRes;
              parsedMessage = {
                TO: ACTOR_ENUM.CODER
              };
              console.log('installPackageCommandRes', installPackageCommandRes);
              break;

            case ACTION_ENUM.EXECUTE_COMMAND:
              const executedCommandLogPath = path.join(oThis.workspaceRootPath, Constants.HISTORY_FOLDER, oThis.sirjiRunId);
              const executedCommandRes = await executeCommand(parsedMessage.COMMAND, executedCommandLogPath);
              rawMessage = executedCommandRes;
              parsedMessage = {
                TO: ACTOR_ENUM.CODER
              };
              console.log('executedCommandRes', executedCommandRes);
              break;

            case ACTION_ENUM.CREATE_FILE:
              const createFileRes = await createFile(oThis.workspaceRootPath, parsedMessage.FILENAME, parsedMessage.CONTENT);
              rawMessage = createFileRes;
              parsedMessage = {
                TO: ACTOR_ENUM.CODER
              };
              console.log('Create', createFileRes);
              break;

            case ACTION_ENUM.READ_DIR:
              const readDirContentRes = await readContent(oThis.workspaceRootPath, parsedMessage.DIRPATH);
              rawMessage = readDirContentRes;
              parsedMessage = {
                TO: ACTOR_ENUM.CODER
              };
              break;

            case ACTION_ENUM.READ_FILE:
              const readFileContentRes = await readContent(oThis.workspaceRootPath, parsedMessage.FILENAME);
              rawMessage = readFileContentRes;
              parsedMessage = {
                TO: ACTOR_ENUM.CODER
              };
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
          oThis.chatPanel?.webview.postMessage({
            type: 'botMessage',
            content: { message: `Received message with unknown TO: ${parsedMessage.TO}. Raw message: ${rawMessage}`, allowUserMessage: true }
          });
          keepFacilitating = false;
          break;
      }
    }
  }
}
