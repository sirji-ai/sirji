import fs from 'fs';
import path from 'path';
import { Session } from './session_manager';
import { LLM_MODEL_PRICING } from './constants';

export class TokenManager {
  private filePath: string;
  private conversationFolderPath: string;
  private aggregateTokenFilePath: string;
  private aggregateTokens: {
    [key: string]: { prompt_tokens: number; completion_tokens: number; prompt_token_valuation_in_dollar: number; completion_token_valuation_in_dollar: number; llm_model: string };
  } = {};
  private finalAggregateTokens: {
    [key: string]: { prompt_tokens: number; completion_tokens: number; prompt_token_valuation_in_dollar: number; completion_token_valuation_in_dollar: number; llm_model: string };
  } = {};

  constructor(filePath: string, conversationFolderPath: string, aggregateTokenFilePath: string) {
    this.filePath = filePath;
    this.conversationFolderPath = conversationFolderPath;
    this.aggregateTokenFilePath = aggregateTokenFilePath;

    console.log('TokenManager: filePath:', this.filePath);
    console.log('TokenManager: conversationFolderPath:', this.conversationFolderPath);
    console.log('TokenManager: aggregateTokenFilePath:', this.aggregateTokenFilePath);
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
    const { prompt_tokens, completion_tokens, llm_model } = orchestratorFileContent;
    this.addTokensToAggregateTokens('ORCHESTRATOR', prompt_tokens, completion_tokens, llm_model);
  }

  public async addTokensToAggregateTokens(key: string, prompt_tokens: number, completion_tokens: number, llm_model: string) {
    console.log('TokenManager: addTokensToAggregateTokens:', { key, prompt_tokens, completion_tokens, llm_model });

    if (!this.aggregateTokens[key]) {
      this.aggregateTokens[key] = {
        prompt_tokens: 0,
        completion_tokens: 0,
        prompt_token_valuation_in_dollar: 0,
        completion_token_valuation_in_dollar: 0,
        llm_model: ''
      };
    }

    this.aggregateTokens[key].prompt_tokens = prompt_tokens;
    this.aggregateTokens[key].completion_tokens = completion_tokens;
    this.aggregateTokens[key].llm_model = llm_model;

    const llmModelPricing = LLM_MODEL_PRICING[llm_model];
    if (!llmModelPricing) {
      console.error('Error: llm_model not found in LLM_MODEL_PRICING:', llm_model);
      return;
    }
    this.aggregateTokens[key].prompt_token_valuation_in_dollar = (this.aggregateTokens[key].prompt_tokens * LLM_MODEL_PRICING[llm_model].PROMPT_TOKEN_PRICE_PER_MILLION_TOKENS) / 1000000.0;
    this.aggregateTokens[key].completion_token_valuation_in_dollar = (this.aggregateTokens[key].completion_tokens * LLM_MODEL_PRICING[llm_model].COMPLETION_TOKEN_PRICE_PER_MILLION_TOKENS) / 1000000.0;

    console.log('TokenManager: aggregateTokens:', this.aggregateTokens);

    this.writeAggregateTokensFile(this.aggregateTokens);
  }

  public generateAggregateTokens(): void {
    const data = this.readSessionsFile();
    data.sessions.forEach((session: Session) => {
      console.log('TokenManager: session:', session);
      const fileName = `${session.callStack}.${session.sessionId}.json`;
      const filePath = path.join(this.conversationFolderPath, fileName);
      console.log('TokenManager: filePath:', filePath);

      if (fs.existsSync(filePath)) {
        const fileContents = fs.readFileSync(filePath, 'utf8');
        const parsedContent = JSON.parse(fileContents);
        const { prompt_tokens, completion_tokens, llm_model } = parsedContent;

        if (typeof prompt_tokens !== 'number' || typeof completion_tokens !== 'number') {
          console.error('Error: prompt_tokens and completion_tokens should be numbers.', { prompt_tokens, completion_tokens });
          return;
        }

        console.log('TokenManager: prompt_tokens:', prompt_tokens);
        console.log('TokenManager: completion_tokens:', completion_tokens);

        // const splittedCallStack = session.callStack.split('.');
        const key = session.callStack;

        this.addTokensToAggregateTokens(key, prompt_tokens, completion_tokens, llm_model);
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
    [key: string]: { prompt_tokens: number; completion_tokens: number; prompt_token_valuation_in_dollar: number; completion_token_valuation_in_dollar: number; llm_model: string };
  }): void {
    try {
      this.finalAggregateTokens = {};
      Object.keys(data).forEach((key) => {
        const splittedKey = key.split('.');
        const newKey = splittedKey[0];
        if (!this.finalAggregateTokens[newKey]) {
          this.finalAggregateTokens[newKey] = {
            prompt_tokens: 0,
            completion_tokens: 0,
            prompt_token_valuation_in_dollar: 0,
            completion_token_valuation_in_dollar: 0,
            llm_model: ''
          };
        }

        this.finalAggregateTokens[newKey].prompt_tokens += data[key].prompt_tokens;
        this.finalAggregateTokens[newKey].completion_tokens += data[key].completion_tokens;
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

    let prompt_tokens = 0;
    let completion_tokens = 0;
    let total_prompt_tokens_value = 0;
    let completion_tokens_value = 0;

    Object.keys(aggregateTokens).forEach((key) => {
      prompt_tokens += aggregateTokens[key].prompt_tokens;
      completion_tokens += aggregateTokens[key].completion_tokens;
      total_prompt_tokens_value += aggregateTokens[key].prompt_token_valuation_in_dollar;
      completion_tokens_value += aggregateTokens[key].completion_token_valuation_in_dollar;
    });

    return {
      total_prompt_tokens: prompt_tokens,
      total_completion_tokens: completion_tokens,
      total_prompt_tokens_value: total_prompt_tokens_value,
      total_completion_tokens_value: completion_tokens_value
    };
  }
}
