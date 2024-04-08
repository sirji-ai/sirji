# Contributing to Sirji

Thank you for your interest in contributing to Sirji, a VS Code Extension aimed at enhancing your coding workflow. This guide will help you set up your environment for contributing to Sirji.

## Getting Started

Before contributing, you'll need to clone the repository and set up the project on your local machine. Follow these steps to get started:

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

Install the project dependencies to ensure that everything will run smoothly:

```zsh
npm install
```

### 5. Compile TypeScript

Compile the TypeScript code to JavaScript:

```zsh
npm run compile
```

## Debugging the Extension

To start debugging the extension and see your changes in action, follow these steps:

1. **Open the Run and Debug View**

   - You can open this view from the Activity Bar on the left side of the window or by using the shortcut `Cmd+Shift+D`.

2. **Select Debug Configuration**

   - From the dropdown menu at the top of the **Run and Debug** view, select the `Run Extension` option.

3. **Start Debugging**

   - Press the **Start Debugging** button (the green play icon) to launch a new VS Code window (Extension Development Host) where the extension will be loaded.

### Activating the Extension

To activate the extension in the Extension Development Host:

- Open the Command Palette with `Cmd+Shift+P`, type `Sirji`, and press `Enter`.

Now the Sirji chat interface should open, allowing you to interact with Sirji via the chat.

## Contribution Guidelines

We encourage you to contribute to Sirji! Please consider the following guidelines when planning your contributions:

- Ensure any code changes are properly documented and include relevant comments.
- Adhere to the existing code style and standards.
- Test your changes thoroughly in the Extension Development Host before submitting a pull request.
- Include a descriptive message with your pull request detailing what has been changed or added.

## Questions or Problems?

If you encounter any problems or have questions about contributing to Sirji, please open an issue on our GitHub repository. We're here to help!

Again, thank you for your interest in contributing to Sirji. Happy coding!