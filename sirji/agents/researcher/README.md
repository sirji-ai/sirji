# Researcher

Whenever Sirji comes across requirements in which there are knowledge points, outside of its knowledge, it invokes the Researcher module. Researcher is based on the RAG (Retrieval-Augmented Generation) framework.

Current implementation uses OpenAI Assistants API. We have taken care of making the module composable, which will make strategy changes easier (described in detail below).

The Researcher module has 2 main parts: Embeddings Manager and Inferer.

## Embeddings Manager

There can be different strategies for implementing the Embeddings manager. Factory and strategy design patterns are used to improve composability and to make the addition of new strategies easy. Presently, OpenAI Assistants API is used to upload new documents to the assistant.

Embeddings manager has 2 major functions:

- **Index**: This is where the new knowledge points are indexed.
- **Retrieve Context**: This is where the matching context based on the problem statement is retrieved and passed to the Inferer as a part of the prompt. In the current OpenAI Assistant API implementation, this step is not needed and so it is implemented using an empty method. If we use a vector database for storing embeddings, we would implement this part for shortlisting and populating the retrieved context using embeddings match.

## Inferer

In this part, the LLM model is called to infer using a prompt that has both the problem statement and the retrieved context from the previous part. In the present OpenAI Assistant API implementation, the inference is made on the same assistant (assistant id preserved in object). There can be different strategies for implementing this part and to make it composable, we have used strategy and factory design patterns.

## Fun Fact

When developing the Researcher module, we needed to go through the OpenAI Assistants API documentation. This documentation was outside the knowledge of our LLM (gpt-4-turbo-preview). So the model was not able to assist us in development. Rather than going through the documentation manually, we thought of using the Sirji approach to research. We manually indexed (manual, since the automated process is what we needed to develop) a new assistant with the PDF prints of the documentation. After this indexing, the assistant helped us to write the Researcher. This also proved to us that the Sirji way of research works!

## Sample Usage

```python
from sirji.agents.researcher import Researcher

# Initialize Researcher
researcher = Researcher('openai_assistant', 'openai_assistant')

# For given URLs, convert to markdown files. Generate and store embeddings.
researcher.index(['https://example.com'])

# For a given query, perform Google search, convert result pages to markdown. Generate and store embeddings.
researcher.search_and_index('YOUR QUERY HERE')

# Retrieve the matching context uisng embeddings and pass it along prompt for inference.
researcher.infer('Sample question')
```
