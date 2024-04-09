import * as fs from 'fs';
import * as path from 'path';
import { Constants } from './constants';

export class MaintainHistory {
  public createHistoryFolder(workspaceRootPath: any, sirjiRunId: string): void {
    const dirPath = path.join(workspaceRootPath, Constants.HISTORY_FOLDER, sirjiRunId);
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
