# Sirji Studio

## What is Sirji Studio?

Sirji Studio is the GitHub repository where you create and manage your custom agents and recipes for Sirji.

## Why Create Sirji Studio?

Sirji Studio offers version control for your custom agents and recipes, making it easier for team members to share, modify, and update them in response to changing project conventions.

## Creating Sirji Studio

To set up Sirji Studio and make your repository compatible with Sirji, follow these steps:

1. **Create Folders**: At the root level of your repository, create `recipes` and `agents` folders.
2. **Copy Configuration Files**: Copy [ORCHESTRATOR.yml](../sirji/vscode-extension/src/defaults/agents/ORCHESTRATOR.yml) and [RECIPE_SELECTOR.yml](../sirji/vscode-extension/src/defaults/agents/RECIPE_SELECTOR.yml) into the `agents` folder.
3. **Create `index.json`**: In the `recipes` folder, create an `index.json` file. This file should list your recipe JSON files, mapping each to an object with `name` and `description` keys. Refer to [this example](../sirji/vscode-extension/src/defaults/recipes/index.json) for the format.
4. **Create Recipe JSON Files**: Add your recipe JSON files in the `recipes` folder. Refer to [this example](../sirji/vscode-extension/src/defaults/recipes/new_project.json) for the format.
5. **Create Agent YAML Files**: Add the necessary agent YAML files in the `agents` folder. Use [this example](../sirji/vscode-extension/src/defaults/agents/NODE_JS_CREATE_API_PLANNER.yml) as a reference.

## Configuring Sirji to Use Sirji Studio

To configure Sirji to use your custom agents and recipes from Sirji Studio, follow these steps:


1. Click the "Open Sirji Studio" button in the left panel.
   
2. In the opened VS Code window, open a terminal.

3. Remove the existing "studio" folder, which contains generic open-source agents, by running:
   ```zsh
   rm -rf studio
   ```
4. Clone your GitHub repository with custom agents and recipes into the "studio" folder:
   ```zsh
   git clone <repo url> studio
   ```
