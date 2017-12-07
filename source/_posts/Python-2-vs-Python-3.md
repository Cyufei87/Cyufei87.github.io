---
title: Python 3 vs Python 2
date: 2017-11-18 14:24:15
tags: Python
category: 技术探索
---
### 前言
虽然Python 3早在2008年就发布了，但是似乎Python 3的使用率仍然不高([来自PyCharm的一个统计](https://twitter.com/pycharm/status/865659029460209664))。本文将在四个方面对Python 2和Python 3进行对比。
### 兼容性
这个大概是许多Python 2用户不愿意转向Python 3的最重要原因。但是根据[py3readiness](http://py3readiness.org/)的数据，将近96%的使用最多的Python包已经支持了Python 3。
而根据[PEP 373](https://www.python.org/dev/peps/pep-0373/)，Python 2将于2020年停止维护。[许多流行的Python项目也声明将于2020年以前停止对Python 2的支持](http://www.python3statement.org/)。
Python最流行的Web框架Django也声明了，[Django1.11将是最后一个支持Python 2的版本](https://docs.djangoproject.com/en/dev/faq/install/#what-python-version-should-i-use-with-django)。

### Python 3的新特性(截止到Python 3.6)
这里简述几个比较重要的
1. 类型注解。它允许你给函数增加一些说明的信息
2. 标准库asyncio提供了内置的异步IO支持。不再需要gevent，tornado等第三方库
3. lazy化。许多函数例如range，map，dict.keys不再直接返回list，而是返回一个可迭代对象
4. 更清晰明确的字符串表示。str表示Unicode字符串，bytes表示二进制数据

### 性能
[PyCon2017有一个关于Python 3.6性能的分享](https://speakerdeck.com/playpauseandstop/python-3-dot-6-and-performance-a-love-story)，得出的结论如下：
> Python 2.7 is still fastest Python
> Python 3.5 much faster Python 3.4
> Python 3.6 faster Python 3.5
> Python 3.7 has some significant improvements already

[这里](https://speed.python.org/comparison/?exe=12%2BL%2B3.6%2C12%2BL%2B2.7&ben=616%2C617%2C618%2C619%2C620%2C621%2C622%2C623%2C624%2C625%2C626%2C627%2C628%2C629%2C630%2C631%2C632%2C680%2C633%2C634%2C635%2C636%2C637%2C638%2C639%2C640%2C641%2C642%2C643%2C644%2C645%2C646%2C647%2C648%2C681%2C649%2C650%2C651%2C652%2C653%2C654%2C655%2C656%2C657%2C658%2C659%2C660%2C661%2C682%2C662%2C663%2C664%2C665%2C666%2C667%2C669%2C668%2C670%2C671%2C672%2C673%2C674%2C675%2C678%2C677%2C676%2C679&env=1&hor=false&bas=12%2BL%2B2.7&chart=normal+bars)是最新Python 2.7和Python 3.6在各个基准测试上的结果，[这里](http://pyperformance.readthedocs.io/benchmarks.html#available-benchmarks)是不同测试的一些说明
分享截图如下(写本篇文章时的数据)：
![](/images/python_speed.jpg)
可以看出，除了python_startup，python_startup_no_site，unpickle_pure_python三个测试的数据上，Python 3.6的性能要远远落后Python 2.7以外，其他所有的测试Python 3.6仅落后Python 2.7很少，或者相对于Python 2.7的性能有所提升

### 学习成本
不可否认，大多数关于Python的学习资料还是Python 2的，网络上各个技术论坛或技术网站涉及到Python的内容大多也是指Python 2。
但是另一方面，Python 3虽然增加了不少新特性，但绝大多数Python 2的问题解决方案或文档也是适用于Python 3的，而且Python 2.7作为一个过渡版本，也启到了一定的作用。而且可以预料，关于Python 3的资料会越来越多。

### 其他
1. 有一个反对使用Python 3的文章[The Case Against Python 3](https://learnpythonthehardway.org/book/nopython3.html)及对它的[反驳](https://eev.ee/blog/2016/11/23/a-rebuttal-for-python-3/)
2. [PyCon2017上分享的Instagram为何和如何迁移到Python 3](http://python.jobbole.com/87814/)([YouTube上的视频](https://www.youtube.com/watch?v=66XoCk79kjM))

### 我的看法
* 未来是Python 3的
* 新项目可以完全使用Python 3，老的项目可以根据项目的状况选择是否迁移到Python 3
* 就学习Python而言，因为大部分的资料仍然是Python 2的，可以根据自己的计算机基础选择Python 2或者Python 3，比选择更重要的是踏实学和实践
