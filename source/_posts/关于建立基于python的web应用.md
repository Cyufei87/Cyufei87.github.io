---
title: 关于建立基于python的web应用
tags:
  - 技术探索
date: 2015-03-06 17:57:43
---

基于python的web应用的开发目前大多基于WSGI，主要分为web服务器和web应用程序（或框架）两大部分。
关于WSGI，可以参考：
[http://brief.sinaapp.com/blog/31/](http://brief.sinaapp.com/blog/31/)
[http://zh.wikipedia.org/wiki/Web%E6%9C%8D%E5%8A%A1%E5%99%A8%E7%BD%91%E5%85%B3%E6%8E%A5%E5%8F%A3](http://zh.wikipedia.org/wiki/Web%E6%9C%8D%E5%8A%A1%E5%99%A8%E7%BD%91%E5%85%B3%E6%8E%A5%E5%8F%A3)
web服务器有多种选择，具体比较参见：
[https://www.digitalocean.com/community/tutorials/a-comparison-of-web-servers-for-python-based-web-applications](https://www.digitalocean.com/community/tutorials/a-comparison-of-web-servers-for-python-based-web-applications)
目前应用比较多的是uwsgi
web开发框架也有多种选择，参见：
[https://www.airpair.com/python/posts/django-flask-pyramid](https://www.airpair.com/python/posts/django-flask-pyramid)
值得一提的是，pyramid是“The Pylons Project”的第一个package([http://www.pylonsproject.org/](http://www.pylonsproject.org/))

另外，这些web服务器一般使用nginx或者apache作为反向代理