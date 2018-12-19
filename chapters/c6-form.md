# 第 6 章：表单

在 HTML 页面里，我们需要编写表单来获取用户输入。一个典型的表单元素如下所示：

```html
<form method="post">  <!-- 指定提交方法为 POST -->
    名字：<input type="text" name="name"><br>  <!-- 文本输入框 -->
    职业：<input type="text" name="occupation"><br>  <!-- 文本输入框 -->
    <input type="submit" name="submit" value="提交">  <!-- 提交按钮 -->
</form>
```

编写表单的 HTML 代码有下面几个需要注意点：

* 在 `<form>` 标签里使用 method 将提交表单数据的 HTTP 请求方法指定为 POST。如果不指定，则会默认使用 GET 方法，这会将表单数据通过 URL 提交，容易导致数据泄露，而且不适用与包含大量数据的情况。
* `<input>`元素必须要指定 `name` 属性，否则无法提交数据，在服务器端，我们也需要通过这个 `name`值来获取对应字段的数据。

## 编写创建新条目页面

我们需要为程序编写一个创建电影条目的页面，如下所示：

* templates/create.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>New item - {{ name }}的 Watchlist</title>
</head>
<body>
    <h2>Create New Item</h2>
    <form method="post">
        Name：<br>
        <input type="text" name="name"><br>  <!-- 文本输入框 -->
        Year：<br>
        <input type="text" name="year"><br>  <!-- 文本输入框 -->
        <input type="submit" name="submit">  <!-- 提交按钮 -->
	</form>
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

在 app.py 里创建一个新的视图函数来返回这个模板：

```python
@app.route('/create')
def create():
    return render_template('create.html', name=name)
```

看起来相当简单，现在我们再在主页模板（index.html）里添加一个链接指向这个页面：

```jinja2
<a href="{{ url_for('create') }}">New Item</a>
```

现在，当我们点击主页上的这个链接，就会访问 /create，打开创建新条目的页面。

接下来，我们需要考虑如何获取提交的表单数据。

## 获取表单数据

默认情况下，当表单中的提交按钮被按下，浏览器会创建一个新的请求，发往当前 URL。比如我们为 /create 返回的表单，提交后就会被发送到这个地址。不同的是，因为我们在模板里为表单定义了 POST 方法。为了能够处理 POST 请求，我们需要修改一下视图函数：

```python
@app.route('/create', methods=['GET', 'POST'])
def create():
    return render_template('create.html', name=name)
```

在 app.route() 装饰器里，我们可以用 methods 关键字传递一个包含 HTTP 方法字符串的列表，表示这个视图函数处理哪种方法类型的请求。默认只接受 GET 请求，如果你对不接受 POST 请求的视图函数发送 POST 请求，Flask 会自动返回一个 405 错误提示（Method Not Allowed）。

现在，GET 请求和 POST 请求都会触发这个 create() 函数，两种方法的请求有不同的处理逻辑，为了在函数内加以区分，我们添加一个 if 判断：

```python
from flask import request

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        pass  # 如果是提交表单的 POST 请求，则执行 if 内的代码
    return render_template('create.html', name=name)
```

因为提交表单的的请求会是 POST 请求，所以会执行 if 语句内的代码；对于普通的 GET 请求，则会执行 if 外部的代码，正常渲染模板。下面我们在 if 语句内编写代码获取并处理表单数据：

```python
from flask import request

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        # 获取表单数据
        title = request.form.get('title')
        year = request.form.get('year')
        # 验证数据
        if not title or not year:
            return redirect(url_for('create'))
        # 保存表单数据到数据库
        # 重定向回主页
        return redirect(url_for('index'))
    return render_template('create.html', name=name)
```



## flash 消息

## 使用模板继承组织模板



### 编写基础模板

我们首先需要创建的是程序的主界面，我们把它命名为index.html。

因为每一个页面都是一个 HTML 文件，这就意味着我们需要创建大量的 HTML 页面，这会带来下面这些问题：

- 导航栏、页脚等信息在每一个页面都要包含，那么久意味着每一个页面都包含这部分重复代码。如果哪天想要改动导航栏或页脚，那就要同时修改所有 HTML 文件。

为了避免这种情况，Jinja2 支持**模板继承**，这和 Python 类的继承概念很接近。我们可以定义一个基础模板，简称为基模板或父模板。基模板里包含 HTML 基本结构和导航栏、页脚等其他页面共用的页面元素。页面里需要在实际的子模板中追加或重写的部分则可以定义成块。

块使用 block 标签创建，`{% block 块名称 %}` 作为开始标记，`{% endblock %}` 或 `{% endblock 块名称 %}` 作为结束标记。在子模板里，通过定义一个同样名称的块，你就可以向基模板的对应块位置追加内容或是重写块的内容。

```html
<!DOCTYPE html>
<html lang="en">
<head>
    {% block head %}
        <meta charset="utf-8">
        <title>{% block title %}{% endblock title %} - {{ config.BLOG_TITLE }}</title>
        <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css">
    {% endblock %}
</head>
<body>

<nav>
    <ul>
        <li><a href="{{ url_for('blog.index') }}"><strong>{{ config.BLOG_TITLE }}</strong></a></li>
        <li><a href="{{ url_for('blog.index') }}">主页</a></li>
        {% if current_user.is_authenticated %}
            <li><a href="{{ url_for('blog.create_post') }}">添加条目</a></li>
        {% endif %}
    </ul>
</nav>

<main>
    {% block content %}{% endblock %}
</main>

<footer>
    ...
</footer>

</body>
</html>
```



### 创建子模板



传递提示消息



移动到附录章节：自定义错误页面



## 进阶提示

使用 Flask-WTF

使用 CSRFProtect

编写宏渲染表单字段

使用 Bootstrap-Flask 渲染表单

删除按钮的行内 js 代码改为事件监听函数，写到单独的 js 文件里。