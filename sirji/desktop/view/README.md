# View

This is Sirji's view module for the dogfood release. For dogfood, it will be a command line based tool, which will later on be taken to a browser based view in later releases.

It will have logs from various agents displayed in different terminal windows. Let's go over all the sub-modules of the view module.

## Terminal

The Terminal module is used to open a new terminal window on macOS and run a specified command in it. It arranges terminal windows in a 3x2 grid layout based on the specified position, and allows setting a window size and a custom title for the terminal tab. To keep the terminals from overlapping on each other, we keep 5px margin.

AppleScript is used to control the Terminal application on macOS.

## Screen

The Screen module provides a method to retrieve the current screen resolution on macOS systems. Utilizing the AppKit framework, it captures and returns the main screen's width and height in pixels.

## Chat

A simple, singleton-based chat interface built with [tkinter](https://docs.python.org/3/library/tkinter.html). It utilizes a message queue for communicating between components and provides a neat GUI for user interaction.

- Singleton Design Pattern: Ensures only one instance of the chat application runs.
- Multithreaded Message Queue Support: Allows sending messages to be queued and processed asynchronously.
- Used in Sirji's main process to take problem statement and feedback on the solution from the user.
