import * as vscode from 'vscode';

export async function searchFileInWorkspace(
  searchText: string,
  folderPath: string = '',
  fileType: string = '*',
  maxResults: number = 10,
  exclude: string = '**/node_modules/**'
): Promise<vscode.Uri[]> {
  const basePath = folderPath ? `${folderPath}/` : '**/';
  const namePattern = searchText.includes('*') ? searchText : `*${searchText}*`;
  const pattern = `${basePath}${namePattern}.${fileType}`;

  try {
    const result = await vscode.workspace.findFiles(pattern, exclude, maxResults);
    console.log(`Found ${result.length} files`);
    return result;
  } catch (error) {
    return [];
  }
}
