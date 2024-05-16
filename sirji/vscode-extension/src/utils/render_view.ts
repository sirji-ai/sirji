import * as vscode from 'vscode';
import path from 'path';
import * as fs from 'fs';

export function renderView(context: vscode.ExtensionContext | undefined, view: string, projectRootUri: any, projectRootPath: any, sirjiRunId: string): vscode.WebviewPanel {
  let viewDetails: any;

  if (view === 'chat') {
    viewDetails = getChatViewDetails(context);
  } else {
    throw new Error(`View not defined ${view} in renderer.ts`);
  }

  viewDetails.replaceInHtml.nonce = sirjiRunId;

  const panel = viewDetails.panel;

  panel.webview.html = getWebviewContent(viewDetails.htmlFilePath, viewDetails.replaceInHtml);

  return panel;
}

function getWebviewContent(htmlFilePath: string, replaceInHtml: { [key: string]: string }): string {
  // load required html file
  let htmlContent = fs.readFileSync(htmlFilePath, { encoding: 'utf8' });

  htmlContent = Object.keys(replaceInHtml).reduce((str, key) => {
    const regex = new RegExp(`\\$\\{${key}\\}`, 'g');
    return str.replace(regex, replaceInHtml[key]);
  }, htmlContent);

  checkForUnresolvedPlaceholders(htmlContent);

  return htmlContent;
}

function checkForUnresolvedPlaceholders(htmlContent: string): void {
  const placeholderRegex = /\$\{[^}]+\}/;
  const match = htmlContent.match(placeholderRegex);

  if (match) {
    throw new Error(`Unresolved placeholder found: ${match[0]}`);
  }
}

function getChatViewDetails(context: vscode.ExtensionContext | undefined): object {
  const panel = vscode.window.createWebviewPanel('SirjiChat', 'Sirji', vscode.ViewColumn.One, {
    enableScripts: true,
    retainContextWhenHidden: true
  });

  const htmlFilePath = path.join(__dirname, '..', 'views', 'chat', 'chat.html');
  const chatScriptUri = panel.webview.asWebviewUri(vscode.Uri.file(path.join(__dirname, '..', 'views', 'chat', 'chat.js')));
  const chatStyleUri = panel.webview.asWebviewUri(vscode.Uri.file(path.join(__dirname, '..', 'views', 'chat', 'chat.css')));
  return {
    panel: panel,
    htmlFilePath: htmlFilePath,
    replaceInHtml: {
      chatScriptUri: chatScriptUri,
      chatStyleUri: chatStyleUri
    }
  };
}
