import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';

export async function fetchRecipes(FolderPath: string): Promise<string> {
  try {
    const fileName = 'index.json';

    const uri = vscode.Uri.file(path.join(FolderPath, fileName));

    const directoryPath = path.dirname(uri.fsPath);

    if (!fs.existsSync(directoryPath)) {
      await vscode.workspace.fs.createDirectory(vscode.Uri.file(directoryPath));
    }

    if (!fs.existsSync(uri.fsPath)) {
      return 'Index not found';
    }

    const content = await vscode.workspace.fs.readFile(uri);

    const index = JSON.parse(Buffer.from(content).toString('utf-8'));
    let recipeContent = '';
    for (const file in index) {
      const fileContent = await vscode.workspace.fs.readFile(vscode.Uri.file(path.join(FolderPath, file)));
      recipeContent += `Content of ${file}\n---\n${Buffer.from(fileContent).toString('utf-8')}\n\n`;
    }

    return `Index\n---\n${JSON.stringify(index, null, 2)}\n\n${recipeContent}`;
  } catch (e) {
    const errorMessage = `Failed to create or write to the file. Error: ${e}`;
    return errorMessage;
  }
}
