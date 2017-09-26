---
title: 关于一致性Hash的一些思考
tags:
  - 技术探索
date: 2015-12-27 21:25:22
---

单位memcached服务器迁移，发现对一致性Hash仍有迷惑，在一番学习下，新认识到了以下几点(针对[libmemcached的一致性哈希算法](http://www.last.fm/user/RJ/journal/2007/04/10/rz_libketama_-_a_consistent_hashing_algo_for_memcache_clients))：

1.一致性Hash需要对不同的memcached服务器做Hash操作，而Hash的对象是memcached服务器相关字符串(见[update_continuum](https://github.com/trondn/libmemcached/blob/ca739a890349ac36dc79447e37da7caa9ae819f5/libmemcached/hosts.c#L102)方法中的变量sort_host)。而这个其实是很重要的，这个意味着，只要ip或port不变，此memcached的各个虚拟节点在一致性哈希环上的位置永远不变，增加或减少memcached服务器或其他操作对这个毫无影响。

2.虚拟节点是非常重要的，如果没有虚拟节点，一致性哈希在服务器节点比较少的情况下很可能出现严重不满足均衡性的情况，且新增加一个节点只能改善随机一个已有节点的压力。增加了虚拟节点，使上述情况出现的概率大幅度降低。

&nbsp;