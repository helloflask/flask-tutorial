# 第 1 章：准备工作

在通过这本书学习 Flask 开发前，我假设你已经了解了 Python 和 HTML 的基础知识。如果还没有，那么可以先从下面这些在线资源入手：

* 《[使用 HTML、CSS 和 Javascript 构建简单的网站](https://docs.microsoft.com/learn/modules/build-simple-website/?WT.mc_id=OSS-MVP-5003485)》 - Microsoft Learn
* 《[Web 入门教程](https://developer.mozilla.org/zh-CN/docs/learn)》 - MDN
* 《[Python 教程](https://docs.python.org/zh-cn/3/tutorial/)》 - Python.org

这个教程对你的操作系统没有要求：你可以使用 Windows，也可以使用 macOS 或 Linux。不过你的 Python 版本需要是 3.9 及以上版本。


## 安装编辑器和浏览器

对于编辑器来说，每个人都有不同的偏好，你可以自由选择。可以选择功能丰富的IDE（集成开发环境），比如 [PyCharm](https://www.jetbrains.com/pycharm/)；也可以选择相对轻量的编辑器，比如 [VS Code](https://code.visualstudio.com/) 或 [Sublime Text](https://www.sublimetext.com/)。浏览器建议使用 [Firefox](https://www.mozilla.org/en-US/firefox/new/) 或 [Chrome](https://www.google.com/chrome/)。

## 使用命令行

在本书中，你需要使用命令行窗口来执行许多操作。在 Windows 下，推荐使用 Powershell 而不是 CMD.exe，在 macOS 和 Linux 下则可以使用任何你喜欢的终端程序（默认为 Terminal）。下面我们执行一个最简单的 `whoami` 命令（即 Who Am I？）：

```bash
$ whoami
greyli
```

这个命令会打印出当前计算机用户的名称。其他常用的命令还有 `cd` 命令，用来切换目录（**c**hange **d**irectory）；`mkdir` 命令，用来创建目录（**m**a**k**e **dir**ectory）。在不同的操作系统上，执行某个操作的命令可能会有所不同，在必要的地方，本书会进行提示。

我们先来为我们的程序创建一个文件夹：

```bash
$ mkdir watchlist
$ cd watchlist
```

除非特别说明，从现在开始，本书假设你的工作目录将是在项目的根目录，即 watchlist/ 目录。

为了确保你已经正确安装了 Python，可以执行下面的命令测试是否有报错：

```bash
$ python --version
Python 3.9.10
```

在 Linux 和 macOS 中，对应 Python 3 版本的命令将会是 `python3`（类似的，Python 3 对应的 pip 命令为 `pip3`）：

```bash
$ python3 --version
Python 3.9.10
```

对于 Windows 用户，可以考虑在这个教程的学习过程中使用 [WSL](https://learn.microsoft.com/en-us/windows/wsl/install?WT.mc_id=OSS-MVP-5003485)（Windows Subsystem for Linux，在 Windows 上运行的 Linux 子系统）或是 Git Bash（安装 Git for Windows 后附带的终端程序，下一节会介绍 Git 安装） 来代替系统自带的 CMD.exe 或 Powershell。Git Bash 支持一些在 Linux 或 macOS 下才能使用的命令（程序），比如 ls、cat、nano、ssh 等，这些命令我们在后面会用到。

> **提示** 如果你打算在这个教程的学习中继续使用 CMD.exe 或 Powershell，那么需要注意下列命令的区别：
>
> - 在 CMD.exe 中使用 `dir` 命令替代 `ls` 命令，使用 `type` 命令替代 `cat` 命令
> - 对于 `nano` 命令，你可以替换为其他已安装的编辑器命令，比如对于 VS Code，可以使用 `code` 命令。或者，你也可以直接使用编辑器的图形界面创建文件并编辑。
> - 对于 Windows 10 1809，OpenSSH 程序（相关命令 `ssh`、`ssh-keygen`）可以在控制面板中额外安装（[相关文档](https://docs.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse)）；旧版本 Windows 可以安装第三方 OpenSSH 客户端，比如 Putty，或直接使用 Git Bash。


## 使用 Git

[Git](https://git-scm.com) 是一个流行的版本控制工具，我们可以用它来记录程序源码和文件的变动情况，或是在开发时进行多人协作，你可以把它看做一个代码变动备份工具。

如果你还不熟悉 Git 也没关系，可以先按照书中的命令去操作，有时间再去了解原理。现在要做的第一件事就是在你的电脑上[安装 Git](https://git-scm.com/book/zh/v1/%E8%B5%B7%E6%AD%A5-%E5%AE%89%E8%A3%85-Git)。

> **附注** 阅读短教程[《Git 简明指南》](http://rogerdudler.github.io/git-guide/index.zh.html)或访问 Microsoft Learn 上的引导式教程《[Git 简介](https://docs.microsoft.com/zh-cn/learn/modules/intro-to-git?WT.mc_id=OSS-MVP-5003485)》了解相关基础知识。

安装后可以在命令行先使用使用下面的命令查看版本，没有报错则表示已正确安装：

```bash
$ git --version
git version 2.17.1
```

为了让 Git 知道你是谁，以便在提交代码到版本仓库的时候进行记录，使用下面的命令设置你的信息：

```bash
$ git config --global user.name "Your Name"  # 替换成你的名字
$ git config --global user.email "your_email@example.com"  # 替换成你的邮箱地址
```

现在为我们的项目文件夹创建一个 Git 仓库，这会在我们的项目根目录创建一个 .git 文件夹：

```bash
$ git init
Initialized empty Git repository in ~/watchlist/.git/
```

Git 默认会追踪项目文件夹（或者说代码仓库）里所有文件的变化，但是有些无关紧要的文件不需要记录变化，我们在项目根目录创建一个 .gitignore 文件，在文件中写入忽略文件的规则。因为文件内容比较简单，我们直接在命令行使用 nano 来创建：

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

使用 Control + O 和 Enter 键保存，然后按下 Control + X 键退出。在后续章节，对于简单的文件，都会使用 nano 创建，这部分操作你也可以使用编辑器的图形界面来完成。


## 将程序托管到 GitHub（可选）

这一步是可选的。将程序托管到 GitHub、GitLab 或是 BitBucket 等平台上，可以更方便地备份、协作和部署。这些托管平台作为 Git 服务器，你可以为本地仓库创建一个远程仓库，然后将其上传到这些平台上。

首先要注册一个 GitHub 账户，点击访问[注册页面](https://github.com/join)，根据指示完成注册流程。登录备用。

> **附注** 你可以访问 Microsoft Learn 上的引导式教程《[GitHub 简介](https://docs.microsoft.com/zh-cn/learn/modules/introduction-to-github?WT.mc_id=OSS-MVP-5003485)》了解相关基础知识。


### 设置 SSH 密钥

一般情况下，当推送本地改动到远程仓库时，需要输入用户名和密码。因为传输通常是通过 SSH 加密，所以可以通过设置 SSH 密钥来省去验证账号的步骤。

使用下面的命令生成 SSH 密钥对，否则复制输出的值备用：

```bash
$ ssh-keygen -t ed25519 -C "your_email@example.com"
```

替换上面命令中的邮箱地址，然后一路按下 Enter 采用默认值，最后会在用户根目录 .ssh 文件夹下创建两个文件，id_ed25519 和 id_ed25519.pub，前者是私钥，不能泄露出去，后者是公钥，用于认证身份，就是我们要保存到 GitHub 上的密钥值。再次使用前面提到的命令获得文件内容：

```bash
$ cat ~/.ssh/id_ed25519.pub
ssh-rsa AAAAB3Nza...省略 N 个字符...3aph book@greyli
```

如果你使用的 OpenSSH 版本过低，无法使用更安全的 ed25519 算法，可以使用下面的命令使用 RSA 算法：

```shell
$ ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
```

这时生成为密钥文件则分别为 id_rsa 和 id_rsa.pub，获取公钥内容的命令相应变为：

```shell
$ cat ~/.ssh/id_rsa.pub
```

选中并复制输出的公钥内容，访问 GitHub 的 [SSH 设置页面](https://github.com/settings/keys)（导航栏头像 - Settings - SSH and GPG keys），点击 New SSH key 按钮，将复制的内容粘贴到 Key 输入框里，再填一个标题，比如“My PC”，最后点击“Add SSH key”按钮保存。 


### 创建远程仓库

访问[新建仓库页面](https://github.com/new)（导航栏“+” - New repository），在“Repository name”处填写仓库名称，这里填“watchlist”即可，接着选择仓库类型（公开或私有）等选项，最后点击“Create repository”按钮创建仓库。

因为我们已经提前创建了本地仓库，所以需要指定本地仓库的远程仓库地址：

```bash
$ git remote add origin git@github.com:greyli/watchlist.git  # 注意更换地址中的用户名
```

这会为本地仓库关联一个名为“origin”的远程仓库，**注意将仓库地址中的“greyli”换成你的 GitHub 用户名**。

如果还没有创建本地仓库，则可以直接将远程仓库克隆到本地（这会在当前目录创建一个名为 watchlist 的文件夹）：

```bash
$ git clone git@github.com:greyli/watchlist.git  # 注意更换地址中的用户名
```


## 创建虚拟环境

虚拟环境是独立于 Python 全局环境的 Python 解释器环境，使用它的好处如下：

* 保持全局环境的干净
* 为同一个库在不同环境下指定不同的版本
* 方便记录和管理某个项目相关的依赖

我们将使用 Python 3 内置的 venv 模块创建虚拟环境，使用下面的命令即可为当前项目创建一个虚拟环境：

```bash
$ python -m venv .venv  # Windows
```

或：

```bash
$ python3 -m venv .venv  # Linux 和 macOS
```

如果

> **提示** 上述命令的最后一个参数是虚拟环境名称，你可以自由定义，比如 venv、env、.venv，或是“项目名-venv”，这里使用了 .venv。

这会在当前目录创建一个包含 Python 解释器环境的虚拟环境文件夹，名称为 .venv。这个文件的内容不需要提交到 Git 仓库，因此需要将文件夹名称 `.venv` 加入到项目根目录的 .gitignore 文件中。

## 激活虚拟环境

创建虚拟环境后，我们可以使用下面的命令来激活虚拟环境（通过执行环境内的激活脚本实现）：

```bash
$ .venv\Scripts\activate  # Windows
```

> **提示** 如果你在 Windows 中使用 Git Bash，则需要使用 `source .venv/Scripts/activate` 命令

或：

```bash
$ source .venv/bin/activate  # Linux 或 macOS
```

这时命令提示符前会显示虚拟环境的名称，表示已经激活成功：

```bash
(.venv) $
```

在激活虚拟环境后，无论操作系统和 Python 版本，都可以统一使用 `python` 和 `pip` 命令来调用当前虚拟环境内的 Python 和 pip 程序/二进制文件。此时执行 `python` 或 `pip` 命令指向的程序和激活脚本在同一个目录下，在 Windows 下所在目录为 `.venv\Scripts\`，Linux 和 macOS 下所在目录为 `.venv/bin/`。

最后，执行 `deactivate` 即可退出虚拟环境：

```bash
(.venv) $ deactivate
$
```

> **注意** 除了 Git 相关命令外，除非特别说明，本书后续的所有命令均需要在激活虚拟环境后执行。

> **提示** 建议为 pip 更新 PyPI 源，改为使用国内的 PyPI 镜像源以提高下载速度，具体见[这篇文章](https://zhuanlan.zhihu.com/p/57872888)。


## 安装 Flask

激活虚拟环境后，使用下面的命令来安装 Flask：

```bash
(.venv) $ pip install flask
```

这会把 Flask 以及相关的一些依赖包安装到对应的虚拟环境。本书写作时的 Flask 最新版本为 3.1.1，你执行这条命令时也许会安装更新的版本。如果你想指定安装 3.1.1 版本，可以使用下面的命令：

```bash
(.venv) $ pip install flask==3.1.1
```

> **提示** 如果你没有使用虚拟环境，记得将 Flask 更新到最新版本（`pip install -U flask`）。


## 使用 uv 管理虚拟环境和依赖（可选）

uv（<https://github.com/astral-sh/uv>）是一个使用 Rust 编写的 Python 依赖和虚拟环境管理工具。前面我们学习了如何使用 venv 模块创建虚拟环境，以及用 pip 来安装依赖包。你可以使用 uv 可以加速这些操作。

首先安装 uv。macOS 或 Linux：

```shell
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows：

```shell
$ powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

你也可以使用 pip 进行安装：

```shell
$ pip install --user uv
```

现在使用 uv 重新创建虚拟环境：

```shell
$ uv venv
```

uv 默认也使用 .venv 作为虚拟环境文件夹名称，所以会提示是否覆盖已有的虚拟环境，按下 y 确认即可。现在激活虚拟环境：

```shell
$ source .venv/bin/activate  # Windows 使用 .venv\Scripts\activate 命令
```

然后使用 uv 安装依赖：

```shell
$ uv pip install flask
```

除了像这样使用 uv 来代理 pip 操作，你也可以完成使用 uv 自带的依赖管理系统，详情可以访问文档 <https://docs.astral.sh/uv/guides/projects/> 了解。

除此之外，uv 也可以用来管理 Python 版本。下面是一些常用的命令示例。

安装指定的 Python 版本，之后可以使用 python3.10、python3.11、python3.12 来打开对应的 Python 解释器：

```shell
$ uv python install 3.10 3.11 3.12
```

用指定的版本创建虚拟环境：

```shell
$ uv venv --python 3.12
```

固定当前项目使用的 Python 版本，将会写入版本信息到 `.python-version` 文件（这个文件不需要提交到仓库，因此需要写入文件名到 .gitignore 文件）：

```shell
$ uv python pin 3.12
```


## 本章小结

当你进行到这里，就意味这我们已经做好学习和开发 Flask 程序的全部准备了。使用 `git status` 命令可以查看当前仓库的文件变动状态：

```bash
$ git status
```

下面让我们将文件改动提交进 Git 仓库，并推送到在 GitHub 上创建的远程仓库：

```bash
$ git add .
$ git commit -m "Init the project"
$ git push -u origin main # 如果你没有把仓库托管到 GitHub，则跳过这条命令，后面章节亦同
```

这里最后一行命令添加了 `-u` 参数，会将推送的目标仓库和分支设为默认值，后续的推送直接使用 `git push` 命令即可。在 GitHub 上，你可以通过 [https://github.com/你的用户名/watchlist](https://github.com/helloflask/watchlist) 查看你的仓库内容。

## 进阶提示

* 如果你打算开源你的程序，在项目根目录中添加一个 README.md（自述文件）和 LICENSE（授权声明）是很有必要的。详情可以访问 [Open Source Guides](https://opensource.guide/) 了解。
