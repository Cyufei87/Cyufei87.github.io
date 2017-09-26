---
title: Django的cache机制
tags:
  - 技术探索
date: 2015-03-07 22:30:15
---

先看代码：
`
from django.http import HttpResponse
import random
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.views.decorators.cache import cache_control
import datetime

@cache_page(15)
def cache1(request):
    return HttpResponse("It is %s"%datetime.datetime.now())

def cache2(request):
    res = cache.get("cache2")
    if res is not None:return HttpResponse(res)
    res = "It is %s"%datetime.datetime.now()
    cache.set("cache2", res, 15)
    return HttpResponse(res)

@cache_control(public=True, max_age=10)
def cache3(request):
    return HttpResponse("It is %s"%datetime.datetime.now())

def nocache(request):
    return HttpResponse("It is %s"%datetime.datetime.now())
`
1、服务器端cache1
[http://182.92.214.184:8800/cache1/?p=1](http://182.92.214.184:8800/cache1/?p=1)
[http://182.92.214.184:8800/cache1/?p=2](http://182.92.214.184:8800/cache1/?p=2)
说明：用cache_page实现的话，代码比较简洁，同一url不同查询参数独立缓存
2、服务器端cache2
[http://182.92.214.184:8800/cache2/?p=1](http://182.92.214.184:8800/cache2/?p=1)
[http://182.92.214.184:8800/cache2/?p=2](http://182.92.214.184:8800/cache2/?p=2)
说明：这种cache方式完全由用户自定义
3、浏览器cache
[http://182.92.214.184:8800/cache3/?p=1](http://182.92.214.184:8800/cache3/?p=1)
[http://182.92.214.184:8800/cache3/?p=2](http://182.92.214.184:8800/cache3/?p=2)
说明：这个只是在response的header中定义了cache-control，这种cache方式受到浏览器的影响（control+F5就什么都没了）
4、无cache
[http://182.92.214.184:8800/nocache/](http://182.92.214.184:8800/nocache/)
说明：啥都没有..