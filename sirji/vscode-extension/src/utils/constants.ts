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
