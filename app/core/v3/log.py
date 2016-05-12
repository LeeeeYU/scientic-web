# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 14:40:17 2016

@author: Coco
"""
# --------------测试logging功能------------------
#import logging  
#logging.basicConfig(level=logging.DEBUG,  
#                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',  
#                    datefmt='%a, %d %b %Y %H:%M:%S',  
#                    filename='./test.log',  
#                    filemode='w')  
#  
#logging.debug('debug message')  
#logging.info('info message')  
#logging.warning('warning message')  
#logging.error('error message')  
#logging.critical('critical message')  


# --------------测试python变量作用域------------------
#a='a'
#c='c'
#def test():
#    global a
#    c
#    print a
#    print c
#    
#test()
#print c



# ---------------测试装饰器和with as使用在多个函数下的情况--------------------
#class _connection(object):
#    def __init__(self):
#        self.transaction = 0
#    def __enter__(self):
#        print 'check connection'
#    def __exit__(self, exctype, excvalue, traceback):
#        print "close connection"
#
#def connection():
#    return _connection()
#
#def update():
#    print 'update data'
#
#def delete():
#    print 'delete data'
#
#def select():
#    print 'select data'
#def commit():
#    print 'commit'
#with connection():
#    select()
#    update()
#    commit()



class TestMetaclass(type):
    subclass = {}
    def __new__(cls,name,bases,attrs):
        print name
        return type.__new__(cls,name,bases,attrs)

class Test(object):
    __metaclass__ = TestMetaclass
    def __init__(self):
        print 1

Test()

