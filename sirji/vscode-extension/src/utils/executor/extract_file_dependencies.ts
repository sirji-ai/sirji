import fs from 'fs';
import path from 'path';
import glob from 'glob-promise';
import * as parser from '@babel/parser';
import traverse from '@babel/traverse';
import { Node, Identifier, StringLiteral, BinaryExpression } from '@babel/types';

const variableValues = new Map<string, string>();

const readCode = async (filePath: string): Promise<string> => {
  return fs.promises.readFile(filePath, 'utf8');
};

const resolvePath = (node: Node): string | null => {
  if (node.type === 'BinaryExpression' && node.operator === '+') {
    const left = resolvePath(node.left as any);
    const right = resolvePath(node.right as any);
    return left && right ? path.join(left, right) : null;
  } else if (node.type === 'StringLiteral') {
    return node.value;
  } else if (node.type === 'Identifier') {
    return variableValues.get(node.name) || null;
  } else if (node.type === 'TemplateLiteral') {
    let resolvedPath = '';
    for (const part of node.quasis) {
      resolvedPath += part.value.raw;
    }
    if (resolvedPath.startsWith('/')) {
      resolvedPath = resolvedPath.slice(1);
    }
    return resolvedPath;
  }
  return null;
};

const safePathResolve = (baseDir: string, relativePath: string): string => {
  const normalizedBaseDir = path.normalize(baseDir + '/');

  let resolvedPath = normalizedBaseDir;
  const pathParts = relativePath.split('/');

  for (const part of pathParts) {
    if (part === '..') {
      let parentDir = path.dirname(resolvedPath);
      if (parentDir.startsWith(normalizedBaseDir)) {
        resolvedPath = parentDir;
      }
    } else if (part !== '.') {
      resolvedPath = path.join(resolvedPath, part);
    }
  }

  return resolvedPath;
};

const getAllFilePaths = async (dir: string): Promise<string[]> => {
  try {
    const pattern = '**/*'; // Default pattern to match all files
    const fullPathPattern = path.join(dir, pattern);
    const files = await glob(fullPathPattern, { ignore: ['**/node_modules/**'] });
    return files;
  } catch (err: any) {
    throw new Error(`Error fetching files: ${err.message}`);
  }
};

const getFileWithExtension = (filePath: string, baseDir: string, allFilePaths: string[]): string => {
  const absolutePath = safePathResolve(baseDir, filePath); 
  
  let maxMatchLength = 0;
  let bestMatch = '';

  allFilePaths.forEach(currentPath => {
    const currentAbsolutePath = path.resolve(baseDir, currentPath);
    if (currentAbsolutePath.includes(absolutePath) && absolutePath.length > maxMatchLength) {
      maxMatchLength = absolutePath.length;
      bestMatch = currentAbsolutePath;
    }
  });

  if (bestMatch) {
    return path.relative(baseDir, bestMatch);
  }

  return '';
};

const extractDependencies = async (filePath: string, baseDir: string): Promise<string[]> => {
  const code = await readCode(filePath);
  const ast = parser.parse(code, {
    sourceType: 'module',
    plugins: ['dynamicImport']
  });

  const allFilePaths = await getAllFilePaths(baseDir);

  let dependencies = new Set<string>();

  traverse(ast, {
    VariableDeclarator(path) {
      const { node } = path;
      if (node.id.type === 'Identifier' && node.init && node.init.type === 'StringLiteral') {
        variableValues.set(node.id.name, node.init.value);
      }
    },
    CallExpression({ node }) {
      if (node.callee.type === 'Identifier' && node.callee.name === 'require' && node.arguments.length === 1 && node.arguments[0].type !== 'SpreadElement') {
        const arg = node.arguments[0];
        if (arg.type === 'StringLiteral') {
          const fileWithExtension = getFileWithExtension(arg.value, baseDir, allFilePaths);
          if (fileWithExtension) {
            dependencies.add(fileWithExtension);
          }
        } else if (arg.type === 'BinaryExpression' && arg.operator === '+') {
          const resolvedPath = resolvePath(arg);
          if (resolvedPath) {
            const fileWithExtension = getFileWithExtension(resolvedPath, baseDir, allFilePaths);
            if (fileWithExtension) {
              dependencies.add(fileWithExtension);
            }
          }
        } else if (arg.type === 'TemplateLiteral') {
          const resolvedPath = resolvePath(arg);
          if (resolvedPath) {
            const fileWithExtension = getFileWithExtension(resolvedPath, baseDir, allFilePaths);
            if (fileWithExtension) {
              dependencies.add(fileWithExtension);
            }
          }
        }
      }
    }
  });

  return Array.from(dependencies);
};

export const readDependencies = async (body: string, workspaceRootPath: string): Promise<string[]> => {
  const filePaths = body
    .split('[')[1]
    .split(']')[0]
    .split(',')
    .map((filePath) => filePath.trim().slice(1, -1));

  const allDependencies = new Set<string>();

  for (const filePath of filePaths) {
    try {
      const fullPath = path.resolve(workspaceRootPath, filePath);
      const dependencies = await extractDependencies(fullPath, workspaceRootPath);
      dependencies.forEach((dep) => allDependencies.add(dep));
    } catch (error) {
      console.log(`Error processing ${filePath}: ${error}`);
    }
  }

  return Array.from(allDependencies);
};
