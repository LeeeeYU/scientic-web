# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 13:25:26 2016

@author: Coco
"""
from threading import local
from functools import wraps
import time
import MySQLdb
import logging
from utiles import Dict
def _log(msg):
    logging.debug(msg)




# 数据库引擎对象:
class DBError(Exception):
    pass
class MutiColumnsError(DBError):
    pass
def _dummy_connect():
    pass

def _profiling(start, sql=''):
    t = time.time() - start
    if t > 0.1:
        logging.warning('[PROFILING] [DB] %s: %s' % (t, sql))
    else:
        logging.info('[PROFILING] [DB] %s: %s' % (t, sql))

#    raise DBError('Database is not initialized. call init(dbn, ...) first.')
_db_connect = _dummy_connect()
_db_convert = '?'

def init_connect(connect,convert='%?'):
    _log("init database connect.....")
    global _db_connect , _db_convert
    _db_connect = connect
    _db_convert = convert
def init(db_type,db_driver = None,**db_args):
    """
        initialize database.
        
        args:
            db_type : 'mysql'
            db : database name
            host : db host
            port : db port
            user : username
            passwd : userpassword
            driver : db deriver,default to None
            **db_args : other parameters , e.g. charset = 'utf8'
    """
    global _db_connect , _db_convert
    db_type = db_type.lower()
    if db_type == 'mysql':
        _log('init mysql...')
        default_args = {
            'host' : 'localhost',
            'port' : 3306,
            'db' : '',
            'user' : '',
            'passwd' : '',
            'use_unicode' : True,
            'charset' : 'utf8'
        }
        import MySQLdb
        for k,v in default_args.iteritems():
            db_args[k] = db_args.get(k,v)
        _db_connect = MySQLdb.connect(**db_args)
        _db_convert = '%s'
    else:
        raise DBError('Unsupported db: %s' % db_type)

class _LasyConnection(object):
    def __init__(self):
        self.connection = None
    
    def cursor(self):
        if self.connection is None:
            _log('open connection')
            self.connection = _db_connect
        return self.connection.cursor()
    def commit(self):
        self.connection.commit()
    def rollback(self):
        self.connection.rollback()
    def cleanup(self):
        if self.connection:
            _connection = self.connection
            self.connection = None
            _log('close connection')
            _connection.close()

# 持有数据库连接的上下文对象:
class _DbCtx(local):
    def __init__(self):
        self.connection = None
        self.transactions = 0

    def is_init(self):
        return not self.connection is None

    def init(self):
        global engine
        self.connection = _LasyConnection()
        self.transactions = 0

    def cleanup(self):
        self.connection.cleanup()
        self.connection = None

    def cursor(self):
        if self.connection is None:
            self.init()
        return self.connection.cursor()

_db_ctx = _DbCtx()


class _ConnectionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exctype, excvalue, traceback):
        global _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()
def connection():
    return _ConnectionCtx()

def _select(sql,first=False,*args):
    global _db_connect , _db_convert
    cur = None
    if _db_convert != '?':
        sql = sql.replace('?',_db_convert)
    _log("SQL:%s , ARGS:%s" % (sql,args))
    start = time.time()
    try:
        cur = _db_ctx.cursor()
        cur.execute(sql,args)
        if cur.description:
            names = [x[0] for x in cur.description]
        if first:
            values = cur.fetchone()
            if not values:
                return None
            return Dict(names,values)
        results = [Dict(names,x) for x in cur.fetchall()]
        return results
    except MySQLdb.Error,e:
        print e[0],":",e[1]
    finally:
        if cur:
            cur.close()
        _profiling(start, sql)
def select_one(sql,*args):
    return _select(sql,True,*args)

def select_int(sql,*args):
    results = _select(sql,True,*args)
    if results is None:
        return 0
    if len(results)!=1:
        raise MutiColumnsError("expect only one column")
    return results.values()[0]

def select(sql,*args):
    return _select(sql,False,*args)

def _update(sql,args,post_func = None):
    cur = None
    if _db_convert != '?':
        sql = sql.replace('?',_db_convert)
    start = time.time()
    try:
        cur = _db_ctx.cursor()
        cur.execute(sql,args)
        row = cur.rowcount()
        print row
        post_func is not None and post_func()
        return row
    except:
        pass
    finally:
        if cur:
            cur.close()
        _profiling(start,sql)

def insert(table,**kw):
    cols,args = zip(*kw.iteritems)
    sql = "INSERT INTO %s (%s) VALUES(%s)" % (table,','.join(cols),','.join([_db_convert for i in range(len(cols))]))
    return _update(sql,args)
def update(sql,*args):
    return _update(sql,args)
def commit():
    try:
        _db_ctx.connection.commit()
    except:
        rollback()
        raise
def update_kw(table, where, *args, **kw):
    if len(kw)==0:
        raise ValueError('No kw args.')
    sqls = ['update', table, 'set']
    params = []
    updates = []
    for k, v in kw.iteritems():
        updates.append('%s=?' % k)
        params.append(v)
    sqls.append(', '.join(updates))
    sqls.append('where')
    sqls.append(where)
    sql = ' '.join(sqls)
    params.extend(args)
    return update(sql, *params)

def rollback():
    _db_ctx.connection.rollback()


init(db_type = 'Mysql',db_driver = None,user='ly',passwd='ly',charset='utf8',db='powerforest')
