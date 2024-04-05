import path from 'path';

export const Constants = {
  ENV_VARS_KEY: 'sirjiSecrets',
  HISTORY_FOLDER: '.sirji',
  PYHTON_VENV_FOLDER: getPythonVenvPath(),
  CODER_JSON_FILE: 'coder.json',
  PLANNER_JSON_FILE: 'planner.json',
  RESEARCHER_JSON_FILE: 'researcher.json',
  PYTHON_INPUT_FILE: 'input.txt'
};

function getPythonVenvPath(): string {
  return path.join('.sirji', 'venv');
}

export const ACTION_ENUM = {
  //user and coder conversations
  PROBLEM_STATEMENT: 'PROBLEM_STATEMENT',
  QUESTION: 'QUESTION',
  ANSWER: 'ANSWER',
  INFORM: 'INFORM',
  STEP_STARTED: 'STEP_STARTED',
  STEP_COMPLETED: 'STEP_COMPLETED',
  ACKNOWLEDGE: 'ACKNOWLEDGE',
  SOLUTION_COMPLETE: 'SOLUTION_COMPLETE',
  FEEDBACK: 'FEEDBACK',

  // coder and planner conversations
  GENERATE_STEPS: 'GENERATE_STEPS',
  STEPS: 'STEPS',

  //coder and researcher conversations
  TRAIN_USING_URL: 'TRAIN_USING_URL',
  TRAIN_USING_SEARCH_TERM: 'TRAIN_USING_SEARCH_TERM',
  TRAINING_OUTPUT: 'TRAINING_OUTPUT',
  INFER: 'INFER',
  RESPONSE: 'RESPONSE',

  //coder and executor conversations
  EXECUTE_COMMAND: 'EXECUTE_COMMAND',
  CREATE_FILE: 'CREATE_FILE',
  READ_FILE: 'READ_FILE',
  READ_DIR: 'READ_DIR',
  INSTALL_PACKAGE: 'INSTALL_PACKAGE',
  OUTPUT: 'OUTPUT',
  OPEN_BROWSER: 'OPEN_BROWSER'
};

export const ACTOR_ENUM = {
  USER: 'USER',
  CODER: 'CODER',
  PLANNER: 'PLANNER',
  RESEARCHER: 'RESEARCHER',
  EXECUTOR: 'EXECUTOR'
};
