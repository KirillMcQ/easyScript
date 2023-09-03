#!/bin/bash

# Define the installation directory
INSTALL_DIR="$HOME/easyScript"

# Create the installation directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Download parse.py from your repository and rename it to easyScript
curl -L -o "$INSTALL_DIR/easyScript" https://raw.githubusercontent.com/KirillMcQ/easyScript/master/parse.py

# Define and Create the helper directory
HELPER_DIR="$INSTALL_DIR/helpers"
mkdir -p "$HELPER_DIR"

# Download checkers.py and place it in the helper directory
curl -L -o "$HELPER_DIR/checkers.py" https://raw.githubusercontent.com/KirillMcQ/easyScript/master/helpers/checkers.py

# Make easyScript executable
chmod +x "$INSTALL_DIR/easyScript"

# Add the installation directory to the user's PATH if not already added
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
  echo 'export PATH="$HOME/easyScript:$PATH"' >> "$HOME/.bashrc"
  source "$HOME/.bashrc"
fi

# Add the helper directory to Python's sys.path
echo 'import sys' >> "$HOME/.bashrc"
echo "sys.path.append('$HELPER_DIR')" >> "$HOME/.bashrc"

echo "easyScript is now installed. You can run it using 'easyScript'."
