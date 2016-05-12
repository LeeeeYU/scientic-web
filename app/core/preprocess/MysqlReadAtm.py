# -*- coding: utf-8 -*-

import MySQLdb

"""
Created on Thu Mar 17 17:14:19 2016

@author: Coco
"""
try:
    conn = MySQLdb.connect(
        host='localhost',
        user='ly',
        passwd='ly',
        port=3306,
        db='powerforest',
        charset='utf8')

    cur = conn.cursor()

    wb = open('../atm_of_shanwei.txt', 'r')
    wb.readline()
    line = wb.readline()
    while line:
        content = line.strip()
        ca = content.split(' ')
        ca.append('shanwei')
        ca.append(ca[1] + "-" + ca[2] + "-" + ca[3])
# print "INSERT INTO"+"powerforest.atmosphere_history ("+"station_id,
# year, month, day, airPressureAve, airPressureMax, airPressureMin,
# temperatureAve, temperatureMax, temperatureMin, waterPressureAve,
# relativeHumidityAve, relativeHumidityMin, `20-20precipitation`,
# smallEvaporation, largeEvaporation, windVelocityAve, windVelocityMax,
# windVelocityDirection, extremeWindVelocity, extremeWindVelocityDir,
# hoursOfSunshine,cityName, date) "+"VALUES ('%s', '%s', '%s', '%s', '%s',
# '%s', '%s', '%s', '%s, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s',
# '%s', '%s', '%s', '%s', '%s', '%s','%s')"% tuple(ca)
        cur.execute("INSERT INTO " +
                    "powerforest.atmosphere_history (" +
                    "station_id, year, month, day," +
                    "airPressureAve, airPressureMax," +
                    "airPressureMin, temperatureAve," +
                    "temperatureMax, temperatureMin," +
                    "waterPressureAve, relativeHumidityAve," +
                    "relativeHumidityMin, `precipitation`," +
                    "smallEvaporation, largeEvaporation," +
                    "windVelocityAve, windVelocityMax," +
                    "windVelocityDirection, extremeWindVelocity," +
                    "extremeWindVelocityDir, hoursOfSunshine,cityName," +
                    "date) " +
                    " VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s','%s')" % tuple(ca))
        line = wb.readline()
    conn.commit()
    cur.close()
    conn.close()
except MySQLdb.Error, e:
    print e.args[0], ":", e.args[1]
