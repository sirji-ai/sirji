import * as vscode from 'vscode';
import path from 'path';
import { openBrowser } from './open_browser';
import { executeCommand } from './execute_command';
import { createFile } from './create_file';
import { invokeAgent } from './invoke_agent';

export async function handleChatMessage(
 message: string,
 panel: vscode.WebviewPanel,
 context: vscode.ExtensionContext,
 workspaceRootPath: any
) {
 try {
  const response = await invokeAgent(path.join(__dirname, '..', 'pycode', 'message.py'), [message]);

  console.log('Response: ', response);
  const splittedResponse = response.split(':'),
   responseCommand = splittedResponse.shift().trim(),
   responseDetails = splittedResponse.join(':').trim();

  switch (responseCommand) {
   case 'Browse':
    openBrowser(responseDetails);
    panel.webview.postMessage('Browser Opened');
    break;
   case 'Execute':
    executeCommand(responseDetails);
    panel.webview.postMessage('Command Executed');
    break;
   case 'Create':
    createFile(workspaceRootPath, 'yourFile.txt', responseDetails);
    panel.webview.postMessage('File Created');
    break;
   default:
    panel.webview.postMessage(response);
  }
 } catch (error: any) {
  console.error(error);
  panel.webview.postMessage(`Error: ${error.message}`);
 }
}
