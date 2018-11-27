# 数据库

大部分程序都需要保存数据，所以不可避免要使用数据库。数据库有很多选择，对于不同类型的程序，不同的程序功能，都可以找到适合的选项。为了简化数据库操作，我们将使用一个使用 Python 编写的数据库工具来操作数据库。它属于 ORM，借助 ORM，你可以使用定义 Python 类来表示一张表，通过对这个类进行实例化操作、调用查询函数等来代替写 SQL 语句。这个类我们称之为「模型类」。

## 使用 SQLAlchemy 操作数据库

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

为了设置 Flask、扩展或是我们程序本身的一些行为，我们需要定义一些配置变量。Flask 提供了一个统一的接口来写入和获取这些配置变量：`Flask.config` 字典。我们先来写入一个 `SQLALCHEMY_DATABASE_URI` 变量存储数据库的地址：

```python
app.config['SQLALCHEMY_DATABASE_URI'] = app.root_path
```

为了方便开发，这里使用了 SQLite，因为它支持把数据存储在独立的文件中，不用配置数据库服务器。在生产环境，你可以更换更合适的 DBMS，因为 SQLAlchemy 支持多种 SQL 数据库引擎，所以只需更换这个配置的值即可。



注意 配置变量的名称必须使用大写。

提示 你可以访问  c查看 Flask 内置的配置变量，访问 查看 Flask-SQLAlchemy 提供的配置变量。

## 创建数据库模型

两类数据要保存，一类是用户信息，另一类是电影条目信息。

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

现在 Python Shell 里测试一下：



编写一个命令来创建账户

## 进阶提示

支持多用户，可以创建一个 User 表，并建立关联。

我们假定程序只有一个用户，所以