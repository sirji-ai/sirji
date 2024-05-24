import * as vscode from 'vscode';
import * as fs from 'fs';
import path from 'path';

function delay(ms: number) {
  return new Promise((res) => setTimeout(res, ms));
}

async function checkForSyntaxErrors(document: vscode.TextDocument): Promise<string[]> {
  await delay(4500);
  const diagnostics = vscode.languages.getDiagnostics(document.uri);
  const syntaxErrors: string[] = diagnostics.map((diag) => `${diag.message} at line ${diag.range.start.line}, column ${diag.range.start.character}`);
  return syntaxErrors;
}

async function discardAndCloseEditor(uri: vscode.Uri) {
  const originalDocument = await vscode.workspace.openTextDocument(uri);
  const emptyEdit = new vscode.WorkspaceEdit();
  emptyEdit.replace(uri, new vscode.Range(new vscode.Position(0, 0), new vscode.Position(Number.MAX_SAFE_INTEGER, Number.MAX_SAFE_INTEGER)), originalDocument.getText());
  await vscode.workspace.applyEdit(emptyEdit);
  await vscode.commands.executeCommand('workbench.action.revertAndCloseActiveEditor');
}
async function insertCode(document: vscode.TextDocument, editor: vscode.TextEditor, textToInsert: string, line: number, insertPosition: string): Promise<boolean> {
  return editor.edit((editBuilder) => {
    if (insertPosition.toLowerCase() === 'above') {
      editBuilder.insert(new vscode.Position(line, 0), textToInsert + '\n');
    } else if (insertPosition.toLowerCase() === 'below') {
      editBuilder.insert(new vscode.Position(line + 1, 0), textToInsert + '\n');
    }
  });
}

export const insertText = async (body: string, projectRootPath: string, globPattern?: string, exclude: string = '**/node_modules/**'): Promise<string> => {
  let searchText, textToInsert, filePath, insertPosition;

  try {
    searchText = body.split('FIND_CODE:')[1].split('---')[0].trim();
  } catch (error) {
    console.error('Error parsing body:', error);
    return `The error in parsing the BODY: ${error}. Either the FIND_CODE key is missing from the BODY or it's not in the correct format. The correct format is FIND_CODE: {{Text to find without any special characters}} ---. Your response must conform strictly to the INSERT_TEXT Response Template with all the keys present in the BODY.`;
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
    insertPosition = body.split('INSERT_DIRECTION:')[1].split('---')[0].trim();
  } catch (error) {
    console.error('Error parsing body:', error);
    return `The error in parsing the BODY: ${error}. Either the INSERT_DIRECTION key is missing or not in the correct format. The correct format is INSERT_DIRECTION: {{above or below}} ---. Your response must conform strictly to INSERT_TEXT Response Template with all the keys present in the BODY`;
  }

  filePath = path.join(projectRootPath, filePath);

  console.log(`Inserting text into file: ${filePath} based on search text: '${searchText}' with replacement: '${textToInsert}' and insert position: '${insertPosition}'`);

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
      return `ERROR: The provided FIND_CODE: ${searchText} was not found in the file. Please make sure to provided FIND_CODE exists in the file without any special characters or newlines. The FIND_CODE is case-sensitive`;
    }

    const position = document.positionAt(index);
    const line = position.line;

    const checkPreviousSyntaxErrors = await checkForSyntaxErrors(document);

    let editApplied = await insertCode(document, editor, textToInsert, line, insertPosition);

    if (!editApplied) {
      console.error('Failed to apply the edit');
      return 'Failed to apply the edit';
    }

    let syntaxErrors = await checkForSyntaxErrors(document);
    console.log('checkForSyntaxErrors Syntax errors comparision', syntaxErrors.length, checkPreviousSyntaxErrors.length);
    if (checkPreviousSyntaxErrors.length < syntaxErrors.length) {
      await discardAndCloseEditor(document.uri);

      // Keeping the Retry with the opposite insertion position we might need later
      // const alternativeInsertPosition = insertPosition.toLowerCase() === 'above' ? 'below' : 'above';
      // console.log(`Retrying insertion with alternative position: ${alternativeInsertPosition}`);

      // const documentRetry = await vscode.workspace.openTextDocument(filePath);
      // const editorRetry = await vscode.window.showTextDocument(documentRetry);

      // editApplied = await insertCode(documentRetry, editorRetry, textToInsert, line, alternativeInsertPosition);

      // if (!editApplied) {
      //   console.error('Failed to apply the edit on retry');
      //   return 'Failed to apply the edit on retry';
      // }

      // syntaxErrors = await checkForSyntaxErrors(documentRetry);
      // console.log('Retry checkForSyntaxErrors Syntax errors comparision', syntaxErrors.length, checkPreviousSyntaxErrors.length);
      // if (checkPreviousSyntaxErrors.length < syntaxErrors.length) {
      //   await discardAndCloseEditor(documentRetry.uri);
      return 'After performing the specified code insertion, the file syntax was found to be incorrect. The code insertion was reverted. Please correct the keys specified in the body of the INSERT_TEXT action so that the code does not cause syntax errors. If you find insertion has failed more than two times, please QUESTION to SIRJI_USER for assistance by providing the necessary details.';
      // }
    }

    await document.save();
    await vscode.commands.executeCommand('workbench.action.closeActiveEditor');
    console.log('Text insertion completed in file:', filePath);
    return 'Done';
  } catch (error) {
    console.error(`Error processing file: ${error}`);
    return `Failed to process file: ${error}`;
  }
};
