import * as fs from 'fs';
import path from 'path';

export class StepManager {
  private filePath: string;

  constructor(filePath: string) {
    this.filePath = filePath;
  }

  public createStepsFile(fileName: string, data: string): string {
    try {
      console.log('file path', this.filePath);
      console.log('Creating steps file:', fileName, 'data present for the file', data);

      fileName = '.json';
      let dataSplit = data.split('Steps: ');
      let steps = dataSplit[1].split(',');
      let stepsArray: string[] = [];

      steps.forEach((step) => {
        stepsArray.push(step);
      });

      data = JSON.stringify(stepsArray, null, 4);

      let filePath = path.join(this.filePath, fileName);

      console.log('complete file path', filePath, 'data', data);

      fs.writeFileSync(filePath, data, 'utf8');
      return 'Done';
    } catch (error) {
      return '';
      console.error('Error writing the steps file:', error);
    }
  }

  public readStepsFile(fileName: string): string {
    try {
      const fileContents = fs.readFileSync(this.filePath + fileName, 'utf8');
      return fileContents;
    } catch (error) {
      console.error('Error reading the steps file:', error);
      return '';
    }
  }
}
