import * as vscode from 'vscode';
import path from 'path';
import { openBrowser } from './open_browser';
import { executeCommand } from './execute_command';
import { createFile } from './create_file';
import { invokeAgent } from './invoke_agent';
// import { configStorage } from './secret_storage';

export async function handleChatMessage(message: string, panel: any, context: any, workspaceRootPath: any) {
 try {
  // TODO: Daksh, please pass path.join(oThis.workspaceRootPath, 'venv') as the first argument in the following.
  const response = await invokeAgent('', path.join(__dirname, '..', 'py_scripts', 'message.py'), [message]);

  // const secretStorage = configStorage(context);

  // if (secretStorage.isApiKey(message)) {
  //  console.log('API Key: ', message);
  //  const secretKey = 'userAPIKey';
  //  await secretStorage.storeSecret(secretKey, message);
  //  panel.webview.postMessage('Your API key has been securely stored.');
  //  return;
  // }

  // if (message === 'Get API Key') {
  //  const secretKey = 'userAPIKey';
  //  const secret = await secretStorage.retrieveSecret(secretKey);
  //  return secret;
  // }

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
