---
title: django中的索引和约束
tags:
  - 技术探索
date: 2016-11-07 18:30:31
---

1.db_index控制单个field是否要创建索引
2.如果field是外键类型，则db_constraint控制是否有外键约束
3.如果是外键类型，默认会创建索引和约束
4.unique_together和index_together控制创建联合索引，在mysql中，联合索引中field的顺序会对部分查询产生影响