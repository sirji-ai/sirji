import * as vscode from 'vscode';
import * as fs from 'fs';
import path from 'path';

const escapeRegExp = (string: string) => {
  return string.replace(/[.*+\-?^${}()|[\]\\]/g, '\\$&');
};

export const findAndReplaceInProjectFile = async (body: string, projectRootPath: string, globPattern?: string, exclude: string = '**/node_modules/**'): Promise<any> => {
  let searchText, replacement, filePath;

  try {
    searchText = body.split('FIND:')[1].split('---')[0].trim();
  } catch (error) {
    console.error('Error parsing body:', error);
    return `The error in parsing the BODY: ${error}. Either the FIND key is missing or not in the correct format. The correct format is FIND: {{Code to Find without any special characaters}} ---. Your response must conform strictly to FIND_AND_REPLACE Response Template with all the keys present in the BODY`;
  }

  try {
    replacement = body.split('REPLACE:')[1].split('---')[0].trim();
  } catch (error) {
    console.error('Error parsing body:', error);
    return `The error in parsing the BODY: ${error}. Either the REPLACE key is missing or not in the correct format. The correct format is REPLACE: {{Code to Replace without any special characaters}} ---. Your response must conform strictly to FIND_AND_REPLACE Response Template with all the keys present in the BODY`;
  }

  try {
    filePath = body.split('FILE_PATH:')[1].split('---')[0].trim();
  } catch (error) {
    console.error('Error parsing body:', error);
    return `The error in parsing the BODY: ${error}. Either the FILE_PATH key is missing or not in the correct format. The correct format is FILE_PATH: {{File path}} ---. Your response must conform strictly to FIND_AND_REPLACE Response Template with all the keys present in the BODY`;
  }

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
        return `ERROR: The provided FIND: ${searchText} was not found in the file. Please make sure to provided FIND exists in the file without any special characters or newlines. The FIND is case-sensitive`;
      }

      await editor.edit((editBuilder) => {
        const regex = new RegExp(escapeRegExp(searchText), 'g');
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
