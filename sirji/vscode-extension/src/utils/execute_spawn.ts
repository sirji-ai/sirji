import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import { spawn } from 'child_process';

const fsPromises = fs.promises;

function constructResponse(success: boolean, output: string): string {
  const response = success ? 'Execute command complete.' : 'Error executing failed.';
  const additionalInfo = `Output:\n\n${output}`;
  return response + additionalInfo;
}

// let sirjiTerminal: vscode.Terminal | undefined;
export async function executeSpawn(command: string, workspaceRootPath: string): Promise<string> {
  let successResp = '';
  let errorResp = '';
  const [cmd, ...args] = command.split(/\s+/);

  return new Promise(async (resolve, reject) => {
    const child = spawn(cmd, args, {
      cwd: workspaceRootPath,
      shell: true
    });

    child.stdout.on('data', (data) => {
      successResp += data;
    });

    child.stderr.on('data', (data) => {
      errorResp += data;
    });

    child.on('close', (code) => {
      if (code === 0) {
        resolve(constructResponse(true, successResp));
      } else {
        resolve(constructResponse(false, errorResp));
      }
    });

    child.on('error', (error) => {
      resolve(constructResponse(false, `Failed to start subprocess: ${error.message}`));
    });
  });
}
