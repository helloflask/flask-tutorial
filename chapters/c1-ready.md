# 准备工作

在开始之前，我们有一些准备工作要做。

首先，你需要一台安装了 Python 电脑。这里的 Python 可以是 Python 2.7 版本，也可以是 Python 3.3 及以上版本。电脑的系统可以是 Windows，也可以是 macOS 或 Linux。

在通过这本书学习Flask开发前，你需要对下面的编程语言有所了解：

* HTML
* Python

不用担心，你并不需要完全精通这些语言，简单了解即可。网上有大量的免费教程，你可以用一天的时间来入门 HTML、CSS 和 Javascript，了解基本用法即可。对于 Python，你可以花上一周的时间来学习基本语法。

## 选择编辑器

对于编辑器来说，每个人都有不同的偏好，你可以自由选择。对于初学者来说，一般可以选择功能丰富的IDE（集成开发环境），比如PyCharm；也可以选择相对轻量的编辑器，比如Atom和Sublime Text。如果你暂时还不知道选择哪个好，那就下载一个Sublime Text吧。

## 使用命令行

在本书中，你需要使用命令行窗口来执行许多操作。这里的命令行指的是Windows下的cmd.exe，或是macOS和Linux下的终端（Terminal），你也可以使用其他命令行工具（对于 Windows，推荐使用 [cmder](http://cmder.net)）。比如，下面我们执行一个最简单的whoami命令（即Who Am I？）：

```bash
$ whoami
greyli
```

这个命令会打印出当前用户的名称。其他常用的命令还有 cd 命令，用来切换目录；mkdir 命令，用来创建目录。在不同的操作系统上，执行某个操作的命令可能会有所不同，在必要的地方，书里会进行提示。

我们先来为我们的程序创建一个文件夹：

```bash
$ mkdir watchlist
$ cd watchlist
```

除非特别说明，从现在开始，本书假设你的工作目录将是在项目的根目录，即 watchlist/ 目录。

另外，为了确保你已经正确安装了 Python 和 Git，你可以执行下面的命令测试是否有报错：

```bash
$ python --version
Python 2.7.10
```

## 使用 Git

[Git](https://git-scm.com/downloads) 是一个流行的版本控制工具，我们可以用它来记录程序源码和文件的变动情况，或是在编程时进行多人协作，你可以把它看做一个优雅的代码变动备份工具。

如果你还不熟悉 Git 也没关系，我建议你先按照书中的命令去做，有时间再去了解原理。现在你要做的就是在你的电脑上[安装 Git](https://git-scm.com/book/zh/v1/%E8%B5%B7%E6%AD%A5-%E5%AE%89%E8%A3%85-Git)。

安装后可以在命令行先使用使用下面的命令查看版本，没有报错则表示已正确安装：

```bash
$ git --version
git version 2.17.1
```

为了让 Git 知道你是谁，以便在提交代码到版本仓库的时候进行记录，我们使用下面的命令设置你的信息：

```bash
$ git config --global user.name "Grey Li"
$ git config --global user.email "withlihui@gmail.com"
```

> 提示 记得把上面的姓名和邮件地址替换成你的。

现在为我们的项目文件夹创建一个 Git 仓库，这会在我们的项目根目录创建一个 .git 文件夹：

```bash
$ git init
Initialized empty Git repository in ~/mylog/.git/
```

Git 默认会追踪项目文件夹（或者说代码仓库）里的所有文件的变化，但是有些无关紧要的文件不需要记录变化，我们可以在项目根目录创建一个 .gitignore 文件，在文件中写入忽略文件的规则。打开编辑器，创建这个文件，并写入下面这些常见的可忽略文件规则：

```
*.pyc
*~
__pycache__
.DS_Store
```

## 将程序托管到 GitHub（可选）

这一步是可选的，需要注意，

### 注册账户

### 设置 SSH 密钥

### 创建远程仓库

### 推送代码

## 创建虚拟环境

虚拟环境是独立于Python全局环境的Python解释器环境，使用它的好处如下：

* 保持全局环境的干净
* 指定不同的依赖版本
* 方便的记录和管理依赖

我们将使用Pipenv来创建和管理虚拟环境、以及在虚拟环境中安装和卸载依赖包。它集成了pip和virtualenv，可以替代这两个工具的惯常用法。另外，它还集成了Pipfile，它是新的依赖记录标准，使用Pipfile文件记录项目依赖，使用Pipfile.lock文件记录固定版本的依赖列表。这两个文件替代了手动通过requirements.txt文件记录依赖的方式。我们首先使用pip安装Pipenv，添加--user选项执行“用户安装”：

```bash
$ pip install --user pipenv
```

使用Pipenv创建虚拟环境非常简单，使用pipenv install命令即可为当前项目创建一个虚拟环境：

```bash
$ pipenv install
```

这个命令执行的过程包含下面的行为：

* 为当前目录创建一个Python解释器环境，按照pip、setuptool、virtualenv等工具库。
* 如果当前目录有Pipfile文件或 requirements.txt 文件，那么从中读取依赖列表并安装。
* 如果没有发现Pipfile文件，就自动创建。

创建虚拟环境后，我们可以使用pipenv shell命令来激活虚拟环境，如下所示：

```bash
$ pipenv shell
```

## 安装Flask

无论激活虚拟环境与否，你都可以使用下面的命令来安装Flask：

```bash
$ pipenv install flask
```

这会把Flask以及相关的一些依赖包安装到对应的虚拟环境，同时Pipenv会自动更新依赖文件中。

## 本章小结

当你进行到这里，就意味这我们已经做好学习和开发Flask程序的全部准备了，快翻到下一页吧。

```bash
$ git add .
$ git commit -m "I'm ready!"
$ git push  # 如果你没有把仓库托管到 GitHub，则跳过这条命令，后面章节亦同
```

## 进阶提示

* 阅读 MDN 的 [《Web 入门教程》](https://developer.mozilla.org/zh-CN/docs/learn)（了解 HTML、CSS、JavaScript）。
* 阅读短教程[《Git 简明指南》](http://rogerdudler.github.io/git-guide/index.zh.html)。
* 阅读文章[《Pipenv：新一代Python项目环境与依赖管理工具》](https://zhuanlan.zhihu.com/p/37581807)或 [Pipenv 官方文档](https://pipenv.readthedocs.io/en/latest/)。