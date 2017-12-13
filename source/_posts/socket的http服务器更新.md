---
title: socket的http服务器更新
tags: [HTTP]
category: 技术探索
date: 2015-04-17 12:08:08
---

前些日子写了[python的socket实现http服务器](http://182.92.214.184/?p=127)之后,最开始这个极微型服务器似乎运行正常,之后也没有去管他

去了优酷土豆之后,偶然在公司的ubuntu开发机上访问服务器,发现出现了异常,服务器没有返回正常的响应,开始没有去管他,只是重启了下脚本

再次访问,发现异常依旧,于是仔细查了下原因

通过以下命令的输出:
![1](http://182.92.214.184/wp-content/uploads/2015/04/1.png)

可以定位到代码在:
`
while True:
    r,w,e = select.select([cs],[],[],0)
    if len(r)>0:req += cs.recv(1024)
    else:break
`
处发生了死循环,另外考虑到网络延迟,和恶意程序发送过大的http请求,代码修改如下:
`
while True:
    #set timeout to 0.1s
    r,w,e = select.select([cs],[],[],0.1)
    if len(r)>0:
        data = cs.recv(1024)
        #in case client close the connect
        if data==b"":break
        req += data
    else:break
    #in case too big request
    if len(req)>8*1024:break
`
完整修改已应用到[python的socket实现http服务器](http://182.92.214.184/?p=127)

异常分析:某些应用程序(浏览器或恶意程序)在连接到服务器,发送了request(或没有发送)之后,立即关闭了到服务器的连接(不一定关闭服务器到client的连接,这个可以参考TCP的四次挥手和python的socket模块的socket._socketobject.shutdown方法)

备注:真正的web服务器一般会逐行读取request的header(根据http协议),遇到header结束标志(以CRLF开始的一行),表示request的header的结束...