# 第 2 章：代码清单

## 目录

```text
watchlist/
├── app.py
├── .env
├── .flaskenv
└── .gitignore
```

> **提示** 实际目录中的 .venv 和 .git 没有列出。
## 代码

### app.py

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'
```

### .gitignore

```diff
*.pyc
*~
__pycache__
.DS_Store
.venv
+.env
```

## 命令

### 激活虚拟环境

```bash
$ .venv\Scripts\activate  # Windows
```

或：

```bash
$ source .venv/bin/activate  # Linux 或 macOS
```

> **提示** 确保在执行 `flask`、`python`、`pip` 等命令前激活了虚拟环境，后续章节不再列出激活命令。

### 启动程序

默认启动命令：

```bash
(.venv) $ flask run
```

以调试模式启动程序：

```bash
(.venv) $ flask run --debug
```

设置不同的端口：

```bash
(.venv) $ flask run --debug --port 8000
```

### 安装 python-dotenv

```bash
(.venv) $ pip install python-dotenv
```

### 创建 .env 和 .flaskenv 文件

```bash
$ touch .env .flaskenv
```

### 提交代码

```bash
$ git add .
$ git commit -m "Add a minimal home page"
$ git push
```
