import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { createFile, sanitizePath } from './create_file';

export async function storeInAgentOutputFolder(agentOutputFolderPath: string, messageBody: string, agentId: string): Promise<string> {
  try {
    // const [filePathString, agentOutputFileContentString, filePathContentDescriptionString] = messageBody.split('---');
    const filePathMatch = messageBody.match(/File path:\s*(.+?)\s*---/s);
    const fileContentMatch = messageBody.match(/File content:\s*([\s\S]+?)\s*---(?=\nFile content description:)/s);
    const fileDescriptionMatch = messageBody.match(/File content description:\s*(.+)$/s);
    if (filePathMatch && fileContentMatch && fileDescriptionMatch) {
      let filePath = filePathMatch[1].trim();
      filePath = sanitizePath(filePath);
      let agentOutputFileContent = fileContentMatch[1].trim();
      let filePathContentDescription = fileDescriptionMatch[1].trim();

      const bodyForFileCreation = `File path:${filePath}---${agentOutputFileContent}`;
      const fileCreationRes = await createFile(agentOutputFolderPath, false, bodyForFileCreation);

      let fileDescription = '';
      if (filePathContentDescription) {
        fileDescription = filePathContentDescription.trim();
      }

      const fileContent = {
        [filePath]: {
          description: fileDescription,
          created_by: agentId
        }
      };

      const uri = vscode.Uri.file(path.join(agentOutputFolderPath, 'index.json'));

      const directoryPath = path.dirname(uri.fsPath);
      if (!fs.existsSync(directoryPath)) {
        await vscode.workspace.fs.createDirectory(vscode.Uri.file(directoryPath));
      }

      let content: Buffer;

      if (fs.existsSync(uri.fsPath)) {
        const existingContent = await vscode.workspace.fs.readFile(uri);
        const existingContentString = Buffer.from(existingContent).toString('utf-8');
        const existingContentJson = JSON.parse(existingContentString);
        existingContentJson[filePath] = fileContent[filePath];
        content = Buffer.from(JSON.stringify(existingContentJson, null, 2), 'utf8');
      } else {
        content = Buffer.from(JSON.stringify(fileContent, null, 2), 'utf8');
      }

      await vscode.workspace.fs.writeFile(uri, content);

      return 'Stored the file and registered it in the Agent Output Index file successfully';
    }
    return 'Failed to store the file in the Agent Output Folder. Make sure you provided the body with correct structure as mentioned in the Allowed response template.';
  } catch (e) {
    const errorMessage = `Failed to create or write to the file. Make sure you provided the body with correct structure as mentioned in the Allowed response template. Error: ${e}`;
    return errorMessage;
  }
}
