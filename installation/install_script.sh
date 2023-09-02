#!/bin/bash

# Define the installation directory
INSTALL_DIR="$HOME/easyScript"

# Create the installation directory if it doesn't exist
mkdir -p "$INSTALL_DIR"

# Download parse.py from your repository and rename it to easyScript
curl -L -o "$INSTALL_DIR/easyScript" https://raw.githubusercontent.com/KirillMcQ/easyScript/master/parse.py

# Make easyScript executable
chmod +x "$INSTALL_DIR/easyScript"

# Add the installation directory to the user's PATH if not already added
if [[ ":$PATH:" != *":$INSTALL_DIR:"* ]]; then
  echo 'export PATH="$HOME/easyScript:$PATH"' >> "$HOME/.zshrc"
  source "$HOME/.zshrc"
fi

echo "easyScript is now installed. You can run it using 'easyScript'."
