import * as vscode from 'vscode';

let sirjiTerminal: vscode.Terminal | undefined;

export function executeCommand(command: string) {
  if (!sirjiTerminal) {
    sirjiTerminal = vscode.window.createTerminal(`Sirji Terminal`);

    //Clear the reference if the terminal is closed
    vscode.window.onDidCloseTerminal((terminal) => {
      if (terminal === sirjiTerminal) {
        sirjiTerminal = undefined;
      }
    });
  }

  sirjiTerminal.show();
  sirjiTerminal.sendText(command);
}
