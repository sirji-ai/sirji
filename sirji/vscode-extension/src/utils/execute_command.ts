import * as vscode from 'vscode';
import * as fs from 'fs';
import path from 'path';

const fsPromises = fs.promises;
let sirjiTerminal: vscode.Terminal | undefined;

export async function executeCommand(command: string, workspaceRootPath: string): Promise<any> {
  if (!sirjiTerminal) {
    sirjiTerminal = vscode.window.createTerminal(`Sirji Terminal`);

    vscode.window.onDidCloseTerminal((terminal) => {
      if (terminal === sirjiTerminal) {
        sirjiTerminal = undefined;
      }
    });
  }

  sirjiTerminal.show();

  const fileName = `output.txt`;
  const filePath = path.join(workspaceRootPath, fileName);

  command = `${command} 2>&1 | tee ${filePath}`;

  sirjiTerminal.sendText(command);

  try {
    await waitForFile(filePath);
  } catch (error) {
    throw error;
  }

  await new Promise((resolve) => setTimeout(resolve, 1000));

  const fileContent = await fsPromises.readFile(filePath, 'utf8');

  return fileContent;
}

async function waitForFile(filePath: string): Promise<void> {
  return new Promise((resolve, reject) => {
    const dir = path.dirname(filePath);
    const basename = path.basename(filePath);

    const watcher = fs.watch(dir, (eventType, filename) => {
      if (filename && path.basename(filename) === basename) {
        watcher.close();
        resolve();
      }
    });

    const timeout = setTimeout(() => {
      watcher.close();
      reject(new Error(`File ${basename} did not appear after timeout`));
    }, 15000);

    watcher.on('close', () => {
      clearTimeout(timeout);
    });
  });
}
