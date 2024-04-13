# How to use this repository


## 1) Set Up Dependencies

### `yarn install && pip install -r requirements.txt`

This command installs the necessary dependencies for Node and Python, respectively.

## 2) Running Locally

### `python server.py runserver`

This command runs a WSGI server on localhost port.

### `gunicorn --worker-class eventlet -w 1 chess_gui:app`

This command runs a local development server using Gunicorn which is suitable for deployment.

## 3) Testing

### `python -m doctest -v tests/move_generation.py`

This command runs the tests used to verify that this chess engine faithfully implements the rules. To test that chess rules are implemented appropriately we compare the number of possible moves our engine generates to known values. In particular testing is done in the *tests/move_generation.py* file and the reference values are given by the [chess programming wiki](https://www.chessprogramming.org/Perft_Results). Running the tests can take quite as there are many possible moves if the engine is allowed to look far enough ahead.


## 4) Hosting

Many different hosting options exist although we opted to use [render](https://render.com) primarily because it was free and easy to set up.
We used the aforementioned commands regarding dependencies and Gunicorn for the build and start commands respectively.