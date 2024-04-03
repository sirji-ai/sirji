import * as vscode from 'vscode';

export class SecretStorage {
 private context: vscode.ExtensionContext | undefined = undefined;

 public constructor(context: vscode.ExtensionContext | undefined) {
  this.context = context;
 }

 public async storeSecret(key: string, value: any): Promise<void> {
  if (!this.context) {
   throw new Error('SecretStorage not initialized');
  }

  await this.context.secrets.store(key, value);
 }

 public async removeSecret(key: string): Promise<void> {
  await this.context?.secrets.delete(key);
 }

 public async retrieveSecret(key: string): Promise<string | undefined> {
  if (!this.context) {
   throw new Error('SecretStorage not initialized');
  }

  const secret = await this.context.secrets.get(key);
  return secret;
 }
}
