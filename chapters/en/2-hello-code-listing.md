# Chapter 2: Code listing

## Directory structure

```text
watchlist/
├── app.py
├── .env
├── .flaskenv
└── .gitignore
```

> **Tip** The .venv and .git directories are omitted from this listing.
## Code

### app.py

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'
```

### .gitignore

```diff
*.pyc
*~
__pycache__
.DS_Store
.venv
+.env
```

## Commands

### Activate the virtual environment

```bash
$ .venv\Scripts\activate  # Windows
```

Or:

```bash
$ source .venv/bin/activate  # Linux or macOS
```

> **Tip** Activate the virtual environment before running commands such as `flask`, `python`, and `pip`. Later chapters do not repeat the activation commands.

### Run the application

Use the default command:

```bash
(.venv) $ flask run
```

Run in debug mode:

```bash
(.venv) $ flask run --debug
```

Use a different port:

```bash
(.venv) $ flask run --debug --port 8000
```

### Install python-dotenv

```bash
(.venv) $ pip install python-dotenv
```

### Create the .env and .flaskenv files

```bash
$ touch .env .flaskenv
```

### Commit the code

```bash
$ git add .
$ git commit -m "Add a minimal home page"
$ git push
```
