---
title: Python对象的创建
tags: [Python]
category: 技术探索
date: 2015-08-13 20:07:57
---

现有代码：
`
class Foo(object):pass
foo = Foo()
`
那么foo对象是怎样创建的呢，事实上是，会调用Foo的__call__方法，而在__call__里，主要进行了两个步骤：
1\. 调用Foo.__new__
2\. 调用Foo.__init__
具体可参见[这里](http://eli.thegreenplace.net/2012/04/16/python-object-creation-sequence)

考虑到Foo也是一个对象，结合[这里](http://eli.thegreenplace.net/2012/06/15/under-the-hood-of-python-class-definitions)，某种程度上，上述规则也试用于Foo.