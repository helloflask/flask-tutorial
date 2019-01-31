# 第 1 章：准备工作

在通过这本书学习 Flask 开发前，我假设你了解了 Python 和 HTML 的基础知识。你的 Python 版本可以是 2.7，也可以是 3.3 及以上版本。电脑的操作系统可以是 Windows，也可以是 macOS 或 Linux。

## 安装编辑器和浏览器

对于编辑器来说，每个人都有不同的偏好，你可以自由选择。可以选择功能丰富的IDE（集成开发环境），比如 [PyCharm](https://www.jetbrains.com/pycharm/)；也可以选择相对轻量的编辑器，比如 [Atom](https://atom.io/) 或 [Sublime Text](https://www.sublimetext.com/)。浏览器建议使用 [Firefox](https://www.mozilla.org/en-US/firefox/new/) 或 [Chrome](https://www.google.com/chrome/)。

## 使用命令行

在本书中，你需要使用命令行窗口来执行许多操作。你可以使用 Windows 下的 cmd.exe，或是 macOS 和 Linux 下的终端（Terminal）。下面我们执行一个最简单的 `whoami` 命令（即 Who Am I？）：

```bash
$ whoami
greyli
```

这个命令会打印出当前计算机用户的名称。其他常用的命令还有 `cd` 命令，用来切换目录（**c**hange **d**irectory）；`mkdir` 命令，用来创建目录（**m**a**k**e **dir**ectory）。在不同的操作系统上，执行某个操作的命令可能会有所不同，在必要的地方，书里会进行提示。

我们先来为我们的程序创建一个文件夹：

```bash
$ mkdir watchlist
$ cd watchlist
```

除非特别说明，从现在开始，本书假设你的工作目录将是在项目的根目录，即 watchlist/ 目录。

为了确保你已经正确安装了 Python，可以执行下面的命令测试是否有报错：

```bash
$ python --version
Python 2.7.11
```

对于 Windows 用户，请使用 [cmder](http://cmder.net)（一个基于  [ConEmu](https://conemu.github.io/) 实现的终端模拟器） 来代替系统自带的 cmd.exe，或是使用安装 Git for Windows 后（下一节）附带的 Git Bash。cmder 集成了 Git Bash，支持一些在 Linux 或 macOS 下才能使用的命令（程序），比如 ls、cat、nano、ssh 等，这些命令我们在后面会用到。

## 使用 Git

[Git](https://git-scm.com) 是一个流行的版本控制工具，我们可以用它来记录程序源码和文件的变动情况，或是在编程时进行多人协作，你可以把它看做一个优雅的代码变动备份工具。

如果你还不熟悉 Git 也没关系，可以先按照书中的命令去做，有时间再去了解原理。现在要做的第一件事就是在你的电脑上[安装 Git](https://git-scm.com/book/zh/v1/%E8%B5%B7%E6%AD%A5-%E5%AE%89%E8%A3%85-Git) （可以执行 `git --help` 命令检查是否已经安装，没有提示“命令未找到（Command not found）”则表示已安装）。

安装后可以在命令行先使用使用下面的命令查看版本，没有报错则表示已正确安装：

```bash
$ git --version
git version 2.17.1
```

为了让 Git 知道你是谁，以便在提交代码到版本仓库的时候进行记录，使用下面的命令设置你的信息：

```bash
$ git config --global user.name "Grey Li"  # 替换成你的名字
$ git config --global user.email "withlihui@gmail.com"  # 替换成你的邮箱地址
```

现在为我们的项目文件夹创建一个 Git 仓库，这会在我们的项目根目录创建一个 .git 文件夹：

```bash
$ git init
Initialized empty Git repository in ~/watchlist/.git/
```

Git 默认会追踪项目文件夹（或者说代码仓库）里所有文件的变化，但是有些无关紧要的文件不需要记录变化，我们在项目根目录创建一个 .gitignore 文件，在文件中写入忽略文件的规则。因为文件内容比较简单，我们直接在命令使用 nano 来创建：

```bash
$ nano .gitignore
```

在 nano 编辑界面写入常见的可忽略文件规则：

```python
*.pyc
*~
__pycache__
.DS_Store
```

使用 Control + O 和 Enter 键保存，然后按下 Control + X 键退出。在后续章节，对于简单的文件，都会使用 nano 创建，这部分操作你也可以使用编辑器来完成。

## 将程序托管到 GitHub（可选）

这一步是可选的，将程序托管到 GitHub、GitLab 或是 BitBucket 等平台上，可以更方便的备份、协作和部署。这些托管平台作为 Git 服务器，你可以为本地仓库创建远程仓库。

首先要注册一个 GitHub 账户，点击访问[注册页面](https://github.com/join)，根据指示完成注册流程。登录备用。

### 设置 SSH 密钥

一般情况下，当推送本地改动到远程仓库时，需要输入用户名和密码。因为传输通常是通过 SSH 加密，所以可以通过设置 SSH 密钥来省去验证账号的步骤。

首先使用下面的命令检查是否已经创建了 SSH 密钥：

```bash
$ cat ~/.ssh/id_rsa.pub
```

如果显示“No such file or directory”，就使用下面的命令生成 SSH 密钥对，否则复制输出的值备用：

```bash
$ ssh-keygen
```

一路按下 Enter 采用默认值，最后会在用户根目录创建一个 .ssh 文件夹，其中包含两个文件，id_rsa 和 id_rsa.pub，前者是私钥，不能泄露出去，后者是公钥，用于认证身份，就是我们要保存到 GitHub 上的密钥值。再次使用前面提到的命令获得文件内容：

```bash
$ cat ~/.ssh/id_rsa.pub
ssh-rsa AAAAB3Nza...省略 N 个字符...3aph book@greyli
```

选中并复制输出的内容，访问 GitHub 的 [SSH 设置页面](https://github.com/settings/keys)（导航栏头像 - Settings - SSH and GPG keys），点击 New SSH key 按钮，将复制的内容粘贴到 Key 输入框里，再填一个标题，比如“My PC”，最后点击“Add SSH key”按钮保存。 

### 创建远程仓库

访问[新建仓库页面](https://github.com/new)（导航栏“+” - New repository），在“Repository name”处填写仓库名称，这里填“watchlist”即可，接着选择仓库类型（公开或私有）等选项，最后点击“Create repository”按钮创建仓库。

因为我们已经提前创建了本地仓库，所以需要指定仓库的远程仓库地址（如果还没有创建，则可以直接将远程仓库克隆到本地）：

```bash
$ git remote add origin git@github.com:greyli/watchlist.git  # 注意更换地址中的用户名
```

这会为本地仓库关联一个名为“origin”的远程仓库，**注意将仓库地址中的“greyli”换成你的 GitHub 用户名**。

## 创建虚拟环境

虚拟环境是独立于 Python 全局环境的 Python 解释器环境，使用它的好处如下：

* 保持全局环境的干净
* 指定不同的依赖版本
* 方便记录和管理依赖

我们将使用 Pipenv 来创建和管理虚拟环境、以及在虚拟环境中安装和卸载依赖包。它集成了 pip 和 virtualenv，可以替代这两个工具的惯常用法。另外，它还集成了 Pipfile，它是新的依赖记录标准，使用 Pipfile 文件记录项目依赖，使用 Pipfile.lock 文件记录固定版本的依赖列表。这两个文件替代了手动通过 requirements.txt 文件记录依赖的方式。

我们首先使用 pip 安装 Pipenv，Windows 系统使用下面的命令：

```bash
$ pip install pipenv
```

Linux 和 macOS 使用下面的命令：

```bash
$ sudo -H pip install pipenv
```

使用 Pipenv 创建虚拟环境非常简单，使用 `pipenv install` 命令即可为当前项目创建一个虚拟环境：

```bash
$ pipenv install
```

这个命令执行的过程包含下面的行为：

* 为当前目录创建一个 Python 解释器环境，按照 pip、setuptool、virtualenv 等工具库。
* 如果当前目录有 Pipfile 文件或 requirements.txt 文件，那么从中读取依赖列表并安装。
* 如果没有发现 Pipfile 文件，就自动创建。

创建虚拟环境后，我们可以使用 `pipenv shell` 命令来激活虚拟环境，如下所示（执行 `exit` 可以退出虚拟环境）：

```bash
$ pipenv shell
```

**注意** 除了 `pipenv install` 命令和 Git 相关命令外，除非特别说明，本书后续的所有命令均需要在激活虚拟环境后执行。如果你不想每次都激活虚拟环境，可以在命令前添加 `pipenv run` 前缀，比如 `pipenv run pip list` 即表示在虚拟环境内执行 `pip list` 命令。

## 安装 Flask

无论是否已经激活虚拟环境，你都可以使用下面的命令来安装 Flask：

```bash
$ pipenv install flask
```

这会把 Flask 以及相关的一些依赖包安装到对应的虚拟环境，同时 Pipenv 会自动更新依赖文件。

**提示** 如果你没有使用虚拟环境，记得将 Flask 更新到最新版本（`pip install -U flask`）。

## 本章小结

当你进行到这里，就意味这我们已经做好学习和开发Flask程序的全部准备了。使用 `git status` 命令可以查看当前仓库的文件变动状态：

```bash
$ git status
```

下面让我们将文件改动提交进 Git 仓库，并推送到在 GitHub 上创建的远程仓库：

```bash
$ git add .
$ git commit -m "I'm ready!"
$ git push -u origin master # 如果你没有把仓库托管到 GitHub，则跳过这条命令，后面章节亦同
```

这里最后一行命令添加了 `-u` 参数，会将推送的目标仓库和分支设为默认值，后续的推送直接使用 `git push` 命令即可。在 GitHub 上，你可以通过 [https://github.com/你的用户名/watchlist](https://github.com/greyli/watchlist) 查看你的仓库内容。

**提示** 你可以在 GitHub 上查看本书示例程序的对应 commit：[1b6fe4a](https://github.com/greyli/watchlist/commit/1b6fe4ae117c2b964f247d8b12d79753ea69406f)。

## 进阶提示

* 阅读 MDN 的 [《Web 入门教程》](https://developer.mozilla.org/zh-CN/docs/learn)（了解 HTML、CSS、JavaScript）。
* 阅读短教程[《Git 简明指南》](http://rogerdudler.github.io/git-guide/index.zh.html)。
* 阅读文章[《Pipenv：新一代Python项目环境与依赖管理工具》](https://zhuanlan.zhihu.com/p/37581807)或 [Pipenv 官方文档](https://pipenv.readthedocs.io/en/latest/)。
* 如果你打算开源你的程序，在项目根目录中添加一个 README.md （自述文件）和 LICENSE （授权声明）是很有必要的。详情可以访问 [Open Source Guides](https://opensource.guide/) 了解。
* 在安装 Pipenv 时，你也可以使用 `--user` 选项进行用户安装（即 `pip install --user pipenv`）。用户安装可以避免破坏全局的包，而且可以避免对不可信的包使用 sudo pip 导致的潜在安全问题。详情见 [Pipenv 文档安装章节](https://docs.pipenv.org/install/#installing-pipenv)。