#!/bin/bash

# Install uri-opener extension on container startup
EXTENSION_PATH="/config/my-ext/uri-opener/uri-opener-0.0.1.vsix"

if [ -f "$EXTENSION_PATH" ]; then
    echo "Installing uri-opener extension..."
    code-server --install-extension "$EXTENSION_PATH" --force
    echo "uri-opener extension installed."
else
    echo "Extension not found at $EXTENSION_PATH"
fi
