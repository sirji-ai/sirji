import * as childProcess from 'child_process';
import * as vscode from 'vscode';
import path from 'path';
import os from 'os';
import { SecretStorage } from './secret_storage';
import { Constants } from './constants';
import fs from 'fs';

export async function invokeAgent(context: vscode.ExtensionContext | undefined, workspaceRootPath: string, sirjiRunId: string, scriptPath: string, args: string[] = []): Promise<any> {
  console.log('Executing command:', 'python3', [scriptPath, ...args].join(' '));
  const response = await executePythonScript(context, workspaceRootPath, sirjiRunId, scriptPath, args);
  console.log(response);
  return response;
}

function getPythonPath(workspaceRootPath: string, venvPath: string): string {
  let pythonPath = 'python3';

  if (fs.existsSync(venvPath)) {
    // Determine the correct path for the Python executable based on the OS
    const pythonExecutable = os.platform() === 'win32' ? 'python.exe' : 'bin/python3';

    // Generate the full path to the Python executable inside the virtual environment
    pythonPath = path.join(venvPath, pythonExecutable);
  }

  return pythonPath;
}

async function getEnvVars(context: vscode.ExtensionContext | undefined, workspaceRootPath: string): Promise<any> {
  const secretManager = new SecretStorage(context);
  const envVars = JSON.parse((await secretManager.retrieveSecret(Constants.ENV_VARS_KEY)) || '{}');
  envVars.SIRJI_WORKSPACE = workspaceRootPath;

  return envVars;
}

async function executePythonScript(context: vscode.ExtensionContext | undefined, workspaceRootPath: string, sirjiRunId: string, scriptPath: string, args: string[] = []): Promise<any> {
  const venvPath = path.join(workspaceRootPath, Constants.PYHTON_VENV_FOLDER);
  const pythonPath = getPythonPath(workspaceRootPath, venvPath);
  const envVars = await getEnvVars(context, workspaceRootPath);
  envVars.SIRJI_RUN_ID = sirjiRunId;

  return new Promise((resolve, reject) => {
    const process = childProcess.spawn(pythonPath, [scriptPath, ...args], {
      env: envVars
    });

    let responseData = '',
      errorData = '';

    process.stdout.on('data', (data) => {
      responseData += data.toString();
    });

    process.stderr.on('data', (data) => {
      errorData += data.toString();
    });

    process.on('error', (error) => {
      vscode.window.showErrorMessage(`Sirji> Python script execution error: ${error.message}`);
      reject(error);
    });

    process.on('close', (code) => {
      if (code === 0) {
        resolve(responseData);
      } else {
        if (errorData) {
          vscode.window.showErrorMessage(`Sirji> Python script execution error: ${errorData}`);
        }
        reject(errorData);
      }
    });
  });
}
