# Claude instructions

## The objective

We have at hand a set of markdown files that we wish to browse with the help of

- a web-browser as only tool on the client side
- code-server packaged within an open source Docker container on the server side

We want to allow a user to access and browse those markdown based texts with an URI support

- with an IDE reader like experience (although edition might not possible, just browsing)
- allowing URI referencing that is refer to a specific position within the text with an URL (relative to the docker/Kubernetes deployment)
- allowing the cursor positioning down to the line and column
- allowing the a prescribed range to be selected (maybe with a character based range the way the open-with-selection extension does it)

## Hints

- URI using `&payload=[["gotoLineMode","true"],["openFile","vscode-remote:///config/2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1_-_local_converter.md:100:50"]]` work natively. Only the range is missing.
- Write a tiny ~50 lines extension that registers parser UriHandler, parser an URI of the form `<file>:sl=10:sc=1:el=12:ec=8` an calls e.g. `showTextDocument(uri, { selection })`
- The best pattern is to use “workspace-local extension” (as opposed to cleanly registering the extension on VSX registry) that is locating the extension code in the repository in example `.vscode/extension/uri-opener` subdirectory (with an `extension.js` and a `package.json` files)
- Possibly combine the above with devcontainer.json
- Note that open-with-selection extension is not available on VSX registry
- Place all this content in @/Doc/ToolTesting/WebbrowsingMarkdown/workspace subdirectory


## Constraints

Only the files located in @/Doc/ToolTesting/WebbrowsingMarkdown directory must be used as context. Exclude all other files of the git repository.
