import * as vscode from 'vscode';
import * as fs from 'fs';
import path from 'path';

let sirjiTerminal: vscode.Terminal | undefined;

export function executeCommand(command: string, workspaceRootPath: string): any {
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

  //TODO:QUESTION: instead of adding a tee command from openAI side, should we always add it from our side? As we want to create the file inside the .sirji directory and capture the output of the command
  if (command.includes('tee')) {
    sirjiTerminal.sendText(command);
    const fileName = command.split('tee')[1].trim().split(' ')[0];
    const filePath = path.join(workspaceRootPath, fileName);

    setTimeout(() => {
      const fileContent = fs.readFileSync(filePath, 'utf8');
      return fileContent;
    }, 15000);
  } else {
    const fileName = `output_${new Date().getTime()}.txt`;
    const filePath = path.join(workspaceRootPath, fileName);

    command = `${command} 2>&1 | tee ${filePath}`;

    sirjiTerminal.sendText(command);

    setTimeout(() => {
      const fileContent = fs.readFileSync(filePath, 'utf8');

      return fileContent;
    }, 15000);
  }
}
