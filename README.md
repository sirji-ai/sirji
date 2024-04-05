<p align="center">
  <a href="." target="blank"><img src="https://github.com/sirji-ai/sirji/assets/7627517/363fc6dd-69af-4d84-8b7c-a91ec092058d" width="250" alt="Sirji Logo" /></a>
</p>

<p align="center">
  <em>Sirji is an Open Source AI Software Development Agent.</em>
</p>

<p align="center">
  Built with :heart: by <a href="https://truesparrow.com/" target="_blank">True Sparrow</a>
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


## Description

> “Sirji” is everywhere. A fun jab among friends. A chuckle on the Zoom call. Much more than respect. It's our vibe.

Sirji is a Visual Studio Code Extension (developed in TypeScript) that provides an interactive chat interface right within VS Code IDE to assist the user in inputting their problem statement, submitting feedback or enhancement requests, and getting answers to various queries during the problem-solving process.

## Architecture Diagram
<img width="893" alt="vs code extension - architecture" src="https://github.com/sirji-ai/sirji/assets/7627517/6120d7cc-550c-4497-9d83-587bc2a8bc8a">

The extension leverages the capabilities of VS Code, such as Editor, Terminal, Browser and Project Explorer.

Additionally, it introduces an Executor Agent built-in TypeScript that facilitates:
- Running Commands
- Filesystem Create, Read, Update, Delete (CRUD) operations
- Installing Packages

A chat interface is implemented within the VS Code IDE to interact with the user.

## PyPI Packages
To reuse code across multiple user interfaces (including the earlier GUI of Dogfood, the current VS Code Extension, and the future Browser interface), we have published these three PyPI packages:

### sirji-agents [![PyPI version](https://img.shields.io/pypi/v/sirji-agents.svg)](https://pypi.org/project/sirji-agents/)

`sirji-agents` is a PyPI package, developed in the `agents` folder of this monorepo. It implements these three key agents:
- The **Planning Agent** takes in a problem statement and breaks it down into steps.
- The **Coding Agent** goes step by and generates code to solve it programmatically.
- The **Research Agent** utilizes RAG, and gets trained on URLs and Search terms. Later, it can use the training knowledge to infer for answering the questions asked by the Coding Agent.

The Planning Agent and Coding Agent utilize OpenAI Chat Completions API, but they can be easily extended to infer from other LLMs.
Similarly, the Research Agent is currently built using the OpenAI Assistants API and can be easily extended to use vector databases to store the embeddings and implement the RAG approach.

For more details, visit the [sirji-agents page on PyPI](https://pypi.org/project/sirji-agents/).





--------







## Demo Videos

For demo videos, visit [here](./demos).

## How to Use<a name="how-to-use"></a>

The dogfood version of Sirji is ready.

Follow these [setup steps](./docs/setup-steps.md) to start Sirji.

## Capabilities<a name="capabilities"></a>

Sirji is being built using Python. It currently uses OpenAI chat completions API and OpenAI assistants API.

To begin with, it will be equipped with:

- **Chat Terminal**: To give problem statements and continuously interact with Sirji.

- **Shell**: To create, modify, and execute files and install packages.

- **Browser**: To research different topics to solve the problem.

## How It Works<a name="how-it-works"></a>

In the dogfood version of Sirji, we are planning to have 4 layers in its architecture as shown in the high-level architecture diagram below.

- User Interaction Layer, i.e. Sirji>, will be the front-facing layer interacting with the user. Users can give the problem statement, and give suggestions or modification requests through this layer. Here, users can also see the progress made by Sirji. A command line chat terminal will be used to take user inputs.

- The Agents and Tools Layer will contain multiple agents and tools to be used by Sirji. The available agents will be the Planner, Coder, Security Analyser, Researcher, and Debugger. And, the available tools will be Crawler, Executor, and Logger. To check the work done by agents and tools, we will publish logs in their respective log files.

- The last two layers will consist of the Model & Embeddings Layer, and the Capabilities Layer with browser and shell access.

![Sirji Architecture Diagram](https://github.com/sirji-ai/sirji/assets/4491083/4204d366-ccbc-473a-8a0b-233333ce1fdc)

## Sequence Diagram<a name="sequence-diagram"></a>

The sequence diagram below shows how the user initiates Sirji by giving a problem statement through a chat terminal. From this point onwards, Sirji initiates a hands-free solution approach. However, the user can interact with Sirji by sending messages and asking to improve or modify the solution.

![Sirji Sequence Diagram](https://github.com/sirji-ai/sirji/assets/4491083/807e62d8-3ded-47c8-81cb-89dfa959ff72)

## Supported AI Models<a name="supported-ai-models"></a>

We are planning to use the `gpt-4-turbo-preview` model for the dogfood release. But the package will be designed to be composable for supporting other AI models too.

## Contribution

We welcome more helping hands to make Sirji better. Feel free to report issues, and raise PRs for fixes & enhancements.

<p align="left">Built with :heart: by <a href="https://truesparrow.com/" target="_blank">True Sparrow</a></p>
