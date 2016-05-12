# -*- coding: utf-8 -*-
import MySQLdb
"""
Created on Sun Mar 20 15:50:23 2016

@author: Coco
"""
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
    cur.execute("SELECT " +
                "MAX(ah.airPressureMax) as airPressureMax," +
                "MIN(ah.airPressureMin) as airPressureMin," +
                "MAX(ah.temperatureMax) as temperatureMax," +
                "MIN(ah.temperatureMin) as temperatureMin," +
                "MAX(ah.waterPressureAve) as waterPressureMax," +
                "MIN(ah.waterPressureAve) as waterPressureMin," +
                "MAX(ah.`20-20precipitation`) as `20-20precipitationMax`," +
                "MAX(ah.smallEvaporation) as smallEvaporationMax," +
                "MIN(ah.smallEvaporation) as smallEvaporationMin," +
                "MAX(ah.largeEvaporation) as largeEvaporationMax," +
                "MIN(ah.largeEvaporation) as largeEvaporationMin," +
                "MAX(ah.windVelocityMax) as windVelocityMax," +
                "MAX(ah.hoursOfSunshine) as hoursOfSunshineMax," +
                "MIN(ah.hoursOfSunshine) as hoursOfSunshineMin" +
                " FROM " +
                "atmosphere_history ah" +
                " where cityname='" + cityName + "'")
    result = cur.fetchone()
    print result
except MySQLdb.Error, e:
    print e.args[0], ":", e.args[1]
