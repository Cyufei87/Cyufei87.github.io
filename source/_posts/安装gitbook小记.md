---
title: 安装GitBook小记
tags: [GitBook]
category: 技术探索
date: 2017-01-19 20:01:07
---

看[小程序文档](https://mp.weixin.qq.com/debug/wxadoc/introduction/index.html)时，发现文档是使用[gitbook](https://www.gitbook.com/)生成的，很喜欢这种风格的页面，于是尝试着在自己的服务器上也搭建一个。
从[这里](http://www.chengweiyang.cn/gitbook/gitbook.com/README.html)，首先在服务器上安装npm，使用命令yum install npm，能找到安装包，可是总在安装过程中被莫名杀死。
于是尝试着下载nodejs安装包，编译安装，同样报错被杀死
![6](http://dahui1990.com/wp-content/uploads/2017/01/6.jpg)然后尝试下载编译好的程序，解压时报错
![5](http://dahui1990.com/wp-content/uploads/2017/01/5.jpg)终于发现是服务器的内存问题。。
![3](http://dahui1990.com/wp-content/uploads/2017/01/3.jpg)可用内存不足100MB
然后发现
![1](http://dahui1990.com/wp-content/uploads/2017/01/1.jpg)23个php-fpm进程占据了将近70%的内存。
我是使用的阿里云的云服务器，内存只买了1G的，包括这个wordpress博客，mysql数据库，一些自己弄着玩的程序都跑在这台服务器上。php-fpm使用的是默认的配置，结果造成内存使用率过高。
而实际上，我的博客的访问量并不算大(可以说很小。)，于是，更改php-fpm配置，降低其工作进程数，重启后
![2](http://dahui1990.com/wp-content/uploads/2017/01/2.jpg)然后使用yum install npm，终于安装了npm..
接下来按部就班。。
请见第一个[book](http://dahui1990.com:4000/)