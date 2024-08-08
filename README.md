<p align="center">
  <a href="." target="blank"><img src="https://github.com/sirji-ai/sirji/assets/7627517/363fc6dd-69af-4d84-8b7c-a91ec092058d" width="250" alt="Sirji Logo" /></a>
</p>

<p align="center">
  <em>Sirji is a framework to build & run custom AI agents for your everyday dev tasks.</em>
</p>

<p align="center">
  Built with ❤️ by <a href="https://truesparrow.com/" target="_blank">True Sparrow</a>
</p>

<p align="center">
  <a href="https://docs.sirji.ai/">
    <img alt="Documentation" src="https://img.shields.io/badge/docs-website-blue.svg">
  </a>
  <img alt="GitHub License" src="https://img.shields.io/github/license/sirji-ai/sirji">
  <img alt="GitHub commit activity" src="https://img.shields.io/github/commit-activity/m/sirji-ai/sirji">
  <img alt="GitHub Open Issues" src="https://img.shields.io/github/issues/sirji-ai/sirji">
  <img alt="GitHub Closed Issues" src="https://img.shields.io/github/issues-closed/sirji-ai/sirji">
</p>

<p align="center">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/sirji-ai/sirji">
  <img alt="GitHub forks" src="https://img.shields.io/github/forks/sirji-ai/sirji">
  <img alt="GitHub watchers" src="https://img.shields.io/github/watchers/sirji-ai/sirji">
</p>

## Sirji

Sirji is a framework designed to build and run custom AI agents for your everyday development tasks.

An agent in the Sirji framework is a modular AI component designed to perform specific task based on custom pseudocode. [Here](./docs/How%20to%20Write%20an%20Agent.md) is a guide for writing your own custom agent.

[Here](./docs/Sirji%20Studio.md) is a guide to organize and share your custom agents.

## Installation

You can start using Sirji by installing this [extension](https://marketplace.visualstudio.com/items?itemName=TrueSparrow.sirji) from the Visual Studio Marketplace.

Make sure you have installed all of the following prerequisites on your machine:
- Visual Studio Code (>= 1.80.2)
- Node.js (>= 18) and npm (>= 8.19)
- Python (>= 3.10) - Make sure `python --version` runs without error.
- tee command - Make sure `which tee` runs without error.

For LLM inference, you would need an API key from at least one of OpenAI, Anthropic or DeepSeek.

## Demo Video

Here's a three-minute demo. We tasked Sirji with creating a new API and its test cases in an existing Node.js repository. Sirji uses these custom agents we developed:
- **Code Planner**: Generates an implementation guide with steps and code snippets based on domain knowledge.
- **Test Planner**: Generates an implementation guide for test cases, following the existing framework and conventions.
- **Code Writer**: Implements the code changes specified in the guides.

Watch on YouTube: <a href="https://www.youtube.com/watch?v=NA7uPIvcvmg" target="_blank">https://www.youtube.com/watch?v=NA7uPIvcvmg</a>

<a href="https://www.youtube.com/watch?v=NA7uPIvcvmg" target="_blank"><img src="https://github.com/sirji-ai/sirji/assets/7627517/8156bdd5-7324-47e4-a375-df0d29e095c9" alt="Custom Agents for Creating a New API and Test Cases in an Existing Node.js Repository"></a>

**Note:
Sirji is still rough on the edges. We are also working on better documentation (particularly for Sirji Studio). So we suggest if you want to try Sirji, please let us give you a walkthrough. You can book a call with us [here](https://calendly.com/nishith-true-sparrow/30min).**

## Architecture

Let's go step by step in understanding the architecture.

### Agent

An Agent in the Sirji framework is a modular AI component that performs a specific task based on a custom pseudo code.

An agent defines its skill and pseudo code to follow for working on that skill in an agent.yml file. It also specifies the LLM provider and model to be used for inference. Additionally, it lists the sub-agents that can be invoked from within the agent to complete certain parts of the task.

### Recipe (recipe.json)

A Recipe is a file that lists prescribed tasks and tips for solving a particular problem. It also indicates which agent should perform each task. The tips provide guidance for addressing issues that arise when tasks are performed out of the prescribed order. Each tip specifies the task and the agent responsible for it.

### Orchestrator

The Orchestrator is the central component in the Sirji framework and is responsible for the following:
- Showing the list of available recipes to the user and asking them for their choice.
- Reading the selected recipe and managing the flow & execution of prescribed tasks from the selected recipe.

### Agent Sessions
An agent can be invoked in either a fresh session or asked to continue an existing session. When invoked in a new session, it starts with a new system prompt and does not retain the context from the previous session. Sessions help keep the context focused on specific tasks.

### Messaging Protocol
The messaging protocol defines how the response from an LLM inference for an agent should appear. It specifies the recipient-specific allowed Response Templates. These Response Templates also adhere to an interface that mandates the presence of keys: FROM, TO, BODY, SUMMARY, and ACTION. The BODY may contain an ACTION-specific information schema.

### Project Folder
The Project Folder is the primary directory for accessing all user-specific project files, including code files, documentation, and other relevant resources. When initializing Sirji, the user selects this folder as the primary workspace for the project.

### Agent Output Folder
The Agent Output Folder is designated for storing the results and data outputs generated by the agents. This folder is different from the project folder and this ensures that operational data is kept separate from project files.

#### Agent Output Index
The Agent Output Index is an index file for the Agent Output Folder that keeps track of all files written by agents in that folder along with the a brief description of the file contents.

### PyPI Packages

We have published the following 3 PyPI packages, implementing different responsibilities. These packages are invoked by Python Adapter Scripts, which are spawned by the extension.

#### sirji-agents <a href="https://pypi.org/project/sirji-agents/"><img src="https://img.shields.io/pypi/v/sirji-agents.svg" alt="Sirji Agents on PyPI" height="15"></a>

[`sirji-agents`](https://pypi.org/project/sirji-agents/) (located in the `agents` folder of this monorepo) is a PyPI package that implements the following components of the Sirji AI agentic framework:
- **Orchestrator**: The Orchestrator is the central component in the Sirji framework, responsible for managing the flow and execution of tasks across different agents.
- **Generic Agent**: Run time composable class providing the agent functionality as per the pseudo code provided in the agent.yml file.
- **Research Agent**: Utilizes RAG (Retrieval-Augmented Generation) and gets trained on URLs and search terms.

#### sirji-messages <a href="https://pypi.org/project/sirji-messages/"><img src="https://img.shields.io/pypi/v/sirji-messages.svg" alt="Sirji Messages on PyPI" height="15"></a>

[`sirji-messages`](https://pypi.org/project/sirji-messages/) (located in the `messages` folder of this monorepo) is a PyPI package that implements the Sirji messaging protocol with the following highlights:
- **Message Factory**: A factory that provides a Message class for a given action.
- **Message Parser**: Parse structured message strings into Python dictionaries for easy access to the message components.
- **Allowed Response Templates**: Provides the part of the system prompt describing allowed Response Templates for a given agent pair.
- **Custom Exceptions**: A set of custom exceptions thrown by the message parser.
- **Enums for Agents and Actions**: Provides easy auto-completion while writing code.

#### sirji-tools <a href="https://pypi.org/project/sirji-tools/"><img src="https://img.shields.io/pypi/v/sirji-tools.svg" alt="Sirji Tools on PyPI" height="15"></a>

[`sirji-tools`](https://pypi.org/project/sirji-tools/) (located in the `tools` folder of this monorepo) implements these tools:
- Crawling (downloading web pages to markdown files)
- Searching on Google
- Custom Logging

### Architecture Diagram
![Sirji - Architecture Diagram](https://github.com/sirji-ai/sirji/assets/7627517/0edd8cfe-1d49-4119-8960-1a3f2bf1f73f)

## Contributing

We welcome contributions to Sirji! If you're interested in helping improve this VS Code extension, please take a look at our [Contributing Guidelines](./CONTRIBUTING.md) for more information on how to get started.

Thank you for considering contributing to Sirji. We look forward to your contributions!

## Reporting Issues

If you run into any issues or have suggestions, please report them by following our [issue reporting guidelines](./ISSUES.md). Your reports help us make Sirji better for everyone.

## Stay In Touch

<a href="https://calendly.com/nishith-true-sparrow/30min" target="_blank">Office Hours</a>

## License

Distributed under the MIT License. See `LICENSE` for more information.
