#!/bin/sh

set -xe

if ! [ -d venv ]; then
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    deactivate
fi

source venv/bin/activate
export FLASK_APP=myapp.py
flask run &>/tmp/myapp.log &
pid=$!
trap "kill $pid" EXIT
sleep 1


echo "SUCCESS"
