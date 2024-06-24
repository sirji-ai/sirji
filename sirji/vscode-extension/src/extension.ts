import * as vscode from 'vscode';
import { Facilitator } from './utils/facilitator';
import path from 'path';
import * as fs from 'fs';

// Variable to keep track of the chat panel instance
let chatPanel: vscode.WebviewPanel | undefined = undefined;

/**
 * Function to activate the extension.
 * This function is called when the extension is activated.
 * It registers a command and adds it to the context's subscriptions.
 *
 * @param context - The extension context
 */
function activate(context: vscode.ExtensionContext) {
  // Register the command `sirji.chat`. This command is defined in the package.json file.
  let disposable = vscode.commands.registerCommand('sirji.chat', async function () {
    // If chatPanel already exists, reveal it in the first column without creating a new one
    if (chatPanel) {
      chatPanel.reveal(vscode.ViewColumn.One);
      return;
    }
    // Else, create a new chatPanel instance using the Facilitator class and listen for its disposal.
    else {
      chatPanel = await new Facilitator(context).init();
      chatPanel?.onDidDispose(() => {
        // Clean up when the chatPanel is closed by setting it to undefined
        chatPanel = undefined;
      });
    }
  });

  // Register the command `sirji.studio` to open studio
  let openStudio = vscode.commands.registerCommand('sirji.studio', async function () {
    let rootPath = context?.globalStorageUri.path;
    let sirjiInstallationFolderPath = path.join(rootPath, 'Sirji');
    let uri = vscode.Uri.file(sirjiInstallationFolderPath);
    vscode.commands.executeCommand('vscode.openFolder', uri, true);
  });

  // Add the command to the context's subscriptions to ensure proper disposal
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
        vscode.window.showInformationMessage(`Extension updated from version ${previousVersion} to ${currentVersion}`);
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
