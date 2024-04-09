import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path';

async function checkForChanges(filePath: string, previousContent: string): Promise<{ hasChanges: boolean; currentContent: string }> {
  const currentContent = fs.readFileSync(filePath, 'utf-8');

  const hasChanges = currentContent !== previousContent;

  return {
    hasChanges,
    currentContent
  };
}

function constructResponse(isRunning: Boolean, tempFilePath: string, tempFileContent: string): string {
  let response = isRunning ? 'Execute Command still running.' : 'Execute command complete.';
  response += `Command execution output from ${tempFilePath}\n`;
  response += `${tempFileContent}`;
  return response;
}

export async function executeTask(command: string, workspaceRootPath: string): Promise<string> {
  return new Promise(async (resolve, reject) => {
    const tempFileName = `output.txt`;
    const tempFilePath = path.join(workspaceRootPath, tempFileName);
    let tempFileContent: string;

    command = `(${command}) > "${tempFilePath}" 2>&1`;

    const shellExecution = new vscode.ShellExecution(command);
    const taskDefinition = { type: 'shell' };
    const task = new vscode.Task(taskDefinition, vscode.TaskScope.Workspace, 'Sirji', 'Custom', shellExecution);

    const disposables: vscode.Disposable[] = [];

    let isTaskExecutionInProgress = false;
    let checkTaskPeriodically: any = null;
    let hasReturnTaskExecutionResponse: Boolean = false;

    try {
      const execution = await vscode.tasks.executeTask(task);

      disposables.push(
        vscode.tasks.onDidStartTask((event) => {
          if (event.execution.task === task) {
            isTaskExecutionInProgress = true;
            checkTaskPeriodically = setInterval(async function () {
              const response = await checkForChanges(tempFilePath, tempFileContent);

              tempFileContent = response.currentContent;
              if (!response.hasChanges && !hasReturnTaskExecutionResponse) {
                hasReturnTaskExecutionResponse = true;

                return resolve(constructResponse(isTaskExecutionInProgress, tempFilePath, tempFileContent));
              }
            }, 30000);
          }
        })
      );

      disposables.push(
        vscode.tasks.onDidEndTaskProcess(async (event) => {
          isTaskExecutionInProgress = false;
          clearTimeout(checkTaskPeriodically);
          if (!hasReturnTaskExecutionResponse) {
            const response = await checkForChanges(tempFilePath, tempFileContent);
            tempFileContent = response.currentContent;
            hasReturnTaskExecutionResponse = true;
            return resolve(constructResponse(isTaskExecutionInProgress, tempFilePath, tempFileContent));
          }
        })
      );
    } catch (error) {
      console.error(`Failed to execute task: ${error}`);
      throw error;
    } finally {
      disposables.forEach((d) => d.dispose());
    }
  });
}
