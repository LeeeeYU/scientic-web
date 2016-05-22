# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 15:48:30 2016

@author: Coco
"""

from copy import copy

# powerConsume,daytype,airPressureAve,airPressureMax,airPressureMin,temperatureAve,temperatureMax,temperatureMin,,waterPressureAve,relativeHumidityAve,relativeHumidityMin,precipitation,smallEvaporation,largeEvaporation,windVelocityAve,windVelocityMax,windVelocityDirection,extremeWindVelocity,extremeWindVelocityDir,hoursOfSunshine
order = ['airPressureAve', 'airPressureMax', 'airPressureMin', 'temperatureAve', 'temperatureMax', 'temperatureMin', 'waterPressureAve',
         'relativeHumidityAve', 'relativeHumidityMin', 'precipitation', 'smallEvaporation', 'largeEvaporation', 'windVelocityAve', 'windVelocityMax', 'windVelocityDirection', 'extremeWindVelocity', 'extremeWindVelocityDir', 'hoursOfSunshine']
fieldDescription = {
    'airPressureAve': '平均气压',
    'airPressureMax': '日最高气压',
    'airPressureMin': '日最低气压',
    'temperatureAve': '平均气温',
    'temperatureMax': '日最高气温',
    'temperatureMin': '日最低气温',
    'waterPressureAve': '平均水汽压',
    'relativeHumidityAve': '平均相对湿度',
    'relativeHumidityMin': '最小相对湿度',
    'precipitation': '20-20时降水量',
    'smallEvaporation': '小型蒸发量',
    'largeEvaporation': '大型蒸发量',
    'windVelocityAve': '平均风速',
    'windVelocityMax': '最大风速',
    'windVelocityDirection': '最大风速的风向',
    'extremeWindVelocity': '极大风速',
    'extremeWindVelocityDir': '极大风速的风向',
    'hoursOfSunshine': '日照时数',
    'cityName': '城市',
    'powerConsume': '电力负荷',
    'daytype': '星期',
    'detailNum': '数据数量',
    'date': '日期',
    'year': '年',
    'month': '月',
    'day': '日'
}
fieldUnit = {
    'airPressureAve': '0.1hPa ',
    'airPressureMax': '0.1hPa ',
    'airPressureMin': '0.1hPa ',
    'temperatureAve': '0.1℃',
    'temperatureMax': '0.1℃',
    'temperatureMin': '0.1℃',
    'waterPressureAve': '0.1hPa',
    'relativeHumidityAve': '1% ',
    'relativeHumidityMin': '1% ',
    'precipitation': '0.1mm ',
    'smallEvaporation': '0.1mm ',
    'largeEvaporation': '0.1mm ',
    'windVelocityAve': '0.1m/s',
    'windVelocityMax': '0.1m/s',
    'windVelocityDirection': '方位',
    'extremeWindVelocity': '0.1m/s',
    'extremeWindVelocityDir': '方位',
    'hoursOfSunshine': '0.1小时',
    'powerConsume': 'kW·h'
}
atmosphere = ['airPressureAve',
              'airPressureMax',
              'airPressureMin',
              'temperatureAve',
              'temperatureMax',
              'temperatureMin',
              'waterPressureAve',
              'relativeHumidityAve',
              'relativeHumidityMin',
              'precipitation',
              'smallEvaporation',
              'largeEvaporation',
              'windVelocityAve',
              'windVelocityMax',
              'windVelocityDirection',
              'extremeWindVelocity',
              'extremeWindVelocityDir',
              'hoursOfSunshine']
atmosphereType = {'airPressureAve': 'airPressure',
                  'airPressureMax': 'airPressure',
                  'airPressureMin': 'airPressure',
                  'temperatureAve': 'temperature',
                  'temperatureMax': 'temperature',
                  'temperatureMin': 'temperature',
                  'waterPressureAve': 'waterPressure',
                  'relativeHumidityAve': 'relativeHumidity',
                  'relativeHumidityMin': 'relativeHumidity',
                  'precipitation': 'precipitation',
                  'smallEvaporation': 'smallEvaporation',
                  'largeEvaporation': 'largeEvaporation',
                  'windVelocityAve': 'windVelocity',
                  'windVelocityMax': 'windVelocity',
                  'windVelocityDirection': 'windVelocityDirection',
                  'extremeWindVelocity': 'extremeWindVelocity',
                  'extremeWindVelocityDir': 'extremeWindVelocityDir',
                  'hoursOfSunshine': 'hoursOfSunshine'
                  }


class AP(object):
    validAtmosphere = []
    __slots__ = ('atmosphereN', 'powerConsumeN', 'sevendayPowerConsumeN',
                 '_sevendayPowerConsume', '_cityName', '_date', '_atmosphere', '_powerConsume', '_daytype')

    def __init__(self, **args):
        self._cityName = ''
        self._date = ''
        self._atmosphere = {}

        self._sevendayPowerConsume = {}

        self._powerConsume = {}
        self._daytype = {'Monday': 0, 'Tuesday': 0, 'Wednesday': 0,
                         'Thursday': 0, 'Friday': 0, 'Saturday': 0, 'Sunday': 0}

        for key, value in args.items():
            if key == "cityName":
                self._cityName = value
            elif key == "date":
                self._date = value
            elif key == "powerConsume":
                self._powerConsume['real'] = float('%5.6f' % value)
            elif key == "daytype":
                if value == '0':
                    self._daytype['Monday'] = 1
                elif value == '1':
                    self._daytype['Tuesday'] = 1
                elif value == '2':
                    self._daytype['Wednesday'] = 1
                elif value == '3':
                    self._daytype['Thursday'] = 1
                elif value == '4':
                    self._daytype['Friday'] = 1
                elif value == '5':
                    self._daytype['Saturday'] = 1
                elif value == '6':
                    self._daytype['Sunday'] = 1
            elif key in AP.validAtmosphere:
                self._atmosphere[key] = int(value)

    def getSimilarityCompareData(self):
        return dict(self.atmosphereN, **self._daytype)

    def getPredictData(self, content):
        temp = []
        if 'A' in content:
            temp.extend(self.atmosphereN.values())
        if 'D' in content:
            temp.extend(self._daytype.values())
        if 'P' in content:
            temp.extend(self.sevendayPowerConsumeN.values())
        return temp

    @property
    def sevendayPowerConsume(self):
        return self._sevendayPowerConsume

    @sevendayPowerConsume.setter
    def sevendayPowerConsume(self, spc):
        self._sevendayPowerConsume = {}
        self._sevendayPowerConsume['oneday'] = spc[6]
        self._sevendayPowerConsume['twoday'] = spc[5]
        self._sevendayPowerConsume['threeday'] = spc[4]
        self._sevendayPowerConsume['fourday'] = spc[3]
        self._sevendayPowerConsume['fiveday'] = spc[2]
        self._sevendayPowerConsume['sixday'] = spc[1]
        self._sevendayPowerConsume['sevenday'] = spc[0]

    @property
    def cityName(self):
        return self._cityName

    @property
    def date(self):
        return self._date

    @property
    def atmosphere(self):
        return self._atmosphere

    @atmosphere.setter
    def atmosphere(self, atmosphere):
        self._atmosphere = atmosphere

    @property
    def powerConsume(self):
        return self._powerConsume

    @powerConsume.setter
    def powerConsume(self, powerConsume):
        self._powerConsume = powerConsume

    @property
    def daytype(self):
        return self._daytype
