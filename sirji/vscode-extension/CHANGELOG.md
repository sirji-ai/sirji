# ChangeLog

## 0.0.31

### Enhancements

- Added support for file absolute path in addition to already existing relative file support in executor actions.
- Added tolerance for file path coming in double quotes from LLM.
- `skills` in the agent YML converted to a single value instead of an array of objects.
- Added specific exceptions for various message related errors.
- Added ability to infer assistant in existing thread. INFER_IN_EXISTING_THREAD action added for the same.

## 0.0.30

### Enhancements

- Improved error handling for network issues.
- Default agents are now read from the `agents` folder within the `default` folder in the codebase if not present in the `agents` folder of Sirji Studio.
- Deprecated the keys `rules` and `definitions` from agent YAML.
- Introduced the code review agent.
- Implemented Factory Design Pattern for system prompt to have model provider specific details.
- Ability to nudge the agent programmatically to bring it on track in case it skips over some pseudo code steps.
- New messaging protocol action DO_NOTHING introduced to make intentional skipping of steps possible.

## 0.0.29

### Features

- Steps taken by the agents, along with their current status, are now shown in the right panel UI.
- Added an open-source test case agent.
- Added `deepseek` as a new model provider for agents.
- Added `anthropic` as a new model provider for agents.
- Added OpenAI Assistants API integration by allowing agents to create, sync, and infer from a RAG (Retrieval-Augmented Generation) assistant. Added `CREATE_ASSISTANT`, `INFER` and `SYNC_CODEBASE` actions in the messaging protocol for the same.

### Bug Fixes

- Fixed the issue of jumping to the last entry while reading logs.
- Constructed the path for opening the studio using the global storage API.
- File editing actions should give the needle text respecting the number of lines in the source code.
- Regenerate venv in case of version change during extension activation.

## 0.0.28

### Bug Fixes

- Fixed the issue with broken logs not being shown.
- Deprecated the steps UI.

## 0.0.27

### Enhancements

Combined two actions: "Store in Agent Output Folder" and "Register in Agent Output Index."
Updated agent terminology from INVOKE_AGENT to Invoke agent and from Scratch pad to Scratchpad.

# 0.0.25

### Features

- Added a new action for storing data in the scratch pad.

### Enhancements

- Made changes to the insert_text action to make it more reliable.

## 0.0.21

### Enhancements

- Added recipe selection before requirement gathering.
- Changed the side panel button label from "Start Sirji Studio" to "Open Sirji Studio".

### Bug Fixes

- Implemented sanitization of file paths for file creation.

## 0.0.19

### Features

- Introduced a left panel for Sirji, which includes features such as:
  - Opening Sirji Studio
  - Creating sessions

### Enhancements

- Moved existing agents to a pseudo-code style of writing instead of using sub-tasks
- Standardized the existing agents.

### Bug Fixes

- Fixed an issue where the orchestrator was being invoked before the user configured the environment. This issue affected new machines without the OpenAI key in VS Code secrets.

## 0.0.12

### Features

- Introduced the AI agentic framework version of Sirji.

### Enhancements

- Added validation to ensure file paths are created within the workspace folder.
- Filesystem CRUD operations for shared resources now use different actions.
- File paths relative to the shared resources folder are now used in these CRUD actions.
- The shared resource index file now also contains paths relative to the shared resources folder

### Bug Fixes

- Fixed issues with the FIND & REPLACE and INSERT TEXT actions.

## 0.0.7

### Enhancements

- Split the screen into two columns to separate the chat terminal and the logs panel([#80](https://github.com/sirji-ai/sirji/issues/80))
- Scroll to the bottom on switching Coder/Planner/Researcher tabs([#55](https://github.com/sirji-ai/sirji/issues/55))

## 0.0.6

### Enhancements

- Introduced the ability to spawn and execute commands ([#46](https://github.com/sirji-ai/sirji/pull/46))
- Introduced ability to read files and folders ([#27](https://github.com/sirji-ai/sirji/issues/27))
- Improved the language used in the output responses for commands that are still running.

## 0.0.5

### Enhancements

- Implemented an interactive loader within the chat terminal.([#38](https://github.com/sirji-ai/sirji/issues/38))
- Added placeholder log lines in the agent log tabs([#40](https://github.com/sirji-ai/sirji/issues/40))
- Updated readme file.

### Bug Fixes

- Fixed an issue where existing tasks did not terminate properly before starting a new task.

## 0.0.4

- First published version of the Sirji extension.
