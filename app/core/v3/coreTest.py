# -*- coding: utf-8 -*-
"""
Created on Mon Mar 28 14:40:54 2016

@author: Coco
"""

import forest

# 测试 class engine

# db.init(db_type = 'Mysql',db_driver = None,user='ly',passwd='ly',charset='utf8',db='powerforest')
# ---------------以下用于测试forest的可用性---------------
bf = forest.forest()
bf.setData(90, "2007-11-30", 7)
bf.normalizeData()
bf.countSimilarity()
bf.predict()

print bf.evaluation
print bf.predictPC
#    ---------------截止---------------













# ---------------以下用于测试entity的可用性---------------
#results = db.select("select * from sw_history")
#powerconsume = []
#for row in results:
#    powerconsume.append(entity.PowerConsume(**row))
#for one in powerconsume:
#    print one

#results = db.select("select * from atmosphere_history")
#atms = []
#for row in results:
#    atms.append(entity.Atmosphere(**row))
#for one in atms:
#    print one
#    print

#results = db.select("select ah.*,sh.daytype,sh.detailNum,sh.powerConsume from atmosphere_history ah INNER JOIN sw_history sh on ah.date = sh.date")
#APs = []
#for row in results:
#    APs.append(entity.AP(**row))
#for one in APs:
#    print one
#    print

#    ---------------截止---------------




#count = db.select_int("select count(*) from sw_history")
#print results
#_EngineTest()
#db.engine.connect
# 测试 func connection
#def connectionTest():
#    _EngineTest()
#    with db.connection():
#        r = db.select("select * from sw_history")
#        print len(r)
#connectionTest()
#        
#with db.connection():
#    db.update('UPDATE sw_history SET cityName=? where his_id =?','111',3)
#    db.commit()