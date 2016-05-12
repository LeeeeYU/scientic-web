# -*- coding: utf-8 -*-
import MySQLdb
"""
Created on Sat Mar 19 10:38:26 2016

@author: Coco
"""
# cityName = 'shenzhen'
cityName = 'shanwei'
try:
    conn = MySQLdb.connect(
        host='localhost',
        user='ly',
        passwd='ly',
        port=3306,
        db='powerforest',
        charset='utf8')
    cur = conn.cursor()
    count = cur.execute("SELECT " +
                        "sum(powerConsume) AS powerConsume," +
                        "cityName," +
                        "CONCAT(year,'-',month,'-',day) as datetime," +
                        "year," +
                        "month," +
                        "day," +
                        "daytype " +
                        "from powerConsume_detail " +
                        "where year=2007 " +
                        "and cityName='" + cityName + "' " +
                        "GROUP BY year,month,day ")

#    oneResult = cur.fetchone()
    result = cur.fetchall()
    for index in range(len(result)):
        #    for index in range(1):
        row = result[index]
        print row
        # print "INSERT INTO `powerforest`.`powerConsume` (`powerConsume`,`cityName`,`date`, `year`, `month`, `day`, `daytype`) VALUES (%f, '%s', '%s', %d, %d, %d, '%s')" % row
        cur.execute(
            "INSERT INTO `powerforest`.`powerConsume` (`powerConsume`,`cityName`,`date`, `year`, `month`, `day`, `daytype`) VALUES (%f, '%s', '%s', '%i', '%i', %i, '%s')" % row)

    conn.commit()
    cur.close()
    conn.close()
except MySQLdb.Error, e:
    print e.args[0], ":", e.args[1]
