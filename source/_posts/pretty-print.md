---
title: pretty_print
tags: [Python]
category: 技术探索
date: 2016-07-19 18:43:49
---

Python内置print打出dict, list等，如果这些类型内部含有中文，则会打出其repr之后的样子，很不方面查看[![b1](http://182.92.214.184/wp-content/uploads/2016/07/b1.jpg)](http://182.92.214.184/wp-content/uploads/2016/07/b1.jpg)
```python
def pretty_print(obj):
    def _pretty_str(obj):
        pstr = ""
        if isinstance(obj, dict):
            pstr += "{"
            first_ele = True
            for k, v in obj.iteritems():
                if first_ele:
                    first_ele = False
                else:
                    pstr += ", "
                pstr += _pretty_str(k) + ":" + _pretty_str(v)
            pstr += "}"
        elif isinstance(obj, (list, set, tuple)):
            if isinstance(obj, list):
                left, right = "[", "]"
            elif isinstance(obj, set):
                left, right = "{", "}"
            elif isinstance(obj, tuple):
                left, right = "(", ")"
            pstr += left
            first_ele = True
            for v in obj:
                if first_ele:
                    first_ele = False
                else:
                    pstr += ", "
                pstr += _pretty_str(v)
            pstr += right
        elif isinstance(obj, basestring):
            pstr = '"%s"' % str(obj)
        else:
            pstr = str(obj)
        return pstr
    print(_pretty_str(obj))
```
于是乎写了这个函数，效果如下：
[![b2](http://182.92.214.184/wp-content/uploads/2016/07/b2.jpg)](http://182.92.214.184/wp-content/uploads/2016/07/b2.jpg)
