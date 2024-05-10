import { createFile } from './create_file';
import { executeSpawn } from './execute_spawn';
import { executeTask } from './execute_task';
import { openBrowser } from './open_browser';
import { readContent } from './read_content';
import { readDirectoryStructure } from './read_directory_structure';
import { appendToSharedResourcesIndex } from './append_to_shared_resources_index';
import { readSharedResourcesIndex } from './read_shared_resource_index';

import { ACTION_ENUM } from '../constants';
import { searchFileInWorkspace } from './search_file_in_workspace';
import { findAndReplaceInWorkspace } from './find_and_replace_in_workspace';
import { findAndReplaceInWorkspaceFile } from './find_and_replace_in_workspace_file';
import { insertText } from './insert_text';

export class Executor {
  private parsedMessage: any;
  private workspaceRootPath: any;
  private sharedResourcesFolderPath: any;
  private sirjiRunFolderPath: any;

  public constructor(parsedMessage: any, workspaceRootPath: any, sharedResourcesFolderPath: any, sirjiRunFolderPath: any) {
    const oThis = this;

    oThis.parsedMessage = parsedMessage;
    oThis.workspaceRootPath = workspaceRootPath;
    oThis.sharedResourcesFolderPath = sharedResourcesFolderPath;
    oThis.sirjiRunFolderPath = sirjiRunFolderPath;
  }

  public async perform() {
    const oThis = this;

    let rawOutput = await oThis.handleAction(oThis.parsedMessage.ACTION);
    return oThis.formatMessage(rawOutput);
  }

  private async handleAction(action: string) {
    const oThis = this;

    switch (action) {
      case ACTION_ENUM.CREATE_WORKSPACE_FILE:
        return await createFile(oThis.workspaceRootPath, true, oThis.parsedMessage.BODY);
      case ACTION_ENUM.CREATE_SHARED_RESOURCE_FILE:
        return await createFile(oThis.sharedResourcesFolderPath, false, oThis.parsedMessage.BODY);
      case ACTION_ENUM.EXECUTE_COMMAND:
        return await executeSpawn(oThis.parsedMessage.BODY, oThis.workspaceRootPath);
      case ACTION_ENUM.RUN_SERVER:
        return await executeTask(oThis.parsedMessage.BODY, oThis.sirjiRunFolderPath);
      case ACTION_ENUM.OPEN_BROWSER:
        openBrowser(oThis.parsedMessage.URL);
        return 'Done';
      case ACTION_ENUM.READ_DIR:
        return await readContent(oThis.workspaceRootPath, oThis.parsedMessage.BODY, true);
      case ACTION_ENUM.READ_WORKSPACE_FILES:
        return await readContent(oThis.workspaceRootPath, oThis.parsedMessage.BODY, false);
      case ACTION_ENUM.READ_SHARED_RESOURCES_FILES:
        return await readContent(oThis.sharedResourcesFolderPath, oThis.parsedMessage.BODY, false);
      case ACTION_ENUM.READ_DIR_STRUCTURE:
        return await readDirectoryStructure(oThis.workspaceRootPath, oThis.parsedMessage.BODY);
      case ACTION_ENUM.APPEND_TO_SHARED_RESOURCES_INDEX:
        return await appendToSharedResourcesIndex(oThis.sharedResourcesFolderPath, oThis.parsedMessage.BODY, oThis.parsedMessage.FROM);
      case ACTION_ENUM.READ_SHARED_RESOURCE_INDEX:
        return await readSharedResourcesIndex(oThis.sharedResourcesFolderPath);
      case ACTION_ENUM.SEARCH_FILE_IN_WORKSPACE:
        return await searchFileInWorkspace(oThis.parsedMessage.BODY);
      case ACTION_ENUM.FIND_AND_REPLACE:
        return await findAndReplaceInWorkspaceFile(oThis.parsedMessage.BODY, oThis.workspaceRootPath);
      case ACTION_ENUM.INSERT_TEXT:
        return await insertText(oThis.parsedMessage.BODY, oThis.workspaceRootPath);
      default:
        throw `Invalid message ACTION: ${action} sent to executor.`;
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
