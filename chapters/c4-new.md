# 数据库

大部分程序都需要保存数据，所以不可避免要使用数据库。数据库有很多选择，对于不同类型的程序，不同的程序功能，都可以找到适合的选项。为了简化数据库操作，我们将使用一个使用 Python 编写的数据库工具来操作数据库。它属于 ORM，借助 ORM，你可以使用定义 Python 类来表示一张表，通过对这个类进行实例化操作、调用查询函数等来代替写 SQL 语句。这个类我们称之为「模型类」。

## 使用 SQLAlchemy 操作数据库





## 创建数据库模型

两类数据要保存，一类是用户信息，另一类是电影条目信息。

app.py

```python
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60))
    year = db.Column(db.Interger)
```





## 用户信息保存到配置文件

app.py

NAME=

BIO=



## 进阶提示

支持多用户，可以创建一个 User 表，并建立关联。

我们假定程序只有一个用户，所以