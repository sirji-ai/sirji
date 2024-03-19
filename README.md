# Sirji>

> “Sirji” is everywhere. A fun jab among friends. A chuckle on the Zoom call. Much more than respect. It's our vibe.

Inspired by <a href="https://www.cognition-labs.com/introducing-devin" target="_blank">Devin</a>, Sirji is an initiative by <a href="https://truesparrow.com/" target="_blank">True Sparrow</a> to build an open-source AI software development agent that solves complex problems. It will automatically create a plan to solve the problem statement, prioritize it, organize research, write code, execute it, and fix issues.

Sirji is being built using Python. It currently uses OpenAI chat completions API, and OpenAI assistants API.

To begin with, it will be equipped with:

- **Chat Terminal**: To give problem statements and continuously interact with Sirji.

- **Shell**: To create, modify, and execute files and install packages.

- **Browser**: To research different topics to solve the problem.

## How It Works<a name="how-it-works"></a>

In the dogfood version of Sirji, we are planning to have 4 layers in its architecture as shown in the high-level architecture diagram below.

- User Interaction Layer, i.e. Sirji>, will be the front-facing layer interacting with the user. Users can give the problem statement, and give suggestions or modification requests through this layer. Here, users can also see the progress made by Sirji. A command line chat terminal will be used to take user inputs.

- The Agents and Tools Layer will contain multiple agents and tools to be used by Sirji. The available agents will be the Planner, Solver, Security Analyser, Researcher, and Debugger. And, the available tools will be Crawler, Executor, and Logger. To check the work done by agents and tools, we will publish logs in their respective log files.

- The last two layers will consist of the Model & Embeddings Layer, and the Capabilities Layer with browser and shell access.

![Sirji Architecture Diagram](https://github.com/sirji-ai/sirji/assets/4491083/8b5d846b-168c-4499-ba2a-d0226946a0a6)

## Sequence Diagram<a name="sequence-diagram"></a>

The sequence diagram below shows how the user initiates Sirji by giving a problem statement through a chat terminal. From this point onwards, Sirji initiates a hands-free solution approach. However, the user can interact with Sirji by sending messages and asking to improve or modify the solution.

![Sirji Sequence Diagram](https://github.com/sirji-ai/sirji/assets/4491083/807e62d8-3ded-47c8-81cb-89dfa959ff72)

## How to Use<a name="how-to-use"></a>

The dogfood version of Sirji is under development. The current ETA is Friday, March 22 2024.

## Supported AI Models<a name="supported-ai-models"></a>

We are planning to use the `gpt-4-turbo-preview` model for the dogfood release. But the package will be designed to be composable for supporting other AI models too.

## Contribution

We welcome more helping hands to make Sirji better. Feel free to report issues, and raise PRs for fixes & enhancements.

<p align="left">Built with :heart: by <a href="https://truesparrow.com/" target="_blank">True Sparrow</a></p>
>>>>>>> main
