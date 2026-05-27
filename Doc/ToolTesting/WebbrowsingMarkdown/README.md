# URI Range Opener for code-server

Display markdown files in an editor like fashion (with range selection on opening). Based on [docker based containerization](https://hub.docker.com/r/linuxserver/code-server) of the [code-server (aka coder)](https://coder.com/) (VS Code running on a remote server, accessible through the browser).

## Quick Start

```bash
docker run -d -v /path/to/workspace:/config -p 8443:8443 lscr.io/linuxserver/code-server:latest
```

## Usage examples

Open `sample.md` with lines 7-10 selected/highlighted:

```text
http://127.0.0.1:8443/?folder=/config#sel=/config/sample.md:7:1:10:50
```

Open `samples/another-sample.md` with lines 14-16 selected:

```text
http://127.0.0.1:8443/?folder=/config#sel=/config/samples/another-sample.md:14:1:16:60
```

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

## Testing things a bit more deeply

Make sure that all generated files are properly out of the way by removing them with

```bash
git clean -Xdf
```

## How It Works

The extension creates a temporary webview on activation that reads the URL hash fragment (`#sel=...`), parses the selection parameters, and opens the file with the specified range highlighted.

## Rebuilding the Extension

Only needed when modifying `extension.js` or `package.json`:

```bash
cd workspace/my-ext/uri-opener
npx @vscode/vsce package --allow-missing-repository
```
