---
title: HTTP请求阻塞
tags: [HTTP]
category: 技术探索
date: 2015-02-06 13:45:39
---

今天发现前几天写的一个定时爬虫程序，突然无故暂停了。

程序用了Python定时框架apscheduler，我加了28个Job，其中有3个job出现了异常。

查看日志，发现是某一次的job执行似乎是停住了，而job的最大同时运行实例数为1，所以下一次的任务执行也就跳了过去（程序定时每半小时运行一次）。导致之后差不到两天的数据没能抓取到。

查看代码，感觉像调用urllib2.urlopen时，程序得不到回应，所以停住了。

于是运行

`ps -eLo user,pid,ppid,pgid,nlwp,lwp,sess,start_time,command,wchan|grep write_AQM`

得到结果如下：

![QQ图片20150206150820](http://182.92.214.184/wp-content/uploads/2015/02/QQ图片20150206150820.jpg)

可以看到正好有3个lwp的wchan是sk_wait_data

再次运行

`strace -p pid`

其中pid为那3个lwp的id，得到

![QQ图片20150206150908](http://182.92.214.184/wp-content/uploads/2015/02/QQ图片20150206150908.jpg)

由此，基本可以确定程序在进行http请求时，一直得不到响应，就阻塞在了那里。

解决方法很简单，在调用urllib2.urlopen时，多传一个参数timeout，如timeout=10。