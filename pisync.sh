#!/usr/bin/env bash
rsync -r --exclude=.git /Users/everdrone/projects/github/pi-json-api/ telegram@n4s:/home/telegram/test/pi-json-api
