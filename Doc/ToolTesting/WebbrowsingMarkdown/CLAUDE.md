# Claude instructions

## The objective

We have at hand a set of markdown files that we wish to browse with the help of

- a web-browser as only tool on the client side
- docker server and a set of open source Docker containers on the server side

We want to allow a user to access and browse those markdown based texts

- with an IDE reader like experience (although edition is not possible, just browsing)
- allowing URL referencing that is refer to a specific position within the text with an URL (relative to the docker/Kubernetes deployment)
- allowing the cursor positioning down to the line or even character
- allowing the display of a selected section (maybe with a character interval)

## Constraints

Only the files located in @/Doc/ToolTesting/WebbrowsingMarkdown directory must be used as context. Exclude all other files of the git repository.
