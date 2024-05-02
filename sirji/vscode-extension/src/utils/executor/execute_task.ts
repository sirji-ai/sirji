import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';
import * as os from 'os';

let currentTaskExecution: any = null;

async function checkForChanges(filePath: string, previousContent: string): Promise<{ hasChanges: boolean; currentContent: string }> {
  const currentContent = fs.readFileSync(filePath, 'utf-8');

  const hasChanges = currentContent !== previousContent;

  return {
    hasChanges,
    currentContent
  };
}

function constructResponse(isRunning: Boolean, tempFileRelativePath: string, tempFileContent: string): string {
  let response = isRunning ? 'Command is still running.' : 'Command execution completed.';
  response += `\n------\nOutput from the command is getting logged to ${tempFileRelativePath}`;
  response += `\n------\nOutput till now:\n${tempFileContent}\n------`;
  return response;
}

export async function executeTask(command: string, workspaceRootPath: string): Promise<string> {
  return new Promise(async (resolve, reject) => {
    const tempFileName = `output_${Date.now()}.txt`;

    const tempFileRelativePath = path.join(workspaceRootPath, tempFileName);
    const tempFilePath = path.join(workspaceRootPath, tempFileRelativePath);

    let tempFileContent = '';

    if (os.platform() === 'win32') {
      command = `${command} > "${tempFilePath}" 2>&1`;
    } else {
      command = `(${command}) 2>&1 | tee "${tempFilePath}"`;
    }

    const shellExecution = new vscode.ShellExecution(command);
    const taskDefinition = { type: 'shell' };
    const task = new vscode.Task(taskDefinition, vscode.TaskScope.Workspace, 'Sirji', 'Custom', shellExecution);

    const disposables: vscode.Disposable[] = [];

    let isTaskExecutionInProgress = false;
    let checkTaskPeriodically: any = null;

    try {
      console.log(` executeTask currentTaskExecution ${command}:`, { currentTaskExecution });
      if (currentTaskExecution) {
        try {
          currentTaskExecution.terminate();
          console.log('executeTask Terminated existing task.');
        } catch (terminateError) {
          console.error('executeTask Error terminating existing task:', terminateError);
        }
      }

      const execution = await vscode.tasks.executeTask(task);

      console.log(`executeTask new task ${command}:`, { isTaskExecutionInProgress, tempFileName });

      disposables.push(
        vscode.tasks.onDidStartTask((event) => {
          console.log(`executeTask inside onDidStartTask ${command}:`, event);
          if (event.execution.task === task) {
            if (event.execution.task.name === 'Sirji') {
              currentTaskExecution = event.execution;
            }
            isTaskExecutionInProgress = true;
            console.log(`executeTask setting setInterval ${command}:`, { isTaskExecutionInProgress, tempFileName });
            checkTaskPeriodically = setInterval(async function () {
              const response = await checkForChanges(tempFilePath, tempFileContent);

              console.log(`executeTask setInterval executed ${command}:`, { isTaskExecutionInProgress, tempFileName });

              tempFileContent += response.currentContent;
              clearInterval(checkTaskPeriodically);
              return resolve(constructResponse(isTaskExecutionInProgress, tempFileRelativePath, tempFileContent));
            }, 10000);
          }
        })
      );

      disposables.push(
        vscode.tasks.onDidEndTask(async (event) => {
          console.log(`executeTask inside onDidEndTaskProcess ${command}:`, event);
          isTaskExecutionInProgress = false;
          clearInterval(checkTaskPeriodically);
          const response = await checkForChanges(tempFilePath, tempFileContent);
          tempFileContent = response.currentContent;
          return resolve(constructResponse(isTaskExecutionInProgress, tempFileRelativePath, tempFileContent));
        })
      );
    } catch (error) {
      console.error(`Failed to execute task: ${error}`);
      throw error;
    }
  });
}
