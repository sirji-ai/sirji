import * as vscode from 'vscode';
import * as fs from 'fs';
import path from 'path';

function delay(ms: number) {
  return new Promise((res) => setTimeout(res, ms));
}

async function checkForSyntaxErrors(document: vscode.TextDocument): Promise<string[]> {
  if (!document.fileName.endsWith('.js') && !document.fileName.endsWith('.json')) {
    return [];
  }

  await delay(4500);
  const diagnostics = vscode.languages.getDiagnostics(document.uri);
  const syntaxErrors: string[] = diagnostics.map((diag) => `${diag.message} at line ${diag.range.start.line}, column ${diag.range.start.character}`);
  return syntaxErrors;
}

function normalizeIndentation(text: string): string {
  const lines = text.split('\n');
  const normalizedLines = lines.map((line) => line.trim().replace(/\s/g, ''));
  return normalizedLines.join('\n');
}

async function discardAndCloseEditor(uri: vscode.Uri) {
  const originalDocument = await vscode.workspace.openTextDocument(uri);
  const emptyEdit = new vscode.WorkspaceEdit();
  emptyEdit.replace(uri, new vscode.Range(new vscode.Position(0, 0), new vscode.Position(Number.MAX_SAFE_INTEGER, Number.MAX_SAFE_INTEGER)), originalDocument.getText());
  await vscode.workspace.applyEdit(emptyEdit);
  await vscode.commands.executeCommand('workbench.action.revertAndCloseActiveEditor');
}
async function insertCode(document: vscode.TextDocument, editor: vscode.TextEditor, textToInsert: string, startLine: number, endLine: number, insertPosition: string): Promise<boolean> {
  return editor.edit((editBuilder) => {
    if (insertPosition.toLowerCase() === 'above') {
      editBuilder.insert(new vscode.Position(startLine, 0), textToInsert + '\n');
    } else if (insertPosition.toLowerCase() === 'below') {
      editBuilder.insert(new vscode.Position(endLine + 1, 0), textToInsert + '\n');
    }
  });
}

export const insertText = async (body: string, projectRootPath: string, insertPosition: string, globPattern?: string, exclude: string = '**/node_modules/**'): Promise<string> => {
  let searchText, textToInsert, filePath;

  if (insertPosition.toLowerCase() === 'below') {
    try {
      searchText = body.split('INSERT_BELOW:')[1].split('---')[0].trim();
    } catch (error) {
      console.error('Error parsing body:', error);
      return `The error in parsing the BODY: ${error}. Either the INSERT_BELOW key is missing from the BODY or it's not in the correct format. The correct format is INSERT_BELOW: {{Text to insert below without any special characters}} ---. Your response must conform strictly to the Response Template with all the keys present in the BODY.`;
    }
  } else {
    try {
      searchText = body.split('INSERT_ABOVE:')[1].split('---')[0].trim();
    } catch (error) {
      console.error('Error parsing body:', error);
      return `The error in parsing the BODY: ${error}. Either the INSERT_ABOVE key is missing from the BODY or it's not in the correct format. The correct format is INSERT_ABOVE: {{Text to insert above without any special characters}} ---. Your response must conform strictly to the Response Template with all the keys present in the BODY.`;
    }
  }

  console.log(`==================>======Searching for text: '${searchText}' in the file to insert the new text`);

  try {
    textToInsert = body.split('NEW_CHANGES:')[1].split('---')[0];
  } catch (error) {
    console.error('Error parsing body:', error);
    return `The error in parsing the BODY: ${error}. Either the NEW_CHANGES key is missing or not in the correct format. The correct format is NEW_CHANGES: {{New code to be inserted in the file}} ---. Your response must conform strictly to Response Template with all the keys present in the BODY`;
  }

  try {
    filePath = body.split('FILE_PATH:')[1].split('---')[0].trim();
  } catch (error) {
    console.error('Error parsing body:', error);
    return `The error in parsing the BODY: ${error}. Either the FILE_PATH key is missing or not in the correct format. The correct format is FILE_PATH: {{File path without any special characaters}} ---. Your response must conform strictly to Response Template with all the keys present in the BODY`;
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

    const normalizedSearchText = normalizeIndentation(searchText);

    const lines = text.split('\n');
    let startIndex = -1;
    let endIndex = -1;

    for (let i = 0; i < lines.length; i++) {
      const block = lines.slice(i, i + normalizedSearchText.split('\n').length).join('\n');
      
      if (normalizeIndentation(block).includes(normalizedSearchText)) {
        console.log('Block found:', block);
        startIndex = text.indexOf(block);
        endIndex = startIndex + block.length;
        break;
      }
    }

    console.log('startIndex:', startIndex);
    console.log('endIndex:', endIndex);

    if (startIndex === -1) {
      console.error('Search text not found in the document.');
      return `ERROR: The provided existing code '${searchText}' was not found in the file. Please ensure that the provided existing code is present in the file without any special characters or newlines. The existing code is case-sensitive and must match exactly as it appears in the file, including proper indentation. Try again with the correct existing code.`;
    }

    const startPosition = document.positionAt(startIndex);
    const endPosition = document.positionAt(endIndex);
    const startLine = startPosition.line;
    const endLine = endPosition.line;

    console.log('startLine:', startLine);
    console.log('endLine:', endLine);

    let editApplied = await insertCode(document, editor, textToInsert, startLine, endLine, insertPosition);

    if (!editApplied) {
      console.error('Failed to apply the edit');
      return 'Failed to apply the edit';
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
