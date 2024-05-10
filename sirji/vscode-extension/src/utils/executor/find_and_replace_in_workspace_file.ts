import * as vscode from 'vscode';
import * as fs from 'fs';
import path from 'path';

export const findAndReplaceInWorkspaceFile = async (body: string, workspaceRootPath: string, globPattern?: string, exclude: string = '**/node_modules/**'): Promise<string> => {
  const searchText = body.split('FIND:')[1].split('---')[0].trim();
  const replacement = body.split('REPLACE:')[1].split('---')[0].trim();
  let filePath = body.split('FILE_PATH:')[1].split('---')[0].trim();
  filePath = path.join(workspaceRootPath, filePath);

  console.log(`Searching for files with pattern: ${searchText} in folder: ${filePath} and replacing with: ${replacement}`);

  const basePath = filePath ? `${filePath}/` : '**/';
  const namePattern = '**/*.*';
  const pattern = `${basePath}${namePattern}`;

  console.log(`Searching for files with pattern: ${pattern} and excluding: ${exclude} in folder: ${filePath}`);
  try {
    if (fs.existsSync(filePath)) {
      const document = await vscode.workspace.openTextDocument(filePath);
      const editor = await vscode.window.showTextDocument(document);
      const allText = new vscode.Range(document.positionAt(0), document.positionAt(document.getText().length));

      await editor.edit((editBuilder) => {
        let text = document.getText(allText);
        const regex = new RegExp(searchText, 'g');
        text = text.replace(regex, replacement);
        editBuilder.replace(allText, text);
      });

      await document.save();
      await vscode.commands.executeCommand('workbench.action.closeActiveEditor');
      console.log('Replacement done in file:', filePath);
      return 'Done';
    } else {
      console.error('File does not exist:', filePath);
      return 'Error: File does not exist';
    }
  } catch (error) {
    console.error(`Error replacing text in files: ${error}`);
    return 'Error while replacing text in files. error: ' + error;
  }
};
