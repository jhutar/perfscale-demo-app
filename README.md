My Perf&Scale demo app
======================

Demo application to show some concept of perf&scale work on microservices.

Usage
-----


Developing
----------

This will get you the server running on `http://127.0.0.1:5000/`:

    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    export FLASK_APP=myapp.py
    export FLASK_ENV=development
    flask run


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

Ensure you do not have some server running on port 5000 and run:

    ./tests.sh
