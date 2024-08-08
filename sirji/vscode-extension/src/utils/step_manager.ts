import * as fs from 'fs';
import path from 'path';


interface Step {
  status: string;
  [key: string]: any;
}

interface ValidationResponse {
  isError: boolean;
  shouldDiscard: boolean;
  errorMessage: string;
}

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

  // Method to validate the step number against the current in-progress step
  private validateStepNumber(stepNumber: number, steps: Step[]): ValidationResponse {
    // Find the index of the step that is currently in-progress
    console.log('Starting validation:', stepNumber, steps);
    let inProgressStepNumber = -1;
    for (let i = 0; i < steps.length; i++) {
      if (steps[i].status === 'in-progress') {
        inProgressStepNumber = i + 1;
        break;
      }
    }

    console.log('inProgressStepIndex:', inProgressStepNumber);
    console.log('stepNumber:', stepNumber);

    // Check if the new step number is skipping more than one step from the in-progress step
    if (inProgressStepNumber !== -1 && stepNumber - inProgressStepNumber > 1 ) {
      return {
        isError: true,
        shouldDiscard: true,
        errorMessage: `Error: You skipped some of the pseudo code steps. The highest executed step number as per my record is ${inProgressStepNumber}. Please make sure you do not skip any steps. I am discarding your last message. Resume with the correct step number.`
      };
    }

    // No validation errors, return successful response
    return {
      isError: false,
      shouldDiscard: false,
      errorMessage: ''
    };
  }

  // Method to update the status of the steps in the specified JSON file
  public updateStepStatus(fileName: string, stepNumber: number): ValidationResponse {
    const oThis = this;
    console.log('Updating step status:', fileName, stepNumber);

    const completeFileName = fileName + '.json';
    try {
      const filePath = path.join(oThis.filePath, completeFileName);
      
      // Check if the file exists
      if (!fs.existsSync(filePath)) {
        return { isError: true, shouldDiscard: false, errorMessage: 'Error: File does not exist.' };
      }

      // Read the file content and parse it as JSON
      const fileData = fs.readFileSync(filePath, 'utf8');
      const parsedData: { [key: string]: Step[] } = JSON.parse(fileData);

      // Validate the structure of the parsed data
      if (!parsedData || !parsedData[completeFileName]) {
        return { isError: true, shouldDiscard: false, errorMessage: 'Error: Invalid file format.' };
      }

      const steps = parsedData[completeFileName];

      // Validate the provided step number
      if (stepNumber <= 0 || stepNumber > steps.length) {
        return { isError: true, shouldDiscard: false, errorMessage: 'Error: Invalid step number.' };
      }

      // Validate the step number against the current in-progress step
      console.log('Validating step number:', stepNumber, steps);
      const validationResponse = oThis.validateStepNumber(stepNumber, steps);

      console.log('Validation response:', validationResponse);
      if (validationResponse.isError) {
        return validationResponse;
      }

      // Update the status of each step based on the provided step number
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

      // Write the updated steps back to the file
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
