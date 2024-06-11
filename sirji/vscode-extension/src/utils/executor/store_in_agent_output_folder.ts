import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { createFile, sanitizePath } from './create_file';

export async function storeInAgentOutputFolder(agentOutputFolderPath: string, messageBody: string, agentId: string): Promise<string> {
  try {
    const [filePathString, agentOutputFileContentString, filePathContentDescriptionString] = messageBody.split('---');
    let filePath = filePathString.replace('File path:', '').trim();
    filePath = sanitizePath(filePath); 
    let agentOutputFileContent = agentOutputFileContentString.replace('File content:', '').trim();
    let filePathContentDescription = filePathContentDescriptionString.replace('File content description:', '').trim();
  
    let bodyForFileCreation = `File path:${filePath}---${agentOutputFileContent}`;

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

    return `${fileCreationRes} and Agent Output Index updated successfully`;
  } catch (e) {
    const errorMessage = `Failed to create or write to the file. Make sure you provided the body with correct structure as mentioned in the Allowed response template. Error: ${e}`;
    return errorMessage;
  }
}
