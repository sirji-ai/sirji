<p align="center">
  <a href="." target="blank"><img src="https://github.com/sirji-ai/sirji/assets/7627517/363fc6dd-69af-4d84-8b7c-a91ec092058d" width="250" alt="Sirji Logo" /></a>
</p>

<p align="center">
  <em>Sirji is an agentic AI framework for software development.</em>
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

Sirji as an open-source framework where various AI agents collaborate via a messaging protocol to solve a given software problem. Problems range from building greenfield web apps to solving GitHub issues, writing test cases, and generating documentation.

Sirji uses either the standard or user-generated recipe, that lists prescribed tasks and tips for solving a particular problem. Recipe also indicates which agent should perform each task.

An Agent in the Sirji framework is a modular AI component that performs a specific task based on a custom pseudo code. The community can create a custom agent either by modifying an already existing agent or write entirely new agent with entirely different pseudo code.

Sirji is currently implemented as a Visual Studio Code extension. This extension provides an interactive chat interface right within your IDE through which you can submit your problem statement and give feedback to Sirji.

The extension leverages the capabilities of VS Code, including the Editor, Terminal, and Project Explorer.

Additionally, Sirji sets up your local or remote development environment by installing system-level packages and programming language-specific dependencies. It executes the generated code in your local or remote development environment.

## Prerequisites

Make sure you have installed all of the following prerequisites on your machine:

- Visual Studio Code (>= 1.80.2)
- Node.js (>= 18) and npm (>= 8.19)
- Python (>= 3.10) - Make sure `python --version` runs without error.
- tee command - Make sure `which tee` runs without error.

Also, you will need an OpenAI API key to access the GPT-4o model.

## Demo Video

Here's a three-minute demo showing the five-second Sirji installation, followed by a quick walkthrough of Sirji's attempt to solve a given problem statement (building an interactive Tic-Tac-Toe game website).

Watch on YouTube: <a href="https://www.youtube.com/watch?v=r1wJHLUDVTo" target="_blank">https://www.youtube.com/watch?v=r1wJHLUDVTo</a>

<a href="https://www.youtube.com/watch?v=r1wJHLUDVTo" target="_blank"><img src="https://github.com/sirji-ai/sirji/assets/7627517/a21804a7-06d5-4974-ae94-bb72870b93fd" alt="Tic Tac Toe game by Sirji"></a>

## Installation

You can start using Sirji by installing this [extension](https://marketplace.visualstudio.com/items?itemName=TrueSparrow.sirji) from the Visual Studio Marketplace.

## Architecture

Let's go step by step in understanding the architecture.

### Agent

An Agent in the Sirji framework is a modular AI component that performs a specific task based on a custom pseudo code.

An agent defines its skills in an agent.yml file. This file lists the skills of the agent and the pseudo code to follow for each skill. It also specifies the LLM provider and model to be used for inference. Additionally, it lists the sub-agents that can be invoked from within the agent to complete certain parts of the task.

### Recipe (recipe.json)

A Recipe is a file that lists prescribed tasks and tips for solving a particular problem. It also indicates which agent should perform each task. The tips provide guidance for addressing issues that arise when tasks are performed out of the prescribed order. Each tip specifies the task and the agent responsible for it.

### Orchestrator

The Orchestrator is the central component in the Sirji framework, responsible for managing the flow and execution of tasks across different agents as per the recipe.

### Agent Sessions
An agent can be invoked in either a fresh session or asked to continue an existing session. When invoked in a new session, it starts with a new system prompt and does not retain the context from the previous session. Sessions help keep the context focused on specific tasks.

### Project Folder
The Project Folder is the primary directory for accessing all user-specific project files, including code files, documentation, and other relevant resources. When initializing Sirji, the user selects this folder as the primary workspace for the project.

### Agent Output Folder
The Agent Output Folder is designated for storing the results and data outputs generated by the agents. This folder is different from the project folder and this ensures that operational data is kept separate from project files.

#### Agent Output Index
The Agent Output Index is an index file for the Agent Output Folder that keeps track of all files written by agents in that folder along with the a brief description of the file contents.

### PyPI Packages

The Planning Agent, Coding Agent, and Research Agent are developed within the Python package [`sirji-agents`](https://pypi.org/project/sirji-agents/) (located in the `agents` folder of this monorepo). <a href="https://pypi.org/project/sirji-agents/"><img src="https://img.shields.io/pypi/v/sirji-agents.svg" alt="Sirji Agents on PyPI" height="15"></a>

Communication among these agents is facilitated through a defined message protocol. The Message Factory (responsible for creating, reading, updating, and deleting messages according to the message protocol) and the permissions matrix are developed in the Python package [`sirji-messages`](https://pypi.org/project/sirji-messages/) (located in the `messages` folder of this monorepo).<a href="https://pypi.org/project/sirji-messages/"><img src="https://img.shields.io/pypi/v/sirji-messages.svg" alt="Sirji Messages on PyPI" height="15"></a>

The tools for crawling URLs (converting them into markdowns), searching for terms on Google, and a custom logger are developed within the Python package [`sirji-tools`](https://pypi.org/project/sirji-tools/) (located in the `tools` folder of this monorepo). <a href="https://pypi.org/project/sirji-tools/"><img src="https://img.shields.io/pypi/v/sirji-tools.svg" alt="Sirji Tools on PyPI" height="15"></a>

All these packages are invoked by Python Adapter Scripts, which are spawned by the extension.

### Architecture Diagram
![Sirji - Architecture Diagram](https://github.com/sirji-ai/sirji/assets/7627517/9068c6d1-a11b-4589-b09e-ad494334fd6b)

## Roadmap
We are calling our next release the ‘Core’ Release (ONGOING. ETA - May 20).

Here is the link to the ‘Core’ release’s roadmap: https://github.com/orgs/sirji-ai/projects/5

This is a significant release focused on the following key areas:
- **User accounts**: Users will be required to create an account with Sirji. They can either bring their own LLM key or subscribe to a free but rate-limited Developer plan.
- **Improve reliability**: The first version of the VS Code extension improved usability, but after using it ourselves for a while, we identified several issues and limitations ranging from incomplete solutions to a lack of web debugging capabilities. We are addressing these issues to make Sirji more reliable in solving software problems.
- **Custom agents and recipes**: We are developing the framework to enable users to create and use custom agents and recipes (instructions on how the agents interact). This involves enhancing the orchestration functionality and refactoring existing base agents.

## Contributing

We welcome contributions to Sirji! If you're interested in helping improve this VS Code extension, please take a look at our [Contributing Guidelines](./CONTRIBUTING.md) for more information on how to get started.

Thank you for considering contributing to Sirji. We look forward to your contributions!

## Reporting Issues

If you run into any issues or have suggestions, please report them by following our [issue reporting guidelines](./ISSUES.md). Your reports help us make Sirji better for everyone.

## Stay In Touch

<a href="https://calendly.com/nishith-true-sparrow/30min" target="_blank">Office Hours</a>

## License

Distributed under the MIT License. See `LICENSE` for more information.
