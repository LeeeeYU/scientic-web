# -*- coding: utf-8 -*-
"""
Created on Mon Apr 04 15:48:30 2016

@author: Coco
"""

import forest
import db
from datetime import datetime


def doPredict():
    f = forest.forest()
    f.setData('2007-1-21', 345)
    f.normalize()
    f.countSimilarity()
    f.predict()

    predict_plan = {"description": "test", "datetime": datetime.today().strftime("%Y-%m-%d %H:%M:%S"), "predict_rate": f.predict_rate, "minRel": f.minRel, "predictNum": f.predictNum}
    predict_plan_id = db.insertGetId("predict_plan", **predict_plan)
    predict_plan["plan_id"] = predict_plan_id

    for comparation in f.forestSimilarity:
        base = comparation.base
        base_info = {"pc_id": base.pc_id, "ah_id": base.ah_id, "predict_pc": base.powerConsume['predict'], "date": base.date}
        comparation_id = db.insertGetId("comparation", **base_info)
        for similarity in comparation.similarityEntitys:
            ap = similarity.ap
            ap_info = {"comparation_id": comparation_id, "pc_id": ap.pc_id, "ah_id": ap.ah_id, "similarity": similarity.similarity, "date": ap.date}
            db.insertGetId("similarity", **ap_info)

    db.commit()

    # print datetime.today().strftime("%Y-%m-%d %H:%M:%S")


def relevancyFile():
    from entity import fieldDescription, fieldUnit

    relevancy = forest.relevancy()
    atmNormalRel = relevancy.normalizeRel(relevancy.atmRel)
    atmNormalRel = sorted(atmNormalRel.iteritems(), key=lambda d: d[1], reverse=True)
    f = open('../relevancy.txt', 'w')
    for value in atmNormalRel:
        string = value[0] + " " + fieldDescription[value[0]] + " " + str(value[1]) + " " + str(abs(relevancy.atmRel[value[0]]))
        if value[0] in fieldUnit:
            string += " " + fieldUnit[value[0]]
        string += "\n"
        f.writelines(string)
    f.close()

if __name__ == '__main__':
    relevancyFile()
