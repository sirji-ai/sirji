import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export async function fetchRecipe(FolderPath: string, body: string): Promise<string> {
  try {
    const filePath = body.split('File path:')[1].trim();

    const uri = vscode.Uri.file(path.join(FolderPath, filePath));

    if (!fs.existsSync(uri.fsPath)) {
      return 'Index not found';
    }

    const content = await vscode.workspace.fs.readFile(uri);

    const recipeContent = JSON.parse(Buffer.from(content).toString('utf-8'));

    return `${JSON.stringify(recipeContent, null, 2)}`;
  } catch (e) {
    const errorMessage = `Failed to read the file. Error: ${e}`;
    return errorMessage;
  }
}
