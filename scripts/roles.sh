#!/bin/sh
set -x
rm -rf roles-galaxy/*
ansible-galaxy install -r roles-import.yml -p roles-galaxy -f
