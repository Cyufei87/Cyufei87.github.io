---
title: Python的闭包
date: 2017-11-29 14:53:42
tags: [Python, 闭包]
category: 技术探索
---
来自[维基百科](https://zh.wikipedia.org/wiki/%E9%97%AD%E5%8C%85_%28%E8%AE%A1%E7%AE%97%E6%9C%BA%E7%A7%91%E5%AD%A6%29)：
> 在计算机科学中，闭包（英语：Closure），又称词法闭包（Lexical Closure）或函数闭包（function closures），是引用了自由变量的函数。这个被引用的自由变量将和这个函数一同存在，即使已经离开了创造它的环境也不例外。所以，有另一种说法认为闭包是由函数和与其相关的引用环境组合而成的实体。闭包在运行时可以有多个实例，不同的引用环境和相同的函数组合可以产生不同的实例。

**Python的闭包的环境信息保存在函数对象的属性 \_\_closure\_\_ 中**
测试代码：
```python
# -*- coding: utf-8 -*-
global_var = 100


def add1(a, b):
    return global_var + a + b


def add_one(b):
    def real_add(a):
        return global_var + a + b
    return real_add
add2 = add_one(2)


def add_one_default(default_b):
    def real_add_default(a, b=default_b):
        return global_var + a + b
    return real_add_default
add3 = add_one_default(3)


def add_global_deco(func):
    def _func(*args, **kwargs):
        return func(*args, **kwargs) + global_var
    return _func


@add_global_deco
def add4(a, b):
    return a + b


if __name__ == '__main__':
    print("add1.__closure__ is %s" % repr(add1.__closure__))
    # add1.__closure__ is None
    print("add2.__closure__ is %s" % repr(add2.__closure__))
    # add2.__closure__ is (<cell at 0x10437a7f8: int object at 0x7fea2e605460>,)
    print("add3.__closure__ is %s" % repr(add3.__closure__))
    # add3.__closure__ is None
    print("add4.__closure__ is %s" % repr(add4.__closure__))
    # add4.__closure__ is (<cell at 0x10437a830: function object at 0x104377578>,)
```
可以看出add2、add4是闭包，add1、add3不是

**在嵌套函数中，子函数只有引用了locals()中的自由变量才能成为闭包**
Python关于自由变量的[文档](https://docs.python.org/2/reference/executionmodel.html)：
> If a name is bound in a block, it is a local variable of that block. If a name is bound at the module level, it is a global variable. (The variables of the module code block are local and global.) If a variable is used in a code block but not defined there, it is a free variable.

Python关于locals()的[文档](https://docs.python.org/2/library/functions.html#locals)：
> Update and return a dictionary representing the current local symbol table. Free variables are returned by locals() when it is called in function blocks, but not in class blocks.

注：这里有歧义，按照自由变量的定义，全局变量也应该属于自由变量。但是，全局变量并不会通过locals()返回，而是通过globals()返回

add1在locals()没有自由变量，所以不能形成闭包
add2有自由变量b，所以形成闭包
add3在函数定义中引用了default_b，但是在执行中并未用到（这里的b是局部变量），所以也不能形成闭包
add4是装饰器形式的闭包，这里的自由变量是被装饰的函数add4，所以形成闭包

参考：
[Understanding Python's closures](https://gist.github.com/DmitrySoshnikov/700292)
[Python Closures and Free Variables](http://mathamy.com/python-closures-and-free-variables.html)
[Python 的闭包和装饰器](https://segmentfault.com/a/1190000004461404)
