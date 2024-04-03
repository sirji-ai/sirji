import * as vscode from 'vscode';
import { randomBytes } from 'crypto';
import path from 'path';

import { renderView } from './render_view';
import { MaintainHistory } from './maintain_history';
import { invokeAgent } from './invoke_agent';
import { SecretStorage } from './secret_storage';

export class Facilitator {
 private context: vscode.ExtensionContext | undefined;
 private workspaceRootUri: any;
 private workspaceRootPath: any;
 private problemId: string = '';
 private chatPanel: vscode.WebviewPanel | undefined;
 private problemStatementSent = false;
 private secretManager: SecretStorage | undefined;
 private envVars: any = undefined;
 private historyManager: MaintainHistory | undefined;

 public constructor(context: vscode.ExtensionContext) {
  const oThis = this;

  oThis.context = context;
 }

 public async init() {
  const oThis = this;

  // Setup Environment
  await oThis.setupEnvironment();

  // Setup workspace
  await oThis.selectWorkspace();

  // Setup Python virtual env and Install dependencies
  await oThis.setupVirtualEnv();

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
  oThis.problemId = randomBytes(16).toString('hex');
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

 private async setupVirtualEnv(): Promise<void> {
  const oThis = this;

  await invokeAgent(
   '', // Passing empty string as the virtual env might not be present.
   path.join(__dirname, '..', 'py_scripts', 'setup_virtual_env.py'),
   [path.join(oThis.workspaceRootPath, 'venv')]
  );
 }

 private setupHistoryManager() {
  const oThis = this;
  oThis.historyManager = new MaintainHistory();

  oThis.historyManager.createHistoryFolder(oThis.workspaceRootPath, oThis.problemId);
 }

 private async setupSecretManager() {
  const oThis = this;

  oThis.secretManager = new SecretStorage(oThis.context);
  await oThis.retrieveSecret();
 }

 private async retrieveSecret() {
  const oThis = this;

  oThis.envVars = await oThis.secretManager?.retrieveSecret('sirjiSecrets');
 }

 private async setSecretEnvVars(data: any) {
  const oThis = this;

  let responseContent;

  try {
   await oThis.secretManager?.storeSecret('sirjiSecrets', JSON.stringify(data));
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

  oThis.chatPanel = renderView(oThis.context, 'chat', oThis.workspaceRootUri, oThis.workspaceRootPath, oThis.problemId);

  oThis.chatPanel.webview.onDidReceiveMessage(
   async (message: any) => {
    await oThis.handleMessagesFromChatPanel(message);
   },
   undefined,
   (oThis.context || {}).subscriptions
  );
 }

 private async welcomeMessage() {
  const oThis = this;

  if (!oThis.envVars) {
   oThis.chatPanel?.webview.postMessage({
    type: 'botMessage',
    content:
     "Hello, I am Sirji. Please configure your environment by simply tapping on the settings icon. Let's get you all set up and ready to go!"
   });
  } else {
   oThis.chatPanel?.webview.postMessage({
    type: 'botMessage',
    content: 'Hello, I am Sirji. What would you like me to build today?'
   });
  }
 }

 private async handleMessagesFromChatPanel(message: any) {
  const oThis = this;

  switch (message.type) {
   case 'webViewReady':
    await oThis.welcomeMessage();
    break;

   case 'saveSettings':
    await oThis.setSecretEnvVars(message.content);
    break;

   case 'userMessage':
    await oThis.constructUserMessage(message);
    break;

   default:
    vscode.window.showErrorMessage(`Unknown message received from chat panel: ${message}`);
  }
 }

 private async constructUserMessage(message: string) {
  const oThis = this;

  // TODO:
  // Format user message If first Msg -> Problem Statement
  // From second message onwards remember what message was sent to user, and construct appropraite reply msg.
  if (!oThis.problemStatementSent) {
   const response = await invokeAgent(
    path.join(oThis.workspaceRootPath, 'venv'),
    path.join(__dirname, '..', 'py_scripts', 'generate_problem_statement_message.py'),
    ['-ps', message]
   );
   oThis.problemStatementSent = true;
  }
 }

 private initFacilitation() {}
}
