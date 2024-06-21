import fs from 'fs';
import path from 'path';
import { Session } from './session_manager';
import { LLM_MODEL_PRICING } from './constants';

export class TokenManager {
  private filePath: string;
  private conversationFolderPath: string;
  private aggregateTokenFilePath: string;
  private aggregateTokens: {
    [key: string]: { input_tokens: number; output_tokens: number; prompt_token_valuation_in_dollar: number; completion_token_valuation_in_dollar: number; llm_model: string };
  } = {};
  private finalAggregateTokens: {
    [key: string]: { input_tokens: number; output_tokens: number; prompt_token_valuation_in_dollar: number; completion_token_valuation_in_dollar: number; llm_model: string };
  } = {};

  constructor(filePath: string, conversationFolderPath: string, aggregateTokenFilePath: string) {
    this.filePath = filePath;
    this.conversationFolderPath = conversationFolderPath;
    this.aggregateTokenFilePath = aggregateTokenFilePath;
  }

  private readFile(orchestratorFilePath: string) {
    try {
      if (!fs.existsSync(orchestratorFilePath)) {
        return {};
      }
      const fileContents = fs.readFileSync(orchestratorFilePath, 'utf8');
      return JSON.parse(fileContents);
    } catch (error) {
      console.error('Error reading the orchestrator file:', error);
      return {};
    }
  }

  public generateAggregateTokenForOrchestrator() {
    const orchestratorFilePath = path.join(this.conversationFolderPath, 'ORCHESTRATOR.json');
    const orchestratorFileContent = this.readFile(orchestratorFilePath);
    if (!Object.keys(orchestratorFileContent).length) {
      return;
    }
    const { input_tokens, output_tokens, llm_model } = orchestratorFileContent;
    this.addTokensToAggregateTokens('ORCHESTRATOR', input_tokens, output_tokens, llm_model);
  }

  public async addTokensToAggregateTokens(key: string, input_tokens: number, output_tokens: number, llm_model: string) {
    if (!this.aggregateTokens[key]) {
      this.aggregateTokens[key] = {
        input_tokens: 0,
        output_tokens: 0,
        prompt_token_valuation_in_dollar: 0,
        completion_token_valuation_in_dollar: 0,
        llm_model: ''
      };
    }

    this.aggregateTokens[key].input_tokens = input_tokens;
    this.aggregateTokens[key].output_tokens = output_tokens;
    this.aggregateTokens[key].llm_model = llm_model;

    const llmModelPricing = LLM_MODEL_PRICING[llm_model];
    if (!llmModelPricing) {
      console.error('Error: llm_model not found in LLM_MODEL_PRICING:', llm_model);
      return;
    }
    this.aggregateTokens[key].prompt_token_valuation_in_dollar = (this.aggregateTokens[key].input_tokens * LLM_MODEL_PRICING[llm_model].PROMPT_TOKEN_PRICE_PER_MILLION_TOKENS) / 1000000.0;
    this.aggregateTokens[key].completion_token_valuation_in_dollar = (this.aggregateTokens[key].output_tokens * LLM_MODEL_PRICING[llm_model].COMPLETION_TOKEN_PRICE_PER_MILLION_TOKENS) / 1000000.0;

    console.log('TokenManager: aggregateTokens:', this.aggregateTokens);

    this.writeAggregateTokensFile(this.aggregateTokens);
  }

  public generateAggregateTokens(): void {
    const data = this.readSessionsFile();
    data.sessions.forEach((session: Session) => {
      const fileName = `${session.callStack}.${session.sessionId}.json`;
      const filePath = path.join(this.conversationFolderPath, fileName);

      if (fs.existsSync(filePath)) {
        const fileContents = fs.readFileSync(filePath, 'utf8');
        const parsedContent = JSON.parse(fileContents);
        const { input_tokens, output_tokens, llm_model } = parsedContent;


        if (typeof input_tokens !== 'number' || typeof output_tokens !== 'number') {
          console.error('Error: input_tokens and output_tokens should be numbers.', { input_tokens, output_tokens });
          return;
        }

        // const splittedCallStack = session.callStack.split('.');
        const key = session.callStack;

        this.addTokensToAggregateTokens(key, input_tokens, output_tokens, llm_model);
      }
    });

    console.log('TokenManager: aggregateTokens:', this.aggregateTokens);
  }

  private readSessionsFile(): { sessions: Session[] } {
    try {
      const fileContents = fs.readFileSync(this.filePath, 'utf8');
      return JSON.parse(fileContents) as { sessions: Session[] };
    } catch (error) {
      console.error('Error reading the sessions file:', error);
      return { sessions: [] };
    }
  }

  private writeAggregateTokensFile(data: {
    [key: string]: { input_tokens: number; output_tokens: number; prompt_token_valuation_in_dollar: number; completion_token_valuation_in_dollar: number; llm_model: string };
  }): void {
    try {
      this.finalAggregateTokens = {};
      Object.keys(data).forEach((key) => {
        const splittedKey = key.split('.');
        const newKey = splittedKey[0];
        if (!this.finalAggregateTokens[newKey]) {
          this.finalAggregateTokens[newKey] = {
            input_tokens: 0,
            output_tokens: 0,
            prompt_token_valuation_in_dollar: 0,
            completion_token_valuation_in_dollar: 0,
            llm_model: ''
          };
        }

        this.finalAggregateTokens[newKey].input_tokens += data[key].input_tokens;
        this.finalAggregateTokens[newKey].output_tokens += data[key].output_tokens;
        this.finalAggregateTokens[newKey].prompt_token_valuation_in_dollar += data[key].prompt_token_valuation_in_dollar;
        this.finalAggregateTokens[newKey].completion_token_valuation_in_dollar += data[key].completion_token_valuation_in_dollar;
        this.finalAggregateTokens[newKey].llm_model = data[key].llm_model;
      });

      fs.writeFileSync(this.aggregateTokenFilePath, JSON.stringify(this.finalAggregateTokens, null, 4), 'utf8');
    } catch (error) {
      console.error('Error writing the aggregate tokens file:', error);
    }
  }

  public async getTokenUsedInConversation() {
    try {
      if (!fs.existsSync(this.aggregateTokenFilePath)) {
        return {};
      }
      const fileContents = fs.readFileSync(this.aggregateTokenFilePath, 'utf8');
      return JSON.parse(fileContents);
    } catch (error) {
      console.error('Error reading the aggregate token file:', error);
      return {};
    }
  }

  public async getAggregateTokensUsedInConversation() {
    const aggregateTokens = await this.getTokenUsedInConversation();

    let input_tokens = 0;
    let output_tokens = 0;
    let total_prompt_tokens_value = 0;
    let completion_tokens_value = 0;

    Object.keys(aggregateTokens).forEach((key) => {
      input_tokens += aggregateTokens[key].input_tokens;
      output_tokens += aggregateTokens[key].output_tokens;
      total_prompt_tokens_value += aggregateTokens[key].prompt_token_valuation_in_dollar;
      completion_tokens_value += aggregateTokens[key].completion_token_valuation_in_dollar;
    });


    return {
      input_tokens: input_tokens,
      output_tokens: output_tokens,
      total_prompt_tokens_value: total_prompt_tokens_value,
      total_completion_tokens_value: completion_tokens_value
    };
  }
}
