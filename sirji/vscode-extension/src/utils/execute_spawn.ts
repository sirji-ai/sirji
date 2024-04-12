import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { spawn } from 'child_process';

const fsPromises = fs.promises;

function constructResponse(success: boolean, filePath: string, output: string): string {
  const response = success ? 'Execute command complete.' : 'Error executing failed.';
  const additionalInfo = `\nCommand execution output is saved at ${filePath}`;
  return response + additionalInfo;
}

let sirjiTerminal: vscode.Terminal | undefined;
export async function executeSpawn(command: string, workspaceRootPath: string): Promise<string> {
  const outputPath = path.join(workspaceRootPath, 'output.txt');
  const output = fs.createWriteStream(outputPath, { flags: 'a' });
  const [cmd, ...args] = command.split(/\s+/);

  if (!sirjiTerminal) {
    sirjiTerminal = vscode.window.createTerminal(`Sirji Terminal`);
    vscode.window.onDidCloseTerminal((terminal) => {
      if (terminal === sirjiTerminal) {
        sirjiTerminal = undefined;
      }
    });
  }

  sirjiTerminal.show(true);

  return new Promise(async (resolve, reject) => {
    const child = spawn(cmd, args, {
      cwd: workspaceRootPath,
      shell: true
    });

    sirjiTerminal?.sendText('\n' + command.toString() + '\n', false);

    const isFileExists = fs.existsSync(outputPath);
    if (isFileExists) {
      fs.unlinkSync(outputPath);
    } else {
      resolve(constructResponse(false, outputPath, `Error deleting output file: ${outputPath}`));
    }

    child.stdout.on('data', (data) => {
      sirjiTerminal?.sendText(data.toString(), false);
      output.write(data);
    });

    child.stderr.on('data', (data) => {
      sirjiTerminal?.sendText(data.toString(), false);
      output.write(data);
    });

    child.on('close', (code) => {
      output.end();
      if (code === 0) {
        try {
          const fileContent = fs.readFileSync(outputPath, 'utf-8');
          sirjiTerminal?.sendText(`Command execution done: ${command}`, false);
          resolve(constructResponse(true, outputPath, fileContent));
        } catch (error) {
          resolve(constructResponse(false, outputPath, `Error reading output file: ${error}`));
        }
      } else {
        resolve(constructResponse(false, outputPath, `Command failed with exit code ${code}`));
      }
    });

    child.on('error', (error) => {
      resolve(constructResponse(false, outputPath, `Failed to start subprocess: ${error.message}`));
    });
  });
}
