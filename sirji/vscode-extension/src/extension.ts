import * as vscode from 'vscode';
import { Facilitator } from './utils/facilitator';

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
    let current_user = process.env.USER;
    let folderPath = `/Users/${current_user}/Library/Application Support/Code/User/globalStorage/truesparrow.sirji/Sirji`;
    let uri = vscode.Uri.file(folderPath);
    vscode.commands.executeCommand('vscode.openFolder', uri, true);
  });

  // Add the command to the context's subscriptions to ensure proper disposal
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
