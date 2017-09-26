---
title: DIYwordpress日历样式
tags:
  - 技术探索
date: 2015-03-04 16:41:59
---

一直都不太喜欢博客的日历样式，对于写过日志的那一天没有特殊颜色标示
查看仪表盘，也没有设置这种样式的选项，只能自己DIY了..
用"审查元素"查看写过日志那天的a元素的样式，启作用的样式为：
`
#sidebar a,
#sidebar a:visited {
	color: #2f2f2f;
	text-decoration: none;
}
`
仪表盘提供的有编辑相应主题css的页面，于是加了下面的样式：
`
#calendar_wrap a{
	color: #16D3B5;
}
#calendar_wrap a:visited{
	color: #A09B9B;
}
#calendar_wrap a:hover{
	color: #00a498;
}
`
效果如下：
![rili](http://182.92.214.184/wp-content/uploads/2015/03/rili.png)
变成了
![rili_new](http://182.92.214.184/wp-content/uploads/2015/03/rili_new.png)