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

Sirji is currently made available as a Visual Studio Code extension. This extension provides an interactive chat interface within your IDE, through which you can submit your problem statement and provide feedback to Sirji. The extension takes advantage of the capabilities of VS Code, including the Editor, Terminal, and Project Explorer.

Additionally, Sirji sets up your local or remote development environment by installing system-level packages and programming language-specific dependencies. It also executes the generated code in your local or remote development environment.

## Demo Video

Here's a three-minute demo showing the five-second Sirji installation, followed by a quick walkthrough of Sirji's attempt to solve a given problem statement (building an interactive Tic-Tac-Toe game website).

Watch on YouTube: <a href="https://www.youtube.com/watch?v=r1wJHLUDVTo" target="_blank">https://www.youtube.com/watch?v=r1wJHLUDVTo</a>

<a href="https://www.youtube.com/watch?v=r1wJHLUDVTo" target="_blank"><img src="https://github.com/sirji-ai/sirji/assets/7627517/a21804a7-06d5-4974-ae94-bb72870b93fd" alt="Tic Tac Toe game by Sirji"></a>

## Prerequisites

Sirji has been tested on **macOS** only for now. We know there are certain OS-specific functionalities that we will soon generalize.

Make sure you have installed all of the following prerequisites on your machine:

- Visual Studio Code (>= 1.80.2)
- Node.js (>= 18) and npm (>= 8.19)
- Python (>= 3.10) - Make sure `python --version` runs without error.
- tee command - Make sure `which tee` runs without error.

Also, you will need an OpenAI API key to access the GPT-4 Turbo model.

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
The upcoming [roadmap](https://github.com/orgs/sirji-ai/projects/5/views/1) outlines the plan to achieve Reliability, Extendability, and Accessibility by May 20, 2024.

### Reliability Milestone
**Goal**: Improve Sirji's reliability in solving software problems.

The VS Code extension has enhanced Sirji's usability, but our extensive testing has identified several issues:
- Sirji often indicates that it has solved the problem even when it has not fully implemented the expected functionalities.
- Unable to debug web errors, Sirji relies on manual error reporting by users.
- It incorrectly claims that tasks like installing MongoDB are "outside of my capability."
- Sometimes, it installs system-wide packages like Python or creates files outside the designated workspace without user consent.

To solve these issues, we have identified the following changes:
- Introduce a QA Agent and a Code Review Agent.
- Add workspace and OS awareness along with improved accessibility.
- Generate more elaborated epics and user stories.

### Extendability - Recipes and Custom Agents Milestone
**Goal**: Achieve community-driven customization and flexibility to solve a wide range of software problems.

This milestone enhances Sirji's capabilities by introducing:
- **Recipes and Custom Agents:** Enable the community to develop custom recipes, which are guidelines for how agents interact, and to create custom agents.
- **Orchestration:** Utilize recipes, along with agents' published skills, to manage task assignments and agent invocations.
- **Agent Extendability:** Agents can publish their skills and the allowed incoming & outgoing messages. Custom agents can be modifications of existing ones or completely new implementations written from scratch.

### Accessibility Milestone
**Goal**: Allow users to experience Sirji with or without an OpenAI API key.

The following are the key highlights:
- Enable users to use Sirji seamlessly, with or without an OpenAI API key:
  - **Users with their own OpenAI key** can simply enter it into the extension and start using Sirji.
  - **Users without an OpenAI API key** can utilize Sirji's proxy APIs:
    - **Account Creation:** Users must create an account on Sirji and will be placed on a waitlist. After advancing from the waitlist, they can simply start using Sirji, accessing services like LLM Embedding and LLM Inference via proxy APIs.
    - **Rate Limiting:** Implement rate limits on the daily number of tokens a user consumes.
- Develop a system to collect user feedback.
- Ensure that Sirji runs on Windows and Linux.


### Updated Architecture Diagram
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
