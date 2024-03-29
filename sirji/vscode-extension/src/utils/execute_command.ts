import * as vscode from 'vscode';

export function executeCommand(command: string) {
    let terminal = vscode.window.createTerminal(`Sirji Terminal`);
    terminal.show();
    terminal.sendText(command);
}