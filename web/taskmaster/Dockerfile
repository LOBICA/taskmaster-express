FROM node:20.14 AS base

WORKDIR /usr/src/app
RUN npm install -g @angular/cli

FROM base AS req

COPY package.json .
COPY package-lock.json .
RUN npm install

FROM req AS code
COPY . .

FROM code AS dev

FROM code as build
ARG ENV=production
RUN ng build --configuration $ENV

FROM node:20.14-slim as prod
WORKDIR /usr/src/app
RUN npm install -g http-server

COPY --from=build /usr/src/app/dist/taskmaster/browser .
CMD ["sh", "-c", "http-server -p $PORT -d false --proxy http://localhost:$PORT?"]
