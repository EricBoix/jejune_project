# Web browsing markdown files<!-- omit in toc -->

- [The use case](#the-use-case)
- [Evaluated solutions](#evaluated-solutions)
  - [The VSCode way](#the-vscode-way)
    - [Distinguishing vscode-server from code-server](#distinguishing-vscode-server-from-code-server)
    - [Using code-server](#using-code-server)
  - [Using the Monaco editor as component](#using-the-monaco-editor-as-component)
  - [Converting to html using Mkdocs](#converting-to-html-using-mkdocs)

## The use case

Note: in the following use case, there is a strong dependency towards the notions of [reference](../Needs/CitationsAndReferences/Readme.md). The resulting design/choice for the reference system technically constrains the design answering this use case.

With the help of

- a web-browser as only tool on the client side
- docker server and a set of open source Docker containers on the server side

allow a user to access and browse some markdown based texts

- with an IDE like experience (although edition is not possible, just browsing) like text highlighting, searching for a string, displacing a cursor...
- allow URL referencing that is refer to a specific position within the text with an URL (relative to the docker/Kubernetes deployment)
- allowing the cursor positioning down to the character
- allowing the display of a selected section (maybe with a character interval)

## Evaluated solutions

### The VSCode way

VSCode has native markdown support with

- markdown preview
- programmatic cursor positioning (open a markdown file a place the cursor at a given position) since after a searching a string in a set of files one can access to the selected occurrence with a mouse-click (and the markdown editor will show up with the cursor properly set at the string occurrence).
- many additional extensions for markdown files

And, since VSCode is built with web technologies (JavaScript, HTML, CSS, electron), there exist some VS Code servers with web browsing access (refer below). If we thus have the required functionality when running vscode in desktop mode we can thus hope for the same functionality to be allowed through a web browser.

#### Distinguishing vscode-server from code-server

There is a bit of confusion between

- [vscode-server (Visual Studio Code Server)](https://code.visualstudio.com/docs/remote/vscode-server) that
  - is **a service you can run on a remote development machine [...] that allows you to securely connect to that remote machine from anywhere through a local VS Code client**
  - is developed by [Microsoft](https://code.visualstudio.com/docs/remote/vscode-server)
  - typical use case is "I use a vscode IDE instance on my desktop and I wish to debug code running inside a Docker Container"

and online editors (accessed with a web-browser)

- [code-server](https://github.com/coder/code-server) that
  - allows you to **run VS Code on any machine anywhere and access it in the browser**,
  - is developed by the [CODER company](https://coder.com/)
  - typical use case is "I have a web browser (on my desktop, smartphone, webTV) and I want to develop with the vscode IDE some code hosted else where (e.g. on github)"
- [vscode.dev (Visual Studio Code for the Web)](https://vscode.dev/)
  - is browser-based version of the (VSCode) editor that can be used to edit both local files and remote repositories
  - is developed by [MicroSoft](https://en.wikipedia.org/wiki/Visual_Studio_Code) and hosted by Microsoft

In summary, `vscode.dev` server is hosted by Microsoft while one can deploy `code-server` on premisses.
Yet they are some restrictions (the devil is the details) when using `code-server`, like [**not** having access to Microsoft's extension marketplace](https://coder.com/docs/code-server/FAQ#why-cant-code-server-use-microsofts-extension-marketplace).

#### Using code-server

Because we want to have a server on premisses, our only choice is to go for code-server`. [vscode.dev (Visual Studio Code for the Web)](https://vscode.dev/) does provide the ability to [open a file directly using an URL (with line number)](https://github.com/coder/code-server/issues/1964#issuecomment-1546098145).
But it looks like [code-server does **not** allow to set folder on Open](https://github.com/coder/code-server/issues/816) which is even more restrictive that allowing for a file in a folder and providing a line-number for the prompt. Assert on this !

- URL to open a file at some specified line:
  - Use e.g. `http://127.0.0.1:8443/?folder=/config&payload=[[%22gotoLineMode%22,%22true%22],[%22openFile%22,%22vscode-remote:///config/2019_-_Sayadaw-U-Tejaniya-Collecting-Gold-Dust-Web-Book-1_-_local_converter.md:100:40%22]]`
  - Refer to [this issue](https://github.com/coder/code-server/issues/1964#issuecomment-2455939740)
  - Preloading extensions (only works for VSZX registry): https://open-vsx.org/extension/lostintangent/workspace-layout

### Using the Monaco editor as component

As Claude states it this solution has "Best IDE fidelity, char-level URLs trivial, lightest Docker".

Monaco is the [editor behind vscode](https://microsoft.github.io/monaco-editor/)

Refer to [this sandbox](https://levelup.gitconnected.com/how-to-build-a-web-ide-ab2563f24647) for a small integrated playground demo.

### Converting to html using Mkdocs

- Convert markdown files to html
- Convert line-number based references to html anchors
- Have a system of [citation](https://en.wikipedia.org/wiki/Citation#Concept) allowing for multiple representations
  - an ISBN with some text based, chapter and page number,
  - an URL to some html anchor (the server/host should be set aside)
  - an [URL with payload including a line number)](https://github.com/coder/code-server/issues/1964#issuecomment-1546098145) (ditto for the server/host reference)
