# -*- coding: utf-8 -*-
"""
Created on Thu Apr 07 21:18:44 2016

@author: Coco
"""
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import forest

QTextCodec.setCodecForTr(QTextCodec.codecForName("utf8"))


class Forest(QDialog):

    def __init__(self, parent=None):
        self.forest = forest.forest()
        self.stage = 0
        super(Forest, self).__init__(parent)
        self.setWindowTitle(self.tr("电力负荷预测系统"))

        mainSplitter = QSplitter(Qt.Horizontal)
        mainSplitter.setOpaqueResize(True)
        self.listWidget = QListWidget(mainSplitter)
        self.listWidget.insertItem(0, self.tr("预测流程"))
        self.listWidget.insertItem(1, self.tr("选择预测日期"))
        self.listWidget.insertItem(2, self.tr("计算相似度"))
        self.listWidget.insertItem(3, self.tr("智能预测"))
        frame = QFrame(mainSplitter)
        self.stack = QStackedWidget()
        self.stack.setFrameStyle(QFrame.Panel | QFrame.Raised)
        setProcess = SetProcess()
        setProcess.setPredict(self.forest)
        setDate = SetDate()
        setDate.setDate(self.forest)
        self.countSimilarity = CountSimilarity()
        self.countSimilarity.setData(self.forest)
        doPredict = DoPredict()
        doPredict.setData(self.forest)
        self.stack.addWidget(setProcess)
        self.stack.addWidget(setDate)
        self.stack.addWidget(self.countSimilarity)
        self.stack.addWidget(doPredict)

        self.amendPushButton = QPushButton(self.tr("确定"))
        self.amendPushButton.clicked.connect(self.amendButtonEvent)
        self.nextPushButton = QPushButton(self.tr("下一步"))
        self.nextPushButton.clicked.connect(self.nextStageEvent)

        buttonLayout = QHBoxLayout()
        buttonLayout.addStretch(1)
        buttonLayout.addWidget(self.amendPushButton)
        buttonLayout.addWidget(self.nextPushButton)

        mainLayout = QVBoxLayout(frame)
        mainLayout.setMargin(10)
        mainLayout.setSpacing(6)
        mainLayout.addWidget(self.stack)
        mainLayout.addLayout(buttonLayout)

        self.connect(self.listWidget, SIGNAL(
            "currentRowChanged(int)"), self.stack, SLOT("setCurrentIndex(int)"))
        self.connect(self.listWidget, SIGNAL(
            "currentRowChanged(int)"), self, SLOT("buttonStatus()"))

        layout = QHBoxLayout(self)
        layout.addWidget(mainSplitter)
        self.setLayout(layout)

    def setupUi(self, Dialog):
        self.form = Dialog

    @pyqtSlot()
    def buttonStatus(self):
        if self.listWidget.currentRow() <= self.stage:
            self.amendPushButton.setEnabled(True)
        else:
            self.amendPushButton.setEnabled(False)
        if self.listWidget.currentRow() == 4:
            self.nextPushButton.setText(u"完成")
            self.nextPushButton.setEnabled(False)
        else:
            self.nextPushButton.setText(u"下一步")
            self.nextPushButton.setEnabled(True)

    def nextStageEvent(self):
        row = self.listWidget.currentRow()
        if row < 4:
            self.listWidget.setCurrentRow(row + 1)

    def amendButtonEvent(self):
        msg = self.stack.currentWidget().amend()
        if msg == 'ok':
            self.stage = self.stage + 1
            if self.stage == 2:
                self.countSimilarity.update()
                self.stage += 1
        else:
            QMessageBox.warning(self, "Warning", self.tr(msg))


class SetProcess(QWidget):

    def __init__(self, parent=None):
        super(SetProcess, self).__init__(parent)

    def setPredict(self, Forest):
        self.forest = Forest

        grid = QGridLayout()
        grid.setSpacing(30)

        label = QLabel(self.tr(""))
        grid.addWidget(label, 0, 2, 6, 2)

        col1 = 1
        col2 = 2
        col3 = 3
        # 相关度算法
        label1 = QLabel(self.tr("相关度算法："))
        label1.setAlignment(Qt.AlignHCenter)
        self.relevancyComboBox = QComboBox()

        self.relevancyComboBox.insertItem(0, u"皮尔逊相关系数")
        grid.addWidget(label1, 0, col1)
        grid.addWidget(self.relevancyComboBox, 0, col2, Qt.AlignLeft)
        self.label11 = QLabel(self.tr(""))
        grid.addWidget(self.label11, 0, col3, Qt.AlignLeft)

        label2 = QLabel(self.tr("归一化："))
        label2.setAlignment(Qt.AlignHCenter)
        self.normalizeComboBox = QComboBox()
        self.normalizeComboBox.insertItem(0, u"min-max标准化")
        grid.addWidget(label2, 1, col1)
        grid.addWidget(self.normalizeComboBox, 1, col2, Qt.AlignLeft)
        self.label22 = QLabel(self.tr(""))
        grid.addWidget(self.label22, 1, col3, Qt.AlignLeft)

        label3 = QLabel(self.tr("相似度算法："))
        label3.setAlignment(Qt.AlignHCenter)
        self.similarityComboBox = QComboBox()
        self.similarityComboBox.insertItem(0, u"欧几里得距离")
        grid.addWidget(label3, 2, col1)
        grid.addWidget(self.similarityComboBox, 2, col2, Qt.AlignLeft)
        self.label33 = QLabel(self.tr(""))
        grid.addWidget(self.label33, 2, col3, Qt.AlignLeft)

        label4 = QLabel(self.tr("预测算法："))
        label4.setAlignment(Qt.AlignHCenter)
        self.predictModelComboBox = QComboBox()
        self.predictModelComboBox.insertItem(0, u"支持向量机")
        grid.addWidget(label4, 3, col1)
        grid.addWidget(self.predictModelComboBox, 3, col2, Qt.AlignLeft)
        self.label44 = QLabel(self.tr(""))
        grid.addWidget(self.label44, 3, col3, Qt.AlignLeft)

        self.setLayout(grid)

    def amend(self):
        self.label11.setText(self.relevancyComboBox.currentText())
        self.label22.setText(self.normalizeComboBox.currentText())
        self.label33.setText(self.similarityComboBox.currentText())
        self.label44.setText(self.predictModelComboBox.currentText())
        return 'ok'


class SetDate(QWidget):

    def __init__(self, parent=None):
        super(SetDate, self).__init__(parent)

    def setDate(self, Forest):
        self.forest = Forest

        grid = QGridLayout()
        grid.setSpacing(30)

        label = QLabel(self.tr(""))
        grid.addWidget(label, 0, 2, 6, 2)

        col1 = 1
        col2 = 2
        col3 = 3
        # 相关度算法
        # label1 = QLabel(self.tr("历史日天数："))
        # label1.setAlignment(Qt.AlignHCenter)
        # self.historyNum = QLineEdit()
        # grid.addWidget(label1, 0, col1)
        # grid.addWidget(self.historyNum, 0, col2, Qt.AlignLeft)
        # self.label11 = QLabel(self.tr(""))
        # grid.addWidget(self.label11, 0, col3, Qt.AlignLeft)

        label2 = QLabel(self.tr("预测日期："))
        label2.setAlignment(Qt.AlignHCenter)
        self.predictDate = DateLineEdit()
        self.predictDate.setFather(self)
        grid.addWidget(label2, 1, col1)
        grid.addWidget(self.predictDate, 1, col2, Qt.AlignLeft)
        self.label22 = QLabel(self.tr(""))
        grid.addWidget(self.label22, 1, col3, Qt.AlignLeft)

        label3 = QLabel(self.tr("预测天数："))
        label3.setAlignment(Qt.AlignHCenter)
        self.similarityComboBox = QComboBox()
        self.predictNum = QLineEdit()
        grid.addWidget(label3, 2, col1)
        grid.addWidget(self.predictNum, 2, col2, Qt.AlignLeft)
        self.label33 = QLabel(self.tr(""))
        grid.addWidget(self.label33, 2, col3, Qt.AlignLeft)

        self.setLayout(grid)

        self.cal = QCalendarWidget(self)
        self.connect(
            self.cal, SIGNAL('selectionChanged()'), self.changePredictDate)
        self.cal.hide()
        self.cal.setCurrentPage(2007, 1)
        self.cal.setGeometry(self.geometry().width() / 5, 82, 260, 170)

    def changePredictDate(self):
        date = self.cal.selectedDate()
        self.predictDate.setText(str(date.toPyDate()))
        self.cal.hide()

    def amend(self):
        # historyNum = int(self.historyNum.text())
        predictDate = str(self.predictDate.text())
        predictNum = int(self.predictNum.text())
        self.forest.setData(predictDate, predictNum)
        return 'ok'


class DateLineEdit(QLineEdit):

    def setFather(self, father):
        self.father = father

    def mousePressEvent(self, event):
        self.father.cal.show()


class CountSimilarity(QTabWidget):

    def __init__(self, parent=None):
        super(CountSimilarity, self).__init__(parent)
        self.done = False

    def setData(self, Forest):
        #        self.orderName = []
        #        for value in order:
        #            self.orderName.append(fieldDescription.get(value))
        self.forest = Forest

    def update(self):
        from entity import order, fieldDescription

        # self.historyAtmTable = QTableWidget(
        #     len(self.forest.source) + len(self.forest.forest), len(order))
        # self.historyAtmTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # field = ["cityName", "date", "powerConsume"]
        # field.extend([fieldDescription.get(value).decode('utf-8') for value in order])
        # self.historyAtmTable.setHorizontalHeaderLabels(field)

        self.relTable = QTableWidget(len(self.forest.relevancy.atmRel), 3)
        self.relTable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.relTable.setHorizontalHeaderLabels(
            [u'参数', u'相关度', u'是否采用', u'最小值'])
        i = 0
        for key, value in self.forest.relevancy.atmRel.iteritems():
            newItem = QTableWidgetItem(
                fieldDescription.get(key).decode('utf-8'))
            self.relTable.setItem(i, 0, newItem)
            newItem = QTableWidgetItem(str(value))
            self.relTable.setItem(i, 1, newItem)
            newItem = QTableWidgetItem(
                abs(value) >= self.forest.minRel and u"是" or u"否")
            self.relTable.setItem(i, 2, newItem)
            i += 1
        self.relTable.setSpan(0, 3, len(self.forest.relevancy.atmRel), 1)
        newItem = QTableWidgetItem(str(self.forest.minRel))
        self.relTable.setItem(0, 3, newItem)
        self.addTab(self.relTable, u'相关度')

    def amend(self):
        if self.done is False:
            from entity import AP, fieldDescription
            self.forest.normalize()
            self.forest.countSimilarity()

            for i in range(len(self.forest.forestSimilarity)):
                table = QTableWidget(
                    len(self.forest.forestSimilarity[i].similarityEntitys), len(AP.validAtmosphere) + 4)
                table.setEditTriggers(QAbstractItemView.NoEditTriggers)
                newOrder = [u'相似度']
                field = ["cityName", "date", "powerConsume"]
                field.extend(AP.validAtmosphere)
                field = [fieldDescription.get(value).decode('utf-8') for value in field]
                newOrder.extend(field)
                table.setHorizontalHeaderLabels(newOrder)

                newItem = QTableWidgetItem(
                    str(""))
                table.setItem(0, 0, newItem)

                newItem = QTableWidgetItem(
                    str(self.forest.forestSimilarity[i].base.cityName))
                table.setItem(0, 1, newItem)
                newItem = QTableWidgetItem(
                    str(self.forest.forestSimilarity[i].base.date))
                table.setItem(0, 2, newItem)
                newItem = QTableWidgetItem(
                    str(self.forest.forestSimilarity[i].base.powerConsume['real']))
                table.setItem(0, 3, newItem)

                for n in range(len(AP.validAtmosphere)):
                    newItem = QTableWidgetItem(
                        str(self.forest.forestSimilarity[i].base.atmosphere[AP.validAtmosphere[n]]))
                    table.setItem(0, n + 4, newItem)

                for m in range(len(self.forest.forestSimilarity[i].similarityEntitys)):
                    newItem = QTableWidgetItem(
                        str(self.forest.forestSimilarity[i].similarityEntitys[m].similarity))
                    table.setItem(m + 1, 0, newItem)

                    newItem = QTableWidgetItem(
                        str(self.forest.forestSimilarity[i].similarityEntitys[m].ap.cityName))
                    table.setItem(m + 1, 1, newItem)
                    newItem = QTableWidgetItem(
                        str(self.forest.forestSimilarity[i].similarityEntitys[m].ap.date))
                    table.setItem(m + 1, 2, newItem)
                    newItem = QTableWidgetItem(
                        str(self.forest.forestSimilarity[i].similarityEntitys[m].ap.powerConsume['real']))
                    table.setItem(m + 1, 3, newItem)

                    for n in range(len(AP.validAtmosphere)):
                        newItem = QTableWidgetItem(
                            str(self.forest.forestSimilarity[i].similarityEntitys[m].ap.atmosphere[AP.validAtmosphere[n]]))
                        table.setItem(m + 1, n + 4, newItem)
                self.addTab(
                    table, (self.forest.forestSimilarity[i].base.date.isoformat() + '的相似日').decode('utf-8'))
            self.done = True
        return 'ok'


class DoPredict(QTabWidget):

    def __init__(self, parent=None):
        super(DoPredict, self).__init__(parent)

    def setData(self, Forest):
        self.forest = Forest

    def update(self):
        pass

    def amend(self):
        self.forest.predict()
        table = QTableWidget(len(self.forest.forestSimilarity), 4)
        table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        table.setHorizontalHeaderLabels([u'日期', u'实际值', u'预测值', u'错误率'])
        print len(self.forest.forestSimilarity)
        for i in range(len(self.forest.forestSimilarity)):
            newItem = QTableWidgetItem(
                str(self.forest.forestSimilarity[i].base.date.isoformat()))
            real = self.forest.forestSimilarity[i].base.powerConsume['real']
            predict = self.forest.forestSimilarity[i].base.powerConsume["predict"]
            table.setItem(i, 0, newItem)
            newItem = QTableWidgetItem(str(real))
            table.setItem(i, 1, newItem)
            newItem = QTableWidgetItem(str(predict))
            table.setItem(i, 2, newItem)
            newItem = QTableWidgetItem(str(abs(real - predict) / real))
            table.setItem(i, 3, newItem)
        self.addTab(table, u'预测结果')
        return 'ok'

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    main = Forest()
    main.show()
    app.exec_()
