# Chapter 1: Getting ready

Before you start learning Flask development with this book, I assume that you already know the basics of Python and web development, mainly HTML and CSS. If you do not, you can start with these online resources:

* [Build a simple website using HTML, CSS, and JavaScript](https://learn.microsoft.com/zh-cn/training/modules/get-started-with-web-development/?WT.mc_id=OSS-MVP-5003485) — Microsoft Learn (Chinese)
* [Getting started with the web](https://developer.mozilla.org/zh-CN/docs/learn) — MDN (Chinese)
* [The Python Tutorial](https://docs.python.org/zh-cn/3/tutorial/) — Python.org (Chinese)

This tutorial does not require a particular operating system: you can use Windows, macOS, or Linux. You will need Python 3.9 or later, though.

## Install an editor and a browser

Everyone has different preferences for code editors, so choose whichever you like. You might prefer a full-featured IDE (integrated development environment) such as [PyCharm](https://www.jetbrains.com/pycharm/), or a lighter editor such as [VS Code](https://code.visualstudio.com/) or [Sublime Text](https://www.sublimetext.com/). For your browser, I suggest [Firefox](https://www.mozilla.org/en-US/firefox/new/) or [Chrome](https://www.google.com/chrome/).

## Use the command line

Throughout this book, you will use a command-line window to perform many tasks. On Windows, PowerShell is recommended over CMD.exe. On macOS and Linux, you can use your preferred terminal application (the default is Terminal). Open your terminal and try a simple command, `whoami` (“Who am I?”):

```bash
$ whoami
greyli
```

This command prints the name of the current user on your computer. Other common commands include `cd`, which changes directories (**c**hange **d**irectory), and `mkdir`, which creates a directory (**m**a**k**e **dir**ectory). Commands for the same task may differ between operating systems; this book will point out those differences where needed.

First, create a folder for our application:

```bash
$ mkdir watchlist
$ cd watchlist
```

Unless stated otherwise, from this point on the book assumes that your working directory is the project's root directory, watchlist/.

To check that Python is installed correctly, run the following command and make sure it does not report an error:

```bash
$ python --version
Python 3.9.10
```

On Linux and macOS, the command for Python 3 is `python3` (and the corresponding pip command is `pip3`):

```bash
$ python3 --version
Python 3.9.10
```

On Windows, consider using [WSL](https://learn.microsoft.com/en-us/windows/wsl/install?WT.mc_id=OSS-MVP-5003485) (Windows Subsystem for Linux, which runs a Linux environment on Windows) or Git Bash while working through this tutorial. Git Bash is a terminal application included with Git for Windows; we will cover installing Git in the next section. It provides commands (programs) normally available on Linux or macOS, such as ls, cat, nano, and ssh, which we will use later.

> **Tip** If you continue using CMD.exe or PowerShell for this tutorial, keep these command differences in mind:
>
> - In CMD.exe, use `dir` instead of `ls`, and `type` instead of `cat`.
> - You can replace `nano` with the command for another installed editor. For example, use `code` for VS Code. You can also create and edit files through your editor's graphical interface.
> - On Windows 10 version 1809, OpenSSH (which provides `ssh` and `ssh-keygen`) can be installed as an optional component through the control panel ([documentation](https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse)). On older versions of Windows, you can install a third-party SSH client such as PuTTY, or simply use Git Bash.

## Use Git

[Git](https://git-scm.com) is a popular version control tool. It records changes to your application's source code and files and helps people collaborate on development. You can think of it as a tool for keeping a history of changes to your code.

If you are not familiar with Git yet, that is fine. You can follow the commands in the book for now and learn how it works when you have time. The first step is to [install Git](https://git-scm.com/book/zh/v1/%E8%B5%B7%E6%AD%A5-%E5%AE%89%E8%A3%85-Git) on your computer (installation guide in Chinese).

> **Note** For the basics, read the short tutorial [Git — the simple guide](http://rogerdudler.github.io/git-guide/index.zh.html) or the guided [Introduction to Git](https://docs.microsoft.com/zh-cn/learn/modules/intro-to-git?WT.mc_id=OSS-MVP-5003485) module on Microsoft Learn (both links are in Chinese).

After installation, check the version from the command line. If no error appears, Git is installed correctly:

```bash
$ git --version
git version 2.17.1
```

Tell Git who you are so that it can record your identity when you commit changes to a repository:

```bash
$ git config --global user.name "Your Name"  # Replace with your name
$ git config --global user.email "your_email@example.com"  # Replace with your email address
```

Now create a Git repository in the project folder. This creates a .git folder in the project root:

```bash
$ git init
Initialized empty Git repository in ~/watchlist/.git/
```

By default, Git notices changes to files in the project folder (the repository), but you do not need to keep a history of every incidental file. Create a .gitignore file in the project root to specify which files to ignore. Because its contents are simple, we will create it directly from the command line with nano:

```bash
$ nano .gitignore
```

In nano, enter these patterns for common files to ignore:

```text
*.pyc
*~
__pycache__
.DS_Store
```

Press Control + O, then Enter to save, and Control + X to exit. In later chapters, we will also use nano to create simple files. You can use your editor's graphical interface for these steps instead.

## Host your application on GitHub (optional)

This step is optional. Hosting your application on a platform such as GitHub, GitLab, or Bitbucket makes backups, collaboration, and deployment easier. These platforms act as Git servers: you can create a remote repository for your local repository and upload your work to it.

First, sign up for a GitHub account. Visit the [sign-up page](https://github.com/join), follow the instructions, and sign in so that you are ready for the next steps.

> **Note** To learn the basics, work through the guided [Introduction to GitHub](https://docs.microsoft.com/zh-cn/learn/modules/introduction-to-github?WT.mc_id=OSS-MVP-5003485) module on Microsoft Learn (Chinese).

### Set up an SSH key

Pushing local changes to a remote repository requires authentication. When you connect over SSH, you can set up an SSH key to authenticate without entering your account credentials each time.

Generate an SSH key pair with the following command, replacing the email address with your own:

```bash
$ ssh-keygen -t ed25519 -C "your_email@example.com"
```

Press Enter at each prompt to accept the defaults. Two files, id_ed25519 and id_ed25519.pub, will be created in the .ssh folder in your home directory. The first is your private key, which you must keep secret. The second is your public key, which is used to authenticate you and is the key you will save on GitHub. Display its contents with:

```bash
$ cat ~/.ssh/id_ed25519.pub
ssh-ed25519 AAAAC3Nza...characters omitted...3aph book@greyli
```

If your version of OpenSSH is too old to support the more secure Ed25519 algorithm, use RSA instead with the following command:

```shell
$ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

The resulting key files will be named id_rsa and id_rsa.pub. The command to display the public key becomes:

```shell
$ cat ~/.ssh/id_rsa.pub
```

Select and copy the public key output, then visit GitHub's [SSH settings page](https://github.com/settings/keys) (your profile picture in the navigation bar → Settings → SSH and GPG keys). Click **New SSH key**, paste the copied text into the **Key** field, and enter a title such as “My PC”. Finally, click **Add SSH key** to save it.

### Create a remote repository

Visit the [new repository page](https://github.com/new) (“+” in the navigation bar → New repository). Enter “watchlist” in **Repository name**, choose whether the repository should be public or private and set any other options, then click **Create repository**.

Because we have already created a local repository, we need to specify its remote repository address:

```bash
$ git remote add origin git@github.com:greyli/watchlist.git  # Replace the username in the address
```

This associates a remote named “origin” with the local repository. **Replace “greyli” in the repository address with your own GitHub username.**

If you have not created a local repository, you can clone the remote repository instead. This creates a folder named watchlist in the current directory:

```bash
$ git clone git@github.com:greyli/watchlist.git  # Replace the username in the address
```

## Create a virtual environment

A virtual environment is a Python interpreter environment that is separate from your global Python environment. It lets you:

* Keep the global environment clean
* Use different versions of the same library in different environments
* Record and manage the dependencies for a particular project more easily

We will use Python 3's built-in venv module to create a virtual environment. Run the following command to create one for the current project:

```bash
$ python -m venv .venv  # Windows
```

Or:

```bash
$ python3 -m venv .venv  # Linux and macOS
```

> **Tip** The last argument is the virtual environment's name. You can choose any name, such as venv, env, .venv, or “projectname-venv”. We use .venv here.

This creates a folder named .venv in the current directory containing the Python interpreter environment. Its contents do not need to be committed to Git, so add `.venv` to the .gitignore file in the project root:

```text
*.pyc
*~
__pycache__
.DS_Store
.venv
```

## Activate the virtual environment

After creating the virtual environment, activate it with the following command, which runs the activation script inside the environment:

```bash
$ .venv\Scripts\activate  # Windows
```

> **Tip** If you use Git Bash on Windows, run `source .venv/Scripts/activate` instead.

Or:

```bash
$ source .venv/bin/activate  # Linux or macOS
```

The virtual environment's name now appears before the command prompt, showing that activation succeeded:

```bash
(.venv) $
```

Once the virtual environment is active, you can use `python` and `pip` to run the Python and pip programs inside it, regardless of your operating system or Python version. These programs are in the same directory as the activation script: `.venv\Scripts\` on Windows, or `.venv/bin/` on Linux and macOS.

To leave the virtual environment, run `deactivate`:

```bash
(.venv) $ deactivate
$
```

> **Important** Unless stated otherwise, activate the virtual environment before running any commands in the rest of this book, apart from Git commands.

> **Tip** If you are in China, consider configuring pip to use a local PyPI mirror—the server from which it downloads packages—to improve download speed. See [this article](https://zhuanlan.zhihu.com/p/57872888) (Chinese) for details.

## Install Flask

With the virtual environment active, install Flask:

```bash
(.venv) $ pip install flask
```

This installs Flask and its dependencies into the active virtual environment, rather than the global interpreter environment. At the time of writing, the latest Flask version is 3.1.2. You may get a newer version when you run this command. To install version 3.1.2 specifically, use:

```bash
(.venv) $ pip install flask==3.1.2
```

> **Tip** If you are not using a virtual environment and have already installed Flask, remember to update it to the latest version with `pip install -U flask`.

## Manage virtual environments and dependencies with uv (optional)

uv (<https://github.com/astral-sh/uv>) is a Python dependency and virtual environment management tool written in Rust. We have just learned how to create virtual environments with venv and install packages with pip. You can use uv to speed up these operations. This section is optional; a brief introduction is enough for now.

First, install uv. On macOS or Linux:

```shell
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows:

```shell
$ powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

You can also install it with pip:

```shell
$ pip install --user uv
```

Now recreate the virtual environment with `uv venv`:

```shell
$ uv venv
```

uv also uses .venv as the default virtual environment folder, so it will ask whether to overwrite the existing environment. Press y to confirm. Now activate it:

```shell
$ source .venv/bin/activate  # On Windows, use .venv\Scripts\activate
```

Then install dependencies with `uv pip`:

```shell
(.venv) $ uv pip install flask
```

Besides using `uv pip` for pip-style operations, you can use uv's own dependency management system throughout your project. See <https://docs.astral.sh/uv/guides/projects/> for details.

uv can also manage Python versions. Here are a few common commands.

Install specific Python versions. You can then use `python3.10`, `python3.11`, and `python3.12` to start the corresponding interpreters:

```shell
$ uv python install 3.10 3.11 3.12
```

Create a virtual environment with a specific Python version:

```shell
$ uv venv --python 3.12
```

Pin the Python version for the current project. This writes the version to a `.python-version` file. This book leaves that file out of the repository, so add its name to .gitignore:

```shell
$ uv python pin 3.12
```

## Chapter summary

You are now ready to learn Flask and develop your application. Use `git status` to see which files in the repository have changed:

```bash
$ git status
```

Commit your changes to Git and push them to the remote repository you created on GitHub:

```bash
$ git add .
$ git commit -m "Init the project"
$ git push -u origin main # Skip this command if you are not hosting the repository on GitHub; the same applies in later chapters
```

The `-u` option in the last command sets the default destination repository and branch for future pushes. After that, you can use `git push` on its own. On GitHub, you can view your repository at [https://github.com/your-username/watchlist](https://github.com/helloflask/watchlist).

## Going further

* If you plan to release your application as open source, add a README.md file to introduce it and a LICENSE file to state its license in the project root. Visit [Open Source Guides](https://opensource.guide/) to learn more.
