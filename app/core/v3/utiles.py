# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 20:07:16 2016

@author: Coco
"""
from math import sqrt
class Dict(dict):
    '''
    Simple dict but support access as x.y style.

    >>> d1 = Dict()
    >>> d1['x'] = 100
    >>> d1.x
    100
    >>> d1.y = 200
    >>> d1['y']
    200
    >>> d2 = Dict(a=1, b=2, c='3')
    >>> d2.c
    '3'
    >>> d2['empty']
    Traceback (most recent call last):
        ...
    KeyError: 'empty'
    >>> d2.empty
    Traceback (most recent call last):
        ...
    AttributeError: 'Dict' object has no attribute 'empty'
    >>> d3 = Dict(('a', 'b', 'c'), (1, 2, 3))
    >>> d3.a
    1
    >>> d3.b
    2
    >>> d3.c
    3
    '''
    def __init__(self, names=(), values=(), **kw):
        super(Dict, self).__init__(**kw)
        for k, v in zip(names, values):
            self[k] = v

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Dict' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value


def enum(**enums):
    return type('Enum', (), enums)


def multipl(a, b):
    sumofab = 0.0
    for i in range(len(a)):
        temp = a[i] * b[i]
        sumofab += temp
    return sumofab


def sim_pearson(p1, p2):
    n = len(p1)
    # 求所有偏好的和
    sum1 = sum(p1)
    sum2 = sum(p2)
    # 求平方和
    sum1Sq = sum([pow(val, 2) for val in p1])
    sum2Sq = sum([pow(val, 2) for val in p2])
    # 求乘积和
    pSum = multipl(p1, p2)
    # 计算皮尔逊相关系数
    num = pSum - (float(sum1) * float(sum2) / n)
    den = sqrt(
        (sum1Sq - float(pow(sum1, 2)) / n) * (sum2Sq - float(pow(sum2, 2)) / n))
    if den == 0:
        return 0
    r = num / den
    return r


def clearList(list):
    del list[:]
    list = []
