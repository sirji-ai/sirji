import * as vscode from 'vscode';
import * as fs from 'fs';
import path from 'path';

export const insertText = async (body: string, projectRootPath: string, globPattern?: string, exclude: string = '**/node_modules/**'): Promise<string> => {
  let searchText, textToInsert, filePath, insertPosition;

  try {
    searchText = body.split('FIND:')[1].split('---')[0].trim();
  } catch (error) {
    console.error('Error parsing body:', error);
    return `The error in parsing the BODY: ${error}. Either the FIND key is missing from the BODY or it's not in the correct format. The correct format is FIND: {{Text to find without any special characters}} ---. Your response must conform strictly to the INSERT_TEXT Response Template with all the keys present in the BODY.`;
  }

  try {
    textToInsert = body.split('CODE_TO_INSERT:')[1].split('---')[0];
  } catch (error) {
    console.error('Error parsing body:', error);
    return `The error in parsing the BODY: ${error}. Either the CODE_TO_INSERT key is missing or not in the correct format. The correct format is CODE_TO_INSERT: {{Code to insert without any special characaters}} ---. Your response must conform strictly to INSERT_TEXT Response Template with all the keys present in the BODY`;
  }

  try {
    filePath = body.split('FILE_PATH:')[1].split('---')[0].trim();
  } catch (error) {
    console.error('Error parsing body:', error);
    return `The error in parsing the BODY: ${error}. Either the FILE_PATH key is missing or not in the correct format. The correct format is FILE_PATH: {{File path without any special characaters}} ---. Your response must conform strictly to INSERT_TEXT Response Template with all the keys present in the BODY`;
  }

  try {
    insertPosition = body.split('INSERT_POSITION_RELATIVE_TO_FIND:')[1].split('---')[0].trim();
  } catch (error) {
    console.error('Error parsing body:', error);
    return `The error in parsing the BODY: ${error}. Either the INSERT_POSITION_RELATIVE_TO_FIND key is missing or not in the correct format. The correct format is INSERT_POSITION_RELATIVE_TO_FIND: {{above or below}} ---. Your response must conform strictly to INSERT_TEXT Response Template with all the keys present in the BODY`;
  }

  filePath = path.join(projectRootPath, filePath);

  console.log(`Inserting text in file: ${filePath} based on search text: '${searchText}' with replacement: '${textToInsert}' and insert position: '${insertPosition}'`);

  try {
    if (!fs.existsSync(filePath)) {
      console.error('File does not exist:', filePath);
      return 'Error: File does not exist';
    }

    const document = await vscode.workspace.openTextDocument(filePath);
    const editor = await vscode.window.showTextDocument(document);

    const range = new vscode.Range(document.positionAt(0), document.positionAt(document.getText().length));
    const text = document.getText(range);

    const index = text.indexOf(searchText);
    if (index === -1) {
      console.error('Search text not found in the document.');
      return `ERROR: The provided FIND: ${searchText} was not found in the file. Please make sure to provided FIND exists in the file without any special characters or newlines. The FIND is case-sensitive`;
    }

    const position = document.positionAt(index);
    const line = position.line;

    await editor.edit((editBuilder) => {
      if (insertPosition.toLowerCase() === 'above') {
        editBuilder.insert(new vscode.Position(line, 0), textToInsert + '\n');
      } else if (insertPosition.toLowerCase() === 'below') {
        editBuilder.insert(new vscode.Position(line + 1, 0), textToInsert + '\n');
      }
    });

    await document.save();
    await vscode.commands.executeCommand('workbench.action.closeActiveEditor');
    console.log('Text insertion completed in file:', filePath);
    return 'Done';
  } catch (error) {
    console.error(`Error processing file: ${error}`);
    return `Failed to process file: ${error}`;
  }
};
