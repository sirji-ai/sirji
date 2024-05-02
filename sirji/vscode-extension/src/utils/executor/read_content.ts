import * as path from 'path';
import * as fs from 'fs/promises';
import * as mimetype from 'mime-types';

const SKIP_LIST = ['__pycache__', '.git', '.github', '.gitlab', '.vscode', '.idea', 'node_modules', '.DS_Store', 'venv', '.venv', '.sass-cache', 'dist', 'out', 'build', 'logs', '.npm', 'temp', 'tmp'];

// Define media MIME types to skip
const MEDIA_MIME_TYPES = [
  'image',
  'video',
  'audio'
  // 'application/pdf', // PDF files
  // 'application/zip', // ZIP archives
  // 'application/x-tar', // TAR archives
  // 'application/x-gzip', // GZIP archives
  // 'application/x-rar-compressed', // RAR archives
  // 'application/vnd.ms-excel', // Excel files
  // 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', // Excel files (xlsx)
  // 'application/msword', // Word documents
  // 'application/vnd.openxmlformats-officedocument.wordprocessingml.document', // Word documents (docx)
  // 'application/vnd.ms-powerpoint', // PowerPoint presentations
  // 'application/vnd.openxmlformats-officedocument.presentationml.presentation', // PowerPoint presentations (pptx)
  // 'application/vnd.oasis.opendocument.text', // OpenDocument Text
  // 'application/vnd.oasis.opendocument.spreadsheet', // OpenDocument Spreadsheet
  // 'application/vnd.oasis.opendocument.presentation' // OpenDocument Presentation
];

function isPathInsideRoot(rootPath: string, targetPath: string): boolean {
  const resolvedRoot = path.resolve(rootPath);
  const resolvedTarget = path.resolve(targetPath);
  return resolvedTarget.startsWith(resolvedRoot);
}

export async function readContent(workspaceRootPath: string, body: string, isDirectory: boolean): Promise<string> {
  async function shouldSkip(name: string): Promise<boolean> {
    return SKIP_LIST.includes(name);
  }

  async function readFile(filePath: string): Promise<string> {
    try {
      const fileMimetype = mimetype.lookup(filePath);
      let content = null;
      const relativePath = path.relative(workspaceRootPath, filePath);

      const stats = await fs.stat(filePath);
      if (stats.size > 102400) {
        content = `Skipping file of size greater than 100 KB: ${filePath}`;
      } else if (fileMimetype && MEDIA_MIME_TYPES.some((type) => fileMimetype.startsWith(type))) {
        content = `Skipping file of media type: ${filePath}`;
      } else if (fileMimetype && fileMimetype.startsWith('application/octet-stream')) {
        content = `Skipping binary file: ${filePath}`;
      } else {
        content = await fs.readFile(filePath, 'utf8');
      }

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
        if (await shouldSkip(file.name)) {
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

  let result = '';
  let inputPaths = [];

  if (isDirectory) {
    const directoryPath = body.split('Directory:')[1].trim();
    inputPaths.push(directoryPath);
  } else {
    const filePaths = body.split('File paths:')[1];
    inputPaths = JSON.parse(filePaths);
  }

  console.log('-------inputPaths', inputPaths);

  for (const inputPath of inputPaths) {
    try {
      const fullPath = path.isAbsolute(inputPath) ? inputPath : path.join(workspaceRootPath, inputPath);

      if (!isPathInsideRoot(workspaceRootPath, fullPath)) {
        throw new Error(`Path '${inputPath}' is not within the workspace root.`);
      }

      console.log('-------fullPath', fullPath);
      const stats = await fs.stat(fullPath);

      if (stats.isDirectory()) {
        result += await readDirectory(fullPath);
      } else {
        result += await readFile(fullPath);
      }
    } catch (e) {
      const errorMessage = `Failed to read the path ${inputPath}. Error: ${e}`;
      console.error(errorMessage);
      result += errorMessage;
    }
  }
  return result;
}
