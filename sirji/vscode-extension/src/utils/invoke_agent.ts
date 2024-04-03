import * as childProcess from 'child_process';
import * as vscode from 'vscode';
import path from 'path';
import os from 'os';

export async function invokeAgent(venvPath: string, scriptPath: string, args: string[] = []): Promise<any> {
 console.log('Executing command:', 'python3', [scriptPath, ...args].join(' '));
 const response = await executePythonScript(venvPath, scriptPath, args);
 console.log(response);
 return response;
}

async function executePythonScript(venvPath: string, scriptPath: string, args: string[] = []): Promise<any> {
 let pythonPath = 'python3';

 if (venvPath !== '') {
  // Determine the correct path for the Python executable based on the OS
  const pythonExecutable = os.platform() === 'win32' ? 'python.exe' : 'bin/python3';

  // Generate the full path to the Python executable inside the virtual environment
  pythonPath = path.join(venvPath, pythonExecutable);
 }

 return new Promise((resolve, reject) => {
  const process = childProcess.spawn(pythonPath, [scriptPath, ...args]);

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
    reject(new Error(`script exited with code ${code}`));
   }
  });
 });
}
