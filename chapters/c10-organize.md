# 第 10 章：组织你的代码

虽然我们的程序开发已经完成，但随着功能的增多，把所有代码放在 app.py 里会让后续的开发和维护变得麻烦。这一章，我们要对项目代码进行一次重构，让项目组织变得更加合理。

Flask 对项目结构没有固定要求，你可以使用单脚本，也可以使用包。这一章我们会学习使用包来组织程序。

先来看看我们目前的项目文件结构：

```
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


## 使用包组织代码

我们会创建一个包，然后把 app.py 中的代码按照类别分别放到多个模块里。下面是我们需要执行的一系列操作（这些操作你也可以使用文件管理器或编辑器完成）：

```bash
$ mkdir watchlist  # 创建作为包的文件夹
$ mv static templates watchlist  # 把 static 和 templates 文件夹移动到 watchlist 文件夹内
$ cd watchlist  # 切换进包目录
$ touch __init__.py views.py errors.py models.py commands.py  # 创建多个模块
```

我们把这个包称为程序包，包里目前包含的模块和作用如下表所示：

| 模块            | 作用                     |
| --------------- | ------------------------ |
| \_\_init\_\_.py | 包构造文件，创建程序实例 |
| views.py        | 视图函数                 |
| errors.py       | 错误处理函数             |
| models.py       | 模型类                   |
| commands.py     | 命令函数                 |

> **提示** 除了包构造文件外，其他的模块文件名你可以自由修改，比如 views.py 也可以叫 routes.py。

创建程序实例，初始化扩展的代码放到包构造文件里（\_\_init\_\_.py），如下所示：

```python
import os
import sys

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# ...

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'
# 注意更新这里的路径，把 app.root_path 添加到 os.path.dirname() 中
# 以便把文件定位到项目根目录
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
	from watchlist.models import User
	user = User.query.get(int(user_id))
	return user

login_manager.login_view = 'login'

@app.context_processor
def inject_user():
	from watchlist.models import User
	user = User.query.first()
	return dict(user=user)

from watchlist import views, errors, commands
```

在构造文件中，为了让视图函数、错误处理函数和命令函数注册到程序实例上，我们需要在这里导入这几个模块。但是因为这几个模块同时也要导入构造文件中的程序实例，为了避免循环依赖（A 导入 B，B 导入 A），我们把这一行导入语句放到构造文件的结尾。同样的，`load_user()` 函数和 `inject_user()` 函数中使用的模型类也在函数内进行导入。

其他代码则按照分类分别放到各自的模块中，这里不再给出具体代码，你可以参考[源码仓库](https://github.com/helloflask/watchlist)。在移动代码之后，注意添加并更新导入语句，比如使用下面的导入语句来导入程序实例和扩展对象：

```python
from watchlist import app, db
```

使用下面的导入语句来导入模型类：

```python
from watchlist.models import User, Movie
```

以此类推。

包名称这里使用了 watchlist，所以导入时要从 watchlist 包导入，如果你使用了更常规的名字，比如 app，那么导入语句也要相应变化：

```python
from app import app, db
from app.models import User, Movie
```


## 组织模板

模块文件夹 templates 下包含了多个模板文件，我们可以创建子文件夹来更好的组织它们。下面的操作创建了一个 errors 子文件夹，并把错误页面模板都移动到这个 errors 文件夹内（这些操作你也可以使用文件管理器或编辑器完成）：

```bash
$ cd templates  # 切换到 templates 目录
$ mkdir errors  # 创建 errors 文件夹
$ mv 400.html 404.html 500.html errors  # 移动错误页面模板到 errors 文件夹
```

因为错误页面放到了新的路径，所以我们需要修改代码中的 3 处模板文件路径，以 400 错误处理函数为例：

```python
@app.errorhandler(400)
def bad_request(e):
    return render_template('errors/400.html'), 400
```


## 单元测试

你也可以将测试文件拆分成多个模块，创建一个 tests 包来存储这些模块。但是因为目前的测试代码还比较少，暂时不做改动，只需要更新导入语句即可：

```python
from watchlist import app, db
from watchlist.models import Movie, User
from watchlist.commands import forge, initdb
```

因为要测试的目标改变，测试时的 `--source` 选项的值也要更新为包的名称 `watchlist`：

```bash
(env) $ coverage run --source=watchlist test_watchlist.py
```

> **提示** 你可以创建配置文件来预先定义 `--source` 选项，避免每次执行命令都给出这个选项，具体可以参考文档[配置文件章节](https://coverage.readthedocs.io/en/v4.5.x/config.html)。

现在的测试覆盖率报告会显示包内的多个文件的覆盖率情况：

```bash
$ coverage report
Name                    Stmts   Miss  Cover
-------------------------------------------
watchlist\__init__.py      25      1    96%
watchlist\commands.py      35      1    97%
watchlist\errors.py         8      2    75%
watchlist\models.py        16      0   100%
watchlist\views.py         77      2    97%
-------------------------------------------
TOTAL                     161      6    96%
```


## 启动程序

因为我们使用包来组织程序，不再是 Flask 默认识别的 app.py，所以在启动开发服务器前需要使用环境变量 `FLASK_APP` 来给出程序实例所在的模块路径。因为我们的程序实例在包构造文件内，所以直接写出包名称即可。在 .flaskenv 文件中添加下面这行代码：

```
FLASK_APP=watchlist
```

最终的项目文件结构如下所示：

```
├── .flaskenv
├── test_watchlist.py
└── watchlist  # 程序包
    ├── __init__.py
    ├── commands.py
    ├── errors.py
    ├── models.py
    ├── views.py
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


## 本章小结

对我们的程序来说，这样的项目结构已经足够了。但对于大型项目，你可以使用蓝本和工厂函数来进一步组织程序。结束前，让我们提交代码：

```bash
$ git add .
$ git commit -m "Organize application with package"
$ git push
```

> **提示** 你可以在 GitHub 上查看本书示例程序的对应 commit：[f705408](https://github.com/helloflask/watchlist/commit/f7054083c8f87f83bf842a1125a3d8d0244b0f62)。


## 进阶提示

- [蓝本](https://flask.palletsprojects.com/blueprints/)类似于子程序的概念，借助蓝本你可以把程序不同部分的代码分离开（比如按照功能划分为用户认证、管理后台等多个部分），即对程序进行模块化处理。每个蓝本可以拥有独立的子域名、URL 前缀、错误处理函数、模板和静态文件。
- [工厂函数](https://flask.palletsprojects.com/patterns/appfactories/)就是创建程序的函数。在工厂函数内，我们先创建程序实例，并在函数内完成初始化扩展、注册视图函数等一系列操作，最后返回可以直接运行的程序实例。工厂函数可以接受配置名称作为参数，在内部加载对应的配置文件，这样就可以实现按需创建加载不同配置的程序实例，比如在测试时调用工厂函数创建一个测试用的程序实例。
- 如果你是[《Flask Web 开发实战》](http://helloflask.com/book/1)的读者，第 7 章介绍了使用包组织程序，第 8 章介绍了大型项目结构以及如何使用蓝本和工厂函数组织程序。 
