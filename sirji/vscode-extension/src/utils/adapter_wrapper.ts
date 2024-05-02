import * as childProcess from 'child_process';
import * as vscode from 'vscode';
import path from 'path';
import os from 'os';
import { SecretStorage } from './secret_storage';
import { Constants } from './constants';
import fs from 'fs';
import { readDirectoryStructure } from './executor/read_directory_structure';

export async function spawnAdapter(
  context: vscode.ExtensionContext | undefined,
  sirjiInstallationPath: string,
  sirjiRunPath: string,
  workspaceRootPath: string,
  scriptPath: string,
  args: string[] = []
): Promise<any> {
  console.log('Executing command:', 'python3', [scriptPath, ...args].join(' '));

  const venvPath = path.join(sirjiInstallationPath, 'venv');
  const pythonPath = getPythonPath(venvPath);
  const envVars = await getEnvVars(context, sirjiInstallationPath, workspaceRootPath, sirjiRunPath);

  console.log('---------env vars', envVars);

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

function getPythonPath(venvPath: string): string {
  let pythonPath = 'python3';

  if (fs.existsSync(venvPath)) {
    // Determine the correct path for the Python executable based on the OS
    const pythonExecutable = os.platform() === 'win32' ? 'scripts/python.exe' : 'bin/python3';

    // Generate the full path to the Python executable inside the virtual environment
    pythonPath = path.join(venvPath, pythonExecutable);
  }

  return pythonPath;
}

async function getEnvVars(context: vscode.ExtensionContext | undefined, sirjiInstallationPath: string, workspacePath: string, sirjiRunPath: string): Promise<any> {
  const secretManager = new SecretStorage(context);
  const envVars = JSON.parse((await secretManager.retrieveSecret(Constants.ENV_VARS_KEY)) || '{}');
  envVars.SIRJI_INSTALLATION_DIR = sirjiInstallationPath;
  envVars.SIRJI_WORKSPACE = workspacePath;
  envVars.SIRJI_RUN_PATH = sirjiRunPath;
  envVars.SIRJI_WORKSPACE_STRUCTURE = await readDirectoryStructure(workspacePath, 'Directory: /');
  return envVars;
}
