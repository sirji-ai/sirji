# How to Write Agent Pseudocode

## Introduction

An agent in the Sirji framework is a modular AI component designed to perform specific tasks based on custom pseudocode.

Think of the custom agent as a new team member. You need to provide it with your understanding of the existing architecture, design patterns, and code conventions used in the repository where you plan to use the custom agent to solve a problem. This understanding is conveyed through the agent's pseudocode.

This guide will explain the terminology involved, provide example pseudocode snippets with their corresponding messages generated according to the [messaging protocol](./Messaging%20Protocol.md), and outline best practices for writing pseudocode.

[Here](../sirji/vscode-extension/src/defaults/agents/NODE_JS_CREATE_API_PLANNER.yml) is an example of an agent pseudocode.

## Terminology

- **SIRJI_USER**: The developer using Sirji.
- **Agent**: A modular AI component in the Sirji framework that performs a specific task based on custom pseudocode.
- **Recipe**: A file listing prescribed tasks for solving a particular problem, indicating which agent should perform each task.
- **Project Folder**: The primary directory for all user-specific project files, including code files, documentation, and other relevant resources.
- **Agent Output Folder**: The designated folder for storing the results and data outputs generated by the agents.

## Pseudocode Use Cases

In this section, we will go over different use cases encountered while writing pseudocode, providing example pseudocode snippets and their corresponding messages generated by LLM, as per the Sirji messaging protocol.

### Use Case 1: Ask SIRJI_USER a Question

Example pseudocode snippet:

```
Ask SIRJI_USER to provide the route of the new API and the file path of the sequence diagram.
```

Corresponding message generated by LLM:

```
***
FROM: RECIPE_SELECTOR
TO: SIRJI_USER
ACTION: QUESTION
SUMMARY: Empty
BODY:
Please provide the route of the new API and the file path of the sequence diagram.
***
```

### Use Case 2: Create Project File

Example pseudocode snippet:

```
Under the services folder in the project, create a service file for the API, following the conventions used in the inspiration service file.
```

Corresponding message generated by LLM:

```
***
FROM: IMPLEMENTATION_GUIDE_CODE_WRITER
TO: EXECUTOR
ACTION: CREATE_PROJECT_FILE
SUMMARY: Creating a new service file to handle the business logic for updating a todo.
BODY:
File path: src/services/updateTodoService.js
---
const todoStorage = require('../storage/todoStorage');

const updateTodo = (id, data) => {
    return todoStorage.updateTodo(id, data);
};

module.exports = updateTodo;
***
```

### Use Case 3: Read Project Files

Example pseudocode snippet:

```
Using the project folder structure, determine the file paths for the following core codebase files and read them for the specified purposes:
    - OpenAPI file: Understand the input parameter and response specifications for the API.
    - Sequence diagram relevant to the Target API: Understand the logic to be implemented.
```

Corresponding message generated by LLM:

```
***
FROM: NODE_JS_CREATE_API_PLANNER
TO: EXECUTOR
ACTION: READ_PROJECT_FILES
SUMMARY: Reading core codebase files to understand the conventions and requirements for the new API route.
BODY:
File paths: ["docs/openapi.yaml", "docs/sequenceDiagrams/updateTodo.mermaid"]
***
```

### Use Case 4: Make Edits to File

Example pseudocode snippet:

```
Make the necessary changes to the storage file.
```

Corresponding message generated by LLM:

```
***
FROM: IMPLEMENTATION_GUIDE_CODE_WRITER
TO: EXECUTOR
ACTION: INSERT_BELOW
SUMMARY: Adding the new method `updateTodo` to the storage management file.
BODY:
FILE_PATH:
src/storage/todoStorage.js
---
NEW_CHANGES:
const updateTodo = (id, data) => {
    const todo = todos.find(t => t.id === id);
    if (!todo) return null;

    todo.title = data.title !== undefined ? data.title : todo.title;
    todo.description = data.description !== undefined ? data.description : todo.description;
    todo.completed = data.completed !== undefined ? data.completed : todo.completed;

    return todo;
};
---
INSERT_BELOW:
const addTodo = (data) => {
    const todo = { id: uuidv4(), title: data.title, description: data.description, completed: false, created_at: new Date() };
    todos.push(todo);
    return todo;
};
---

***
```

### Use Case 5: Writing File to Agent Output Folder

Example pseudocode snippet:

```
Store the problem statement (mentioning your understanding) in the Agent Output Folder.
```

Corresponding message generated by LLM:
The pseudo code snippet gets converted into the following 2 messages:

```
***
FROM: NODE_JS_CREATE_API_CODER
TO: EXECUTOR
ACTION: CREATE_AGENT_OUTPUT_FILE
SUMMARY: Creating a problem statement file for the new API route and sequence diagram.
BODY:
File path: NODE_JS_CREATE_API_CODER/problem_statement.json
---
{
    "route": "PUT /todos/{id}",
    "sequence_diagram": "docs/sequenceDiagrams/updateTodo.mermaid"
}
***
```

```
***
FROM: NODE_JS_CREATE_API_CODER
TO: EXECUTOR
ACTION: APPEND_TO_AGENT_OUTPUT_INDEX
SUMMARY: Registering the problem statement file in the Agent Output Index.
BODY:
File path: NODE_JS_CREATE_API_CODER/problem_statement.json
---
Description of the file contents: Problem statement for creating a new API route and sequence diagram.
Created by: NODE_JS_CREATE_API_CODER
***
```

### Use Case 6: Read from Agent Output Folder

Example pseudocode snippet:

```
Read the problem statement from the Agent Output Folder.
```

Corresponding message generated by LLM:

```
***
FROM: NODE_JS_CREATE_API_PLANNER
TO: EXECUTOR
ACTION: READ_AGENT_OUTPUT_FILES
SUMMARY: Reading the problem statement to identify the Target API route and sequence diagram file path.
BODY:
File paths: ["NODE_JS_CREATE_API_CODER/problem_statement.json"]
***
```

### Use Case 7: Write to Scratchpad

Example pseudocode snippet:

```
Understand the code conventions followed in the existing code which you have read and store your understanding in the scratchpad.
```

Corresponding message generated by LLM:

```
***
FROM: NODE_JS_CREATE_API_PLANNER
TO: EXECUTOR
ACTION: STORE_IN_SCRATCH_PAD
SUMMARY: Storing understanding of the code conventions and requirements in the scratchpad.
BODY:
Understanding of the code conventions and requirements:

1. **OpenAPI Specification**:
   - The `PUT /todos/{id}` route is defined to update a todo by ID.
   - It requires a path parameter `id` (string) and a request body containing `title`, `description`, and `completed` fields.
   - The response is a 200 OK with the updated todo object or a 404 if the todo is not found.

2. **Sequence Diagram**:
   - The sequence diagram outlines the flow for updating a todo.
   - The client sends a PUT request to the server with the todo ID and data.
   - The server calls the service layer's `updateTodo` method.
   - The service layer calls the storage layer's `updateTodo` method.
   - The storage layer returns the updated todo to the service layer.
   - The service layer returns the updated todo to the server.
   - The server responds to the client with the updated todo.

3. **Route File (src/routes/todoRoutes.js)**:
   - The route file uses Express.js to define routes.
   - Existing routes include `GET /todos`, `GET /todos/{id}`, `POST /todos`, and `DELETE /todos/{id}`.
   - Each route handler calls a corresponding service method and sends the response to the client.

4. **Storage File (src/storage/todoStorage.js)**:
   - The storage file manages the in-memory storage of todos.
   - It includes methods for getting all todos, getting a todo by ID, adding a todo, and deleting a todo.
   - The `updateTodo` method needs to be implemented to update a todo by ID.

5. **Service File (src/services/getTodoByIdService.js)**:
   - The service file follows a simple pattern of requiring the storage module and exporting a function that calls a storage method.
   - The `updateTodoService` file will follow a similar pattern, calling the `updateTodo` method from the storage module.

6. **Main Index File (src/server.js)**:
   - The `package.json` file indicates that the main index file is `src/server.js`.
   - This file acts as the primary routing file that includes all other sub-routers and defines top-level routes.

7. **Inspiration Service File (src/services/getTodoByIdService.js)**:
   - The service file for getting a todo by ID is straightforward, requiring the storage module and exporting a function that calls a storage method.
   - The new service file for updating a todo will follow a similar pattern.

***
```

### Use Case 8: Invoke Other Agents

Example pseudocode snippet:

```
Invoke agent NODE_JS_CREATE_API_PLANNER to create a comprehensive implementation guide for the new API to be implemented.
```

Corresponding message generated by LLM:

```
***
FROM: NODE_JS_CREATE_API_CODER
TO: NODE_JS_CREATE_API_PLANNER
ACTION: INVOKE_AGENT
SUMMARY: Invoking the Node.js API Planner to create an implementation guide for the new API.
BODY:
Create a comprehensive implementation guide for the new API route "PUT /todos/{id}" using the sequence diagram at "docs/sequenceDiagrams/updateTodo.mermaid".
***
```

TODO: add examples for INVOKE_AGENT_EXISTING_SESSION

### Use Case 9: Run Commands

TODO: add examples for EXECUTE_COMMAND

### Use Case 10: Run Server

TODO: add examples for RUN_SERVER

## Best Practices

Follow these best practices when writing agent pseudocode:

- **Ask Questions Early:** As much as possible, ask questions to SIRJI_USER at the beginning to prevent unnecessary messages in the conversation, which can reduce costs.
- **Read Files Efficiently:** Read multiple files in one go to minimize redundant file content being sent in API calls, leading to lower costs.
- **Structure Clearly:** Have a clear structure for the pseudocode to improve understanding and ease of editing.
- **Define Terms Clearly:** Define terms clearly for easy reference later in the pseudocode. Use phrases like "Let's call this ..." to establish terminology.
- **Break Large Problem into Small Steps:** Proceed incrementally when writing pseudo code. This allows LLM to perform small tasks sequentially instead of one complex task in one go. It is best to break your problem into several small steps.
- **Use Scratchpad to Remember LLM's Understanding** Wherever you want the LLM to remember its understanding of the step you should explicitly ask it to save it in the scratchpad.