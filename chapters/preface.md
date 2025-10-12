# 前言

## 关于作者

**李辉（Grey Li）**

我从 2015 年开始自学编程，Python 和 Flask 是我最先学习的语言和框架。在经过一些学习和探索后，我开始写作[《Flask Web 开发实战》](http://helloflask.com/book/1)。在这本书出版的同一年成为 Flask 的维护者，也在之后的这些年里为 Flask 以及许多 Flask 扩展提交大量代码贡献。作为第一本书的升级版，我的新书[《Flask 从入门到进阶》](http://helloflask.com/book/4)也将在 2025 年 11 月出版上市。

时至今日，Flask 仍然是我最喜欢的 Python Web 框架。希望未来可以为 Flask 社区作出更多贡献。

欢迎访问我的[个人主页](http://greyli.com)了解更多信息。

## 关于本书

Flask（<https://github.com/pallets/flask>）是一个使用 Python 语言编写的 Web 框架，它可以让你高效地编写 Web 程序。Web 程序即“网站”或“网页程序”，是指可以通过浏览器进行交互的程序。我们日常使用浏览器访问的豆瓣、知乎、百度等网站都是 Web 程序。

通过这本书，你会学到 Flask 开发的基础知识，并开发出一个简单的 Watchlist（观影清单）程序。如果感兴趣的话，可以先来这里看看其他读者朋友的读后感和成果分享：<https://codekitchen.community/t/topic/64>。

当你想要完成一个比较大的目标时，通常会把这个目标分解成多个小目标，然后逐一去完成。开发程序也是这样，在一开始就编写出像豆瓣、IMDB 这样的程序恐怕不太现实，但是你可以先模仿其中的一小部分。我们要完成的 Watchlist 程序就是一个很好的开始。在功能上，这个程序可以看做是简化版的 IMDB Watchlist / 豆瓣豆单：你可以添加、删除和修改你收藏的电影信息。

![Watchlist 程序](images/7-2.png)

你可以访问 <http://watchlist.helloflask.com> 查看示例程序的在线 Demo。示例程序源码可以在 <https://github.com/helloflask/watchlist> 找到。如果你无法访问 GitHub，可以<del>想办法让自己能够正常访问</del>点击[这里](http://helloflask.com/downloads/watchlist.zip)下载示例程序源码。阅读源码仓库中的 README.md 文件了解如何运行示例程序。

## 本书特点

- 基于 Flask 最新的 3.1.x 版本
- 使用一个 Watchlist 程序作为贯穿全书的示例
- 复原完整的开发流程，让你可以动手一起写程序
- 只提供入门所需的最少信息，让你更容易建立起信心
- 优化术语解释，用已知的概念去解释未知的概念，更容易理解

## 阅读方法

本书复原了编写这个 Watchlist 程序的完整流程，包括每一行代码块，每一个需要执行的命令。在阅读时，你需要自己输入每一个代码和命令，检查输出是否和书中一致。在这个过程中，你也可以对它进行一些调整。比如，示例程序的界面语言使用了英文，你可以修改为中文或是其他语言。对于页面布局和样式，你也可以自由修改。

在本书的最后，你会把你自己编写的 Watchlist 部署到互联网上，让任何人都可以访问。

## 讨论与求助

如果你想和其他同学交流 Flask、Web 开发等相关话题，或是在学习中遇到了问题，想要寻求帮助，下面是一些好去处：

* [代码厨房社区](https://codekitchen.community)（Steak Overcooked 板块）
* [HelloFlask QQ 群](http://shang.qq.com/wpa/qunwpa?idkey=3cbf3e3ede8252eb3ae584a356131123ed68a9f3bd5bcee0652b401914eb01bb)（419980814）

## 反馈与勘误

欢迎通过下面的方式提出反馈、建议和勘误：

* 在源码仓库[创建 Issue](https://github.com/helloflask/flask-tutorial/issues/new)。
* 在[代码厨房社区](https://codekitchen.community)发布帖子，并选择“Flask 入门教程”分类。
* 通过邮箱 <flasktutorial@greyli.com> 联系作者。

## 相关资源

* 本书主页：<http://helloflask.com/book/3>
* 本书论坛：<https://codekitchen.community>
* 本书源码：<https://github.com/helloflask/flask-tutorial>
* 示例程序源码：<https://github.com/helloflask/watchlist>
* 示例程序源码下载：<https://helloflask.com/downloads/watchlist.zip>
* 示例程序在线 Demo：<http://watchlist.helloflask.com>
