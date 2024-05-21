import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export async function fetchRecipeIndex(FolderPath: string): Promise<string> {
  try {
    const fileName = 'index.json';

    const uri = vscode.Uri.file(path.join(FolderPath, fileName));

    if (!fs.existsSync(uri.fsPath)) {
      return 'Index not found';
    }

    const content = await vscode.workspace.fs.readFile(uri);

    const index = JSON.parse(Buffer.from(content).toString('utf-8'));

    return `The recipe index has following content: ${JSON.stringify(index, null, 2)}`;
  } catch (e) {
    const errorMessage = `Failed to read the file. Error: ${e}`;
    return errorMessage;
  }
}
