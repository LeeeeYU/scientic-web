# -*- coding: utf-8 -*-
from app import app
from flask import render_template, flash, redirect, jsonify, request
from .forms import LoginForm
from init import relevancy as rel
from .core.v3 import db


@app.route('/')
@app.route('/index')
def index():
    user = {'nickname': 'ly'}
    return render_template("index.html", title='Home', user=user)
    # return "hello, world!"


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')

    return render_template('login.html')


@app.route('/ajax')
def ajax():
    return render_template('ajax.html')


@app.route('/getData')
def getData():
    return jsonify(result=1)


@app.route("/echarts-demo")
def echartsDemo():
    return render_template("echarts-demo.html")


@app.route("/relevancy")
def relevancy():
    return render_template("relevancy.html", navigate="relevancy")


@app.route("/json/getRelevancy")
def getRelevancy():
    data = {}
    category = []
    series = [[], []]
    for value in rel:
        category.append(value[1])
        series[0].append(value[2])
        series[1].append(value[3])
    data['legend'] = [u'气象相关度', u"气象相关度(normal)"]
    data['category'] = category
    data['series'] = []
    data['series'].append({"data": series[1], "name": u"气象相关度(normal)", "type": "bar"})
    data['series'].append({"data": series[0], "name": u"气象相关度", "type": "bar"})
    return JSONResponse(200, data)


@app.route("/history_powerComsume")
def historyPowerConsume():
    return render_template("history_powerConsume.html", navigate="history_powerConsume")


@app.route("/json/getHistoryPowerConsume")
def getHistoryPowerConsume():
    dates = db.select("SELECT DISTINCT year,month FROM powerconsume where year = 2007 ORDER BY year,month")
    series = []
    legend = ["日电力负荷"]
    category = []
    temp = []
    for date in dates:
        powerconsume = db.select("SELECT powerConsume,day FROM powerconsume WHERE year = " + str(date['year']) + " and month = " + str(date['month']) + " ORDER BY date")
        category.extend([str(date['month']) + "-" + str(value['day']) for value in powerconsume])
        temp.extend([float("%5.6f" % value["powerConsume"]) for value in powerconsume])
    series.append({"data": temp, "name": "日电力负荷", "type": "line"})
    data = {"series": series, "legend": legend, "category": category}
    return JSONResponse(200, data)


@app.route("/history_atmsphere")
def historyAtmsphere():
    return render_template("/history_atmsphere.html", navigate="history_atmsphere")


@app.route("/json/getHistoryAtmsphereAndPC")
def getHistoryAtmsphereAndPC():
    dates_pc = db.select("SELECT DISTINCT year,month FROM powerconsume where year = 2007 ORDER BY year,month")
    series = []
    legend = ["日电力负荷", rel[0][1]]
    category = []
    temp_pc = []
    for date in dates_pc:
        powerconsume = db.select("SELECT powerConsume,day FROM powerconsume WHERE year = " + str(date['year']) + " and month = " + str(date['month']) + " ORDER BY date")
        category.extend([str(date['month']) + "-" + str(value['day']) for value in powerconsume])
        temp_pc.extend([float("%5.6f" % value["powerConsume"]) for value in powerconsume])
    series.append({"data": temp_pc, "name": "日电力负荷", "type": "line"})

    dates_atm = db.select("SELECT %s FROM atmosphere_history WHERE year=2007 ORDER BY year,month,day" % rel[0][0])
    temp_atm = [int(value[rel[0][0]]) for value in dates_atm]
    series.append({"data": temp_atm, "name": rel[0][1], "type": "line", "unit": rel[0][4]})

    data = {"series": series, "legend": legend, "category": category}
    return JSONResponse(200, data)


@app.route("/json/getRawRelevancy")
def getRawRelevancy():
    return JSONResponse(status=200, data=rel)


@app.route("/json/getHistoryAtmsphere")
def getHistoryAtmsphere():
    atm_type = request.args.get('atmsphere', None)
    if atm_type is None or atm_type is "":
        atm_type = rel[0][0]
    atm = []
    for value in rel:
        if value[0] == atm_type:
            atm = value
            break
    series = []
    legend = [atm[1], ]
    category = []
    dates_atm = db.select("SELECT %s FROM atmosphere_history WHERE year=2007 ORDER BY year,month,day" % atm_type)
    temp_atm = [int(value[atm[0]]) for value in dates_atm]
    series.append({"data": temp_atm, "name": atm[1], "type": "line", "unit": atm[4]})

    data = {"series": series, "legend": legend, "category": category}
    return JSONResponse(status=200, data=data)


@app.route("/similarity")
def similarity():
    return render_template("similarity.html", navigate="similarity")


@app.route("/json/getSimilarity")
def getSimilarity():
    date = request.args.get('date', None)
    data = db.select("SELECT c.comparation_id,c.date,p.powerConsume,p.firstday,p.secondday,p.thirdday,p.fourthday,p.fifthday, p.sixthday, p.seventhday,ah.temperatureAve,ah.temperatureMax,ah.temperatureMin,ah.waterPressureAve,ah.airPressureMax,ah.airPressureAve,ah.airPressureMin FROM comparation c INNER JOIN powerconsume p INNER JOIN atmosphere_history ah ON p.pc_id = c.pc_id AND c.ah_id = ah.ah_id WHERE c.date = ?", date)
    legendData = []
    seriesData = []
    similarityData = []
    legendData.append(data[0]['date'].strftime("%Y-%m-%d"))
    seriesData.append({"name": data[0]['date'].strftime("%Y-%m-%d"), "value": [int(data[0]['firstday']), int(data[0]['temperatureAve']), int(data[0]['temperatureMax']), int(data[0]['temperatureMin']), int(data[0]['waterPressureAve']), int(data[0]['airPressureMax']), int(data[0]['airPressureAve']), int(data[0]['airPressureMin']), int(data[0]['seventhday']), int(data[0]['sixthday']), int(data[0]['fifthday']), int(data[0]['fourthday']), int(data[0]['thirdday']), int(data[0]['secondday'])]})
    data = db.select("SELECT s.similarity,s.date,p.powerConsume,p.firstday,p.secondday,p.thirdday,p.fourthday,p.fifthday,p.sixthday,p.seventhday,ah.temperatureAve,ah.temperatureMax,ah.temperatureMin,ah.waterPressureAve,ah.airPressureMax,ah.airPressureAve,ah.airPressureMin FROM similarity s INNER JOIN powerConsume p INNER JOIN atmosphere_history ah ON s.pc_id = p.pc_id AND ah.ah_id = s.ah_id WHERE s.comparation_id=? ORDER BY s.similarity DESC LIMIT 20", data[0]['comparation_id'])
    for item in data:
        similarityData.append({"similarity":item["similarity"]})
        legendData.append(item['date'].strftime("%Y-%m-%d"))
        seriesData.append({"name": item['date'].strftime("%Y-%m-%d"), "value": [int(item['firstday']), int(item['temperatureAve']), int(item['temperatureMax']), int(item['temperatureMin']), int(item['waterPressureAve']), int(item['airPressureMax']), int(item['airPressureAve']), int(item['airPressureMin']), int(item['seventhday']), int(item['sixthday']), int(item['fifthday']), int(item['fourthday']), int(item['thirdday']), int(item['secondday'])]})

    data = {'legendData': legendData, 'seriesData': seriesData, "similarityData": similarityData}
    return JSONResponse(status=200, data=data)


@app.route("/predictResult")
def predictResult():
    return render_template("predict_result.html", navigate="predictResult")


@app.route("/json/getPredictResult")
def getPredictResult():
    data = db.select("SELECT p.date,p.powerConsume,c.predict_pc FROM powerconsume p LEFT JOIN comparation c ON p.date=c.date ORDER BY p.date")
    series = []
    legend = ["电力负荷", "预测负荷"]
    category = []
    realPCTemp = []
    preidctPCTemp = []
    for value in data:
        category.append(value['date'].strftime("%Y-%m-%d"))
        realPCTemp.append(float("%5.6f" % value["powerConsume"]))
        if value['predict_pc'] is None:
            preidctPCTemp.append('-')
        else:
            preidctPCTemp.append(float("%5.6f" % value["predict_pc"]))
    series.append({"name": "电力负荷", "data": realPCTemp, "type": "line"})
    # series.append({"data": temp, "name": "日电力负荷", "type": "line"})
    series.append({"name": "预测负荷", "data": preidctPCTemp, "type": "line"})
    data = {"series": series, "legend": legend, "category": category}
    return JSONResponse(200, data)


def JSONResponse(status, data=None):
    if status == 200:
        return jsonify(status=status, info='sucess', data=data)
    else:
        return jsonify(status=status, info='error')
