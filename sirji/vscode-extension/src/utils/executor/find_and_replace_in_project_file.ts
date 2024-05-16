import * as vscode from 'vscode';
import * as fs from 'fs';
import path from 'path';

export const findAndReplaceInProjectFile = async (body: string, projectRootPath: string, globPattern?: string, exclude: string = '**/node_modules/**'): Promise<string> => {
  const searchText = body.split('FIND:')[1].split('---')[0].trim();
  const replacement = body.split('REPLACE:')[1].split('---')[0].trim();
  let filePath = body.split('FILE_PATH:')[1].split('---')[0].trim();
  filePath = path.join(projectRootPath, filePath);

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

      let text = document.getText(allText);
      if (!text.includes(searchText)) {
        return 'ERROR: The specified string to find was not found in the document. Please re-read the content of the file and ensure you have provided the correct string to search for, then try again.';
      }

      await editor.edit((editBuilder) => {
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
