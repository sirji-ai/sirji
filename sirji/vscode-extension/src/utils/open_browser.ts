import * as vscode from "vscode";

export function openBrowser(url: string) {
  console.log("openBrowser", url);
  vscode.commands.executeCommand("simpleBrowser.api.open", url);
}
