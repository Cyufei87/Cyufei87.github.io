# -*- coding: utf-8 -*-
""" 理解Python的闭包 """
global_var = 100


def add1(a, b):
    return global_var + a + b


def add_one(b):
    def real_add(a):
        return global_var + a + b
    return real_add
add2 = add_one(2)


def add_one_default(default_b):
    def real_add_default(a, b=default_b):
        return global_var + a + b
    return real_add_default
add3 = add_one_default(3)


def add_global_deco(func):
    def _func(*args, **kwargs):
        return func(*args, **kwargs) + global_var
    return _func


@add_global_deco
def add4(a, b):
    return a + b


if __name__ == '__main__':
    print("add1.__closure__ is %s" % repr(add1.__closure__))
    # add1.__closure__ is None
    print("add2.__closure__ is %s" % repr(add2.__closure__))
    # add2.__closure__ is (<cell at 0x10437a7f8: int object at 0x7fea2e605460>,)
    print("add3.__closure__ is %s" % repr(add3.__closure__))
    # add3.__closure__ is None
    print("add4.__closure__ is %s" % repr(add4.__closure__))
    # add4.__closure__ is (<cell at 0x10437a830: function object at 0x104377578>,)
