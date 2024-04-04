import * as vscode from 'vscode';
import path from 'path';

export function createFile(workspaceRootPath: any, fileName: string, fileContent: string) {
  const uri = vscode.Uri.file(path.join(workspaceRootPath, fileName));
  const content = new Uint8Array(Buffer.from(fileContent, 'utf8'));
  vscode.workspace.fs.writeFile(uri, content);
}
