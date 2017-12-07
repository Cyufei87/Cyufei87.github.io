---
title: protobuf vs json vs xml
tags: [protobug, json, xml]
category: 技术探索
date: 2015-05-22 21:05:15
---

[protobuf](https://developers.google.com/protocol-buffers/):google 的一种数据交换的格式.

[json](http://json.org/):一种轻量级的数据交换格式.

[xml](http://zh.wikipedia.org/wiki/XML):可扩展标记语言.

按本人的认识，说到底，他们只是定义了一种数据存储的规则，其中，json和xml是直接可读的，他们的生成和解析只要符合相应规则即可，而protobuf的生成和解析需要调用Google提供的特定的方法，甚至对于特定格式的protobuf数据，需要按特定语法定义一个.proto文件。

xml:出现最早，应该也是当前应用最普遍，良好的工具支持，直接可读，浏览器默认直接支持

json:在许多方面大有替代xml的趋势，直接可读，浏览器需要插件才能直接支持（指浏览器打开json类型的网页），但是javascript原生支持，冗余数据少

protobuf:应用的普遍度不如json和xml，二进制，需要借助工具阅读（也需要有相应的格式定义），更少的冗余数据，快速的处理速度，官方只提供了c++,java,python的处理工具

关于冗余的认识：xml的冗余多主要指除了实际需要存储的数据外，维护格式本身占用的空间多。protobuf一方面维护格式占用的空间少，对于实际数据本身的存储也有优化

在实际选择时，除非xml有特殊的优势（比如用到的库和对接的系统只支持xml），一般不会选择xml。protobuf比较适用于内部系统，适用于对处理速度和体积要求较高的地方。json算是中庸吧..

注：最开始注意到protobuf是因为新浪的微博系统用到了它，其实在hadoop中也有用到它，如果源码安装hadoop，需要先安装protobuf。