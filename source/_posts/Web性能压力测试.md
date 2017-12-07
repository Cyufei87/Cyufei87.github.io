---
title: Web性能压力测试
tags: [Web, 测试]
category: 技术探索
date: 2017-01-11 10:35:02
---

用ApacheBench进行网站压力测试
原理：ab命令会创建很多的并发访问线程，模拟多个访问者同时对某一URL地址进行访问。
使用方式网上有很多，主要参数是-n(请求总数，设为参数n)和-c(并发数，创建的线程数, 设为参数c)
结果分析：
Concurrency Level: 即参数c
Time taken for tests: 整个测试持续的时间, 设为参数t
Total transferred: 整个测试过程网络数据传输量，设为b
Requests per second(mean): 即n/t
Time per request(mean): 即t/(n/c)
Time per request(mean, across all concurrent requests): 即t/n
Transfer rate: 即b/t
根据我的使用经验，需要注意的是：
1.这个只是服务器性能测试，并不能测试网络状况。也因此，测试机网络状况需要足够好，相对于服务器的带宽要足够高（大于Transfer rate）
2.因为是固定URL, 可能有时测试并不能反映实际情况
3.根据需求，可以做集群压测，或者是单机压测