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

Sirji is a Visual Studio Code Extension that acts as an AI Software Development Agent, an open-source alternative to Devin. It functions as a virtual software developer, geared towards solving the given problem statement. These problem statements can either involve fresh, greenfield development or efforts aimed at enhancing existing code, bug fixing, documentation, and test case creation in brownfield development.

The extension leverages the capabilities of VS Code, including the Editor, Terminal, Browser, and Project Explorer.

Additionally, it provides an interactive chat interface through which users can submit their problem statements, enhancement requests, feedback, and answers to requests for elaboration.

## Demo Videos
TODO: Show 2 good demo videos - side by side. Then afterwards, give a link to the demos page.

## Getting Started
TODO: Add steps for how to get started with using Sirji.

## Architecture

Sirji gets the work done using it's following agents:
- The **Planning Agent** takes a problem statement and breaks it down into steps.
- The **Coding Agent** proceeds step by step through the generated steps to solve the problem programmatically.
- The **Research Agent** utilizes RAG (Retrieval-Augmented Generation) and gets trained on URLs and search terms. It can later use this acquired knowledge to answer questions posed by the Coding Agent.
- The **Executor Agent** is responsible for Filesystem CRUD, executing commands, and installing dependencies. The Executor Agent is implemented directly within the extension and is written in TypeScript.

### Architecture Diagram
<img width="100%" alt="VS Code Extension - Architecture" src="https://github.com/sirji-ai/sirji/assets/7627517/0cee6e34-a42a-4db0-81db-d2f930132465">

### PyPI Packages
The Planning Agent, Coding Agent, and Research Agent are developed in the Python package [`sirji-agents`](https://pypi.org/project/sirji-agents/)<a href="https://pypi.org/project/sirji-agents/"><img src="https://img.shields.io/pypi/v/sirji-agents.svg" alt="Sirji Agents on PyPI" height="15"></a>

The communication between all these agents is defined as a message protocol. The Message Factory (CRUD for messages as per the message protocol) and permissions matrix are developed in the Python package [`sirji-messages`](https://pypi.org/project/sirji-messages/)<a href="https://pypi.org/project/sirji-messages/"><img src="https://img.shields.io/pypi/v/sirji-messages.svg" alt="Sirji Messages on PyPI" height="15"></a>

The tools for crawling URLs (converting them to markdowns), searching for a term on Google, and custom logger are developed in the Python package [`sirji-tools`](https://pypi.org/project/sirji-tools/)<a href="https://pypi.org/project/sirji-tools/"><img src="https://img.shields.io/pypi/v/sirji-tools.svg" alt="Sirji Tools on PyPI" height="15"></a>

All these packages are called from Python Adapter Scripts, which are spawned by the extension.

## For Contributors
TODO: Add a link to the doc in which steps for contributors to set up a local dev environment.

## License

Distributed under the MIT License. See `LICENSE` for more information.
