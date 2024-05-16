import * as vscode from 'vscode';
import * as fs from 'fs';

export async function searchFileInProject(body: string, fileType: string = '*', maxResults: number = 10, exclude: string = '**/node_modules/**'): Promise<vscode.Uri[]> {
  const searchText = body.split('Search:')[1].split('---')[0].trim();
  const folderPath = body.split('Directory:')[1].trim();

  console.log(`Searching for files with pattern: ${searchText} in folder: ${folderPath}`);

  const basePath = folderPath ? `${folderPath}/` : '**/';
  const namePattern = searchText.includes('*') ? searchText : `*${searchText}*`;
  const pattern = `${basePath}${namePattern}.${fileType}`;

  try {
    const files = await vscode.workspace.findFiles(pattern, exclude, maxResults);

    const result: vscode.Uri[] = [];

    for (const file of files) {
      console.log(`Found file: ${file.fsPath}`);
      const content = fs.readFileSync(file.fsPath, 'utf-8');
      if (content.includes(searchText)) {
        result.push(file);
      }
    }

    console.log(`Found ${result.length} files`);
    return result;
  } catch (error) {
    return [];
  }
}
