FROM node:20.14 AS base

WORKDIR /usr/src/app
RUN npm install -g @angular/cli

FROM base AS req

COPY package.json .
COPY package-lock.json .
RUN npm install

FROM req AS code
COPY . .

FROM code AS app
