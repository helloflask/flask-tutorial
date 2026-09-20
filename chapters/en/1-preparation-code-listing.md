# Chapter 1: Code listing

Each chapter is followed by a code listing that brings together all the code changes and related commands from that chapter. The aim is to give you a clear reference to use as you write your code.

## Directory structure

```text
watchlist/
├── .venv/
├── .git/
└── .gitignore
```

## Code

### .gitignore

```text
*.pyc
*~
__pycache__
.DS_Store
.venv
```

## Commands

### Create the project directory

```bash
$ mkdir watchlist
$ cd watchlist
```

### Set your Git identity

```bash
$ git config --global user.name "Your Name"  # Replace with your name
$ git config --global user.email "your_email@example.com"  # Replace with your email address
```

### Initialize the Git repository

```bash
$ git init
Initialized empty Git repository in ~/watchlist/.git/
```

### Create the .gitignore file

```bash
$ nano .gitignore
```

### Generate an SSH key

```bash
$ ssh-keygen -t ed25519 -C "your_email@example.com"
$ cat ~/.ssh/id_ed25519.pub
```

### Set the remote repository

```bash
$ git remote add origin git@github.com:greyli/watchlist.git  # Replace the username in the URL
```

### Create a virtual environment

```bash
$ python -m venv .venv  # Windows
```

Or:

```bash
$ python3 -m venv .venv  # Linux and macOS
```

### Activate the virtual environment

```bash
$ .venv\Scripts\activate  # Windows
```

Or:

```bash
$ source .venv/bin/activate  # Linux or macOS
```

### Install Flask

```bash
(.venv) $ pip install flask
```

### Commit the code

```bash
$ git add .
$ git commit -m "Init the project"
$ git push -u origin main
```
