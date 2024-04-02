import * as vscode from 'vscode';
import { randomBytes } from 'crypto';

import { Facilitator } from './utils/facilitator';

let chatPanel: vscode.WebviewPanel | undefined = undefined;

function activate(context: vscode.ExtensionContext) {
 //TODO: implement config management
 //  configStorage(context);

 let disposable = vscode.commands.registerCommand('sirji.chat', async function () {
  if (chatPanel) {
    chatPanel.reveal(vscode.ViewColumn.One);
    return;
  } else {
    chatPanel = await new Facilitator(context).init() || vscode.window.createWebviewPanel('DummyView', 'Dummy', vscode.ViewColumn.One, {});

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
