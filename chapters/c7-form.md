# 第 7 章：表单

在 HTML 页面里，我们需要编写表单来获取用户输入。一个典型的表单如下所示：

```html
<form method="post">  <!-- 指定提交方法为 POST -->
    名字：<input type="text" name="name"><br>  <!-- 文本输入框 -->
    职业：<input type="text" name="occupation"><br>  <!-- 文本输入框 -->
    <input type="submit" name="submit" value="登录">  <!-- 提交按钮 -->
</form>
```

编写表单的 HTML 代码有下面几点需要注意：

* 在 `<form>` 标签里使用 `method` 属性 将提交表单数据的 HTTP 请求方法指定为 POST。如果不指定，则会默认使用 GET 方法，这会将表单数据通过 URL 提交，容易导致数据泄露，而且不适用于包含大量数据的情况。
* `<input>`元素必须要指定 `name` 属性，否则无法提交数据，在服务器端，我们也需要通过这个 `name`值来获取对应字段的数据。

## 创建新条目

创建新条目可以放到一个新的页面来实现，也可以直接在主页实现。这里我们采用后者，首先在主页模板里添加一个表单：

*templates/index.html：添加创建新条目表单*

```html
<p>{{ movies|length }} Titles</p>
<form method="post">
    Name <input type="text" name="name" autocomplete="off" required>
    Year <input type="text" name="year" autocomplete="off" required>
    <input type="submit" name="submit" value="Add">
</form>
```

在这两个输入字段中，`autocomplete` 属性设为 `off` 来关闭自动完成（按下输入框不显示历史输入记录）；另外还添加了 `required` 标志属性，如果用户没有输入内容就按下了提交按钮，浏览器会显示错误提示。

接下来，我们需要考虑如何获取提交的表单数据。

## 处理表单数据

默认情况下，当表单中的提交按钮被按下，浏览器会创建一个新的请求，默认发往当前 URL（在 `<form>` 元素使用 `action` 属性可以自定义目标 URL）。

因为我们在模板里为表单定义了 POST 方法，当你输入数据，按下提交按钮，一个 POST 请求会发往根地址。你会看到一个 405 Method Not Allowed 错误提示。这是因为处理根地址请求的 `index` 视图默认只接受 GET 请求。

**提示** 在 HTTP 中，GET 和 POST 是两种最常见的请求方法，其中 GET 请求用来请求资源，而 POST 则用来创建 / 更新资源。我们访问一个链接，通常会发送 GET 请求，而提交表单通常会发送 POST 请求。

为了能够处理 POST 请求，我们需要修改一下视图函数：

```python
@app.route('/', methods=['GET', 'POST'])
```

在 `app.route()` 装饰器里，我们可以用 `methods` 关键字传递一个包含 HTTP 方法字符串的列表，表示这个视图函数处理哪种方法类型的请求。默认只接受 GET 请求，上面的写法表示同时接受 GET 和 POST 请求。

两种方法的请求有不同的处理逻辑：对于 GET 请求，返回渲染后的页面；对于 POST 请求，则获取提交的表单数据并保存。为了在函数内加以区分，我们添加一个 if 判断：

```python
from flask import request, flash

# ...

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item Created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页

    user = User.query.first()
    movies = Movie.query.all()
    return render_template('index.html', user=user, movies=movies)
```

在 if 语句内，我们编写了处理表单数据的代码，其中涉及 3 个新的知识点，下面来一一了解。

### 请求对象

Flask 会在请求触发后把请求信息放到 request 对象里，你可以从 `flask` 包导入它：

```python
from flask import request
```

因为它在请求触发时才会包含数据，所以你只能在视图函数内部调用它。它包含请求相关的所有信息，比如请求的路径（`request.path`）、请求的方法（`request.method`）、表单数据（`request.form`）、查询字符串（`request.args`）等等。

在上面的 if 语句中，我们首先通过 `request.method` 的值来判断请求方法。在 if 语句内，我们通过 `request.form` 来获取表单数据。`request.form` 是一个特殊的字典，用表单字段的 `name` 属性值可以获取用户填入的对应数据。

```python
if request.method == 'POST':
    title = request.form.get('title')
    year = request.form.get('year')
```

### flash 消息

在用户执行某些动作后，我们通常会在处理完相应的工作后，在页面上显示一个提示消息。最简单的实现就是在视图函数里定义一个包含消息内容的变量，传入模板，然后在模板里渲染显示它。因为这个需求很常用，Flask 内置了相关的函数。其中 `flash()` 用来在视图函数里向模板传递提示消息，`get_flashed_messages()` 则用来在模板中调用显示提示消息。

`flash()` 的用法在上面已经展示过了，首先从 `flask` 包导入 `flash` 函数：

```python
from flask import flash
```

然后在视图函数里调用，传入要显示的消息内容：

```python
flash('Item Created.')
```

`flash()` 函数在内部会把消息存储到 Flask 提供的 session 对象里。session 用来在请求间存储数据，它会把数据签名后存储到浏览器的 cookie 中，所以我们需要设置签名所需的密钥：

```python
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
```

**提示** 这个密钥在开发时可以随便设置，基于安全的考虑，在部署时应该设置为随机字符，且不应该明文写在代码里， 在部署章节会详细介绍。

下面在基模板（base.html）里使用 `get_flashed_messages()` 函数获取提示消息并显示：

```python
<!-- 插入到导航栏下方 -->
{% for message in get_flashed_messages() %}
	<div class="alert">{{ message }}</div>
{% endfor %}
```

为提示消息增加样式：

```css
.alert {
    position: relative;
    padding: 10px;
    margin-bottom: 10px;
    border: 1px solid transparent;
    color: #004085;
    background-color: #cce5ff;
    border-color: #b8daff;
}
```

通过在 `<input>` 元素内添加 `required` 实现的验证（客户端验证）并不完全可靠，我们还要在服务器端追加验证。

```python
if not title or not year:
    flash('Invalid input.')  # 显示错误提示
    return redirect(url_for('index'))
# ...
flash('Item Created.')  # 显示成功创建的提示
```

**提示** 在真实世界里，你会进行更严苛的验证，比如对数据去除首尾的空格。一般情况下，我们会使用第三方库（比如 [WTForms](https://github.com/wtforms/wtforms)）来实现表单数据的验证工作。

如果输入的某个数据为空，就显示错误提示“Invalid input.”，否则显示成功创建的提示“Item Created.”。

### 重定向响应

```python
if not title or not year:
    flash('Invalid title or year!')  
    return redirect(url_for('index'))  # 重定向回主页
flash('Movie Created!')
return redirect(url_for('index'))  # 重定向回主页
```

## 编辑条目

编辑按钮

编辑页面

编辑视图

## 删除条目

删除表单

删除视图

删除按钮

## 本章小结



## 进阶提示

- 本书主页 & 相关资源索引：[http://helloflask.com/tutorial](http://helloflask.com/tutorial)
- 使用 Flask-WTF
- CSRF 保护问题，使用 CSRFProtect
- 编写宏渲染表单字段
- 使用 Bootstrap-Flask 渲染表单
- 删除按钮的行内 js 代码改为事件监听函数，写到单独的 js 文件里。
- [《Flask Web 开发实战》](http://helloflask.com/book/)第 4 章