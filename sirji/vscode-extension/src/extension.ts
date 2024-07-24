import * as vscode from 'vscode';
import { Facilitator } from './utils/facilitator';
import path from 'path';
let facilitatorInstance: Facilitator | undefined = undefined;
import * as fs from 'fs';

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

  const currentVersion = vscode.extensions.getExtension('TrueSparrow.sirji')!.packageJSON.version;
    const previousVersion = context.globalState.get('extensionVersion');

    console.log('Current version:', currentVersion);
    console.log('Previous version:', previousVersion);

    let rootPath = context?.globalStorageUri.path || '';
    let sirjiInstallationFolderPath = path.join(rootPath, 'Sirji');

    const venvPath = path.join(sirjiInstallationFolderPath, 'venv');

    if (previousVersion && currentVersion !== previousVersion) {
        vscode.window.showInformationMessage(`Sirji extension updated from version ${previousVersion} to ${currentVersion}`);
        removeVenv(venvPath);
    }

    // Store the current version in global state
    context.globalState.update('extensionVersion', currentVersion);

}

function removeVenv(venvPath: string) {
  if (fs.existsSync(venvPath)) {
    fs.rmdirSync(venvPath, { recursive: true });
  }
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
