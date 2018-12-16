# 第 4 章：使用静态文件

静态文件（static files）和我们的模板概念相反，指的是内容不需要动态生成的文件。比如图片、CSS 文件和 JavaScript 脚本等。在主页上，我们需要引入一个 CSS 文件来为页面添加一些基本的样式，还要在页面中插入一张图片——显示我的头像。

在 Flask 中，我们需要创建一个 static 文件夹来保存静态文件，它应该和程序模块、templates 文件夹在同一目录层级，所以我们在项目根目录创建它：

```bash
$ mkdir static
```

## 在模板中引入静态文件

在 HTML 文件里，引入这些静态文件需要给出资源所在的 URL，为了更加灵活，这些文件的 URL 可以通过 Flask 提供的 url_for() 函数来生成。这里传入的 static 端点是 Flask 内置的视图函数，专门用来提供静态文件服务，它接受 filename 参数来传入相对于 static 文件夹的文件路径。

使用 Flask 自动添加到模板里的函数和对象，比如 `url_for()` 函数

*提示 在 Python 脚本里，这个 `url_for()` 函数需要从 flask 包中导入，而在模板中则可以直接调用。因为 Flask 把一些常用的函数和对象添加到了模板上下文（环境）里。*

- templates/index.html：引入静态文件

```jinja2
<head>
    ...
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css">
</head>

<h2>
    <img src="{{ url_for('static', filename='avatar.jpg') }}" width="50"> {{ user.username }}
</h2>
```

## 添加 CSS 样式

整个页面的样式定义

## flash 消息

