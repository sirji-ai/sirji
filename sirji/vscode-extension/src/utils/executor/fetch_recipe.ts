import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { getFilePath } from './helper';

export async function fetchRecipe(FolderPath: string, body: string): Promise<any> {
  try {
    const filePath = body.split('File path:')[1].trim();
    let fullFilePath = '';
    try {
      fullFilePath = getFilePath(filePath, FolderPath);
    } catch (error) {
      return error;
    }

    const uri = vscode.Uri.file(fullFilePath);

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
