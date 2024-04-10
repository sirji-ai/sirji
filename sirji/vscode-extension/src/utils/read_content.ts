import * as vscode from 'vscode';
import * as path from 'path';
import * as fs from 'fs/promises';

const SKIP_LIST = ['__pycache__', '.git', '.github', '.gitlab', '.vscode', '.idea', 'node_modules', '.DS_Store', 'venv', '.venv', '.sass-cache', 'dist', 'out', 'build', 'logs', '.npm', 'temp', 'tmp'];

export async function readContent(workspaceRootPath: string, inputPath: string): Promise<string> {
  let fullPath = path.join(workspaceRootPath, inputPath);

  function shouldSkip(name: string): boolean {
    return SKIP_LIST.includes(name);
  }

  async function readFile(filePath: string): Promise<string> {
    try {
      const content = await fs.readFile(filePath, 'utf8');
      const relativePath = path.relative(workspaceRootPath, filePath);
      return `File: ${relativePath}\n\n${content}\n\n---\n\n`;
    } catch (err) {
      console.error(`Failed to read file ${filePath}:`, err);
      throw err;
    }
  }

  async function readDirectory(directoryPath: string): Promise<string> {
    try {
      let files = await fs.readdir(directoryPath, { withFileTypes: true });
      let results = [];

      for (const file of files) {
        // Skip logic implementation
        if (shouldSkip(file.name)) {
          continue; // Skips current iteration if name matches any in SKIP_LIST
        }

        const currentPath = path.join(directoryPath, file.name);
        if (file.isDirectory()) {
          results.push(await readDirectory(currentPath));
        } else {
          results.push(await readFile(currentPath));
        }
      }

      return results.join('');
    } catch (err) {
      console.error(`Failed to read directory ${directoryPath}:`, err);
      throw err;
    }
  }

  try {
    const stats = await fs.stat(fullPath);

    if (stats.isDirectory()) {
      return readDirectory(fullPath);
    } else {
      return readFile(fullPath);
    }
  } catch (e) {
    const errorMessage = `Failed to read the path. Error: ${e}`;
    return errorMessage;
  }
}
