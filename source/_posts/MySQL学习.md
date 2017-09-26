---
title: MySQL学习
tags:
  - 技术探索
date: 2017-02-17 00:35:44
---

首先推荐三篇文章：
1.[MySQL索引背后的数据结构及算法原理](http://blog.codinglabs.org/articles/theory-of-mysql-index.html)
总体概括了MySQL内部的索引原理及索引使用策略
2.[剖析Mysql的InnoDB索引](http://blog.csdn.net/voidccc/article/details/40077329)
侧重剖析了InnoDB的Page结构，更加详细的见Jeremy Cole的[博客](https://blog.jcole.us/innodb/)
3.Judy的[B树](https://github.com/julycoding/The-Art-Of-Programming-By-July/blob/master/ebook/zh/03.02.md)
侧重数据结构的分析，注意只是数据结构。。
此外还有官方的[InnoDB文档](https://dev.mysql.com/doc/refman/5.7/en/innodb-storage-engine.html)

总结重要的内容如下：
1\. 使用B+的原因，相对于红黑树等二叉查找树，树的高度低，能减少IO次数。相对于B-树，稳定，更利于范围查询。相对于Hash表，更利于范围查询，伸缩性更好（在无法预知表中记录数时），详细见[这里的讨论](http://stackoverflow.com/questions/7306316/b-tree-vs-hash-table)
2\. InnoDB与MyISAM索引实现的区别，聚集索引和非聚集索引的区别
3\. 建索引时的最左前缀原理，数据库表的主键选择
4\. 慢查询日志及explain关键字