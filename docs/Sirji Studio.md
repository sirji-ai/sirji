# Sirji Studio

## What is Sirji Studio?

Sirji Studio is a collection of your custom agents and recipes, organized in a specific folder structure. We recommend storing these agents and recipes in a GitHub repository.

## Why Use a GitHub Repository for Sirji Studio?

A GitHub repository provides version control for your custom agents and recipes, making sharing them with your team members easier. Moreover, it helps with modifying and updating them as project conventions change.

## Creating Sirji Studio from Scratch

To set up Sirji Studio, follow these steps:

1. **Create Folders**: At the root level of your Sirji Studio folder, create `recipes` and `agents` folders.
2. **Copy Configuration Files**: Copy [ORCHESTRATOR.yml](../sirji/vscode-extension/src/defaults/agents/ORCHESTRATOR.yml) and [RECIPE_SELECTOR.yml](../sirji/vscode-extension/src/defaults/agents/RECIPE_SELECTOR.yml) into the `agents` folder.
3. **Create `index.json`**: In the `recipes` folder, create an `index.json` file that lists your recipe JSON files, each mapped to an object with `name` and `description` keys. Refer to [this example](../sirji/vscode-extension/src/defaults/recipes/index.json) for the format.
4. **Create Recipe JSON Files**: Add your recipe JSON files in the `recipes` folder. Refer to [this example](../sirji/vscode-extension/src/defaults/recipes/new_project.json) for the format.
5. **Create Agent YAML Files**: Add the necessary agent YAML files in the `agents` folder. Use [this example](../sirji/vscode-extension/src/defaults/agents/NODE_JS_CREATE_API_PLANNER.yml) as a reference.
6. **Commit to GitHub Repository (Optional)**: Optionally, commit the `agents` and `recipes` folders and all their files to a GitHub repository for version control.

## Configuring Sirji to Use Sirji Studio

To configure Sirji to use your custom agents and recipes from a GitHub repository, follow these steps:

1. Click the "Open Sirji Studio" button in the left panel.
2. In the opened VS Code window, open a terminal.
3. Remove the contents of the "studio" folder.
   ```zsh
   rm -rf studio && mkdir studio
   ```
4. Bring your custom agents and recipes to the "studio" folder:
   - **From your GitHub Repository**: Clone your GitHub repository into the "studio" folder:
     ```zsh
     cd studio && git clone <repo URL> . && cd ..
     ```
   - **Without version control**: Manually copy the `agents` and `recipes` folders into the "studio" folder.

