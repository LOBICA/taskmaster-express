#!/usr/bin/env bash

set -e
docker build --platform linux/amd64 --build-arg="ENV=test" -t help-it-done-web .
docker tag help-it-done-web registry.heroku.com/help-it-done-test-web/web
docker push registry.heroku.com/help-it-done-test-web/web
heroku container:release web -a help-it-done-test-web
