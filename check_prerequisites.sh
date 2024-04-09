#!/bin/bash

# Function to compare versions
version_gte() { test "$(printf '%s\n' "$@" | sort -V | head -n 1)" != "$1"; }

# Initial error message
errorMsg=""

# Check Visual Studio Code version
vscode_version=$(code --version | head -n 1)
required_vscode_version="1.80.2"
if ! command -v code &> /dev/null || ! version_gte "$vscode_version" "$required_vscode_version"; then
    errorMsg+="Visual Studio Code version >= 1.80.2 is required. Current version: $vscode_version\n"
fi

# Check Node.js version
node_version=$(node --version | cut -d 'v' -f 2)
required_node_version="18"
if ! command -v node &> /dev/null || ! version_gte "$node_version" "$required_node_version"; then
    errorMsg+="Node.js version >= 18 is required. Current version: $node_version\n"
fi

# Check NPM version
npm_version=$(npm --version)
required_npm_version="8.19"
if ! command -v npm &> /dev/null || ! version_gte "$npm_version" "$required_npm_version"; then
    errorMsg+="npm version >= 8.19 is required. Current version: $npm_version\n"
fi

# Check Python version
python_version=$(python3 --version 2>&1 | sed 's/Python //g')
required_python_version="3.10"
if ! command -v python3 &> /dev/null || ! version_gte "$python_version" "$required_python_version"; then
    errorMsg+="Python version >= 3.10 is required. Current version: $python_version\n"
fi

# Check if tee command is available
if ! command -v tee &> /dev/null; then
    errorMsg+="tee command is not available or not in PATH.\n"
fi

# Display error messages if any prerequisites are missing
if [[ -n $errorMsg ]]; then
    echo -e "Some prerequisites are missing or don't meet the version requirements:\n"
    echo -e "$errorMsg"
    exit 1
else
    echo "All prerequisites are met."
fi