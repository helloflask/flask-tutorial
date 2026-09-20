# 第 1 章：代码清单

每一章后面都会有一个代码清单章节，这里会列出上一章所有的代码变动和相关命令。本章的目的是提供一个更清晰的代码改动列表，供你在编写代码时作为参考。

## 目录

```text
watchlist/
├── .venv/
├── .git/
└── .gitignore
```

## 代码

### .gitignore

```text
*.pyc
*~
__pycache__
.DS_Store
.venv
```

## 命令

### 创建项目文件夹

```bash
$ mkdir watchlist
$ cd watchlist
```

### 设置 Git 身份信息

```bash
$ git config --global user.name "Your Name"  # 替换成你的名字
$ git config --global user.email "your_email@example.com"  # 替换成你的邮箱地址
```

### 初始化 Git 仓库

```bash
$ git init
Initialized empty Git repository in ~/watchlist/.git/
```

### 创建 .gitignore 文件

```bash
$ nano .gitignore
```

### 生成 SSH 密钥

```bash
$ ssh-keygen -t ed25519 -C "your_email@example.com"
$ cat ~/.ssh/id_ed25519.pub
```

### 设置远程仓库

```bash
$ git remote add origin git@github.com:greyli/watchlist.git  # 注意更换地址中的用户名
```

### 创建虚拟环境

```bash
$ python -m venv .venv  # Windows
```

或：

```bash
$ python3 -m venv .venv  # Linux 和 macOS
```

### 激活虚拟环境

```bash
$ .venv\Scripts\activate  # Windows
```

或：

```bash
$ source .venv/bin/activate  # Linux 或 macOS
```

### 安装 Flask

```bash
(.venv) $ pip install flask
```

### 提交代码

```bash
$ git add .
$ git commit -m "Init the project"
$ git push -u origin main
```
