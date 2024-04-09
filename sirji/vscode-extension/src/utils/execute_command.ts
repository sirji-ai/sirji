import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

const fsPromises = fs.promises;
let sirjiTerminal: vscode.Terminal | undefined;

async function checkForChanges(filePath: string, previousContent: string): Promise<{ hasChanges: boolean; currentContent: string }> {
  const currentContent = await fsPromises.readFile(filePath, 'utf-8');
  const hasChanges = currentContent !== previousContent;
  return {
    hasChanges,
    currentContent
  };
}

function constructResponse(isRunning: boolean, tempFilePath: string, tempFileContent: string): string {
  let response = isRunning ? 'Execute Command still running.' : 'Execute command complete.';
  response += ` Command execution output from ${tempFilePath}:\n`;
  response += tempFileContent;
  return response;
}

export async function executeCommand(command: string, workspaceRootPath: string): Promise<string> {
  if (!sirjiTerminal) {
    sirjiTerminal = vscode.window.createTerminal(`Sirji Terminal`);
    vscode.window.onDidCloseTerminal((terminal) => {
      if (terminal === sirjiTerminal) {
        sirjiTerminal = undefined;
      }
    });
  }

  sirjiTerminal.show(true);

  const fileName = `output.txt`;
  const filePath = path.join(workspaceRootPath, fileName);
  command = `(${command}) 2>&1 | tee "${filePath}"`;

  sirjiTerminal.sendText(command);

  await new Promise((resolve) => setTimeout(resolve, 1000));

  let previousContent = '';

  const checkForChangesAndConstructResponse = (): Promise<string> => {
    return new Promise((resolve, reject) => {
      const intervalId = setInterval(async () => {
        const { hasChanges, currentContent } = await checkForChanges(filePath, previousContent);

        if (!hasChanges) {
          clearInterval(intervalId);
          resolve(constructResponse(false, filePath, currentContent));
        } else {
          previousContent = currentContent;
        }
      }, 30000);
    });
  };

  return await checkForChangesAndConstructResponse();
}
