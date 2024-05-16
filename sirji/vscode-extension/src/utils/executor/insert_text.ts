import * as vscode from 'vscode';
import * as fs from 'fs';
import path from 'path';

export const insertText = async (body: string, projectRootPath: string, globPattern?: string, exclude: string = '**/node_modules/**'): Promise<string> => {
  let searchText, textToInsert, filePath, insertPosition;

  try {
    searchText = body.split('FIND:')[1].split('---')[0].trim();
    textToInsert = body.split('TEXT_TO_INSERT:')[1].split('---')[0].trim();
    filePath = body.split('FILE_PATH:')[1].split('---')[0].trim();
    insertPosition = body.split('INSERT_POSITION:')[1].split('---')[0].trim();
  } catch (error) {
    console.error('Error parsing body:', error);
    return 'Error in processing your last response. Your response must conform strictly to one of the allowed Response Templates, as it will be processed programmatically and only these templates are recognized. Your response for the INSERT_TEXT action must conform this response template: FILE_PATH: {{File path}} ---FIND: {{Text to find}} ---INSERT_POSITION: {{above or below}}---TEXT_TO_INSERT: {{Text to insert}}--- ';
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
      return 'ERROR: The specified string to find was not found in the document. Please re-read the content of the file and ensure you have provided the correct string to search for, then try again';
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
