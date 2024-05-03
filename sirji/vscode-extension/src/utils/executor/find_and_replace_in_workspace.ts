import * as vscode from 'vscode';
import * as fs from 'fs';

export const findAndReplaceInWorkspace = async (searchText: string, replacement: string, folderPath?: string, globPattern?: string, exclude: string = '**/node_modules/**') => {
  const basePath = folderPath ? `${folderPath}/` : '**/';
  const namePattern = '**/*.*';
  const pattern = `${basePath}${namePattern}`;

  console.log(`Searching for files with pattern: ${pattern} and excluding: ${exclude} in folder: ${folderPath}`);
  try {
    const files = await vscode.workspace.findFiles(pattern, exclude);
    const foundFiles: vscode.Uri[] = [];

    for (const file of files) {
      console.log(`Found file: ${file.fsPath}`);
      const content = fs.readFileSync(file.fsPath, 'utf-8');
      if (content.includes(searchText)) {
        foundFiles.push(file);
      }
    }

    console.log(`Found ${files.length} files with pattern: ${pattern}`);

    for (const file of foundFiles) {
      console.log(`Replacing in file: ${file.fsPath}`);
      const document = await vscode.workspace.openTextDocument(file);
      const editor = await vscode.window.showTextDocument(document);

      const allText = new vscode.Range(document.positionAt(0), document.positionAt(document.getText().length));

      await editor.edit((editBuilder) => {
        let text = document.getText(allText);
        const regex = new RegExp(searchText, 'g');
        text = text.replace(regex, replacement);
        editBuilder.replace(allText, text);
      });
      await document.save();
      //close the file
      await vscode.commands.executeCommand('workbench.action.closeActiveEditor');
    }
  } catch (error) {
    console.error(`Error replacing text in files: ${error}`);
    vscode.window.showErrorMessage(`Error replacing text in files: ${error}`);
  }
};
