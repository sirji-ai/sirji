import path from 'path';

export const getFilePath = (filePath: string, projectRootPath: string): string => {
  if (path.isAbsolute(filePath)) {
    if (filePath.includes(projectRootPath)) {
      return filePath;
    } else {
      throw new Error('Error: File does not exist in the project root path');
    }
  } else {
    return path.join(projectRootPath, filePath);
  }
};
