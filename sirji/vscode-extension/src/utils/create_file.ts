import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export async function createFile(workspaceRootPath: string, body: string): Promise<string> {
  try {
    const [filePath, fileContent] = body.split('---');
    const fileName = filePath.replace('File path:', '').trim();

    const uri = vscode.Uri.file(path.join(workspaceRootPath, fileName));

    const directoryPath = path.dirname(uri.fsPath);
    if (!fs.existsSync(directoryPath)) {
      await vscode.workspace.fs.createDirectory(vscode.Uri.file(directoryPath));
    }

    const content = Buffer.from(fileContent, 'utf8');
    await vscode.workspace.fs.writeFile(uri, content);

    console.log(`File created successfully: ${uri.fsPath}`);

    return 'Done';
  } catch (e) {
    const errorMessage = `Failed to create or write to the file. Error: ${e}`;
    return errorMessage;
  }
}
