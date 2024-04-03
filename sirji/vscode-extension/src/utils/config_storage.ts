import * as vscode from 'vscode';

class SecretStorage {
 private context: vscode.ExtensionContext | null = null;

  public constructor(context: vscode.ExtensionContext) {
    this.context = context;
  }

  public async storeSecret(key: string, value: string): Promise<void> {
    if (!this.context) { throw new Error('SecretStorage not initialized'); }
  
    await this.context.secrets.store(key, value);
  }

  public async retrieveSecret(key: string): Promise<string | undefined> {
    if (!this.context) { throw new Error('SecretStorage not initialized'); }

    const secret = await this.context.secrets.get(key);
    return secret;
  }
  public isApiKey(message: string): boolean {
    // TODO: Implement a more robust check for API keys
    return message.toUpperCase().includes('API_KEY');
  }
}

export function configStorage(context: vscode.ExtensionContext) {
  return new SecretStorage(context);
}
