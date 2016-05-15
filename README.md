# 概要
本项目目的是实现一种根据历史日的气象数据和电力负荷数据预测未来电力负荷的系统，到scientic-web，scientic-web已经是开发过程的第四个版本，前面经历了scientic/com,scientic/core,scientic/v3，预测过程的功能包括：
 - 读取txt，xlsx文件的数据信息  preprocess/
 - 数据库连接，curd功能模块db.py
 - 数据预处理 preprocess/
 - 计算相关度、获取待遇差日期数据、数据归一化、计算相似度 forest.py
 - 预测结果评估 follow_work.py 这是scientic-web的主要工作内容
v3已经实现预测的全部流程，但是由于精度太低和console界面运行的缺点，scientic-web的工作就是在利用echarts图像库在web前端优良的数据显示效果，一方面增加整个系统的“颜值”，方便其他人使用，同时图表可以方便分析数据，找出预测过程的不足，提高预测精度。

#部署
####文件结构
 - scientic-web 主目录
   - app 项目主要内容
     - core 预测过程
       - preprocess 数据预处理
       - v3 预测过程主要模块
     - static web前段静态文件
       - echarts-asset
       - js
         - echarts
         - zrender-master
     - templates
   - backup
   - conf
   - dist
   - flask
     - Include
     - Lib
      ..
       - site-packages
     - Scripts
   - temp
   - test

scientic-web： 主目录
app： 项目主要内容
preprocess： 数据预处理
v3： 预测过程主要模块
flask/Lib/site-packages/： python库位置
flask/Scripts/：pip,python 命令所在位置
####环境配置
 - python 2.7
 - pip （https://pip.pypa.io/en/stable/installing/）
 - virtualenv (https://virtualenv.pypa.io/en/latest/)
 - mysql-python (https://pypi.python.org/pypi/MySQL-python/1.2.5)
 - flask (http://flask.pocoo.org/docs/0.10/installation/#virtualenv)

mysql-python在virtualenv的外部环境也会安装，可以直接复制python/site-packages下的:
1. MySQLdb/
2. MySQL_python-1.2.3-py2.7.egg-info/
3. _mysql.pyd
4. _mysql_exceptions.py
5. _mysql_exceptions.pyc
6. _mysql_exceptions.pyo
到flask的site-packags.

