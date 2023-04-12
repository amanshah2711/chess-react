# How to use this repository


## 1) Set Up Dependencies

### `yarn install && pip install -r requirements.txt`

This command installs the necessary dependencies for Python and Node.

## 2) Running Locally

### `python server.py runserver`

This command runs a WSGI server on localhost port.

### `gunicorn --worker-class eventlet -w 1 chess_gui:app`

This command runs a local development server using Gunicorn which is suitable for deployment.

## 3)Hosting

Many different hosting options exist although we opted to use [render](https://render.com) primarily because it was free and easy to set up.
We used the aforementioned commands regarding dependencies and Gunicorn for the build and start commands respectively.