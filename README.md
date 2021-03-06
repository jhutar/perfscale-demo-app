My Perf&Scale demo app
======================

Demo application to show some concept of perf&scale work on microservices.

Usage
-----


Developing
----------

Start DB:

    podman run -d --name postgresql_database -e POSTGRESQL_USER=user -e POSTGRESQL_PASSWORD=pass -e POSTGRESQL_DATABASE=db -p 5432:5432 quay.io/centos7/postgresql-13-centos7

Setup terminal environment with what you need to run the app:

    python -m venv venv
    source venv/bin/activate
    pip install -U pip
    pip install -r requirements.txt
    export FLASK_APP=myapp.py
    export FLASK_ENV=development
    export POSTGRESQL_HOST=localhost
    export POSTGRESQL_PORT=5432
    export POSTGRESQL_USER=user
    export POSTGRESQL_PASSWORD=pass
    export POSTGRESQL_DATABASE=db

Initialize DB and create some testing data:

    flask db upgrade
    flask test-data

And finally this will get you the server running on `http://127.0.0.1:5000/`:

    flask run

Handy command to look into the DB:

    PGPASSWORD=$POSTGRESQL_PASSWORD psql --host=$POSTGRESQL_HOST --username=$POSTGRESQL_USER --port=$POSTGRESQL_PORT $POSTGRESQL_DATABASE


Build image
-----------

Image should be available form quay.io repo:

    podman pull quay.io/rhcloudperfscale/perfscale-demo-app

BUt if you want to build the image locally from git repo:

    sudo podman build -t perfscale-demo-app .

And to run it:

    podman run --rm -ti -p 5000:5000 perfscale-demo-app


Testing
-------

To test basic functionality, ensure you do not have some server listening
on port 5000 and run:

    ./tests.sh

To run API perf-test:

    locust --locustfile testing.py --headless --users 1 --spawn-rate 1 -H http://localhost:5000 --run-time 3 --print-stats --only-summary

Or when deployed in OCP:

    locust --locustfile testing.py --headless --users 10 --spawn-rate 10 -H http://perfscale-demo-service.perfscale-demo-app.svc --run-time 3 --print-stats --only-summary
