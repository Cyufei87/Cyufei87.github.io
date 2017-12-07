---
title: Django REST framework小探
tags: [Django, REST framework]
category: 技术探索
date: 2017-09-07 19:19:26
---

偶然发现
1\. 不带CSRF信息
2\. 没有session相关的cookie
也能正常访问API

调试发现，接口的访问通过REST framework的ApiView，而这个View的authentication_classes和permission_classes, throttle_classes都是使用的默认的
在默认情况下，authentication_classes的值是：
<pre>'DEFAULT_AUTHENTICATION_CLASSES': (
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication'
)</pre>
permission_classes的值是：
<pre>'DEFAULT_PERMISSION_CLASSES': (
    'rest_framework.permissions.AllowAny',
)</pre>
throttle_classes的值是：
<pre>'DEFAULT_THROTTLE_CLASSES': (),</pre>
而根据Django REST framework的[设定](http://www.django-rest-framework.org/api-guide/authentication/)（[相关代码](https://github.com/encode/django-rest-framework/blob/3.2.2/rest_framework/authentication.py#L125)）:
<pre>Authentication is the mechanism of associating an incoming request with a set of identifying credentials, such as the user the request came from, or the token that it was signed with. The [permission](http://www.django-rest-framework.org/api-guide/permissions/) and [throttling](http://www.django-rest-framework.org/api-guide/throttling/) policies can then use those credentials to determine if the request should be permitted.</pre>
authentication本身并不决定请求是否应该被拒绝，所以在没有用户登录的情况下(没有session相关cookie)，请求仍能到达业务处理函数

另一个问题是，CSRF为何没有发挥作用，原因是：
根据[这里](https://github.com/encode/django-rest-framework/blob/3.2.2/rest_framework/views.py#L134)：
<pre><span class="pl-c">#</span> Note: session based authentication is explicitly CSRF validated,
<span class="pl-c">#</span> all other authentication is CSRF exempt.</pre>
只有SessionAuthentication才会做CSRF检查，而根据SessionAuthentication的[代码](https://github.com/encode/django-rest-framework/blob/3.2.2/rest_framework/authentication.py#L124)，检测到没有活跃用户，就不再做CSRF防御了