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

  // Add the command to the context's subscriptions to ensure proper disposal
  context.subscriptions.push(disposable);
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
