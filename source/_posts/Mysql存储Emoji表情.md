---
title: MySQLl存储Emoji表情
tags: [MySQL, 数据库]
category: 技术探索
date: 2015-09-24 20:47:19
---

在一个新的项目中，涉及到了用户的评论，测试发现，app不能支持手机内置的表情。

经过一番探索，发现是后台不能支持存储表情相应的字符。
这些表情有个正式的名字[Emoji](http://apps.timwhitlock.info/emoji/tables/unicode)，Emoji在unicode中是有相应的表示的，而为什么后台不能存储这些字符呢。原因是，数据库相应字段都是使用[utf8字符集](https://dev.mysql.com/doc/refman/5.5/en/charset-unicode-utf8.html)(只是指mysql提供的)，而这种字符集使用最多3个字节存储一个字符，而Emoji表情的utf8表示大多需要使用4个字节，于是Emoji当然就存不到数据库里了。

在5.5.3版本之后，mysql提供了[utf8mb4](https://dev.mysql.com/doc/refman/5.5/en/charset-unicode-utf8mb4.html)，这个字符集支持了4个字节的utf8，在数据库中把字符集修改为这个，即可存储Emoji。同时需要将连接Mysql服务器的字符集设为utf8mb4，如在django中，需要加数据库设置：OPTIONS': {'charset':'utf8mb4'}。

讨论：

1.utf8mb4相对utf8的性能，utf8mb4是utf8的超集，性能应该不会超过utf8，但是否更差和差多少呢。

2.网上提供的方法一般是修改整个数据库的字符集，其实只是修改某些字段的字符集也是可以的（经测试，性能未知），但需要注意，字段的索引是区分utf8和utf8mb4的（以前遇见过相关的问题）。

3.数据库server和client都需要版本在5.5.3之上，否则会出现问题。