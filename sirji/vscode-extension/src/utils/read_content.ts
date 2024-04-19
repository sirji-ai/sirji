import * as vscode from 'vscode';
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

export async function readContent(workspaceRootPath: string, inputPath: string): Promise<string> {
  let fullPath = path.join(workspaceRootPath, inputPath);

  function shouldSkip(name: string): boolean {
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

readContent('/Users/vaibhavdighe/workspace/sirji', 'test').then(console.log).catch(console.error);
