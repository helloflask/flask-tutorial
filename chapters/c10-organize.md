# 第 10 章：组织你的代码

Flask 对项目结构没有固定要求，你可以使用单脚本，也可以使用包。这一章，我们会使用包来组织程序。

## 使用包组织代码



```bash
$ mkdir watchlist  # 创建包目录
$ mv static templates watchlist  # 把 static 和 templates 文件夹移动到包目录
$ cd watchlist  # 切换进包目录
$ touch __init__.py view.py errors.py models.py commands.py  # 创建多个模块
```



## 组织模板



```bash
$ cd watchlist/templates
$ mkdir errors
$ mv 400.html 404.html 500.html errors
```



## 组织测试



```bash
$ mkdir tests
$ cd tests
$ touch test_basic.py test_commands.py test_views.py test_models.py
```



## 本章小结



## 进阶提示

- 蓝本
- 工厂函数