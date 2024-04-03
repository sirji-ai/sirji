import * as vscode from 'vscode';
import { randomBytes } from 'crypto';
import path from 'path';

import { renderView } from './render_view';
import { maintainHistory } from './maintain_history';
import { invokeAgent } from './invoke_agent';

export class Facilitator {
 private context: vscode.ExtensionContext | undefined;
 private workspaceRootUri: any;
 private workspaceRootPath: any;
 private problemId: string = '';
 private chatPanel: vscode.WebviewPanel | undefined;
 private problemStatementSent = false;

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

  // Setup History Maintainor
  oThis.setupHistoryMaintainor();

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

 private setupHistoryMaintainor() {
  const oThis = this;

  maintainHistory().createHistoryFolder(oThis.workspaceRootPath, oThis.problemId);
 }

 private openChatViewPanel() {
  const oThis = this;

  oThis.chatPanel = renderView(oThis.context, 'chat', oThis.workspaceRootUri, oThis.workspaceRootPath, oThis.problemId);

  oThis.chatPanel.webview.onDidReceiveMessage(
   async (message: string) => {
    await oThis.constructUserMessage(message);
   },
   undefined,
   (oThis.context || {}).subscriptions
  );
 }

 private async constructUserMessage(message: string) {
  const oThis = this;

  // TODO:
  // Format user message If first Msg -> Problem Statement
  // From second message onwards remember what message was sent to user, and construct appropraite reply msg.
  if (!oThis.problemStatementSent) {
   const response = await invokeAgent(
    path.join(__dirname, '..', 'py_scripts', 'generate_problem_statement_message.py'),
    ['-ps', message]
   );
   oThis.problemStatementSent = true;
  }
 }

 private initFacilitation() {}
}
