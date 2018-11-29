# 数据库

大部分程序都需要保存数据，所以不可避免要使用数据库。数据库有很多选择，对于不同类型的程序，不同的程序功能，都可以找到适合的选项。在这个教程中，我们选择了更为常用的 SQL 数据库，对于数据库管理系统（DBMS），我们使用了更简单的 SQLite，它基于文件，不需要单独启动数据库服务器。

## 使用 SQLAlchemy 操作数据库

为了简化数据库操作，我们将使用 SQLAlchemy——一个 Python 数据库工具（ORM，即对象关系映射）。借助 SQLAlchemy，你可以通过定义 Python 类来表示一张表（类属性表示表中的列），通过对这个类进行实例化操作、调用查询函数等来代替写 SQL 语句。这个类我们称之为**模型类**。

Flask 有大量的第三方扩展，这些扩展可以简化和常用的第三方库的集成工作。我们下面将使用一个叫做 Flask-SQLAlchemy 的扩展来集成 SQLAlchemy。

首先使用 Pipenv 安装它：

```bash
$ pipenv install flask-sqlalchemy
```

大部分扩展都需要执行一个“初始化”操作：导入扩展类，实例化并传入 Flask 程序实例。

```python
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)  # 初始化扩展，传入程序实例
```

## Flask 配置

为了设置 Flask、扩展或是我们程序本身的一些行为，我们需要定义一些配置变量。Flask 提供了一个统一的接口来写入和获取这些配置变量：`Flask.config` 字典。下面写入了一个 `SQLALCHEMY_DATABASE_URI` 变量存储数据库的地址：

```python
app.config['SQLALCHEMY_DATABASE_URI'] = app.root_path
```

【代码未完成】

注意 对于 macOS 和 Linux 用户，上面的地址需要写入四个斜线。

为了方便开发，这里使用了 SQLite，因为它支持把数据存储在独立的文件中，不用配置数据库服务器。在生产环境，你可以更换更合适的 DBMS，因为 SQLAlchemy 支持多种 SQL 数据库引擎，所以只需更换这个配置的值即可。

注意 配置变量的名称必须使用大写。

提示 你可以访问  c查看 Flask 内置的配置变量，访问 查看 Flask-SQLAlchemy 提供的配置变量。

## 创建数据库模型

我们有两类数据要保存，一类是用户信息，另一类是电影条目信息。下面分别创建了两个模型类来表示这两张表：

*app.py：创建数据库模型*

```python
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))  # db.String 传入的参数为限制长度
    username = db.Column(db.String(20))
    bio = db.Column(db.Text)
    
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.Integer)
```

模型类的编写有一些限制：

* 模型类要声明继承 db.Model。
* 每一个类属性要实例化 db.Column，传入的参数为列的类型。
* 额外的选项为列进行设置，比如 primary_key 选择设置当前列是否为主键。

## 创建数据库表

模型类创建后，还不能对数据库进行操作，因为我们还没有创建数据库表。下面在 Python Shell 中创建了数据库表：

```python
$ flask shell
>>> from app import db
>>> db.create_all()
```

【提及删除表，表的更新】

你应该发现了，上面打开 Python Shell 使用的是 `flask shell`命令，而不是 `python`。使用这个命令启动的 Python Shell 激活了程序上下文，包含一些特殊变量，这对于某些操作是必须的（比如上面的 `create_all()`调用）。

【简单介绍程序上下文】

再接再厉，我们在 Python Shell 里测试一下常见的增删查改操作：

```python
>>> from app import User, Movie
>>> me = User()  # 创建一个 User 记录
```



和 `flask shell`类似，我们可以编写一个自定义命令来执行创建数据库表操作：



一鼓作气，我们再编写一个命令来创建管理员账户，因为程序只允许一个人使用，就没有必要再编写一个注册页面。下面是创建管理员账户的 admin() 函数：




## 进阶提示

* 我们假定程序只有一个用户，所以没有将 User 表和 Movie 表建立关联，如果要支持多用户，你需要在 User 表……。【】

