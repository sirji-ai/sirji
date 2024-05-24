import * as vscode from 'vscode';
import * as fs from 'fs';
import * as path from 'path'; // Added path module

const sanitizeFolderPath = (folderPath: string) => {
  return folderPath.endsWith('/') ? folderPath.slice(0, -1) : folderPath;
};

const extractSearchTerm = (body: string): string | null => {
  const match = body.match(/Search Term:\s*(.*)/);
  return match ? match[1].trim() : null;
};

export const searchCodeInProject = async (body: string, projectPath: string, globPattern: string = '**/*.*', exclude: string = '**/node_modules/**'): Promise<string[]> => {
  try {
    console.log(`Base path: ${projectPath}`);
    const searchTerm = extractSearchTerm(body);

    if (!searchTerm) {
      console.error('No search term found in body. Ensure "Search Term:" is specified.');
      return [];
    }

    console.log(`Search term extracted: "${searchTerm}"`);

    const basePath = sanitizeFolderPath(projectPath);

    const workspaceFolders = vscode.workspace.workspaceFolders;
    if (!workspaceFolders) {
      console.error('No workspace folders found. Make sure the project is opened in VS Code.');
      return [];
    }

    // Check if the projectPath is part of the workspace
    const isBasePathInWorkspace = workspaceFolders.some((folder) => basePath.startsWith(folder.uri.fsPath));
    if (!isBasePathInWorkspace) {
      console.error(`The path provided (${basePath}) is not part of the opened workspace.`);
      return [];
    }

    const pattern = new vscode.RelativePattern(basePath, globPattern);

    console.log(`Searching for files with pattern: ${pattern} excluding: ${exclude}`);

    const files = await vscode.workspace.findFiles(pattern, new vscode.RelativePattern(basePath, exclude));
    console.log(`Found ${files.length} files with pattern: ${pattern.pattern}`);
    const foundFiles: string[] = [];

    for (const file of files) {
      console.log(`Reading file: ${file.fsPath}`);
      try {
        const content = fs.readFileSync(file.fsPath, 'utf-8');
        if (content.includes(searchTerm)) {
          console.log(`Search term found in file: ${file.fsPath}`);
          foundFiles.push(file.fsPath);
        }
      } catch (readError) {
        console.error(`Error reading file ${file.fsPath}: ${readError}`);
      }
    }

    console.log(`Found ${foundFiles.length} files containing the search term: ${searchTerm}`);
    return foundFiles;
  } catch (error) {
    console.error(`Error searching for code in project: ${error}`);
    throw new Error('Error while searching for code in project: ' + error);
  }
};
