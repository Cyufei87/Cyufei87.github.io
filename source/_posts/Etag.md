---
title: Etag
tags:
  - 技术探索
date: 2015-08-12 11:10:35
---

偶然注意到，线上服务器返回的数据都是304，而我很清楚的知道，我没在服务器端添加任何比较长时间的缓存

而测试服务器上每次都是正常的200

怀疑是负载均衡的问题，于是直接通过线上应用服务器的ip访问，依旧304

怀疑是nginx的问题，于是直接访问nginx代理的后台服务，仍然304

抓包发现，在response Headers里多了一个不熟悉的Etag..

上网查了一下，貌似问题就在于此

在项目代码里搜索Etag，发现Tornado会自动的对于200的GET和HEAD加上Etag并检测If-None-Match，具体代码在tornado.web.RequestHandler.finish，摘录如下：

`
# Automatically support ETags and add the Content-Length header if
# we have not flushed any content yet.
if not self._headers_written:
    if (self._status_code == 200 and
        self.request.method in ("GET", "HEAD") and
        "Etag" not in self._headers):
        etag = self.compute_etag()
        if etag is not None:
            self.set_header("Etag", etag)
            inm = self.request.headers.get("If-None-Match")
            if inm and inm.find(etag) != -1:
                self._write_buffer = []
                self.set_status(304)
    if self._status_code == 304:
        assert not self._write_buffer, "Cannot send body with 304"
        self._clear_headers_for_304()
    elif "Content-Length" not in self._headers:
        content_length = sum(len(part) for part in self._write_buffer)
        self.set_header("Content-Length", content_length)
`

还有一个问题是，为什么测试服务器没有Etag?

经过一番探索，发现nginx在1.4.0后的某个版本中，增加了这样一条规则：如果使用了gzip，自动把Etag去除.....而测试服务器的ngxin的版本是1.6.0，线上服务器的nginx的版本是1.0.4....

值得说明的是，在nginx的比较新的版本中（譬如1.8.0），规则改为：如果使用了gzip，如果Etag是weak的，不做改变，如果是非weak的，将其改为weak的，具体可参见[ngx_http_core_module.c](https://github.com/nginx/nginx/blob/220c36d6128bcf3e869fdd0f7767ead9a4222f08/src/http/ngx_http_core_module.c)的ngx_http_weak_etag方法