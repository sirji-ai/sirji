import * as vscode from 'vscode';

export async function searchFile(name: string, maxResults: number = 10, exclude: string = '**/node_modules/**'): Promise<vscode.Uri[]> {
  const pattern = `**/*${name}*/**/*`;

  try {
    const result = await vscode.workspace.findFiles(pattern, exclude, maxResults);
    console.log(`Found ${result.length} files`);
    return result;
  } catch (error) {
    vscode.window.showErrorMessage(`Error searching files: ${error}`);
    return [];
  }
}
