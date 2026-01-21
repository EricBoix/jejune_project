FROM ubuntu:noble

RUN apt-get update

### Install npm to build neovis.js and to http-serve the result
ENV NODE_VERSION=16.13.0
RUN apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version

### Build neovis.js
RUN apt-get install -y git
RUN git --version
RUN git clone https://github.com/neo4j-contrib/neovis.js.git
COPY ./index.html /neovis.js/index.html
WORKDIR "/neovis.js"
RUN npm install
RUN npm run build

### Eventually serve it through http
RUN npm install -g http-server
EXPOSE 8080 80
CMD ["http-server", "./", "--proxy", "http://localhost:8080?"]