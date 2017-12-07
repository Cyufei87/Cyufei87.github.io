---
title: WordPress初探
tags: [WordPress]
category: 技术探索
date: 2014-11-03 16:45:03
---

一直想拥有自己的一个网站..

在第一份工作期间，接触了除站点部署之外的关于简单web站点的方方面面的知识...html..css..js..服务器端业务处理..页面渲染..数据库... 一直为别人做网站，从未拥有自己的..

在第一份工作辞职之后，面试过创新工场的一个职位，突然才发觉自己的缺陷，web服务器的部署..

偶然的，发现了阿里云服务器...

于是我开始了关于python web框架的探索，在之前的工作中，一直都用的是Django，也接触过Fask和httpd。最终我选择了pyramid，似乎离题了..

发现wordpress是一个偶然的情况，在网上查一些资料，发现一个blog的底部有Power by Wordpress..之类的东西...

由于自己最近的工作都在linux下，很快，把wordpress安装好了。关于部署，之前部署pyramid用到了nginx，很自然的，我也选在nginx来部署wordpress。配置nginx对php的支持，很快..见到了第一个nginx+php的页面..

数据库，之前购买过阿里云的数据库服务，并用webpy测试连接了数据库。mysql已经是很熟悉的了，利用wordpress设置数据库的向导，第一个动态的wordpress页面出来了..

接下来是个痛苦的探索过程，我发现自己的博客，不论使用任何的主题，都出现样式不对的问题。在网上各种搜索，找到过类似的情况，但其解决的方案完全不适用于我的..

怀疑过权限的问题，但把wordpress的各个目录的权限都设置成对所有用户都可读写，仍然不起作用..

怀疑过wordpress版本的问题，我装的是最新的4.0，或许版本不稳定，或许我的安装过程有什么问题..我利用wordpress的管理页面，把wordpress重装了两遍（仍是4.0），也不起作用(我最终还是没用使用低版本)..

一直用chrome浏览器，但不习惯chrome的开发者工具。在firefox上打开了页面..效果是一样的..我用自己的html及css知识，开始自己调试wordpress页面，发现其css是下载了下来的，而且把下载的css应用到页面上，页面是正常的..开始怀疑css链接方式的问题..

把blog的静态页面保存下来，去掉自己不熟悉的某些头标签，以及链入css的标签的某些自己不熟悉的属性..没任何效果..

偶然的，用世界之窗浏览器打开本地静态页面，样式正常...打开网站..样式正常...想到了IE，样式正常..

愈加怀疑wordpress4.0的稳定性..兼容性...唯一不可理解的是...网络上搜不都任何关于4.0版本这方面的问题..

想到了，用firebug加载网页时，css是下载的，但在firebug的css标签下，打开相应的css，却显示是空的..

应该是css解析的问题..

是不是nginx的css之类要特殊处理..

开始查看网页的response的header..content-type是text/plain..

查看正常网页的css的content-type..text/css..

一切都很清楚了..开始寻找nginx关于js/css的配置..没有特殊注意的..

但发现了这两句..

include /etc/nginx/mime.types;
default_type application/octet-stream;

查看nginx.conf.default，这两句赫然在列..

添加到我的nginx.conf里，service nginx restart..

效果出来了..