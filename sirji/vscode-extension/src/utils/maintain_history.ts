import * as fs from 'fs';
import * as path from 'path';
import { Constants } from './constants';

export class MaintainHistory {
  public createHistoryFolder(projectRootPath: any, sirjiRunId: string): void {
    const dirPath = path.join(projectRootPath, sirjiRunId);
    fs.mkdirSync(dirPath, { recursive: true });
  }

  public writeFile(filePath: any, data: any): void {
    fs.writeFileSync(filePath, data, 'utf-8');
  }

  public readFile(filePath: any): any {
    const rawData = fs.readFileSync(filePath, 'utf-8');
    return rawData;
  }

  public checkIfFileExists(filePath: any): boolean {
    return fs.existsSync(filePath);
  }
}
