# -*- coding: utf-8 -*-
"""
Created on Sat Apr 23 10:53:22 2016

@author: Coco
"""
import MySQLdb
from datetime import timedelta
# dt = datetime.datetime(2007,4,1)
# print dt
# dt = dt+datetime.timedelta(0,15*60)
# print dt
try:
    conn = MySQLdb.connect(
        host='localhost',
        user='ly',
        passwd='ly',
        port=3306,
        db='powerforest',
        charset='utf8')
    cur = conn.cursor()
    cur.execute(
        "SELECT datetime,powerConsume FROM powerConsume_detail where cityName='shanwei' ORDER BY datetime")
    result = cur.fetchall()

    endDate = result[len(result) - 1][0]
    curIndex = 0
    while result[curIndex][0] < endDate:
        interval = result[curIndex + 1][0] - result[curIndex][0]
        if interval > timedelta(0, 900):
            n = 0
            while interval > timedelta(0, 900):
                interval -= timedelta(0, 900)
                n += 1
            pc_range = result[curIndex + 1][1] - result[curIndex][1]
            for x in xrange(n):
                dt = result[curIndex][0] + timedelta(0, 900 * (x + 1))
                powerConsume = result[curIndex + x][1] + (x + 1) * pc_range / n
                # print dt,powerConsume    #打印缺失的数据
                cur.execute("INSERT INTO `powerforest`.`powerConsume_detail` " + \
                    "(`cityName`, `powerConsume`, `datetime`, `year`, `month`, `day`, `daytype`, `time`) " + \
                     "VALUES (" + \
                    "'shanwei', '" + str(powerConsume) + "', '" + str(dt) + "', " + str(dt.year) + ", " + str(dt.month) + ", " + str(dt.day) + ", " + str(dt.weekday()) + ", '" + str(dt.time()) + "')")
                conn.commit()
                # print "INSERT INTO `powerforest`.`powerConsume_detail` "+\
                #                 "(`cityName`, `powerConsume`, `datetime`, `year`, `month`, `day`, `daytype`, `time`) "+\
                #               "VALUES ("+\
                #                 "'shanwei', '"+str(powerConsume)+"', '"+str(dt)+"', "+str(dt.year)+", "+str(dt.month)+", "+str(dt.day)+", "+str(dt.weekday())+", '"+str(dt.time())+"')"
        curIndex += 1
    conn.close()
except MySQLdb.Error, e:
    print e.args[0], ":", e.args[1]
