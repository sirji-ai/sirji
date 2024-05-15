import * as vscode from 'vscode';
import * as fs from 'fs';
import path from 'path';

export const insertText = async (body: string, projectRootPath: string, globPattern?: string, exclude: string = '**/node_modules/**'): Promise<string> => {
  const searchText = body.split('FIND:')[1].split('---')[0].trim();
  const textToInsert = body.split('TEXT_TO_INSERT:')[1].split('---')[0].trim();
  let filePath = body.split('FILE_PATH:')[1].split('---')[0].trim();
  let insertPosition = body.split('INSERT_POSITION:')[1].split('---')[0].trim();

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
      return 'Error: Search text not found';
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
