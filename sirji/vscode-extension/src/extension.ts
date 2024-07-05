import * as vscode from 'vscode';
import { Facilitator } from './utils/facilitator';
import path from 'path';
let facilitatorInstance: Facilitator | undefined = undefined;

function activate(context: vscode.ExtensionContext) {
  let disposable = vscode.commands.registerCommand('sirji.chat', async function () {
    if (facilitatorInstance && facilitatorInstance.getChatPanel()) {
      facilitatorInstance.revealChatPanel();
    } else {
      facilitatorInstance = new Facilitator(context);
      const chatPanel = await facilitatorInstance.init();

      if (chatPanel) {
        chatPanel.onDidDispose(async () => {
          console.log('Chat panel is disposed.');
          await facilitatorInstance?.cleanup();
          facilitatorInstance = undefined;
        });
      }
    }
  });

  let openStudio = vscode.commands.registerCommand('sirji.studio', async function () {
    let rootPath = context?.globalStorageUri.path;
    let sirjiInstallationFolderPath = path.join(rootPath, 'Sirji');
    let uri = vscode.Uri.file(sirjiInstallationFolderPath);
    vscode.commands.executeCommand('vscode.openFolder', uri, true);
  });

  context.subscriptions.push(disposable);
  context.subscriptions.push(openStudio);
}

/**
 * Function to deactivate the extension.
 * This function is called when the extension is deactivated.
 * Currently, there is no cleanup necessary on deactivation.
 */
function deactivate() {}

// Export the activate and deactivate functions to be called by VS Code
exports.activate = activate;
exports.deactivate = deactivate;
