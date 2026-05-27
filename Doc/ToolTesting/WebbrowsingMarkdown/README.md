# URI Range Opener for code-server

Open markdown files with range selection via URL in code-server.

## Quick Start

```bash
docker run -d \
  -v /path/to/workspace:/config \
  -p 8443:8443 \
  lscr.io/linuxserver/code-server:latest
```

Install the extension (in code-server terminal):

```bash
code-server --install-extension /config/my-ext/uri-opener/uri-opener-0.0.1.vsix
```

Reload window (Command Palette → "Developer: Reload Window").

## URI Format

```text
http://127.0.0.1:8443/?folder=/config#sel=<file>:<sl>:<sc>:<el>:<ec>
```

| Parameter | Description                              |
| --------- | ---------------------------------------- |
| `file`    | Absolute path to file (inside container) |
| `sl`      | Start line (1-indexed)                   |
| `sc`      | Start column (1-indexed)                 |
| `el`      | End line (1-indexed)                     |
| `ec`      | End column (1-indexed)                   |

## Examples

Select lines 7-10 in sample.md:

```text
http://127.0.0.1:8443/?folder=/config#sel=/config/sample.md:7:1:10:50
```

Select lines 1-5 in a subdirectory file:

```text
http://127.0.0.1:8443/?folder=/config#sel=/config/docs/readme.md:1:1:5:20
```

## How It Works

The extension creates a temporary webview on activation that reads the URL hash fragment (`#sel=...`), parses the selection parameters, and opens the file with the specified range highlighted.
When modify `extension.js` or `package.json`, the extension need to be rebuild with

```bash
cd workspace/my-ext/uri-opener
npx @vscode/vsce package --allow-missing-repository
```
