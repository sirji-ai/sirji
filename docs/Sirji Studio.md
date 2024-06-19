
markdown
Copy code
# Sirji Studio

## What is Sirji Studio?

Sirji Studio is the GitHub repository where you create and manage your custom agents and recipes for Sirji. To set it up, follow these steps to make your repository compatible with Sirji:

1. **Create Folders**: At the root level of your repository, create `recipes` and `agents` folders.
2. **Copy Configuration Files**: Copy [ORCHESTRATOR.yml](../sirji/vscode-extension/src/defaults/agents/ORCHESTRATOR.yml) and [RECIPE_SELECTOR.yml](../sirji/vscode-extension/src/defaults/agents/RECIPE_SELECTOR.yml) into the `agents` folder.
3. **Create `index.json`**: In the `recipes` folder, create an `index.json` file. This file should define an object with keys as the file names of your recipe JSON files. Each key should map to an object with `name` and `description` keys. Refer to [this example](../sirji/vscode-extension/src/defaults/recipes/index.json) for the format.
4. **Create Recipe JSON Files**: Add your recipe JSON files in the `recipes` folder. Refer to [this example](../sirji/vscode-extension/src/defaults/recipes/new_project.json) for the format.
5. **Create Agent YAML Files**: Add the necessary agent YAML files in the `agents` folder. Use [this example](../sirji/vscode-extension/src/defaults/agents/NODE_JS_CREATE_API_PLANNER.yml) as a reference.

## Why Use Sirji Studio?

Sirji Studio provides version control for custom agents and recipes, facilitating team collaboration. It allows team members to share and modify agents. When project conventions change, updates to agents can be managed easily.

## Configuring Sirji to Use Sirji Studio

To configure Sirji to use your custom agents and recipes from your Sirji Studio, follow these steps:

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
