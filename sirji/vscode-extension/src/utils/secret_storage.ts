import * as vscode from 'vscode';

class SecretStorage {
 private context: vscode.ExtensionContext | null = null;

 initialize(context: vscode.ExtensionContext) {
  this.context = context;
 }

 async storeSecret(key: string, value: string) {
  if (!this.context) throw new Error('SecretStorage not initialized');

  await this.context.secrets.store(key, value);
 }

 async retrieveSecret(key: string) {
  if (!this.context) throw new Error('SecretStorage not initialized');

  const secret = await this.context.secrets.get(key);
  return secret;
 }

 isApiKey(message: string) {
  //TODO: Implement a more robust check for API keys
  return message.toUpperCase().includes('API_KEY');
 }
}

export default new SecretStorage();
