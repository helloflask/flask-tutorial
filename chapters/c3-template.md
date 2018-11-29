# 模板和静态文件

在一般的 Web 程序里，访问一个地址通常会返回一个包含各类信息的HTML页面。因为我们的程序是动态的，页面中的某些信息需要根据不同的情况来进行调整，比如对登录和未登录用户显示不同的信息，所以页面需要在用户访问时动态生成。

我们把包含变量和运算逻辑的HTML或其他格式的文本叫做**模板**，执行这些变量替换和逻辑计算工作并最终获得文本的过程被称为**渲染**，这个工作由我们这一章要学习使用的模板渲染引擎——Jinja2来完成。

按照默认的设置，Flask 会从和程序所在模板同级目录的 templates 文件夹中寻找模板，我们的程序目前存储在项目根目录的 app.py 文件里，所以我们要在项目根目录创建这个文件夹：

```bash
$ mkdir templates
```

## 模板基本语法

在社交网站上，每个人都有一个主页，通过使用 Jinja 我们就可以写出一个通用的模板：

```jinja2
<h1>{{ username }}的个人主页</h1>
{% if bio %}
    <p>{{ bio }}</p>  {# 这里的缩进只是为了可读性，不是必须的 #}
{% endif %}  {# 大部分 Jinja 语句都需要声明关闭 #}
```

Jinja 的语法和 Python 大致相同，你在后面会陆续接触到一些常见的用法。你只需要添加特定的定界符将 Jinja 语法标记出来就可以了。在上面这个模板里，我们可以看到三种常用的定界符：

- `{{ ... }}` 用来标记变量。
- `{% ... %}` 用来标记语句，比如 if 语句，for 语句等。
- `{# ... #}` 用来写注释。

这些变量需要在渲染的时候传递进去

仅仅这些？当然不是，除了渲染你自己传递进去的变量、函数，你还可以在模板里做这些事情：

* 对变量调用过滤器
* 使用 Flask 自动添加到模板里的函数和对象，比如

【待补全】

## 编写主页模板

主页需要显示电影条目列表、你的信息、页脚，大概需要下面这些代码：

* templates/index.html：主页模板

```jinja2
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>{{ name }}的 Watchlist</title>
</head>
<body>
    <h2>{{ name }}</h2>
    {% if bio %}  {# 如果 bio 变量存在 #}
        <i>{{ bio }}</i>  {# 显示 bio 的值 #}
    {% else %}   {# 否则显示下面这行文字 #}
        <i>还没来得及写自我介绍。</i>
    {% endif %}  {# 使用 endif 标签结束 if 语句 #}
    {# 使用 length 过滤器获取 movies 变量的长度 #}
    <h5>{{ name }}的 Watchlist （{{ movies|length }}）:</h5>
    <ul>
        {% for movie in movies %}  {# 迭代 movies 变量 #}
        <li>{{ movie.name }} - {{ movie.year }}</li>
        {% endfor %}  {# 使用 endfor 标签结束 for 语句 #}
    </ul>
    <footer>
        <small>
            &copy; 2018 <a href="http://greyli.com">Grey Li</a> /
            <a href="https://github.com/greyli/watchlist">GitHub</a> /
            <a href="http://helloflask.com">HelloFlask</a>
        </small>
	</footer>
</body>
</html>
```

把这个文件保存为 index.html，放在 templates 目录下。

为了方便对变量进行处理，Jinja2 提供了一些过滤器，语法形式如下：

```jinja2
{{ 变量 | 过滤器 }}
```

左侧是变量，右侧是过滤器名。比如，上面的模板里使用的 length 用来获取长度，类似 Python 里的 len() 函数。

*提示 访问 http://jinja.pocoo.org/docs/2.10/templates/#list-of-builtin-filters 查看所有可用的过滤器。*

## 渲染主页模板

为了模拟页面渲染，我们需要先创建一些虚拟数据，用来填充页面内容：

* app.py：定义虚拟数据

```python
name = 'Grey Li'
bio = 'A boy who loves movies and music.'
movies = [
    {'name': 'My Neighbor Totoro', 'year': '1988'},
    {'name': 'Three Colours trilogy', 'year': '1993'},
    {'name': 'Forrest Gump', 'year': '1994'},
    {'name': 'Perfect Blue', 'year': '1997'},
    {'name': 'The Matrix', 'year': '1999'},
    {'name': 'Memento', 'year': '2000'},
    {'name': 'The Bucket list', 'year': '2007'},
    {'name': 'Black Swan', 'year': '2010'},
    {'name': 'Gone Girl', 'year': '2014'},
    {'name': 'CoCo', 'year': '2017'},
]
```

render_template() 函数可以把模板渲染出来，传入模板的名称即可。为了让模板可以正确渲染，我们需要把模板内部使用的变量通过关键字参数传入这个函数：

* app.py：返回渲染好的模板作为响应

```python
from flask import render_template

...

@app.route('/')
def index():
    return render_template('index.html', name=name, bio=bio, movies=movies)
```

最终，这个视图函数最后返回的不再是一行问候，而是一个 HTML 页面。在传入 render_template() 的关键字参数中，左边的 movies 是模板中使用的变量名称，右边的 movies 则是该变量指向的实际对象。

*提示 这里传入的 username 和 bio 是字符串，movies 是字典，但能够传入并在模板里使用的不只这两种数据结构，你也可以传入元组、列表、函数等。*

## 使用静态文件

静态文件（static files）和我们的模板概念相反，指的是内容不需要动态生成的文件。比如图片、CSS 文件和 JavaScript 脚本等。在主页上，我们需要引入一个 CSS 文件来为页面添加一些基本的样式，还要在页面中插入一张图片——显示我的头像。

在 Flask 中，我们需要创建一个 static 文件夹来保存静态文件，它应该和程序模块、templates 文件夹在同一目录层级，所以我们在项目根目录创建它：

```bash
$ mkdir static
```

在 HTML 文件里，引入这些静态文件需要给出资源所在的 URL，为了更加灵活，这些文件的 URL 可以通过 Flask 提供的 url_for() 函数来生成。这里传入的 static 端点是 Flask 内置的视图函数，专门用来提供静态文件服务，它接受 filename 参数来传入相对于 static 文件夹的文件路径。

*提示 在 Python 脚本里，这个 url_for() 函数需要从 flask 包中导入，而在模板中则可以直接调用。因为 Flask 把一些常用的函数和对象添加到了模板上下文（环境）里。*

* templates/index.html：引入静态文件

```jinja2
<head>
    {% block head %}
    ...
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css">
    {% endblock %}
</head>

<h2>
    <img src="{{ url_for('static', filename='avatar.jpg') }}" width="50"> {{ user.username }}
</h2>
```

## 本章小结

这一章我们编写了一个基本的主页。

结束前，让我们提交代码：

```bash
$ git add .
$ git commit -m "Add index page template"
$ git push
```

## 进阶提示

* 使用 Faker 可以实现自动生成虚拟数据，它支持丰富的数据类型，比如时间、人名、地名等等……
* 除了过滤器，Jinja2 还在模板中提供了一些测试器、全局函数可以使用，除此之外，还有更丰富的控制结构支持，有一些我们会在后面学习到，更多的内容则可以访问 [Jinja2 文档](http://jinja.pocoo.org/docs/2.10/templates/)学习。
* 如果你是《Flask Web 开发实战》的读者，模板相关内容可以在第 3 章《模板》找到，Faker 相关内容可以在第 7 章找到。