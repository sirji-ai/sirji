import * as path from 'path';
import * as fs from 'fs/promises';

const SKIP_LIST = new Set<string>([
  '__pycache__', '.git', '.github', '.gitlab', '.vscode', '.idea', 
  'node_modules', '.DS_Store', 'venv', '.venv', '.sass-cache', 
  'dist', 'out', 'build', 'logs', '.npm', 'temp', 'tmp'
]);

export async function readDirectoryStructure(projectRootPath: string, body: string): Promise<string> {
  const inputPath = body.split('Directory:')[1].trim();
  const fullPath = path.join(projectRootPath, inputPath);

  async function readGitignore(): Promise<void> {
    try {
      const gitignorePath = path.join(projectRootPath, '.gitignore');
      const data = await fs.readFile(gitignorePath, 'utf8');
      const gitignoreEntries = data.split('\n')
                                   .map(entry => entry.trim())
                                   .filter(entry => entry && !entry.startsWith('#'));
      gitignoreEntries.forEach(entry => SKIP_LIST.add(entry));
    } catch (err: any) {
      if (err.code !== 'ENOENT') {
        console.warn(`Failed to read .gitignore:`, err);
        throw err;
      }
    }
  }

  function shouldSkip(name: string): boolean {
    return SKIP_LIST.has(name);
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
          return path.relative(projectRootPath, filePath) + '\n';
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