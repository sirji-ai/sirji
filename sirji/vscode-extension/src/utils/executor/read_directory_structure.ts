import * as path from 'path';
import * as fs from 'fs/promises';
import { minimatch } from 'minimatch';

const SKIP_LIST = new Set<string>([
  '__pycache__', '.git', '.github', '.gitlab', '.vscode', '.idea', 
  'node_modules', '.DS_Store', 'venv', '.venv', '.sass-cache', 
  'dist', 'out', 'build', 'logs', '.npm', 'temp', 'tmp'
]);

let gitignorePatterns: string[] = [];

export async function readDirectoryStructure(workspaceRootPath: string, body: string): Promise<string> {
  const inputPath = body.split('Directory:')[1].trim();
  const fullPath = path.join(workspaceRootPath, inputPath);

  async function readGitignore(): Promise<void> {
    try {
      const gitignorePath = path.join(workspaceRootPath, '.gitignore');
      const data = await fs.readFile(gitignorePath, 'utf8');
      gitignorePatterns = data.split('\n')
                               .map(entry => entry.trim())
                               .filter(entry => entry && !entry.startsWith('#'));
    } catch (err: any) {
      if (err.code !== 'ENOENT') {
        console.warn(`Failed to read .gitignore:`, err);
        throw err;
      } else {
        console.log('No .gitignore file found.');
      }
    }
  }

  function shouldSkip(name: string, filePath: string, isDirectory: boolean): boolean {
    if (SKIP_LIST.has(name)) {
      return true;
    }

    const pathToCheck = path.relative(workspaceRootPath, filePath);

    for (const pattern of gitignorePatterns) {
      const isNegatedPattern = pattern.startsWith('!');
      const effectivePattern = isNegatedPattern ? pattern.slice(1) : pattern;

      if (minimatch(pathToCheck, effectivePattern, { dot: true })) {
        if (isNegatedPattern) {
          return false;
        }
        return true;
      }
    }

    return false;
  }

  async function readDirectory(directoryPath: string): Promise<string> {
    try {
      const files = await fs.readdir(directoryPath);
      const promises = files.map(async (file) => {
        const filePath = path.join(directoryPath, file);
        const stats = await fs.stat(filePath);
        if (stats.isDirectory()) {
          if (shouldSkip(file, filePath, true)) {
            return '';
          }
          return readDirectory(filePath);
        } else {
          if (shouldSkip(file, filePath, false)) {
            return '';
          }
          return path.relative(workspaceRootPath, filePath) + '\n';
        }
      });
      const contents = await Promise.all(promises);
      return contents.join('');
    } catch (err) {
      console.error(`Failed to read directory ${directoryPath}:`, err);
      throw err;
    }
  }

  await readGitignore();
  return readDirectory(fullPath);
}
