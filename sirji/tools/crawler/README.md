
# Crawler Tools

This folder contains the components necessary for the crawler functionality within the project. It follows a Factory Design Pattern to create instances of different types of handlers (e.g., GitHub, PDF, Web Page) based on the input provided.

## Design Pattern

The Factory Design Pattern is used to abstract the creation logic of handler objects. This allows for easy addition of new handler types without modifying the existing codebase significantly.

## Sample Usages

- **GitHub Handler**: Used for crawling GitHub repositories.
- **PDF Handler**: Handles the extraction of text from PDF files.
- **Web Page Handler**: Crawls web pages to extract useful information.

Each handler extends from a base handler class (`base.py`), ensuring a consistent interface for all types of handlers.