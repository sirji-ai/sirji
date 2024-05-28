#!/bin/sh

# Get the current user's username
current_user=$(whoami)

# Define the path using the current user's username
base_path="/Users/${current_user}/Library/Application Support/Code/User/globalStorage/truesparrow.sirji/Sirji"

# Open the base path directory in VS Code
code "${base_path}"