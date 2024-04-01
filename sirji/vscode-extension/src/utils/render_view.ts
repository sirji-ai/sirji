import * as vscode from 'vscode';
import path from 'path';
import * as fs from 'fs';
import { randomBytes } from 'crypto';
import { invokeAgent } from './invoke_agent';
import { openBrowser } from './open_browser';
import { executeCommand } from './execute_command';
import { createFile } from './create_file';

export function renderView(
 context: vscode.ExtensionContext,
 view: string,
 workspaceRootUri: any,
 workspaceRootPath: any
): vscode.WebviewPanel {
 let viewDetails: any;

 if (view === 'chat') {
  viewDetails = getChatViewDetails(context);
 } else {
  throw new Error(`View not defined ${view} in renderer.ts`);
 }

 const panel = viewDetails.panel;

 panel.webview.html = getWebviewContent(viewDetails.htmlFilePath, viewDetails.replaceInHtml);

 panel.webview.onDidReceiveMessage(
  (message: string) => {
   invokeAgent(path.join(__dirname, '..', 'pycode', 'script.py'), [message])
    .then((response) => {
     const splittedResponse = response.split(':'),
      responseCommand = splittedResponse.shift().trim(),
      responseDetails = splittedResponse.join(':').trim();

     if (responseCommand === 'Browse') {
      openBrowser(responseDetails);
      panel.webview.postMessage('Browser Opened');
     } else if (responseCommand === 'Execute') {
      executeCommand(responseDetails);
      panel.webview.postMessage('Command Executed');
     } else if (responseCommand === 'Create') {
      createFile(workspaceRootPath, 'yourFile.txt', responseDetails);
      panel.webview.postMessage('File Created');
     } else {
      panel.webview.postMessage(response);
     }
    })
    .catch((error) => {
     console.log(error);
    });
  },
  undefined,
  context.subscriptions
 );

 return panel;
}

function getWebviewContent(htmlFilePath: string, replaceInHtml: { [key: string]: string }): string {
 // load required html file
 let htmlContent = fs.readFileSync(htmlFilePath, { encoding: 'utf8' });

 replaceInHtml.nonce = generateNonce();

 htmlContent = Object.keys(replaceInHtml).reduce((str, key) => {
  const regex = new RegExp(`\\$\\{${key}\\}`, 'g');
  return str.replace(regex, replaceInHtml[key]);
 }, htmlContent);

 checkForUnresolvedPlaceholders(htmlContent);

 return htmlContent;
}

function generateNonce(length = 16): string {
 return randomBytes(length).toString('hex');
}

function checkForUnresolvedPlaceholders(htmlContent: string): void {
 const placeholderRegex = /\$\{[^}]+\}/;
 const match = htmlContent.match(placeholderRegex);

 if (match) {
  throw new Error(`Unresolved placeholder found: ${match[0]}`);
 }
}

function getChatViewDetails(context: vscode.ExtensionContext): object {
 const panel = vscode.window.createWebviewPanel('SirjiChat', 'Sirji', vscode.ViewColumn.One, {
  enableScripts: true,
  retainContextWhenHidden: true
 });

 const htmlFilePath = path.join(__dirname, '..', 'views', 'chat', 'chat.html');
 const chatScriptUri = panel.webview.asWebviewUri(
  vscode.Uri.file(path.join(__dirname, '..', 'views', 'chat', 'chat.js'))
 );
 const chatStyleUri = panel.webview.asWebviewUri(
  vscode.Uri.file(path.join(__dirname, '..', 'views', 'chat', 'chat.css'))
 );
 return {
  panel: panel,
  htmlFilePath: htmlFilePath,
  replaceInHtml: {
   chatScriptUri: chatScriptUri,
   chatStyleUri: chatStyleUri
  }
 };
}
