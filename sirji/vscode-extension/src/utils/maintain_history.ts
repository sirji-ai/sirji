import * as fs from 'fs';
import * as path from 'path';

const HISTORY_FOLDER = '.sirji';

export class MaintainHistory {
 public createHistoryFolder(workspaceRootPath: any, problemId: string): void {
  const dirPath = path.join(workspaceRootPath, HISTORY_FOLDER, problemId);
  fs.mkdirSync(dirPath, { recursive: true });
 }

 public writeJsonFile(workspaceRootPath: any, filename: string, problemId: string, data: any): void {
  const jsonData = JSON.stringify(data, null, 4);

  const filePath = path.join(workspaceRootPath, HISTORY_FOLDER, problemId, `${filename}.json`);

  fs.writeFileSync(filePath, jsonData, 'utf-8');
 }

 public readJsonFile(filePath: string, problemId: string): any {
  const rawData = fs.readFileSync(filePath, 'utf-8');
  return JSON.parse(rawData);
 }
}
