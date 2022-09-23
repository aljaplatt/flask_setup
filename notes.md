1. create virtual environment - pipenv install, pipenv shell
//or python -m venv env
2. app0.py simple get started set up

3. set environment variable // app1.py = the name of the file where you set up flask

In terminal:
```
export FLASK_APP=app1.py
```
```
export FLASK_DEBUG=True  
X OLD - DO NOT USE export FLASK_ENV=development
```

- 'FLASK_ENV' is deprecated and will not be used in Flask 2.3. Use 'FLASK_DEBUG' instead.
