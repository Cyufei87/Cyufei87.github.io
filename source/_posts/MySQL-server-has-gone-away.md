---
title: '''MySQL server has gone away'''
tags:
  - 技术探索
date: 2017-01-19 21:50:12
---

一个很久没有运行的后台服务，在接收到数据，运行时，报了这个错误
原因是服务用的Django ORM与mysql在长久没有数据交互后，它们之间的长连接断掉了。

以下分析基于django1.6.0
Djando自带的ORM是比较定制化的，在django处理一个web请求时，在请求开始时，和请求处理完成时，Django都会尝试关闭数据库连接，如下[代码](https://github.com/django/django/blob/stable/1.6.x/django/db/__init__.py#L87)所示:
`
# Register an event to reset transaction state and close connections past
# their lifetime. NB: abort() doesn't do anything outside of a transaction.
def close_old_connections(**kwargs):
    for conn in connections.all():
        # Remove this when the legacy transaction management goes away.
        try:
            conn.abort()
        except DatabaseError:
            pass
        conn.close_if_unusable_or_obsolete()
signals.request_started.connect(close_old_connections)
signals.request_finished.connect(close_old_connections)
`
不过，根据[close_if_unusable_or_obsolete](https://github.com/django/django/blob/stable/1.6.x/django/db/backends/__init__.py#L461)的定义，除了自动提交和发生错误两种情况外，连接是否确定关闭，还取决于close_at的值，
`
def close_if_unusable_or_obsolete(self):
    """
    Closes the current connection if unrecoverable errors have occurred,
    or if it outlived its maximum age.
    """
    if self.connection is not None:
        # If the application didn't restore the original autocommit setting,
        # don't take chances, drop the connection.
        if self.get_autocommit() != self.settings_dict['AUTOCOMMIT']:
            self.close()
            return

        if self.errors_occurred:
            if self.is_usable():
                self.errors_occurred = False
            else:
                self.close()
                return

        if self.close_at is not None and time.time() >= self.close_at:
            self.close()
            return
`
[self.close_at](https://github.com/django/django/blob/stable/1.6.x/django/db/backends/__init__.py#L109)会在连接时改变:
`
max_age = self.settings_dict['CONN_MAX_AGE']
self.close_at = None if max_age is None else time.time() + max_age
`
所以，具体到每个请求是否关闭连接，还取决于CONN_MAX_AGE的配置，而CONN_MAX_AGE的默认值是0，所以默认情况下，每次处理完毕web请求时，都会关闭数据库连接。
另外一个很重要的一点是，Django中，存储数据库连接的字典是基于[线程](https://github.com/django/django/blob/stable/1.6.x/django/db/utils.py#L148)的：
`
class ConnectionHandler(object):
    def __init__(self, databases=None):
        """
        databases is an optional dictionary of database definitions (structured
        like settings.DATABASES).
        """
        self._databases = databases
        self._connections = local()
`
所以，如果你的web服务器的网络架构是多线程或者多进程的，即使设置CONN_MAX_AGE不为0，也不会复用旧的数据库连接，在这种情况下，如果数据库是mysql，因为Django orm不再会主动关闭数据库连接，mysql服务器会根据[wait_timeout](http://dev.mysql.com/doc/refman/5.7/en/server-system-variables.html#sysvar_wait_timeout)的设置，一直等待着，这种情况下，很有可能，造成mysql连接数过多，反而适得其反。
如果web服务器是单线程或者协程的，例如我测试用的gunicorn+gevents，适当的设置CONN_MAX_AGE，则会复用数据库连接，提升性能。

回到我们遇到的错误。。
我们的服务只用到了Django的ORM，所以在web请求开始和关闭时，django对数据库连接的尝试关闭对于我们的情况完全无效，服务又是一直跑着的单进程单线程，所以，在服务启动时，直到终止，会一直只用同一个数据库连接，长时间的服务不连接数据库，mysql会根据wait_timeout的设置，关闭了连接，所以也就导致了2006，'MySQL server has gone away'错误。
之前，使用tornado提供web服务，而使用Django的ORM时，也遇到过这样的错误，原理一样。
解决方法有：
1.增加mysql中wait_timeout的值，但这有一定的风险，而且不能从根本上解决问题。
2.同Django中的做法，在不需要数据库连接时或者开始数据库操作前，尝试关闭数据库连接。
3.自己DIY了一个变量CONN_WAIT_AGE，同时修改代码如下：
修改[函数](https://github.com/django/django/blob/stable/1.6.x/django/db/backends/__init__.py#L32)，增加：
`
self.conn_wait_age = settings_dict.get("CONN_WAIT_AGE", None)
self.last_access_at = time.time()
`
修改[函数](https://github.com/django/django/blob/stable/1.6.x/django/db/backends/__init__.py#L102)，增加：
`
self.last_access_at = time.time()
`
修改[函数](https://github.com/django/django/blob/stable/1.6.x/django/db/backends/__init__.py#L131)为：
`
def _cursor(self):
    # add by zhaohui, in case, "2006, 'MySQL server has gone away'" error
    if self.conn_wait_age is not None:
        n = time.time()
        if self.last_access_at + self.conn_wait_age < n and self.connection is not None and not self.is_usable():
            self.close()
        self.last_access_at = n
    self.ensure_connection()
    with self.wrap_database_errors:
        return self.create_cursor()
`
CONN_WAIT_AGE需要设置为比wait_timeout小的值，不设置为不启用。