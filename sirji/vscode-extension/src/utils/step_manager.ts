import * as fs from 'fs';
import path from 'path';

export class StepManager {
  private filePath: string;

  constructor(filePath: string) {
    this.filePath = filePath;
  }

  public createStepsFile(fileName: string, data: string): any {
    try {
      fileName = fileName + '.json';
      let dataSplit = data.split('Steps: ')[1];

      if (!dataSplit) {
        return 'Error: Data must start with "Steps: " followed by the steps array. Please send body of action in the correct format as mentioned below \n Steps: [{step_1: step_description }, {step_2: step_description} ]';
      }

      let steps;
      try {
        steps = JSON.parse(dataSplit);
      } catch (parseError) {
        return 'Error: Invalid JSON format. Please ensure the steps are in a valid JSON format: \n Steps: [{step_1: step_description }, {step_2: step_description} ]';
      }

      if (!Array.isArray(steps)) {
        return 'Error: Steps data must be an array. Please send body of action in the correct format as mentioned below \n Steps: [{step_1: step_description }, {step_2: step_description} ]';
      }
      if (steps.length === 0) {
        return 'Error: Steps array cannot be empty. Please provide at least one step: \n Steps: [{step_1: step_description }, {step_2: step_description} ]';
      }

      steps = steps.map((stepObj, index) => {
        if (typeof stepObj !== 'object') {
          return `Error: Step at index ${index} is not an object. Each step must be an object with a single key-value pair: \n Steps: [{step_1: step_description }, {step_2: step_description} ]`;
        }
        const keys = Object.keys(stepObj);
        if (keys.length !== 1) {
          return `Error: Step at index ${index} must have exactly one key. Found ${keys.length} keys: ${keys.join(
            ', '
          )}. Please use the format: \n Steps: [{step_1: step_description }, {step_2: step_description} ]`;
        }
        const stepKey = keys[0];
        return { [stepKey]: stepObj[stepKey], status: '' };
      });

      if (steps.some((step) => typeof step === 'string')) {
        return steps.find((step) => typeof step === 'string');
      }

      let formattedSteps: { [key: string]: any } = {};
      formattedSteps[fileName] = steps;

      let filePath = path.join(this.filePath, fileName);

      fs.writeFileSync(filePath, JSON.stringify(formattedSteps, null, 4), 'utf8');

      return 'Done';
    } catch (error) {
      console.error('Error writing the steps file:', error);
      return error || 'Error: An unexpected error occurred.';
    }
  }

  public readStepsFile(): any {
    try {
      let files = fs.readdirSync(this.filePath);

      let stepsMap = files.reduce((acc: { [x: string]: any }[], file) => {
        if (file.endsWith('.json')) {
          let data = fs.readFileSync(path.join(this.filePath, file), 'utf8');
          let parsedData = JSON.parse(data);

          if (parsedData && typeof parsedData === 'object') {
            acc.push({ [file]: parsedData[file] });
          }
        }
        return acc;
      }, []);

      return stepsMap;
    } catch (error) {
      console.error('Error reading the steps file:', error);
      return '';
    }
  }

  public updateStepStatus(fileName: string, stepNumber: number): object {
    try {
      const filePath = path.join(this.filePath, fileName + '.json');
      if (!fs.existsSync(filePath)) {
        return { isError: true, shouldDiscard: false, errorMessage: 'Error: File does not exist.' };
      }

      const fileData = fs.readFileSync(filePath, 'utf8');
      const parsedData = JSON.parse(fileData);

      if (!parsedData || !parsedData[fileName + '.json']) {
        return { isError: true, shouldDiscard: false, errorMessage: 'Error: Invalid file format.' };
      }

      const steps = parsedData[fileName + '.json'];

      if (stepNumber <= 0 || stepNumber > steps.length) {
        return { isError: true, shouldDiscard: false, errorMessage: 'Error: Invalid step number.' };
      }

      let lastCompletedStep = -1;
      for (let i = 0; i < steps.length; i++) {
        const stepObj = steps[i];
        const stepKey = Object.keys(stepObj)[0];
        if (stepObj.status === 'completed') {
          lastCompletedStep = i;
        }
      }

      if (lastCompletedStep !== -1 && stepNumber - lastCompletedStep >= 2) {
        return {
          isError: true,
          shouldDiscard: true,
          errorMessage: `Error: you have skipped the pseudocode step > ${lastCompletedStep} the last executed step was ${lastCompletedStep}. Please make sure you don't skip any step. I am discarding your last message`
        };
      }

      for (let i = 0; i < steps.length; i++) {
        const stepObj = steps[i];
        if (i < stepNumber - 1) {
          stepObj.status = 'completed';
        } else if (i === stepNumber - 1) {
          stepObj.status = 'in-progress';
        } else {
          stepObj.status = '';
        }
      }

      fs.writeFileSync(filePath, JSON.stringify(parsedData, null, 4), 'utf8');
      return { isError: false, shouldDiscard: false, errorMessage: 'Done' };
    } catch (error) {
      console.error('Error updating the steps file:', error);
      return { isError: true, shouldDiscard: false, errorMessage: `Error: An unexpected error occurred. ${error}` };
    }
  }

  public updateAllStepsToCompleted(fileName: string): any {
    try {
      const filePath = path.join(this.filePath, fileName + '.json');
      if (!fs.existsSync(filePath)) {
        return 'Error: File does not exist.';
      }

      const fileData = fs.readFileSync(filePath, 'utf8');
      const parsedData = JSON.parse(fileData);

      if (!parsedData || !parsedData[fileName + '.json']) {
        return 'Error: Invalid file format.';
      }

      const steps = parsedData[fileName + '.json'];

      for (let i = 0; i < steps.length; i++) {
        const stepObj = steps[i];
        stepObj.status = 'completed';
      }

      fs.writeFileSync(filePath, JSON.stringify(parsedData, null, 4), 'utf8');

      return 'Done';
    } catch (error) {
      return error || 'Error: An unexpected error occurred.';
    }
  }
}
