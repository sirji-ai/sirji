import { createFile } from './create_file';
import { executeSpawn } from './execute_spawn';
import { executeTask } from './execute_task';
import { openBrowser } from './open_browser';
import { readContent } from './read_content';
import { appendToAgentOutputsIndex } from './append_to_agent_output_index';
import { readAgentOutputsIndex } from './read_agent_output_index';
import { fetchRecipe } from './fetch_recipe';

import { ACTION_ENUM } from '../constants';
import { searchFileInProject } from './search_file_in_project';
import { findAndReplaceInProjectFile } from './find_and_replace_in_project_file';
import { insertText } from './insert_text';
import { readDependencies } from './extract_file_dependencies';
import { searchCodeInProject } from './search_code_in_project';
import { fetchRecipeIndex } from './fetch_recipe_index';

export class Executor {
  private parsedMessage: any;
  private projectRootPath: any;
  private agentOutputFolderPath: any;
  private sirjiRunFolderPath: any;
  private sirjiInstallationFolderPath: any;

  public constructor(parsedMessage: any, projectRootPath: any, agentOutputFolderPath: any, sirjiRunFolderPath: any, sirjiInstallationFolderPath: any) {
    const oThis = this;

    oThis.parsedMessage = parsedMessage;
    oThis.projectRootPath = projectRootPath;
    oThis.agentOutputFolderPath = agentOutputFolderPath;
    oThis.sirjiRunFolderPath = sirjiRunFolderPath;
    oThis.sirjiInstallationFolderPath = sirjiInstallationFolderPath;
  }

  public async perform() {
    const oThis = this;

    let rawOutput = await oThis.handleAction(oThis.parsedMessage.ACTION);
    return oThis.formatMessage(rawOutput);
  }

  private async handleAction(action: string) {
    const oThis = this;

    switch (action) {
      case ACTION_ENUM.CREATE_PROJECT_FILE:
        return await createFile(oThis.projectRootPath, true, oThis.parsedMessage.BODY);
      case ACTION_ENUM.CREATE_AGENT_OUTPUT_FILE:
        return await createFile(oThis.agentOutputFolderPath, false, oThis.parsedMessage.BODY);
      case ACTION_ENUM.EXECUTE_COMMAND:
        return await executeSpawn(oThis.parsedMessage.BODY, oThis.projectRootPath);
      case ACTION_ENUM.RUN_SERVER:
        return await executeTask(oThis.parsedMessage.BODY, oThis.sirjiRunFolderPath);
      case ACTION_ENUM.OPEN_BROWSER:
        openBrowser(oThis.parsedMessage.URL);
        return 'Done';
      case ACTION_ENUM.READ_PROJECT_FILES:
        return await readContent(oThis.projectRootPath, oThis.parsedMessage.BODY, false);
      case ACTION_ENUM.READ_AGENT_OUTPUT_FILES:
        return await readContent(oThis.agentOutputFolderPath, oThis.parsedMessage.BODY, false);
      case ACTION_ENUM.APPEND_TO_AGENT_OUTPUT_INDEX:
        return await appendToAgentOutputsIndex(oThis.agentOutputFolderPath, oThis.parsedMessage.BODY, oThis.parsedMessage.FROM);
      case ACTION_ENUM.READ_AGENT_OUTPUT_INDEX:
        return await readAgentOutputsIndex(oThis.agentOutputFolderPath);
      case ACTION_ENUM.FETCH_RECIPE:
        return await fetchRecipe(oThis.sirjiInstallationFolderPath + '/studio/recipes', oThis.parsedMessage.BODY);
      case ACTION_ENUM.FETCH_RECIPE_INDEX:
        return await fetchRecipeIndex(oThis.sirjiInstallationFolderPath + '/studio/recipes');
      case ACTION_ENUM.SEARCH_FILE_IN_PROJECT:
        return await searchFileInProject(oThis.parsedMessage.BODY);
      case ACTION_ENUM.FIND_AND_REPLACE:
        return await findAndReplaceInProjectFile(oThis.parsedMessage.BODY, oThis.projectRootPath);
      case ACTION_ENUM.INSERT_ABOVE:
        return await insertText(oThis.parsedMessage.BODY, oThis.projectRootPath, 'above');
      case ACTION_ENUM.INSERT_BELOW:
        return await insertText(oThis.parsedMessage.BODY, oThis.projectRootPath, 'below');
      case ACTION_ENUM.EXTRACT_DEPENDENCIES:
        return await readDependencies(oThis.parsedMessage.BODY, oThis.projectRootPath);
      case ACTION_ENUM.SEARCH_CODE_IN_PROJECT:
        return await searchCodeInProject(oThis.parsedMessage.BODY, oThis.projectRootPath);
      default:
        return `Invalid message ACTION: ${action} sent to executor. Your response must conform strictly to one of the allowed Response Templates, as it will be processed programmatically and only these templates are recognized. Your response must be enclosed within '***' at the beginning and end, without any additional text above or below these markers. Not conforming above rules will lead to response processing errors.`;
    }
  }

  private formatMessage(rawOutput: any) {
    const oThis = this;

    const newParsedMessage = {
      FROM: oThis.parsedMessage.TO,
      TO: oThis.parsedMessage.FROM,
      ACTION: ACTION_ENUM.RESPONSE,
      SUMMARY: 'Empty',
      BODY: '\n' + rawOutput
    };

    const rawMessage = `***
FROM: ${newParsedMessage.FROM}
TO: ${newParsedMessage.TO}
ACTION: ${newParsedMessage.ACTION}
SUMMARY: ${newParsedMessage.SUMMARY}
BODY: \n${newParsedMessage.BODY}
***`;

    return { rawMessage, parsedMessage: newParsedMessage };
  }
}
