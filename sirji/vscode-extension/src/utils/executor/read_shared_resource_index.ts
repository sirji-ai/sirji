import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export async function readSharedResourcesIndex(sharedResourcesFolderPath: string): Promise<string> {
  try {
    const fileName = 'index.json';

    const uri = vscode.Uri.file(path.join(sharedResourcesFolderPath, fileName));

    const directoryPath = path.dirname(uri.fsPath);

    if (!fs.existsSync(directoryPath)) {
      await vscode.workspace.fs.createDirectory(vscode.Uri.file(directoryPath));
    }

    if (!fs.existsSync(uri.fsPath)) {
      return 'Shared resources index not found';
    }

    const content = await vscode.workspace.fs.readFile(uri);

    return `Content of shared resource index.json\n---\n${Buffer.from(content).toString('utf-8')}`;
  } catch (e) {
    const errorMessage = `Failed to create or write to the file. Error: ${e}`;
    return errorMessage;
  }
}
