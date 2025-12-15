# Using web browse to a file served by VS code-server

## The use case

With the help of

- a web-browser as only tool on the client side
- docker server and a set of open source Docker containers on the server side

allow a user to access and browse some markdown based texts (down to line and character positioning)

- with an IDE like experience (although edition is not possible, just browsing)
- refer to text with an URL (relative to the docker/Kubernetes deployment)

## What is available

The is a bit of confusion between:

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
  - is developed by [MicroSoft](https://en.wikipedia.org/wiki/Visual_Studio_Code)
hosted by Microsoft and can be accessed  

Basically `vscode.dev` server is hosted by Microsoft while one can deploy `code-server` on premisses.
Yet they are some restrictions (the devil is the details) when using `code-server`, like [**not** having access to Microsoft's extension marketplace](https://coder.com/docs/code-server/FAQ#why-cant-code-server-use-microsofts-extension-marketplace).

## Using code-server

Because we want to have a server on premisses, our only choice is to go for code-server`. [vscode.dev (Visual Studio Code for the Web)](https://vscode.dev/) does provide the ability to [open a file directly using an URL (with line number)](https://github.com/coder/code-server/issues/1964#issuecomment-1546098145).
But it looks like [code-server does **not** allow to set folder on Open](https://github.com/coder/code-server/issues/816) which is even more restrictive that allowing for a file in a folder and providing a line-number for the prompt. Assert on this !

## What are the options ?

- Convert markdown files to html
- Convert line-number based references to html anchors
- Have a system of [citation](https://en.wikipedia.org/wiki/Citation#Concept) allowing for multiple representations
  - an ISBN with some text based, chapter and page number,
  - an URL to some html anchor (the server/host should be set aside)
  - a [URL with payload including a line number)](https://github.com/coder/code-server/issues/1964#issuecomment-1546098145) (ditto for the server/host reference)