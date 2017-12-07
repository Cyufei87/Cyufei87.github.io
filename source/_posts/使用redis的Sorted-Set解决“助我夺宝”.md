---
title: 使用redis的Sorted Set解决“助我夺宝”
tags: [redis]
category: 技术探索
date: 2017-03-16 20:01:46
---

助我夺宝需求描述如下：
1.用户可以助威好友
2.用户按照助威数和最后一个助威的时间排名
3.排名特定区间的用户可以获得奖品，如排名1-3获得奖品一，排名4-8可以获得奖品二，等等
4.实时获取用户当前排名，以及距离下一区间奖品需要的助威数

问题的难点在于用户的排名是不断变化中的，利用redis的Sorted Set却可以比较好的完成这项需求

首先可以用关系型数据库mysql存储
prize表 -- 奖品信息
user表 -- 用户信息
access_record表 -- 用户助威好友的记录

然后设置Sorted Set的
member -- 用户ID
score -- 助威数*1e10 + (1e10 - 助威记录ID) # 这里假设助威记录ID小于1e10(根据redis文档，score的取值范围是-2^53与2^53之间)，助威记录ID按照时间递增

然后就可以提供以下功能：
助威 -- 先使用zscore取出旧的score，然后可以算出之前的助威数，将助威数加1，再用zadd将新的score存入redis
计算用户排名 -- 使用zrevrank
获取排名前num的用户 -- 使用zrevrange
计算某一用户距离下一区间奖品需要的助威数 -- 先取出此用户对应rank和score,根据rank计算下一排名区间的最低rank(如4-8名获得奖品二，8-15名获得奖品三，用户当前rank为10，则下一区间奖品最低rank为8)，使用zrevrange得到最低rank对应的score_min,根据score_min和score分别计算得到助威数help_num_min和help_num,则help_num_min+1-help_num即是需要的助威数

假设参与排名的用户数为n个，以上用到的redis操作中，zadd, zrevrank的时间复杂度为O(log(n)),zrevrang根据取出的元素的个数m时间复杂度为O(log(n)+m),zscore的时间复杂度为O(1)