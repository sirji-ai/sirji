import * as vscode from 'vscode';
import * as fs from 'fs';

export const findAndReplaceInWorkspace = async (body: string, globPattern?: string, exclude: string = '**/node_modules/**'): Promise<string> => {
  const searchText = body.split('Find:')[1].split('---')[0].trim();
  const replacement = body.split('Replace:')[1].split('---')[0].trim();
  const folderPath = body.split('Directory:')[1].trim();

  console.log(`Searching for files with pattern: ${searchText} in folder: ${folderPath} and replacing with: ${replacement}`);

  const basePath = folderPath ? `${folderPath}/` : '**/';
  const namePattern = '**/*.*';
  const pattern = `${basePath}${namePattern}`;

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

    console.log(`Found ${files.length} files with pattern: ${pattern}` + ` and ${foundFiles.length} files with search text: ${searchText}`);

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

    return 'Done';
  } catch (error) {
    console.error(`Error replacing text in files: ${error}`);
    return 'Error while replacing text in files. error: ' + error;
  }
};
