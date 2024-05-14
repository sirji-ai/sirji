<p align="center">
  <a href="." target="blank"><img src="https://github.com/sirji-ai/sirji/assets/7627517/363fc6dd-69af-4d84-8b7c-a91ec092058d" width="250" alt="Sirji Logo" /></a>
</p>

<p align="center">
  <em>Sirji is an Open Source AI Software Development Agent.</em>
</p>

<p align="center">
  Built with ❤️ by <a href="https://truesparrow.com/" target="_blank">True Sparrow</a>
</p>

<p align="center">
  <img alt="GitHub License" src="https://img.shields.io/github/license/sirji-ai/sirji">
  <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/sirji-ai/sirji">
  <img alt="GitHub Issues or Pull Requests" src="https://img.shields.io/github/issues/sirji-ai/sirji">
</p>

<p align="center">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/sirji-ai/sirji">
  <img alt="GitHub forks" src="https://img.shields.io/github/forks/sirji-ai/sirji">
  <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/sirji-ai/sirji">
</p>

## Sirji

Sirji is an agentic AI framework that helps developers solve software problems faster. These problems can range from building greenfield web applications to resolving GitHub issues, writing test cases, generating documentation, conducting code reviews, and much more.

Right now, we have implemented Sirji as a VS Code extension. It lives where developers work. It provides an interactive chat interface, through which you can submit your problem statement and provide feedback. It takes advantage of the capabilities of VS Code, including the Editor, Terminal, and Project Explorer.

Additionally, Sirji sets up your local or remote development environment by installing system-level packages and programming language-specific dependencies. It also executes the generated code in your local or remote development environment.

In the next release, we will be making Sirji extendable, building it as a framework where the community can write custom agents having specialized skills, which would generate better results than a generic agent.

## Why Do Developers Need Sirji?

As developers, we aim to dedicate more time to high-impact activities, such as understanding requirements, finalizing architecture, and designing database schemas. We also strive to liberate ourselves from writing routine code—like models, migrations, and routes—and from the ongoing task of keeping test cases and documentation up to date.

When adopting a new tech stack, it often takes time to familiarize ourselves with its concepts. Moreover, we frequently encounter runtime issues, such as missing packages or modules and errors that, while typically simple to resolve, are time-consuming.

We are enthusiastic users and fans of GitHub Copilot, which assists us in writing code and resolving issues. However, Copilot’s contextual awareness is quite limited. To use it, we must first open the specific code file requiring changes and then activate Copilot. This becomes cumbersome in large projects spanning multiple repositories, particularly if developers are unsure where to begin. Additionally, Copilot is limited to the context of the current file, unless other files are explicitly mentioned in the comments.

Furthermore, Copilot does not facilitate the process of getting code to run on our machines, which can require considerable effort and distract from more impactful tasks.

These are all the problems and limitations we want to solve with Sirji, and in the process, build something that we will use ourselves.

## Demo Video

Here's a three-minute demo showing the five-second Sirji installation, followed by a quick walkthrough of Sirji's attempt to solve a given problem statement (building an interactive Tic-Tac-Toe game website).

Watch on YouTube: <a href="https://www.youtube.com/watch?v=r1wJHLUDVTo" target="_blank">https://www.youtube.com/watch?v=r1wJHLUDVTo</a>

<a href="https://www.youtube.com/watch?v=r1wJHLUDVTo" target="_blank"><img src="https://github.com/sirji-ai/sirji/assets/7627517/a21804a7-06d5-4974-ae94-bb72870b93fd" alt="Tic Tac Toe game by Sirji"></a>

## Prerequisites

Sirji has been tested on **macOS** only for now. We know there are certain OS-specific functionalities that we will soon generalize ([Issue #44](https://github.com/sirji-ai/sirji/issues/44)).

Make sure you have installed all of the following prerequisites on your machine:

- Visual Studio Code (>= 1.80.2)
- Node.js (>= 18) and npm (>= 8.19)
- Python (>= 3.10) - Make sure `python --version` runs without error.
- tee command - Make sure `which tee` runs without error.

Also, you will need an OpenAI API key to access the GPT-4o  model.

## Installation

You can start using Sirji by installing this [extension](https://marketplace.visualstudio.com/items?itemName=TrueSparrow.sirji) from the Visual Studio Marketplace.

## Architecture

Sirji gets the work done using it's following agents:

- The **Planning Agent** takes a problem statement and breaks it down into steps.
- The **Coding Agent** proceeds step by step through the generated steps to solve the problem programmatically.
- The **Research Agent** utilizes RAG (Retrieval-Augmented Generation) and gets trained on URLs and search terms. It can later use this acquired knowledge to answer questions posed by the Coding Agent.
- The **Executor Agent** is responsible for Filesystem CRUD, executing commands, and installing dependencies. The Executor Agent is implemented directly within the extension and is written in TypeScript.

### Architecture Diagram

<img width="100%" alt="VS Code Extension - Architecture" src="https://github.com/sirji-ai/sirji/assets/7627517/0cee6e34-a42a-4db0-81db-d2f930132465">

### PyPI Packages

The Planning Agent, Coding Agent, and Research Agent are developed within the Python package [`sirji-agents`](https://pypi.org/project/sirji-agents/) (located in the `agents` folder of this monorepo). <a href="https://pypi.org/project/sirji-agents/"><img src="https://img.shields.io/pypi/v/sirji-agents.svg" alt="Sirji Agents on PyPI" height="15"></a>

Communication among these agents is facilitated through a defined message protocol. The Message Factory (responsible for creating, reading, updating, and deleting messages according to the message protocol) and the permissions matrix are developed in the Python package [`sirji-messages`](https://pypi.org/project/sirji-messages/) (located in the `messages` folder of this monorepo).<a href="https://pypi.org/project/sirji-messages/"><img src="https://img.shields.io/pypi/v/sirji-messages.svg" alt="Sirji Messages on PyPI" height="15"></a>

The tools for crawling URLs (converting them into markdowns), searching for terms on Google, and a custom logger are developed within the Python package [`sirji-tools`](https://pypi.org/project/sirji-tools/) (located in the `tools` folder of this monorepo). <a href="https://pypi.org/project/sirji-tools/"><img src="https://img.shields.io/pypi/v/sirji-tools.svg" alt="Sirji Tools on PyPI" height="15"></a>

All these packages are invoked by Python Adapter Scripts, which are spawned by the extension.

## Roadmap
We are calling our next release the ‘Core’ Release (ONGOING. ETA - May 20).

Here is the link to the ‘Core’ release’s roadmap: https://github.com/orgs/sirji-ai/projects/5

This is a significant release focused on the following key areas:
- **User accounts**: Users will be required to create an account with Sirji. They can either bring their own LLM key or subscribe to a free but rate-limited Developer plan.
- **Improve reliability**: The first version of the VS Code extension improved usability, but after using it ourselves for a while, we identified several issues and limitations ranging from incomplete solutions to a lack of web debugging capabilities. We are addressing these issues to make Sirji more reliable in solving software problems.
- **Custom agents and recipes**: We are developing the framework to enable users to create and use custom agents and recipes (instructions on how the agents interact). This involves enhancing the orchestration functionality and refactoring existing base agents.

### Architecture Diagram (Post Core Release)
![Sirji - Architecture Diagram](https://github.com/sirji-ai/sirji/assets/7627517/9068c6d1-a11b-4589-b09e-ad494334fd6b)

## Contributing

We welcome contributions to Sirji! If you're interested in helping improve this VS Code extension, please take a look at our [Contributing Guidelines](./CONTRIBUTING.md) for more information on how to get started.

Thank you for considering contributing to Sirji. We look forward to your contributions!

## Reporting Issues

If you run into any issues or have suggestions, please report them by following our [issue reporting guidelines](./ISSUES.md). Your reports help us make Sirji better for everyone.

## Stay In Touch

<a href="https://calendly.com/nishith-true-sparrow/30min" target="_blank">Office Hours</a>

## License

Distributed under the MIT License. See `LICENSE` for more information.
