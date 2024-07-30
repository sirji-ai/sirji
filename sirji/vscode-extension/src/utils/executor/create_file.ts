import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs';
import { getFilePath } from './helper';

export function sanitizePath(filePath: string): string {
  return filePath.replace(/^['"]|['"]$/g, '');
}

export async function createFile(rootPath: string, isProjectRoot: boolean, body: string): Promise<any> {
  try {
    const [filePathPart, fileContent] = body.split('---');
    const filePath = filePathPart.replace('File path:', '').trim();
    const sanitizedFilePath = sanitizePath(filePath);

    let fullPath = '';
    try {
      fullPath = getFilePath(sanitizedFilePath, rootPath);
    } catch (error) {
      return error;
    }
    const uri = vscode.Uri.file(fullPath);

    if (isProjectRoot) {
      if (!isInsideProject(uri.fsPath, rootPath)) {
        throw new Error('File path is outside of the project folder tree. Write operation denied.');
      }
    } else {
      if (path.isAbsolute(sanitizedFilePath)) {
        throw new Error('Absolute file path is not allowed while creating file in Agent Output Folder. Write operation denied.');
      }
    }

    const directoryPath = path.dirname(uri.fsPath);
    if (!fs.existsSync(directoryPath)) {
      await vscode.workspace.fs.createDirectory(vscode.Uri.file(directoryPath));
    }

    const content = Buffer.from(fileContent, 'utf8');
    await vscode.workspace.fs.writeFile(uri, content);

    console.log(`File created successfully: ${uri.fsPath}`);

    return 'File created successfully';
  } catch (e) {
    const errorMessage = `Failed to create or write to the file. Make sure you provided the body with correct structure as mentioned in the Allowed response template. Error: ${e}`;
    return errorMessage;
  }
}

function isInsideProject(filePath: string, projectRootPath: string): boolean {
  const relativePath = path.relative(projectRootPath, filePath);
  return !relativePath.startsWith('..') && !path.isAbsolute(relativePath);
}
