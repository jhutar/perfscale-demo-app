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
export FLASK_ENV=production
export POSTGRESQL_HOST=localhost
export POSTGRESQL_PORT=5432
export POSTGRESQL_USER=user
export POSTGRESQL_PASSWORD=pass
export POSTGRESQL_DATABASE=db
flask run &>/tmp/myapp.log &
pid=$!
trap "kill $pid" EXIT
sleep 1

curl --silent -X GET http://127.0.0.1:5000/ | grep --quiet 'Hello world'
curl --silent -X GET http://127.0.0.1:5000/api/users | grep --quiet '{'
curl --silent -X GET http://127.0.0.1:5000/api/users?page=2 | grep --quiet '{'
curl --silent -X GET http://127.0.0.1:5000/api/users?page=-1 | grep --quiet '404 Not Found'
curl --silent -X GET http://127.0.0.1:5000/api/users?page=X | grep --quiet '500 Internal Server Error'
curl --silent -X GET http://127.0.0.1:5000/api/users/1 | grep --quiet '{'
curl --silent -X GET http://127.0.0.1:5000/api/users/XYZ | grep --quiet '404 Not Found'
curl --silent -X GET http://127.0.0.1:5000/api/moves | grep --quiet '{'
curl --silent -X GET http://127.0.0.1:5000/api/users/1 | grep --quiet '{'

echo "SUCCESS"
