---
title: 定制bootstrap
tags:
  - 技术探索
date: 2015-05-20 16:28:19
---

[Bootstrap](http://v3.bootcss.com/)是Twitter推出的一个用于前端开发的开源工具包，如果直接使用bootstrap编译好的css文件，许多样式，如全局字体大小，表单的内边距都是固定的，但也许其中的部分内容是你想要改变的，特别对追求完美的开发者而言...

偶然的机遇，学习了下bootstrap的定制功能。

bootstrap本身使用[Less](http://www.ibm.com/developerworks/cn/web/1207_zhaoch_lesscss/)进行编写，使用[Grunt](http://gruntjs.com/)作为编译系统，而Grunt是基于[Node.js](http://zh.wikipedia.org/wiki/Node.js)的，因此，首先需要安装Node.js，之后用npm来安装Grunt，然后下载bootstrap的源码，再用npm安装某些编译bootstrap依赖的扩展包即可，详见[这里](http://v3.bootcss.com/getting-started/#grunt)。

在bootstap的根目录，当你运行grunt时，会自动执行Gruntfile.js，根据参数的不同，会执行到Gruntfile.js的不同部分。当执行<span style="background-color: #eee;">grunt dist</span>时，Gruntfile.js会自动运行less/bootstrap.less，less/bootstrap.less导入并执行其他less文件，完成css文件的生成。

如果我们要定制bootstrap，当然主要是修改less文件了。在众多less文件中，less/variables.less定义了less用到的众多变量，这个也是主要修改的文件。

其实，[这里](http://v3.bootcss.com/customize/)提供了一个很简单来定制的方法，大概原理也是如上所介绍吧...