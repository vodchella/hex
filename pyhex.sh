#!/usr/bin/env bash

ROOT_PATH=$(cd $(dirname $0) && pwd);
cd $ROOT_PATH || exit

source ./.venv/bin/activate
python3 pyhex.py