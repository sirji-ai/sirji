# Sirji Studio

## What is Sirji Studio?

Sirji Studio refers to the GitHub repository where developers create and manage their custom agents and recipes.

The repository should have a specific folder structure:
- **Root Level**: Contains "recipes" and "agents" folders.
- **Recipes Folder**: Must include an `index.json` file.

## Why Use Sirji Studio?

Sirji Studio offers version control for custom agents and recipes, enabling team collaboration. Team members can share and modify agents, ensuring consistency across the project.

When project conventions change, corresponding updates to agents can be easily managed.

## Setting Up Sirji Studio

To start using Sirji Studio for your custom agents and recipes, follow these steps:

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
