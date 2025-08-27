# 第 9 章：组织你的代码

虽然我们的程序开发已经完成，但随着功能的增多，把所有代码都放在一个 app.py 脚本里会让后续的开发和维护变得麻烦。这一章，我们要对项目代码进行一次重构，让项目组织变得更加合理。

Flask 对项目结构没有固定要求，你可以使用单脚本，也可以使用包。这一章我们会学习使用包来组织程序。同时使用蓝本来模块化程序功能，并引入工厂函数来创建程序实例。

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

## 使用蓝本组织程序

[蓝本](https://flask.palletsprojects.com/blueprints/)（blueprint）在概念上类似子程序。在目前的程序里，我们创建了一个程序实例 app，所有的视图函数和错误处理函数等都注册到这个程序实例上。借助蓝本，我们可以根据功能模块对程序进行拆分。每一个功能模块创建一个蓝本对象，视图函数也相应注册到关联的蓝本对象。每个蓝本可以设定不同的 URL 前缀，注册错误处理函数，使用不同的模板和静态文件夹……

下面创建了两个蓝本，分别对应程序主功能（main）和认证功能（auth）：

```python
from flask import Flask, Blueprint

app = Flask(__name__)
main_bp = Blueprint('main', __name__)
auth_bp = Blueprint('auth', __name__)
```

接着我们更新所有视图函数的 route 装饰器定义，从 `app.route` 改为蓝本对象提供的 route 装饰器（比如 `main_bp.route`）。将视图函数按照类别注册到对应的蓝本：

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

最后调用 app.register_blueprint 把蓝本注册到程序实例上：

```python
app.register_blueprint(main_bp)
app.register_blueprint(auth_bp)
```

注意要在视图函数的下面定义这两行调用，这样可以确保注册蓝本的时候，所有视图函数的信息已经注册到蓝本上。

引入蓝本后，我们还要对程序中所有作为第一个参数传入 url_for() 的端点值进行更新。蓝本扩展了端点的命名空间，所有现在的端点值也要加入蓝本名称，即 `蓝本名.视图函数名`。比如原来的：

```python
url_for('index')
```

则需要更新为：

```python
url_for('main.index')
```

你可以用编辑器的全局搜索功能找到所有 url_for 调用（包括模板里的调用），然后逐一进行更新。

> **提示** 蓝本支持嵌套，你可以在某个蓝本上再注册子蓝本。同时蓝本支持很多特定的方法和属性，具体可以访问[蓝本的 API 文档](https://flask.palletsprojects.com/en/stable/api/#blueprint-objects)查看。


## 创建工厂函数

因为目前的程序直接在脚本中创建，当脚本被执行时，app 实例会被立即创建，接着会更新配置并初始化扩展。这样的做法缺乏灵活性，很难根据不同需求对程序创建过程进行自定义。

更好的处理方法是把创建程序的操作封装到一个函数中，可以根据传入参数动态调整配置。这种模式被称为“程序工厂（application factory）”，这个函数也因此被叫做“[工厂函数](https://flask.palletsprojects.com/patterns/appfactories/)”。

工厂函数就是创建程序的函数。在工厂函数内，我们先创建程序实例，并在函数内完成初始化扩展、注册蓝本、注册各种处理函数等一系列操作，最后返回可以直接运行的程序实例。工厂函数可以接受配置名称作为参数，在内部加载对应的配置文件或配置对象，这样就可以实现按需创建加载不同配置的程序实例，比如在测试时调用工厂函数创建一个测试用的程序实例。

下面创建了一个最简单的工厂函数：

```python
from flask import Flask

def create_app():
    app = Flask(__name__)  # 创建程序实例
	return app  # 返回程序实例
```

> **提示** 按照惯例，工厂函数一般会被命名为 create_app 或 make_app。

使用工厂函数后，最显而易见的好处是，我们可以使用不同的配置来创建程序。下面开发、测试、生产环境分别创建了 3 个存储相应配置的类：

```python
import os
import sys
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
SQLITE_PREFIX = 'sqlite:///' if sys.platform.startswith('win') else 'sqlite:////'


class BaseConfig:  # 创建配置基类
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev')


class DevelopmentConfig(BaseConfig):  # 开发配置
    SQLALCHEMY_DATABASE_URI = SQLITE_PREFIX + str(BASE_DIR / 'data-dev.db')


class TestingConfig(BaseConfig):  # 测试配置
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


class ProductionConfig(BaseConfig):  # 生产配置
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', SQLITE_PREFIX + str(BASE_DIR / 'data.db'))


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
```

最后创建了一个 config 字典来存储配置名和配置类的匹配关系，方便在工厂函数中获取配置类。

对于数据库 URI，不同的环境下设置不同的值。同时为了让配置更加灵活，我们把一些常用的配置设为优先从环境变量中读取，如果没有读取到，则使用默认值：

```python
SECRET_KEY = os.getenv('SECRET_KEY', 'dev')
```

以第一个配置变量为例，`os.getenv('SECRET_KEY', 'dev')` 表示读取系统环境变量 `SECRET_KEY` 的值，如果没有获取到，则使用 `dev`。

> **注意** 像密钥这种敏感信息，保存到环境变量中要比直接写在代码中更加安全。

更新后的工厂函数接受传入对应配置类名称（默认设为 development），然后获取对应的配置类，并调用 `app.config.from_object()` 方法将配置更新到程序中。同时我们将注册蓝本、初始化扩展、错误处理函数、自定义命令等操作移动到工厂函数中：

```python
from flask import Flask

def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 注册蓝本
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

	# 初始化扩展
	db.init_app(app)
	login_manager.init_app(app)

	# 上下文处理函数
	@app.context_processor
	def inject_user():  # 函数名可以随意修改
	    user = db.session.execute(select(User)).scalar()
	    return dict(user=user)

	# 错误处理函数
	...

	# 自定义命令函数
	...

	return app
```

因为扩展对象在程序其他部分需要用到，所以不能放到工厂函数中创建。为了支持工厂函数模式，扩展都提供了一个 `init_app()` 方法，可以用来分离扩展对象的创建和初始化：

```python
# 创建扩展对象，这时不传入程序实例 app
db = SQLAlchemy(model_class=Base)
login_manager = LoginManager()

def create_app(config_name='development'):
    
	# 在工厂函数中调用 init_app 初始化扩展，传入程序实例 app
	db.init_app(app)
	login_manager.init_app(app)

	return app
```

除此之外，我们还会遇到一个问题——没有一个程序实例 app 可以使用。因此在配置数据库 URI 时，我们改为从当前文件而不是 `app.root_path` 来获取基础路径：

```python
BASE_DIR = Path(__file__).resolve().parent
```

对于其他需要使用到程序实例的情况，可以使用代理变量 current_app，它类似 Flask-Login 提供的 current_user 变量，会返回当前程序实例的代理对象。因为程序实例在工厂函数被调用后才会存在，确保你只在视图函数、命令行函数等内部访问它：

```python
from flask import current_app

@main_bp.route('/', methods=['GET', 'POST'])
def index():
    current_app.logger.debug('Visited index page')
    # ...
```

在模板中则可以直接使用 current_app 对象：

```jinja
<p>Debug Mode: {{ current_app.config['DEBUG'] }}</p>
```

Flask 在执行 flask run 命令时，也包含自动寻找工厂函数的设置。它默认会从 app.py 或 wsgi.py 文件中寻找名为 create_app 或 make_app 的工厂函数，并调用它获取程序实例。因为我们的工厂函数现在存放在 app.py 中，所以仍然可以直接执行 flask run 来运行程序： 

```shell
(.venv) $ flask run
```

与此同时，你可以通过 `--app` 参数或环境变量 `FLASK_APP` 来指定工厂函数：

```
FLASK_APP=hello:create_app
```

也可以给出参数，比如：

```
FLASK_APP=hello:create_app(config_name='development')
```

## 使用包组织代码

随着代码增多，你会发现 app.py 变得越来越复杂，找到特定部分的代码开始变得困难。在这一小节，我们会创建一个包，然后把 app.py 中的代码按照类别分别放到多个模块里。下面是我们需要执行的一系列操作（这些操作你也可以使用文件管理器或编辑器完成）：

```bash
$ mkdir watchlist  # 创建作为包的文件夹
$ mv static templates watchlist  # 把 static 和 templates 文件夹移动到 watchlist 文件夹内
$ cd watchlist  # 切换进包目录
$ touch __init__.py errors.py models.py commands.py settings.py extensions.py # 创建多个模块
$ mkdir blueprints  # 创建蓝本文件夹
$ touch blueprints/auth.py blueprints/main.py  # 创建蓝本模块
```

我们把这个包称为程序包，包里目前包含的模块和作用如下表所示：

| 模块                         | 作用             |
| -------------------------- | -------------- |
| \_\_init\_\_.py            | 包构造文件，包含工厂函数定义 |
| settings.py                | 程序配置           |
| errors.py                  | 错误处理函数         |
| models.py                  | 模型类            |
| commands.py                | 命令函数           |
| extensions.py              | 扩展相关代码         |
| blueprints/\_\_init\_\_.py | 蓝本子包的构造文件，内容为空 |
| blueprints/main.py         | main 蓝本和相关视图函数 |
| blueprints/auth.py         | auth 蓝本和相关视图函数 |

> **提示** 除了包构造文件外，其他的模块文件名你可以自由修改，比如 settings.py 也可以叫 config.py。

工厂函数代码放到包构造文件里（`__init__.py`），如下所示。

*watchlist/\_\_init\_\_.py：工厂函数*

```python
from flask import Flask
from sqlalchemy import select

from watchlist.extensions import db, login_manager
from watchlist.blueprints.main import main_bp
from watchlist.blueprints.auth import auth_bp
from watchlist.models import User
from watchlist.errors import register_errors
from watchlist.commands import register_commands


def create_app(config_name='development'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # 注册蓝本
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)

	# 初始化扩展
	db.init_app(app)
	login_manager.init_app(app)

	# 注册错误处理函数和命令
	register_errors(app)
	register_commands(app)

	# 注册上下文处理函数
	@app.context_processor
	def inject_user():  # 函数名可以随意修改
	    user = db.session.execute(select(User)).scalar()
	    return dict(user=user)

	return app
```

扩展对象的创建和相关操作放到单独的 extensions.py 模块。

*watchlist/extensions.py：扩展定义和设置*

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

login_manager.login_view = 'login'
```

因为 models.py 模块需要导入存放在 extensions.py 中的 db 对象，为了避免循环依赖，`load_user()` 函数中使用的 User 模型类在函数内进行导入。

错误处理函数和自定义命令都放到工厂函数会让函数定义太长，我们也拆分到了单独的模块。以错误处理函数为例，我们定义了一个上层函数 `register_errors()` 来接受传入程序实例。

*watchlist/errors.py：错误处理函数*

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

然后在工厂函数中导入并执行这个函数，以便把错误处理函数注册到程序上：

```python
from watchlist.errors import register_errors


def create_app(config_name='development'):
    app = Flask(__name__)

	register_errors(app)

	return app
```

我们为两个蓝本在 blueprints 子包下分别创建了对应的模块（记得为 blueprints 子包创建一个构造文件 `__init__.py`）。以认证蓝本为例，我们把 auth 蓝本的定义和相关视图函数放到了 auth.py 模块下。

*watchlist/blueprints/auth.py：认证蓝本*

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

其他代码则按照分类分别放到各自的模块中，这里不再给出代码，具体可参考[源码仓库](https://github.com/helloflask/watchlist)。在移动代码之后，注意添加并更新导入语句，比如使用下面的导入语句来导入工厂函数：

```python
from watchlist import create_app
```

使用下面的导入语句来导入扩展对象模型类和扩展对象：

```python
from watchlist.models import User, Movie
from watchlist.extensions import db
```

以此类推。

包名称这里使用了 watchlist，所以导入时要从 watchlist 包导入，如果你使用了更常规的名字，比如 app，那么导入语句也要相应变化：

```python
from app import app, db
from app.models import User, Movie
```

另外，因为现在配置文件放到了 watchlist 包内，为了能正确定位到项目根目录的数据库文件，我们需要更新配置文件中的 `BASE_DIR` 定义，再添加一个 parent 属性：

```python
BASE_DIR = Path(__file__).resolve().parent.parent
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


## 启动程序

因为我们使用包来组织程序，不再是 Flask 默认识别的 app.py，所以在启动开发服务器前需要使用环境变量 `FLASK_APP` 来给出工厂函数所在的模块路径。因为我们的工厂函数定义在包构造文件内（`watchlist/__init__.py`），所以直接写出包名称即可。Flask 会自动调用工厂函数创建程序实例，参数 config_name 将使用默认的 development，对应开发配置。在 .flaskenv 文件中添加下面这行代码：

```
FLASK_APP=watchlist
```

为了更直观，我们也可以在项目根目录创建一个程序入口脚本，将其命名为 app.py：

```python
from watchlist import create_app

app = create_app(config_name='development')
```

最终的项目文件结构如下所示：

```
watchlist
├── .flaskenv
├── app.py  # 可选的入口脚本
└── watchlist  # 程序包
    ├── __init__.py
    ├── commands.py
    ├── errors.py
    ├── models.py
    ├── settings.py
	├── extensions.py
    ├── blueprints
	│   ├── __main__.py
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


## 本章小结

对于简单的程序或一次性项目，可以不使用蓝本和工厂函数。但是对于会扩展规模的项目，使用这些组织技巧可以让你为未来的长期开发和维护做好准备。结束前，让我们提交代码：

```bash
$ git add .
$ git commit -m "Organize application with package and blueprint"
$ git push
```

## 进阶提示

- 如果你是[《Flask Web 开发实战》](http://helloflask.com/book/1)的读者，第 7 章介绍了使用包组织程序，第 8 章介绍了大型项目结构以及如何使用蓝本和工厂函数组织程序。 
- 查看《Flask Web 开发实战》示例程序 [Greybook 的源码](https://github.com/greyli/greybook)，了解更大的程序的代码组织结构示例。
