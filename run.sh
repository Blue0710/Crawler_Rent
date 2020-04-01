#!/usr/bin/env bash

git checkout master; git pull --rebase
pipenv install
pipenv run python -m bin.main -r all \
  2> >(tee -a ./log/run.sh.log)
