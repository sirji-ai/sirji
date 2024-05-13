import fs from 'fs';
import path from 'path';
import * as parser from '@babel/parser';
import traverse from '@babel/traverse';
import { Node, Identifier, StringLiteral, BinaryExpression } from '@babel/types';

interface DependencyMap {
  [file: string]: string[];
}

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

const getFileWithExtension = (filePath: string, baseDir: string): string => {
  if (!filePath.startsWith('.')) {
    return filePath;
  }

  const absolutePath = safePathResolve(baseDir, filePath);
  const possibleExtensions = ['.js', '.ts'];

  let finalPath = absolutePath;

  for (let ext of possibleExtensions) {
    let testedPath = absolutePath + ext;
    if (fs.existsSync(testedPath)) {
      finalPath = testedPath;
      break;
    }
  }

  return path.relative(baseDir, finalPath);
};

const extractDependencies = async (filePath: string, baseDir: string): Promise<string[]> => {
  if (!fs.existsSync(filePath) || !filePath.endsWith('.js')) {
    console.log(`Skipping non-existent or non-JS/TS file: ${filePath}`);
    return [];
  }

  const code = await readCode(filePath);
  const ast = parser.parse(code, {
    sourceType: 'module',
    plugins: ['dynamicImport']
  });

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
          dependencies.add(getFileWithExtension(arg.value, baseDir));
        } else if (arg.type === 'BinaryExpression' && arg.operator === '+') {
          const resolvedPath = resolvePath(arg);
          if (resolvedPath) {
            dependencies.add(getFileWithExtension(resolvedPath, baseDir));
          }
        } else if (arg.type === 'TemplateLiteral') {
          const resolvedPath = resolvePath(arg);
          if (resolvedPath) {
            dependencies.add(getFileWithExtension(resolvedPath, baseDir));
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
