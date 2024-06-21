import path from 'path';

export const Constants = {
  ENV_VARS_KEY: 'sirjiSecrets',
  CODER_JSON_FILE: 'coder.json',
  PLANNER_JSON_FILE: 'planner.json',
  RESEARCHER_JSON_FILE: 'researcher.json',
  PYTHON_INPUT_FILE: 'input.txt',
  PROMPT_TOKEN_PRICE_PER_MILLION_TOKENS: 10,
  COMPLETION_TOKEN_PRICE_PER_MILLION_TOKENS: 30,
  SESSIONS: 'sessions'
};

interface LlmModelPricing {
  [key: string]: {
    PROMPT_TOKEN_PRICE_PER_MILLION_TOKENS: number;
    COMPLETION_TOKEN_PRICE_PER_MILLION_TOKENS: number;
  };
}

export const LLM_MODEL_PRICING: LlmModelPricing = {
  'gpt-3.5-turbo': {
    PROMPT_TOKEN_PRICE_PER_MILLION_TOKENS: 0.5,
    COMPLETION_TOKEN_PRICE_PER_MILLION_TOKENS: 1.5
  },
  'gpt-4o': {
    PROMPT_TOKEN_PRICE_PER_MILLION_TOKENS: 5,
    COMPLETION_TOKEN_PRICE_PER_MILLION_TOKENS: 15
  },
  'deepseek-coder': {
    PROMPT_TOKEN_PRICE_PER_MILLION_TOKENS: 0.14,
    COMPLETION_TOKEN_PRICE_PER_MILLION_TOKENS: 0.28
  },
  'claude-3-5-sonnet-20240620': {
    PROMPT_TOKEN_PRICE_PER_MILLION_TOKENS: 3,
    COMPLETION_TOKEN_PRICE_PER_MILLION_TOKENS: 15
  }
};

export const ACTION_ENUM = {
  //user and coder conversations
  PROBLEM_STATEMENT: 'PROBLEM_STATEMENT',
  QUESTION: 'QUESTION',
  ANSWER: 'ANSWER',
  INFORM: 'INFORM',
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
  RUN_SERVER: 'RUN_SERVER',
  CREATE_PROJECT_FILE: 'CREATE_PROJECT_FILE',
  READ_PROJECT_FILES: 'READ_PROJECT_FILES',
  OUTPUT: 'OUTPUT',
  OPEN_BROWSER: 'OPEN_BROWSER',
  READ_AGENT_OUTPUT_FILES: 'READ_AGENT_OUTPUT_FILES',
  STORE_IN_AGENT_OUTPUT: 'STORE_IN_AGENT_OUTPUT',
  READ_AGENT_OUTPUT_INDEX: 'READ_AGENT_OUTPUT_INDEX',
  FETCH_RECIPE: 'FETCH_RECIPE',
  FETCH_RECIPE_INDEX: 'FETCH_RECIPE_INDEX',
  SEARCH_FILE_IN_PROJECT: 'SEARCH_FILE_IN_PROJECT',
  FIND_AND_REPLACE: 'FIND_AND_REPLACE',
  INSERT_ABOVE: 'INSERT_ABOVE',
  INSERT_BELOW: 'INSERT_BELOW',
  EXTRACT_DEPENDENCIES: 'EXTRACT_DEPENDENCIES',
  SEARCH_CODE_IN_PROJECT: 'SEARCH_CODE_IN_PROJECT',
  STORE_IN_SCRATCH_PAD: 'STORE_IN_SCRATCH_PAD'
};

export const ACTOR_ENUM = {
  USER: 'SIRJI_USER',
  CODER: 'CODER',
  PLANNER: 'PLANNER',
  RESEARCHER: 'RESEARCHER',
  EXECUTOR: 'EXECUTOR',
  ORCHESTRATOR: 'ORCHESTRATOR',
  SHORTLISTER: 'SHORTLISTER'
};
