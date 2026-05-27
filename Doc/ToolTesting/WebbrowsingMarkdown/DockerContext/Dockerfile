# Stage 1: Build extension with modern Node.js
FROM node:20-slim AS builder

WORKDIR /build
COPY my-ext/uri-opener/ .

RUN npm install -g @vscode/vsce
RUN vsce package --allow-missing-repository

RUN apt-get update && apt-get install -y unzip
RUN mkdir -p /ext
RUN unzip -o uri-opener-0.0.1.vsix -d /tmp/vsix
RUN cp -r /tmp/vsix/extension/* /ext/

# Stage 2: Final image
FROM lscr.io/linuxserver/code-server:latest

COPY --from=builder /ext/ /config/extensions/local.uri-opener-0.0.1/

COPY sample.md /config/
COPY samples/ /config/samples/

WORKDIR /config
