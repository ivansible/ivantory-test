#!/bin/bash
reinstall=0
pythonver=python3
set -x
sudo apt-get -qy install \
  build-essential virtualenv\
  ${pythonver} ${pythonver}-dev ${pythonver}-virtualenv \
  graphviz imagemagick \
  x11-apps xauth
test $reinstall=1 && rm -rf .venv/*
test -x .venv/bin/activate || virtualenv -p ${pythonver} .venv
set +x
. .venv/bin/activate
set -x
pip install -U pip setuptools wheel
pip install -r requirements.txt