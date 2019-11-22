#!/usr/bin/env bash
rsync -r --exclude=.git /home/telegram/test/pi-json-api/ everdrone@a1708.local:/Users/everdrone/projects/github/pi-json-api
