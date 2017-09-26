---
title: 理解python的字符串编码
tags:
  - 技术探索
date: 2015-03-06 11:55:08
---

首先需要了解的是：
字符集定义了字符的集合，如ascii字符集主要包括英文字母，数字，一些控制符合等，但不包括汉字，日文符号。gb2312字符集包含ascii定义的所有字符，汉字，但也不包含日文符合。unicode字符集包含每种语言中的每个字符。
字符集的编码方案是针对特定字符集的每个字符的计算机二进制表示方案，主要用于计算机内部的存储和网络设备间的传输。
unicode只是定义了一个“字符集”，而utf8、utf16、utf32是针对unicode字符集的编码方案
gb2312也是字符集(unicode的子集)，由于它的编码方案通常只用EUC-CN，也可以说是一种编码方案
gbk是gb2312的延伸（超集），和gb2312类似
可参考：[http://www.zhihu.com/question/20650946](http://www.zhihu.com/question/20650946)
[http://stackoverflow.com/questions/643694/utf-8-vs-unicode](http://stackoverflow.com/questions/643694/utf-8-vs-unicode)

python内部的字符只是unicode字符集中的字符，字符串是这些字符的组合，不涉及编码方案（只是内部处理的话，不涉及存储和传输）。
这点在python3中体现的很明显，内置类型str不涉及编码方案，要具体到编码的话用bytes，而当进行存储或传输时，要求必须是bytes，如urllib.request中的http请求，文件的读写（调用open时，有默认的编码方案，或者用可选参数encoding指定），socket的send方法等。而且str和bytes不允许互操作。
python2中的这点不是很明确，总体来说，python2的u""相当于python3中的str，而普通的""相当于bytes