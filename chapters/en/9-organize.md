# Chapter 9: Organizing your code

The application's features are complete, but keeping everything in app.py will make development and maintenance harder as it grows. In this chapter, we will refactor the project into a more practical structure.

Flask does not impose a project layout. You can use a single script or a package. We will organize the application as a package, use blueprints to separate its features, and introduce a factory function to create application instances.

Here is the project's current structure:

```
watchlist/
├── .flaskenv
├── app.py
├── test_watchlist.py
├── static
│   ├── favicon.ico
│   ├── images
│   │   ├── avatar.png
│   │   └── totoro.gif
│   └── style.css
└── templates
    ├── 400.html
    ├── 404.html
    ├── 500.html
    ├── base.html
    ├── edit.html
    ├── index.html
    ├── login.html
    └── settings.html
```

## Organize the application with blueprints

A [blueprint](https://flask.palletsprojects.com/blueprints/) is somewhat like a sub-application. Until now, we have registered every view and error handler on the application instance, `app`. Blueprints let us group related functionality: create a blueprint for each group and register its views on that blueprint. Blueprints can have their own URL prefixes, error handlers, template and static folders, and more.

Create two blueprints: `main` for the application's main features, and `auth` for authentication:

```python
from flask import Flask, Blueprint

app = Flask(__name__)
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
```

Change each view's decorator from `app.route` to its blueprint's `route` decorator, such as `main_bp.route`. Register the views with the appropriate blueprint:

```python
@main_bp.route('/', methods=['GET', 'POST'])
def index():
    ...

@main_bp.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required
def edit(movie_id):
    ...


@main_bp.route('/movie/delete/<int:movie_id>', methods=['POST'])
@login_required
def delete(movie_id):
    ...


@main_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    ...

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    ...


@auth_bp.route('/logout')
@login_required
def logout():
    ...
```

Finally, register the blueprints on the application with `app.register_blueprint`:

```python
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
```

Place these calls after the view definitions so that all the views have been recorded on their blueprints before registration.

Blueprints also change endpoint names. Update the first argument of each `url_for()` call to include the blueprint name: `blueprint_name.view_function_name`. For example:

```python
url_for('index')
```

becomes:

```python
url_for('main.index')
```

Use your editor's project-wide search to find every `url_for` call, including those in templates, and update them.

> **Tip** Blueprints can be nested: register a child blueprint on another blueprint. They also provide additional methods and attributes; see the [blueprint API documentation](https://flask.palletsprojects.com/en/stable/api/#blueprint-objects).

## Create an application factory

Our script currently creates `app`, loads configuration, and initializes extensions as soon as it runs. This makes it hard to customize application creation for different situations.

A more flexible approach is to put the creation steps inside a function and choose configuration based on its arguments. This is the *application factory* pattern, and the function is called an [application factory](https://flask.palletsprojects.com/patterns/appfactories/).

The factory creates the application, initializes extensions, registers blueprints and handlers, and returns the configured instance. It can accept a configuration name and load the corresponding file or object. For example, tests can call it to create an application with testing settings.

Here is a minimal factory:

```python
from flask import Flask

def create_app():
    app = Flask(__name__)  # Create the application instance
    return app  # Return the application instance
```

> **Tip** By convention, application factories are named `create_app` or `make_app`.

One immediate benefit is the ability to create applications with different configurations. Define classes for development, testing, and production:

```python
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SQLITE_PREFIX = 'sqlite:///' if sys.platform.startswith('win') else 'sqlite:////'


class BaseConfig:  # Base configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')


class DevelopmentConfig(BaseConfig):  # Development configuration
    SQLALCHEMY_DATABASE_URI = SQLITE_PREFIX + str(BASE_DIR / 'data-dev.db').lstrip('/')


class TestingConfig(BaseConfig):  # Testing configuration
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):  # Production configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', SQLITE_PREFIX + str(BASE_DIR / 'data.db').lstrip('/'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
```

The `config` dictionary maps names to configuration classes so the factory can look them up.

Each environment uses a different database URI. For flexibility, some settings first check an environment variable and fall back to a default if it is absent:

```python
SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
```

Here, `os.getenv('SECRET_KEY', 'dev')` reads `SECRET_KEY` from the environment, defaulting to `dev` if it is not set.

> **Important** Keep sensitive settings such as secret keys in environment variables rather than directly in source code.

The updated factory accepts a configuration name, defaulting to `development`. It looks up the class and loads it with `app.config.from_object()`. Move blueprint registration, extension initialization, context processors, error handlers, and custom commands into the factory:

```python
from flask import Flask, current_app

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Context processor
    @app.context_processor
    def inject_user():  # You can choose any function name
        user = db.session.execute(select(User)).scalar()
        return dict(user=user, current_app=current_app)

    # Error handlers
    ...

    # Custom commands
    ...

    return app
```

Other parts of the application need access to the extension objects, so create them outside the factory. Extensions support this pattern through `init_app()`, which separates creating an extension object from attaching it to an application:

```python
# Create extension objects without passing an application instance
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def create_app(config_name='development'):

	# Initialize extensions inside the factory with init_app(app)
	db.init_app(app)
	login_manager.init_app(app)

	return app
```

There is another consequence: we no longer have a global `app` instance available while defining configuration. Build the database path from the current file instead of `app.root_path`:

```python
BASE_DIR = Path(__file__).resolve().parent
```

Elsewhere, use Flask's `current_app` proxy to access the active application. Like Flask-Login's `current_user`, it forwards access to the current object. The application only exists after the factory is called, so access the proxy inside a view, command, or another function running with an application context:

```python
from flask import current_app

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    current_app.logger.debug('Visited index page')
    # ...
```

The context processor above also makes `current_app` available in templates:

```jinja
<p>Debug Mode: {{ current_app.config['DEBUG'] }}</p>
```

The `flask run` command also discovers factories automatically. It looks in app.py or wsgi.py for a function named `create_app` or `make_app` and calls it. Since our factory is still in app.py, we can keep using:

```shell
(.venv) $ flask run
```

You can also identify the factory explicitly with `--app` or the `FLASK_APP` environment variable:

```
FLASK_APP=hello:create_app
```

Arguments can be included too:

```
FLASK_APP=hello:create_app(config_name='development')
```

## Organize code in a package

As app.py grows, finding particular parts becomes harder. Create a package and move the code into modules grouped by purpose. Run these commands, or perform the equivalent operations in a file manager or editor:

```bash
$ mkdir watchlist  # Create the package directory
$ mv static templates watchlist  # Move static and templates into watchlist
$ cd watchlist  # Enter the package directory
$ touch __init__.py errors.py models.py commands.py settings.py extensions.py # Create the modules
$ mkdir blueprints  # Create the blueprints directory
$ touch blueprints/auth.py blueprints/main.py  # Create the blueprint modules
```

This is our *application package*. Its modules have the following roles:

| Module | Purpose |
| --- | --- |
| \_\_init\_\_.py | Package initializer containing the application factory |
| settings.py | Application configuration |
| errors.py | Error handlers |
| models.py | Model classes |
| commands.py | Command functions |
| extensions.py | Extension setup |
| blueprints/\_\_init\_\_.py | Empty initializer for the blueprints subpackage |
| blueprints/main.py | The main blueprint and its views |
| blueprints/auth.py | The auth blueprint and its views |

> **Tip** Apart from package initializers, you can choose different module names. For example, settings.py could be called config.py.

Put the factory in the package initializer, `__init__.py`:

*watchlist/\_\_init\_\_.py: the application factory*

```python
from flask import Flask, current_app
from sqlalchemy import select

from watchlist.extensions import db, login_manager
from watchlist.blueprints.main import main_bp
from watchlist.blueprints.auth import auth_bp
from watchlist.models import User
from watchlist.errors import register_errors
from watchlist.commands import register_commands
from watchlist.settings import config


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Register blueprints
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    # Register error handlers and commands
    register_errors(app)
    register_commands(app)

    # Register a context processor
    @app.context_processor
    def inject_user():  # You can choose any function name
        user = db.session.execute(select(User)).scalar()
        return dict(user=user, current_app=current_app)

    return app
```

Create extension objects and configure them in extensions.py:

*watchlist/extensions.py: extension setup*

```python
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
	from watchlist.models import User
	user = db.session.get(User, int(user_id))
	return user

login_manager.login_view = 'auth.login'
```

models.py imports `db` from extensions.py. To avoid a circular import, the user loader imports `User` inside the function.

Putting all error handlers and commands inside the factory would make it too long, so move them into separate modules as well. For error handlers, define a wrapping function, `register_errors()`, that accepts the application:

*watchlist/errors.py: error handlers*

```python
from flask import render_template


def register_errors(app):

	@app.errorhandler(400)
	def bad_request(e):
	    return render_template('errors/400.html'), 400


	@app.errorhandler(404)
	def page_not_found(e):
	    return render_template('errors/404.html'), 404


	@app.errorhandler(500)
	def internal_server_error(e):
	    return render_template('errors/500.html'), 500
```

Import and call it inside the factory to register the handlers:

```python
from watchlist.errors import register_errors


def create_app(config_name='development'):
    app = Flask(__name__)

    register_errors(app)

    return app
```

Create a module for each blueprint in the blueprints subpackage. Remember to create its `__init__.py` file too. For example, auth.py contains the auth blueprint and its views:

*watchlist/blueprints/auth.py: the authentication blueprint*

```python
from flask import Blueprint

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    ...


@auth_bp.route('/logout')
@login_required
def logout():
    ...
```

Move the remaining code into the appropriate modules. We will not repeat it all here; consult the [source repository](https://github.com/helloflask/watchlist) as needed. Update imports after moving code. To import the factory, use:

```python
from watchlist import create_app
```

Import models and extension objects like this:

```python
from watchlist.models import User, Movie
from watchlist.extensions import db
```

The same principle applies to the other modules.

Our package is named watchlist, so imports begin with `watchlist`. If you choose another name, such as app, change the imports accordingly:

```python
from app import app, db
from app.models import User, Movie
```

Since settings.py is now inside the package, add another `.parent` to `BASE_DIR` to keep locating database files in the project root:

```python
BASE_DIR = Path(__file__).resolve().parent.parent
```

## Organize templates

The templates directory contains several files. Subfolders can make them easier to manage. Create an errors directory and move the error templates into it, using these commands or your file manager:

```bash
$ cd templates  # Enter the templates directory
$ mkdir errors  # Create the errors directory
$ mv 400.html 404.html 500.html errors  # Move error templates into errors
```

Update all three error handlers to use the new template paths. For example:

```python
@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400
```

## Start the application

The factory is now in a package rather than the automatically discovered app.py. Set `FLASK_APP` before starting the development server. Because the factory is in `watchlist/__init__.py`, the package name is enough. Flask discovers and calls the factory, using its default `config_name='development'`. Add this line to .flaskenv:

```
FLASK_APP=watchlist
```

For a more explicit entry point, you can also create app.py in the project root:

```python
from watchlist import create_app

app = create_app(config_name='development')
```

The final structure is:

```
watchlist
├── .flaskenv
├── app.py  # Optional entry-point script
└── watchlist  # Application package
    ├── __init__.py
    ├── commands.py
    ├── errors.py
    ├── models.py
    ├── settings.py
	├── extensions.py
    ├── blueprints
	│   ├── __init__.py
    │   ├── main.py
    │   └── auth.py
    ├── static
    │   ├── favicon.ico
    │   ├── images
    │   │   ├── avatar.png
    │   │   └── totoro.gif
    │   └── style.css
    └── templates
        ├── base.html
        ├── edit.html
        ├── errors
        │   ├── 400.html
        │   ├── 404.html
        │   └── 500.html
        ├── index.html
        ├── login.html
        └── settings.html
```

## Chapter summary

Small applications and one-off projects may not need blueprints or factories. For applications that will grow, these techniques prepare the code for long-term development and maintenance. Before we finish, commit the changes:

```bash
$ git add .
$ git commit -m "Organize application with package and blueprint"
$ git push
```

## Going further

- Explore the [Greybook source code](https://github.com/greyli/greybook), the example application for 《Flask 从入门到进阶》 (Flask: From Beginner to Advanced), to see how a larger application is organized.
