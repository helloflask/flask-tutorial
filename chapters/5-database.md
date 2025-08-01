# 第 5 章：数据库

大部分程序都需要保存数据，所以不可避免要使用数据库。用来操作数据库的数据库管理系统（DBMS）有很多选择，对于不同类型的程序，不同的使用场景，都会有不同的选择。在这个教程中，我们选择了属于关系型数据库管理系统（RDBMS）的 [SQLite](https://www.sqlite.org/)，它基于文件，不需要单独启动数据库服务器，适合在开发时使用，或是在数据库操作简单、访问量低的程序中使用。


## 使用 SQLAlchemy 操作数据库

为了简化数据库操作，我们将使用 [SQLAlchemy](https://www.sqlalchemy.org/)——一个 Python 数据库工具（ORM，即对象关系映射）。借助 SQLAlchemy，你可以通过定义 Python 类来表示数据库里的一张表（类属性表示表中的字段 / 列），通过对这个类进行各种操作来代替写 SQL 语句。这个类我们称之为**模型类**，类中的属性我们将称之为**字段**。

Flask 有大量的第三方扩展，这些扩展可以简化和第三方库的集成工作。我们下面将使用一个叫做 [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x) 的扩展来集成 SQLAlchemy。

首先安装它：

```bash
(env) $ pip install flask-sqlalchemy==2.5.1 sqlalchemy==1.4.47
```

> **提示** Flask-SQLAlchemy 3.x / SQLAlchemy 2.x 版本有一些大的变化，这里分别固定安装 2.5.1 和 1.4.47 版本。后续教程改写后会删除这里的版本限制。

大部分扩展都需要执行一个“初始化”操作。你需要导入扩展类，实例化并传入 Flask 程序实例：

```python
from flask_sqlalchemy import SQLAlchemy  # 导入扩展类

app = Flask(__name__)

db = SQLAlchemy(app)  # 初始化扩展，传入程序实例 app
```

## 设置数据库 URI

为了设置 Flask、扩展或是我们程序本身的一些行为，我们需要设置和定义一些配置变量。Flask 提供了一个统一的接口来写入和获取这些配置变量：`Flask.config` 字典。配置变量的名称必须使用大写，写入配置的语句一般会放到扩展类实例化语句之前。

下面写入了一个 `SQLALCHEMY_DATABASE_URI` 变量来告诉 SQLAlchemy 数据库连接地址：

```python
import os

# ...

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
```

> **注意** 这个配置变量的最后一个单词是 URI，而不是 URL。

对于这个变量值，不同的 DBMS 有不同的格式，对于 SQLite 来说，这个值的格式如下：

```python
sqlite:////数据库文件的绝对地址
```

数据库文件一般放到项目根目录即可，`app.root_path` 返回程序实例所在模块的路径（目前来说，即项目根目录），我们使用它来构建文件路径。数据库文件的名称和后缀你可以自由定义，一般会使用 .db、.sqlite 和 .sqlite3 作为后缀。

另外，如果你使用 Windows 系统，上面的 URI 前缀部分只需要写入三个斜线（即 `sqlite:///`）。在本书的示例程序代码里，做了一些兼容性处理，另外还新设置了一个配置变量，实际的代码如下：

*app.py：数据库配置*

```python
import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

WIN = sys.platform.startswith('win')
if WIN:  # 如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:  # 否则使用四个斜线
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)
```

如果你固定在某一个操作系统上进行开发，部署时也使用相同的操作系统，那么可以不用这么做，直接根据你的需要写出前缀即可。

> **提示** 你可以访问 [Flask 文档的配置页面](https://flask.palletsprojects.com/config/)查看 Flask 内置的配置变量；同样的，在 [Flask-SQLAlchemy 文档的配置页面](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/)可以看到 Flask-SQLAlchemy 提供的配置变量。


## 创建数据库模型

在 Watchlist 程序里，目前我们有两类数据要保存：用户信息和电影条目信息。下面分别创建了两个模型类来表示这两张表：

*app.py：创建数据库模型*

```python
class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 名字


class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份
```

模型类的编写有一些限制：

* 模型类要声明继承 `db.Model`。
* 每一个类属性（字段）要实例化 `db.Column`，传入的参数为字段的类型，下面的表格列出了常用的字段类。
* 在 `db.Column()` 中添加额外的选项（参数）可以对字段进行设置。比如，`primary_key` 设置当前字段是否为主键。除此之外，常用的选项还有 `nullable`（布尔值，是否允许为空值）、`index`（布尔值，是否设置索引）、`unique`（布尔值，是否允许重复值）、`default`（设置默认值）等。

常用的字段类型如下表所示：

| 字段类           | 说明                                          |
| ---------------- | --------------------------------------------- |
| db.Integer       | 整型                                          |
| db.String (size) | 字符串，size 为最大长度，比如 `db.String(20)` |
| db.Text          | 长文本                                        |
| db.DateTime      | 时间日期，Python `datetime` 对象              |
| db.Float         | 浮点数                                        |
| db.Boolean       | 布尔值                                        |


## 创建数据库表

模型类创建后，还不能对数据库进行操作，因为我们还没有创建表和数据库文件。下面在 Python Shell 中创建了它们：

```python
(env) $ flask shell
>>> from app import db
>>> db.create_all()
```

打开文件管理器，你会发现项目根目录下出现了新创建的数据库文件 data.db。这个文件不需要提交到 Git 仓库，我们在 .gitignore 文件最后添加一行新规则：

```
*.db
```

如果你改动了模型类，想重新生成表模式，那么需要先使用 `db.drop_all()` 删除表，然后重新创建：

```python
>>> db.drop_all()
>>> db.create_all()
```

注意这会一并删除所有数据，如果你想在不破坏数据库内的数据的前提下变更表的结构，需要使用数据库迁移工具，比如集成了 [Alembic](https://alembic.sqlalchemy.org/en/latest/) 的 [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate) 扩展。

> **提示** 上面打开 Python Shell 使用的是 `flask shell`命令，而不是 `python`。使用这个命令启动的 Python Shell 激活了“程序上下文”，它包含一些特殊变量，这对于某些操作是必须的（比如上面的 `db.create_all()`调用）。请记住，后续的 Python Shell 都会使用这个命令打开。

和 `flask shell`类似，我们可以编写一个自定义命令来自动执行创建数据库表操作：

*app.py：自定义命令 initdb*

```python
import click


@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:  # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息
```

默认情况下，如果没有指定，函数名称就是命令的名字（注意函数名中的下划线会被转换为连接线），现在执行 `flask initdb` 命令就可以创建数据库表：

```bash
(env) $ flask initdb
```

使用 `--drop` 选项可以删除表后重新创建：

```bash
(env) $ flask initdb --drop
```


## 创建、读取、更新、删除

在前面打开的 Python Shell 里，我们来测试一下常见的数据库操作。你可以跟着示例代码来操作，也可以自由练习。


### 创建

下面的操作演示了如何向数据库中添加记录：

```python
>>> from app import User, Movie  # 导入模型类
>>> user = User(name='Grey Li')  # 创建一个 User 记录
>>> m1 = Movie(title='Leon', year='1994')  # 创建一个 Movie 记录
>>> m2 = Movie(title='Mahjong', year='1996')  # 再创建一个 Movie 记录
>>> db.session.add(user)  # 把新创建的记录添加到数据库会话
>>> db.session.add(m1)
>>> db.session.add(m2)
>>> db.session.commit()  # 提交数据库会话，只需要在最后调用一次即可
```

> **提示** 在实例化模型类的时候，我们并没有传入 `id` 字段（主键），因为 SQLAlchemy 会自动处理这个字段。

最后一行 `db.session.commit()` 很重要，只有调用了这一行才会真正把记录提交进数据库，前面的 `db.session.add()` 调用是将改动添加进数据库会话（一个临时区域）中。


### 读取

通过对模型类的 `query` 属性调用可选的过滤方法和查询方法，我们就可以获取到对应的单个或多个记录（记录以模型类实例的形式表示）。查询语句的格式如下：

```python
<模型类>.query.<过滤方法（可选）>.<查询方法>
```

下面是一些常用的过滤方法：

| 过滤方法    | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| filter()    | 使用指定的规则过滤记录，返回新产生的查询对象                 |
| filter_by() | 使用指定规则过滤记录（以关键字表达式的形式），返回新产生的查询对象 |
| order_by()  | 根据指定条件对记录进行排序，返回新产生的查询对象             |
| group_by()  | 根据指定条件对记录进行分组，返回新产生的查询对象             |

下面是一些常用的查询方法：

| 查询方法       | 说明                                                         |
| -------------- | ------------------------------------------------------------ |
| all()          | 返回包含所有查询记录的列表                                   |
| first()        | 返回查询的第一条记录，如果未找到，则返回 None                 |
| get(id)        | 传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回 None |
| count()        | 返回查询结果的数量                                           |
| first_or_404() | 返回查询的第一条记录，如果未找到，则返回 404 错误响应          |
| get_or_404(id) | 传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回 404 错误响应 |
| paginate()     | 返回一个 Pagination 对象，可以对记录进行分页处理               |

下面的操作演示了如何从数据库中读取记录，并进行简单的查询：

```python
>>> from app import Movie  # 导入模型类
>>> movie = Movie.query.first()  # 获取 Movie 模型的第一个记录（返回模型类实例）
>>> movie.title  # 对返回的模型类实例调用属性即可获取记录的各字段数据
'Leon'
>>> movie.year
'1994'
>>> Movie.query.all()  # 获取 Movie 模型的所有记录，返回包含多个模型类实例的列表
[<Movie 1>, <Movie 2>]
>>> Movie.query.count()  # 获取 Movie 模型所有记录的数量
2
>>> Movie.query.get(1)  # 获取主键值为 1 的记录
<Movie 1>
>>> Movie.query.filter_by(title='Mahjong').first()  # 获取 title 字段值为 Mahjong 的记录
<Movie 2>
>>> Movie.query.filter(Movie.title=='Mahjong').first()  # 等同于上面的查询，但使用不同的过滤方法
<Movie 2>
```

> **提示** 我们在说 Movie 模型的时候，实际指的是数据库中的 movie 表。表的实际名称是模型类的小写形式（自动生成），如果你想自己指定表名，可以定义 `__tablename__` 属性。

对于最基础的 `filter()` 过滤方法，SQLAlchemy 支持丰富的查询操作符，具体可以访问[文档相关页面](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators)查看。除此之外，还有更多的查询方法、过滤方法和数据库函数可以使用，具体可以访问文档的 [Query API](https://docs.sqlalchemy.org/en/latest/orm/query.html) 部分查看。


### 更新

下面的操作更新了 `Movie` 模型中主键为 `2` 的记录：

```python
>>> movie = Movie.query.get(2)
>>> movie.title = 'WALL-E'  # 直接对实例属性赋予新的值即可
>>> movie.year = '2008'
>>> db.session.commit()  # 注意仍然需要调用这一行来提交改动
```

### 删除

下面的操作删除了 `Movie` 模型中主键为 `1` 的记录：

```python
>>> movie = Movie.query.get(1)
>>> db.session.delete(movie)  # 使用 db.session.delete() 方法删除记录，传入模型实例
>>> db.session.commit()  # 提交改动
```

## 在程序里操作数据库

经过上面的一番练习，我们可以在 Watchlist 里进行实际的数据库操作了。


### 在主页视图读取数据库记录

因为设置了数据库，负责显示主页的 `index` 可以从数据库里读取真实的数据：

```python
@app.route('/')
def index():
    user = User.query.first()  # 读取用户记录
    movies = Movie.query.all()  # 读取所有电影记录
    return render_template('index.html', user=user, movies=movies)
```

在 `index` 视图中，原来传入模板的 `name` 变量被 `user` 实例取代，模板 index.html 中的两处 `name` 变量也要相应的更新为 `user.name` 属性：

```jinja2
{{ user.name }}'s Watchlist
```


### 生成虚拟数据

因为有了数据库，我们可以编写一个命令函数把虚拟数据添加到数据库里。下面是用来生成虚拟数据的命令函数：

*app.py：创建自定义命令 forge*

```python
import click


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()
    
    # 全局的两个变量移动到这个函数内
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

现在执行 `flask forge` 命令就会把所有虚拟数据添加到数据库里：

```bash
(env) $ flask forge
```


## 本章小结

本章我们学习了使用 SQLAlchemy 操作数据库，后面你会慢慢熟悉相关的操作。结束前，让我们提交代码：

```bash
$ git add .
$ git commit -m "Add database support with Flask-SQLAlchemy"
$ git push
```

> **提示** 你可以在 GitHub 上查看本书示例程序的对应 commit：[4d2442a](https://github.com/helloflask/watchlist/commit/4d2442a41e55fb454e092864206af08e4e3eeddf)。


## 进阶提示

* 在生产环境，你可以更换更合适的 DBMS，因为 SQLAlchemy 支持多种 SQL 数据库引擎，通常只需要改动非常少的代码。
* 我们的程序只有一个用户，所以没有将 User 表和 Movie 表建立关联。访问 Flask-SQLAlchemy 文档的“[声明模型](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#one-to-many-relationships)”章节可以看到相关内容。 
* 阅读 [SQLAlchemy 官方文档和教程](https://docs.sqlalchemy.org/en/latest/)详细了解它的用法。注意我们在这里使用 Flask-SQLAlchemy 来集成它，所以用法和单独使用 SQLAlchemy 有一些不同。作为参考，你可以同时阅读 [Flask-SQLAlchemy 官方文档](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)。
* 如果你是[《Flask Web 开发实战》](http://helloflask.com/book/1)的读者，第 5 章详细介绍了 SQLAlchemy 和 Flask-Migrate 的使用，第 8 章和第 9 章引入了更复杂的模型关系和查询方法。
