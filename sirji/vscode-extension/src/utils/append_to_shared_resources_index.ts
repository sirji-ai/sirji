import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export async function appendToSharedResourcesIndex(sharedResourcesFolderPath: string, messageBody: string, agentId: string): Promise<string> {
  try {
    const [filePathString, filePathContentDescription] = messageBody.split('---');
    const filePath = filePathString.replace('File path:', '').trim();

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

    const uri = vscode.Uri.file(path.join(sharedResourcesFolderPath, 'index.json'));

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

    console.log(`Shared resource index updated successfully: ${uri.fsPath}`);

    return 'Updated shared resources index file.';
  } catch (e) {
    const errorMessage = `Failed to create or write to the file. Error: ${e}`;
    return errorMessage;
  }
}
