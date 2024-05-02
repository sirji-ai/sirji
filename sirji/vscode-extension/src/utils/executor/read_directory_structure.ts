import * as path from 'path';
import * as fs from 'fs/promises';

const SKIP_LIST = ['__pycache__', '.git', '.github', '.gitlab', '.vscode', '.idea', 'node_modules', '.DS_Store', 'venv', '.venv', '.sass-cache', 'dist', 'out', 'build', 'logs', '.npm', 'temp', 'tmp'];

export async function readDirectoryStructure(workspaceRootPath: string, body: string): Promise<string> {
  const inputPath = body.split('Directory:')[1].trim();

  let fullPath = path.join(workspaceRootPath, inputPath);

  function shouldSkip(name: string): boolean {
    return SKIP_LIST.includes(name);
  }

  async function readDirectory(directoryPath: string): Promise<string> {
    try {
      const files = await fs.readdir(directoryPath);
      const promises = files.map(async (file) => {
        const filePath = path.join(directoryPath, file);
        const stats = await fs.stat(filePath);
        if (stats.isDirectory()) {
          if (shouldSkip(file)) {
            return '';
          }
          return readDirectory(filePath);
        } else {
          return filePath + '\n';
        }
      });
      const contents = await Promise.all(promises);
      return contents.join('');
    } catch (err) {
      console.error(`Failed to read directory ${directoryPath}:`, err);
      throw err;
    }
  }

  return readDirectory(fullPath);
}

readDirectoryStructure('/Users/vaibhavdighe/workspace/sirji/tools', 'Directory: /').then(console.log);
