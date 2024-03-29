import * as vscode from 'vscode';

import { renderView } from './utils/render_view';

async function selectWorkspace() {
 const workspaceRootUri = vscode.workspace.workspaceFolders ? vscode.workspace.workspaceFolders[0].uri : null;
 const workspaceRootPath = workspaceRootUri ? workspaceRootUri.fsPath : null;

 if (!workspaceRootUri) {
  // Prompt user to open a folder
  const openFolderMsg = 'No workspace/folder is open. Please open a folder to proceed.';
  await vscode.window.showErrorMessage(openFolderMsg, 'Open Folder').then(async (selection) => {
   if (selection === 'Open Folder') {
    await vscode.commands.executeCommand('workbench.action.files.openFolder');
    return; // Exit the current command execution to avoid further operations until folder is opened
   }
  });
 }

 return {
  workspaceRootUri: workspaceRootUri,
  workspaceRootPath: workspaceRootPath
 };
}

let chatPanel: vscode.WebviewPanel | undefined = undefined;

function activate(context: vscode.ExtensionContext) {
 let disposable = vscode.commands.registerCommand('sirji.chat', async function () {
  if (chatPanel) {
   chatPanel.reveal(vscode.ViewColumn.One);
   return;
  } else {
   const workspaceRootObj = await selectWorkspace();
   const workspaceRootUri = workspaceRootObj.workspaceRootUri;
   const workspaceRootPath = workspaceRootObj.workspaceRootPath;

   chatPanel = renderView(context, 'chat', workspaceRootUri, workspaceRootPath);

   chatPanel.onDidDispose(() => {
    chatPanel = undefined;
   });
  }
 });

 context.subscriptions.push(disposable);
}

function deactivate() {}

exports.activate = activate;
exports.deactivate = deactivate;
