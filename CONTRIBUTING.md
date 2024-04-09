# Contributing to Sirji

Thank you for your interest in contributing to Sirji, a VS Code Extension that aims to enhance your coding experience. This guide is designed to help you set up your environment for contributing to Sirji and its components, including the associated PyPI packages.

## Prerequisites

Make sure you have installed all of the following prerequisites on your machine:

- Visual Studio Code (>= 1.80.2)
- Node.js (>= 18) and npm (>= 8.19)
- Python (>= 3.10) - Make sure `python --version` runs without error.
- tee command - Make sure `which tee` runs without error.

To check whether your machine meets these prerequisites, run:

```zsh
sh check_prerequisites.sh
```

Also, you will need an OpenAI API key.

## Contributing to VS Code Extension

### 1. Clone the Repository

First, clone the Sirji repository to your local machine using the following command:

```zsh
git clone git@github.com:sirji-ai/sirji.git
```

### 2. Navigate to the Extension Directory

Once the repository is cloned, switch to the VS Code Extension directory:

```zsh
cd sirji/vscode-extension
```

### 3. Open the Project in VS Code

Open the folder in Visual Studio Code by running:

```zsh
code .
```

### 4. Install Dependencies

Install the project dependencies:

```zsh
npm install
```

### 5. Compile TypeScript

Compile the TypeScript code to JavaScript:

```zsh
npm run compile
```

### 6. Run Sirji in Debug Mode

To start debugging the extension and see your changes in action, follow these steps:

- **Open the Run and Debug View**

  - You can open this view from the Activity Bar on the left side of the window or by using the shortcut `Cmd+Shift+D`.

- **Select Debug Configuration**

  - From the dropdown menu at the top of the **Run and Debug** view, select the `Run Extension` option.

- **Start Debugging**

  - Press the **Start Debugging** button (the green play icon) to launch a new VS Code window (Extension Development Host) where the extension will be loaded.

### 7. Activating Sirji

To activate the extension in the Extension Development Host:

- Open the Command Palette with `Cmd+Shift+P`, type `Sirji`, and press `Enter`.

Now the Sirji chat interface should open, allowing you to interact with Sirji via the chat.

## Contributing to the PyPI Packages

To contribute to one of the PyPI packages (`sirji-agents`, `sirji-messages`, `sirji-tools`), please refer to the instructions provided in the respective `README` files within their directories:

- [Agents README](./agents/README.md) for contributing to `sirji-agents`.
- [Messages README](./messages/README.md) for contributing to `sirji-messages`.
- [Tools README](./tools/README.md) for contributing to `sirji-tools`.

## Questions or Issues?

If you face any issues or have questions about contributing, don’t hesitate to open an issue in our GitHub repository. We're here to help and look forward to your contributions!

Thank you for considering contributing to Sirji. Happy coding!
