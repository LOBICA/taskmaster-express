#!/usr/bin/env bash

set -e
docker build --platform linux/amd64 -t help-it-done-api .
docker tag help-it-done-api registry.heroku.com/help-it-done-api/web
docker push registry.heroku.com/help-it-done-api/web
heroku container:release web -a help-it-done-api
