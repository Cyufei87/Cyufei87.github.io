---
title: Python多进程写文件时的一些探究
date: 2017-10-27 20:48:41
tags: [Python, 多进程]
category: 技术探索
---
### 问题提出
在没有并发控制的情况下，Python多进程向同一个文件写数据(限制单次写入数据大小)是安全的吗？
这里的安全是指：
1. 不会有进程的日志丢失（被覆盖）
2. 两次写入的数据不会相互混着输出（譬如A进程单次写入aaaa，B进程写入bbbb，最后的日志不会出现aaababbb）

### 测试
首先，我做了四个测试，测试代码如下(test.py)：
```python
# -*- coding: utf-8 -*-
import os
import sys
import time


class TestBase(object):
    buffering = -1
    test_filename = None
    f = None

    @classmethod
    def init_file(cls):
        assert cls.test_filename is not None
        cls.f = open(cls.test_filename, "w", buffering=cls.buffering)


class Test1(TestBase):
    """测试一
    * buffering参数默认
    * 无自定义buffer控制
    * 文件在进程fork前打开
    """
    test_filename = 'file1.tmp'

    @classmethod
    def run(cls, char, process):
        start_time = time.time()
        chars = "%s\n" % (char * 10)
        for _ in range(int(1e5)):
            cls.f.write(chars)
        cls.f.close()
        print "%s consume %ss" % (process, time.time() - start_time)


class Test2(Test1):
    """测试二
    * 设置buffering参数
    * 无自定义buffer控制
    * 文件在进程fork前打开
    """
    buffering = 1024
    test_filename = 'file2.tmp'


class Test3(TestBase):
    """测试三
        * 设置buffering参数
        * 自定义buffer控制
        * 文件在进程fork前打开
        """
    buffering = 1024
    test_filename = 'file3.tmp'

    @classmethod
    def run(cls, char, process):
        buffer_size = cls.buffering
        start_time = time.time()
        chars = "%s\n" % (char * 10)
        buffer_used = 0
        for _ in range(int(1e5)):
            if buffer_used + len(chars) >= buffer_size:
                cls.f.flush()
                buffer_used = 0
            cls.f.write(chars)
            buffer_used += len(chars)
        cls.f.close()
        print "%s consume %ss" % (process, time.time() - start_time)


class Test4(Test3):
    """测试四
        * 设置buffering参数
        * 自定义buffer控制
        * 文件在进程fork后打开
        """
    test_filename = 'file4.tmp'


if __name__ == '__main__':
    test_num = int(sys.argv[1])
    test_class_map = {
        1: Test1,
        2: Test2,
        3: Test3,
        4: Test4,
    }
    test_class = test_class_map.get(test_num)
    if not test_class:
        sys.stderr.write("unknown test_num")
        sys.exit(1)

    # 前3个测试，在fork前打开文件
    if test_num <= 3:
        test_class.init_file()

    if os.fork() == 0:  # child process
        char = 'a'
        process = 'child'
    else:  # parent process
        char = 'b'
        process = 'parent'

    # 第四个测试，在fork后打开文件
    if test_num == 4:
        test_class.init_file()
    test_class.run(char, process)
```
在都是利用os.fork实现多进程([在Unix下，multiprocessing库默认也是使用os.fork](https://docs.python.org/3/library/multiprocessing.html#contexts-and-start-methods))写一个文件的情况下，四个测试主要有以下不同：
* 在调用Python内建函数[open](https://docs.python.org/2/library/functions.html#open)时，是否设置buffering，默认是-1(也是Python默认值)
* 是否有自定义buffering控制。这里的自定义buffering控制是指，上层代码检测在进行此次写入时，是否会造成缓冲区溢出(大于buffer_size)，如果溢出，先进行flush操作，再进行write操作
* 文件是在fork前还是之后打开

分别执行
```bash
python test.py 1
python test.py 2
python test.py 3
python test.py 4
```
得出结果如下：
测试环境：MAC OS X

| 测试 | Python 2.7.13 | Python 3.6.2 |
| :-: | :-: | :-: |
| Test1 | 无丢失发生，数据混着输出 | 正常 |
| Test2 | 无丢失发生，数据混着输出 | 正常 |
| Test3 | 正常 | 正常 |
| Test4 | 数据丢失一半 | 数据丢失一半 |

### 结果分析
#### 为什么Python 2和Python 3的结果不一样呢？
Python 3使用了New I/O([PEP 3116](https://www.python.org/dev/peps/pep-3116/))。而一个重要的变化是，Python 3在自己这一层实现了buffer机制。[Python 2写文件使用的是C库函数fwrite](https://github.com/python/cpython/blob/2.7/Objects/fileobject.c#L1856)，而buffer机制完全依靠fwrite。[Python 3使用的是write系统调用](https://github.com/python/cpython/blob/3.6/Python/fileutils.c#L1268)，buffer机制是自己实现的

#### 为什么在Python 2中，Test3是正常的呢？
这个推断是在buffer满时，fwrite的处理是不能保证多进程安全的。而在上层代码强制flush的情况下，能保证数据正常写入文件

#### 为什么在fork之后打开文件时，数据会丢失呢？
这个和fork操作对每个文件的current stream position(即调用tell方法返回的)的处理有关，参考[这里](http://blog.csdn.net/u011508527/article/details/46878205)

### 其他

#### Nginx的ngx_http_log_module模块的I/O处理
根据[文档](http://nginx.org/en/docs/http/ngx_http_log_module.html#open_log_file_cache)，说明了在启用buffering时，写入文件的时机：
> When buffering is enabled, the data will be written to the file:
> if the next log line does not fit into the buffer;
> if the buffered data is older than specified by the flush parameter (1.3.10, 1.2.7);
> when a worker process is re-opening log files or is shutting down.

根据[这儿的源代码](https://github.com/phusion/nginx/blob/stable-1.2/src/os/unix/ngx_files.c#L68)，Nginx会根据NGX_HAVE_PWRITE宏的设置，使用pwrite或者write

#### 关于fwrite，write，pwrite的一些讨论：
1. [pwrite(3) - Linux man page](https://linux.die.net/man/3/pwrite)
2. [What are the advantages of pwrite and pread over fwrite and fread?](https://stackoverflow.com/questions/7592822/what-are-the-advantages-of-pwrite-and-pread-over-fwrite-and-fread)
3. [linux下多进程写入文件的原子性](http://tsecer.blog.163.com/blog/static/1501817201311284223689/)

引用1
> Atomic/non-atomic: A write is atomic if the whole amount written in one operation is not interleaved with data from any other process. This is useful when there are multiple writers sending data to a single reader. Applications need to know how large a write request can be expected to be performed atomically. This maximum is called {PIPE_BUF}. This volume of IEEE Std 1003.1-2001 does not say whether write requests for more than {PIPE_BUF} bytes are atomic, but requires that writes of {PIPE_BUF} or fewer bytes shall be atomic.

及根据2，可知在写入少于{PIPE_BUF}bytes的数据时，write及pwrite系统调用应该是原子的
而fwrite相对于write/pwrite有内置buffering，在没有自定义buffering的情况下，能很大的提升写文件的性能
#### Python的logging模块
logging模块的FileHandler也是采用的open函数，在多进程情况下，也符合以上讨论

#### Java的I/O处理
跟据[PEP 3116](https://www.python.org/dev/peps/pep-3116/)中的描述
> The new I/O spec is intended to be similar to the Java I/O libraries, but generally less confusing.

看来Java对I/O的处理更加类似Python 3
