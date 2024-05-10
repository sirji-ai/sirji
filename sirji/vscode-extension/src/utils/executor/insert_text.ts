import * as vscode from 'vscode';
import * as fs from 'fs';
import path from 'path';

export const insertText = async (body: string, workspaceRootPath: string, globPattern?: string, exclude: string = '**/node_modules/**'): Promise<string> => {
  const searchText = body.split('FIND:')[1].split('---')[0].trim();
  const textToInsert = body.split('TEXT_TO_INSERT:')[1].split('---')[0].trim();
  let filePath = body.split('FILE_PATH:')[1].split('---')[0].trim();
  let insertPosition = body.split('INSERT_POSITION:')[1].split('---')[0].trim();

  filePath = path.join(workspaceRootPath, filePath);

  console.log(`Inserting text in file: ${filePath} based on search text: '${searchText}' with replacement: '${textToInsert}' and insert position: '${insertPosition}'`);

  try {
    if (!fs.existsSync(filePath)) {
      console.error('File does not exist:', filePath);
      return 'Error: File does not exist';
    }

    const document = await vscode.workspace.openTextDocument(filePath);
    const editor = await vscode.window.showTextDocument(document);

    await editor.edit((editBuilder) => {
      let text = document.getText();

      let safeSearchText = searchText.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
      const regex = new RegExp(`\\b${safeSearchText}\\b`, 'g');

      if (insertPosition.toLowerCase() === 'above') {
        text = text.replace(regex, `${textToInsert}\n${searchText}`);
      } else if (insertPosition.toLowerCase() === 'below') {
        text = text.replace(regex, `${searchText}\n${textToInsert}`);
      }

      editBuilder.replace(new vscode.Range(document.positionAt(0), document.positionAt(text.length)), text);
    });

    await document.save();
    // await vscode.commands.executeCommand('workbench.action.closeActiveEditor');
    console.log('Text insertion completed in file:', filePath);
    return 'Done';
  } catch (error) {
    console.error(`Error processing file: ${error}`);
    return `Failed to process file: ${error}`;
  }
};
