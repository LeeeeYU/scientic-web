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


def JSONResponse(status, data=None):
    if status == 200:
        return jsonify(status=status, info='sucess', data=data)
    else:
        return jsonify(status=status, info='error')
