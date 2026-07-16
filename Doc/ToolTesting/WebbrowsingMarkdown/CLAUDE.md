# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Objective

Browser-only client, code-server Docker server setup that opens markdown files at a specific line/column range via URL hash fragment. The VS Code extension (`DockerContext/my-ext/uri-opener/`) handles the URI parsing and file-open-with-selection logic.

## Key Commands

```bash
# Build Docker image
docker build -t jejuneness:code-server-uri-opener DockerContext/

# Run container
docker run -d -p 8443:8443 jejuneness:code-server-uri-opener

# Run with persistent data
docker run -d -v /path/to/data:/config -p 8443:8443 jejuneness:code-server-uri-opener

# Rebuild extension VSIX (only when extension.js or package.json changed)
cd DockerContext/my-ext/uri-opener
npx @vscode/vsce package --allow-missing-repository

# Clean generated files
git clean -Xdf
```

## URI Format

```text
http://127.0.0.1:8443/?folder=/config#sel=<file>:<sl>:<sc>:<el>:<ec>[&solo]
```

Parameters: `file` (absolute path inside container), `sl`/`sc` (start line/col, 1-indexed), `el`/`ec` (end line/col, 1-indexed), `&solo` (close all other tabs).

## Architecture

**Docker multi-stage build** (`DockerContext/Dockerfile`):

1. Stage 1 (`node:20-slim`): packages the extension via `vsce`, unzips the VSIX.
2. Stage 2 (`lscr.io/linuxserver/code-server:latest`): copies unpacked extension into `/config/extensions/local.uri-opener-0.0.1/` — code-server picks it up as a workspace-local extension without registry registration.

**Extension** (`DockerContext/my-ext/uri-opener/extension.js`): activates on `onStartupFinished`, creates a hidden webview that reads `window.location.hash` (and `window.top.location.hash`), posts the parsed `#sel=...` fragment back to the extension host, which calls `showTextDocument` with a `Selection`. Also registers a `uri-opener.openRange` command and a `vscode://` URI handler as alternative entry points.

**No `devcontainer.json`** is used; the extension is installed at a fixed path that code-server auto-discovers.
