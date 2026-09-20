# Chapter 5: Databases

Most applications need to save data, so sooner or later you will need a database. There are many database management systems (DBMSs), and the best choice depends on the application and how it will be used. For this tutorial, we will use [SQLite](https://www.sqlite.org/), a relational database management system (RDBMS). SQLite stores data in a file and does not require a separate database server. It is useful during development and for applications with simple database operations and low traffic.

## Work with the database using SQLAlchemy

To simplify database operations, we will use [SQLAlchemy](https://www.sqlalchemy.org/), a Python database toolkit with an ORM (object-relational mapper). With SQLAlchemy, you can define a Python class to represent a database table, with class attributes representing its fields, or columns. You then work with this class instead of writing SQL statements yourself. We call it a **model class**, and we will refer to its mapped attributes as **fields**.

Flask has many third-party extensions that make it easier to integrate other libraries. We will use the [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x) extension to integrate SQLAlchemy.

First, install it:

```bash
(.venv) $ pip install flask-sqlalchemy
```

Most extensions need to be initialized. Import the extension class, create an instance, and pass it your Flask application instance:

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # Import the extension class
from sqlalchemy.orm import DeclarativeBase

app = Flask(__name__)

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(app, model_class=Base)  # Initialize the extension with the application instance, app
```

Along with the application instance, pass a subclass of `DeclarativeBase` as the `model_class` argument. This class is empty for now, but you can customize the base class later as needed. Before initializing the extension, we also need to configure the database connection, as shown next.

## Set the database URI

To control the behavior of Flask, its extensions, and our own application, we define configuration variables. Flask provides one place to set and retrieve them: the `Flask.config` dictionary. Configuration names must be uppercase, and configuration statements usually go before the extension is initialized.

Set `SQLALCHEMY_DATABASE_URI` to tell SQLAlchemy where to connect:

```python
from pathlib import Path

# ...

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(Path(app.root_path) / 'data.db')
```

> **Important** The last word in this configuration name is URI, not URL.

The format depends on the DBMS. For SQLite, an absolute Unix-style path produces a URI like this:

```text
sqlite:////absolute/path/to/database.db
```

The project root is a convenient place to keep the database file. `app.root_path` gives us the directory containing the application module—currently the project root—so we use it to build the path. You can choose any filename and extension; .db, .sqlite, and .sqlite3 are common choices.

On Windows, an absolute path such as `C:/.../data.db` follows three slashes, `sqlite:///`. On Unix-like systems, the absolute path itself starts with `/`, so adding it to the same three-slash prefix produces four slashes in the URI. This gives us one expression that works on both platforms:

*app.py: database configuration*

```python
from pathlib import Path

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(Path(app.root_path) / 'data.db')

db = SQLAlchemy(app, model_class=Base)
```

If you develop and deploy on the same operating system, you can also write the appropriate URI directly. When building it from an absolute path, remember that the path already contains any leading slash it needs.

> **Tip** See the [Flask configuration documentation](https://flask.palletsprojects.com/config/) for Flask's built-in configuration variables, and the [Flask-SQLAlchemy configuration documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/) for the extension's settings.

## Create database models

Watchlist currently needs to store two kinds of data: user information and movie entries. Define a model class for each table:

*app.py: create database models*

```python
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

class User(db.Model):
    __tablename__ = 'user' # Set the table name
    id: Mapped[int] = mapped_column(primary_key=True)  # Primary key
    name: Mapped[str] = mapped_column(String(20))  # Name


class Movie(db.Model):  # The table name is movie
    __tablename__ = 'movie'
    id: Mapped[int] = mapped_column(primary_key=True)  # Primary key
    title: Mapped[str] = mapped_column(String(60))  # Movie title
    year: Mapped[str] = mapped_column(String(4))  # Release year
```

Here are the rules for defining model classes:

* Inherit from `db.Model`.
* Set the table name with `__tablename__`.
* Specify each mapped attribute's type with a type hint, placing the type inside `Mapped[]`. The table below lists common field types and the corresponding Python types.
* Use `mapped_column()` for additional settings. For example, `primary_key` marks a field as a primary key. Other common options include `index` (whether to create an index), `unique` (whether values must be unique), and `default` (the default value).

Common field types are listed below:

| Field type | Description |
| --- | --- |
| int | Integer |
| str | String. Specify its length with `mapped_column(String(size))`; import `String` from `sqlalchemy`. |
| str | Long text. Use `mapped_column(Text)` and import `Text` from `sqlalchemy`. |
| datetime | Date and time, represented by Python's `datetime` type. Import `datetime` from the `datetime` module. |
| float | Floating-point number |
| bool | Boolean |

> **Tip** If type hints are new to you, read the [typing documentation](https://docs.python.org/zh-cn/3.12/library/typing.html) (Chinese). Type hints use special syntax to describe the types of variables, function parameters, return values, and more. For example, in `message: str = 'How are you?'`, `: str` says that `message` is a string. Most built-in types, including str, int, list, dict, and bool, can be used directly in type hints. For more complex annotations, you can import types from the typing module.

## Create the database tables

Defining models does not create the tables or the database file. Create them in a Python shell:

```python
(.venv) $ flask shell
>>> from app import db
>>> db.create_all()
```

Open your file manager and you should see data.db in the project root. Do not commit this file to Git. Add a new rule at the end of .gitignore:

```
*.db
```

If you change your models and want to recreate the table schema, first drop the tables with `db.drop_all()`, then create them again:

```python
>>> db.drop_all()
>>> db.create_all()
```

This deletes all the existing data too. To change a table's structure without losing its data, use a database migration tool, such as the [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate) extension, which integrates [Alembic](https://alembic.sqlalchemy.org/en/latest/).

> **Tip** We opened the Python shell with `flask shell`, not `python`. This command activates an *application context*, which makes certain special variables available. Some operations, including `db.create_all()`, require it. Use `flask shell` for the Python shell examples throughout the rest of this book.

We can also write a custom command, similar to `flask shell`, to create the database tables automatically:

*app.py: the custom init-db command*

```python
import click


@app.cli.command('init-db')  # Register a command with a custom name
@click.option('--drop', is_flag=True, help='Create after drop.')  # Define an option
def init_database(drop):
    """Initialize the database."""
    if drop:  # Check whether the option was supplied
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # Print a message
```

If you do not specify a command name, Flask uses the function name, replacing underscores with hyphens. Here, we explicitly named the command `init-db`. Run it to create the tables:

```bash
(.venv) $ flask init-db
```

Add `--drop` to drop the tables before recreating them:

```bash
(.venv) $ flask init-db --drop
```

## Create, read, update, and delete

Let's try some common database operations in the Python shell we opened earlier. Follow the examples, or experiment on your own.

### Create

Here is how to add records to the database:

```python
>>> from app import User, Movie  # Import the model classes
>>> user = User(name='Grey Li')  # Create a User record
>>> m1 = Movie(title='Leon', year='1994')  # Create a Movie record
>>> m2 = Movie(title='Mahjong', year='1996')  # Create another Movie record
>>> db.session.add(user)  # Add the new record to the database session
>>> db.session.add(m1)
>>> db.session.add(m2)
>>> db.session.commit()  # Commit the database session once, after adding all records
```

> **Tip** We did not supply `id`, the primary key, when creating model instances. SQLAlchemy takes care of that field automatically.

The final `db.session.commit()` call is important: it saves the records to the database. The preceding `db.session.add()` calls only add the pending changes to the database session, which you can think of as a temporary staging area.

### Read

There are two ways to read records. One is to look up a record by its primary key using `db.session.get()`:

```python
>>> db.session.get(Movie, 1)  # Get the movie record with primary key 1
```

The other is to construct a SELECT statement with `select()`, execute it with `db.session.execute()`, and then extract the results. Records are represented as model instances. The general pattern is:

```
db.session.execute(select(...).<optional_filter_method>).<result_method>
```

Import `select` from SQLAlchemy:

```python
from sqlalchemy import select
```

Common methods for refining a statement include:

| Method | Description |
| --- | --- |
| filter() | Filter records using expressions, returning a new statement. |
| filter_by() | Filter records using keyword arguments, returning a new statement. |
| order_by() | Sort records by the given criteria, returning a new statement. |
| group_by() | Group records by the given criteria, returning a new statement. |

Here are common result methods and query helpers:

| Method | Description |
| --- | --- |
| all() | Return all results as a list. |
| first() | Return the first result, or None if there are no results. |
| scalar() | Return the first column of the first result, or None if there are no results. |
| scalars() | Convert a Result into a ScalarResult, so subsequent methods return scalar values rather than Row objects. |
| first_or_404() | Return the first record, or a 404 error response if none is found. |
| get_or_404() | Look up a record by primary key, or return a 404 error response if it does not exist. |
| paginate() | Return a Pagination object for displaying records across multiple pages. |

In practice, we commonly use `scalars().first()` for one record and `scalars().all()` for several. These return scalar values—in these queries, model instances. For this purpose, `scalars().first()` is equivalent to `scalar()`.

The `first_or_404()`, `get_or_404()`, and `paginate()` helpers come from Flask-SQLAlchemy, so call them on `db` directly. For example:

```python
movie = db.get_or_404(Movie, id)
```

Try reading records and making simple queries:

```python
>>> from sqlalchemy import select
>>> from app import Movie  # Import the model classes
>>> movie = db.session.execute(select(Movie)).scalar()  # Get the first Movie record as a model instance
>>> movie.title  # Read fields through the returned model instance
'Leon'
>>> movie.year
'1994'
>>> db.session.execute(select(Movie)).scalars().all()  # Get all Movie records as a list of model instances
[<Movie 1>, <Movie 2>]
>>> db.session.get(Movie, 1)  # Get the record with primary key 1
<Movie 1>
# Get the record whose title is Mahjong
>>> db.session.execute(select(Movie).filter_by(title='Mahjong')).scalar()
<Movie 2>
# The same query using filter instead
>>> db.session.execute(select(Movie).filter(Movie.title=='Mahjong')).scalar()
<Movie 2>
```

A statement can get quite long after adding filters. You can store the statement separately:

```python
>>> stmt = select(Movie).filter(Movie.title=='Mahjong')
>>> db.session.execute(stmt).scalar()
<Movie 2>
```

Once you are comfortable with these operations, use the `db.session.scalars()` and `db.session.scalar()` shortcuts to simplify them:

```python
# scalars
movies = db.session.execute(select(Movie)).scalars().all()
# Use the db.session.scalars() shortcut
movies = db.session.scalars(select(Movie)).all()
# scalar
movie = db.session.execute(select(Movie)).scalar()
# Use the db.session.scalar() shortcut
movie = db.session.scalar(select(Movie))
```

To count the records in a table, use the database function `func.count`:

```python
>>> from sqlalchemy import select, func
>>> db.session.execute(select(func.count(Movie.id))).scalar()
2
```

> **Tip** When we refer to the Movie model, we mean the movie table in the database.

SQLAlchemy supports many operators for expressions passed to `filter()`. See the [operator documentation](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators) for details. The [SQLAlchemy Result documentation](https://docs.sqlalchemy.org/en/20/core/connections.html#sqlalchemy.engine.Result) lists the available result methods.

### Update

Update the Movie record whose primary key is `2`:

```python
>>> movie = db.session.get(Movie, 2)
>>> movie.title = 'WALL-E'  # Assign a new value to the instance attribute
>>> movie.year = '2008'
>>> db.session.commit()  # Remember to commit the changes
```

### Delete

Delete the Movie record whose primary key is `1`:

```python
>>> movie = db.session.get(Movie, 1)
>>> db.session.delete(movie)  # Pass the model instance to db.session.delete() to delete the record
>>> db.session.commit()  # Commit the changes
```

## Use the database in the application

With some practice behind us, we can now use the database in Watchlist itself.

### Read records in the home page view

Now that we have a database, the `index` view can read real records for the home page:

```python
@app.route('/')
def index():
    user = db.session.execute(select(User)).scalar()  # Read the user record
    movies = db.session.execute(select(Movie)).scalars().all()  # Read all movie records
    return render_template('index.html', user=user, movies=movies)
```

> **Tip** The ScalarResult returned by `scalars()` is iterable. If you only need to loop over it, you can use `scalars()` without `.all()`, avoiding the extra step of collecting all the results into a list before iterating.

The `user` instance now replaces the `name` variable previously passed to the template. In index.html, replace both occurrences of `name` with `user.name`:

```jinja2
{{ user.name }}'s Watchlist
```

### Generate sample data

We can now write a command to insert sample data into the database:

*app.py: the custom forge command*

```python
import click


@app.cli.command()
def forge():
    """Generate fake data."""
    db.drop_all()
    db.create_all()

    # Move the two global variables into this function
    name = 'Grey Li'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')
```

Run `flask forge` to populate the database with the sample data:

```bash
(.venv) $ flask forge
```

## Chapter summary

In this chapter, we learned to work with a database through SQLAlchemy. You will become more familiar with these operations as we continue. Before we finish, commit the code:

```bash
$ git add .
$ git commit -m "Add database support with Flask-SQLAlchemy"
$ git push
```

## Going further

* In production, you can switch to a DBMS that better fits your needs. SQLAlchemy supports several SQL database engines, so this usually requires very little code to change.
* Our application has only one user, so we have not defined a relationship between the User and Movie tables. See [Declaring Models](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#one-to-many-relationships) in the Flask-SQLAlchemy documentation to learn about relationships.
* Read the [SQLAlchemy documentation and tutorials](https://docs.sqlalchemy.org/en/latest/) for more detail. We use Flask-SQLAlchemy to integrate it, so some usage differs from using SQLAlchemy on its own. Keep the [Flask-SQLAlchemy documentation](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) at hand as well.
