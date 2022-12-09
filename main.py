from PyQt5 import QtCore, QtGui, QtWidgets
from qt import Ui_MainWindow
from PyQt5.QtWidgets import QAbstractItemView, QFileDialog
import sys
from dataclasses import dataclass
import copy
import threading
from PyQt5.QtCore import QThread,pyqtSignal
import time
from PyQt5.QtCore import QThread, pyqtSignal
_m = 0
@dataclass
class Item:
    value: int
    wt: int
    name: str

class CThread(QThread):
    valueChanged = pyqtSignal(int)
    def __init__(self,value, Frame_1):
        super().__init__()
        self.stop_fill = False
        self.completed = value
        self.frame = Frame_1

    def run(self):
        self.collectbackpack()

    def collectbackpack(self):
        global _m
        self.frame.deletetable_2()
        W = self.frame.ui.spinBox_3.value()
        n = self.frame.ui.tablewidget.rowCount()
        itemmas = []
        for i in range(n):
            itemmas.append(Item(int(self.frame.ui.tablewidget.item(i, 2).text()), int(self.frame.ui.tablewidget.item(i, 1).text()),
                                self.frame.ui.tablewidget.item(i, 0).text()))
        mass2 = [[[] for i in range(W + 1)]
                for i in range(2)]
        mass1 = [[0 for i in range(W + 1)]
               for i in range(2)]
        progress = n / 100
        chek = 0
        i = 0
        while i < n and not self.stop_fill:
            if i > chek:
                chek = chek + progress
                _m = _m + 1
                self.valueChanged.emit(_m)
            j = 0
            if i % 2 == 0:
                while j < W:
                    j += 1
                    if itemmas[i].wt <= j:
                        if itemmas[i].value + mass1[0][j - itemmas[i].wt] > mass1[0][j]:
                            mass1[1][j] = itemmas[i].value + mass1[0][j - itemmas[i].wt]
                            t = copy.copy(mass2[0][j - itemmas[i].wt])
                            t.append(itemmas[i])
                            mass2[1][j] = t
                        else:
                            mass1[1][j] = mass1[0][j]
                            mass2[1][j] = mass2[0][j]
                    else:
                        mass1[1][j] = mass1[0][j]
                        mass2[1][j] = mass2[0][j]
            else:
                while j < W:
                    j += 1
                    if itemmas[i].wt <= j:
                        if itemmas[i].value + mass1[1][j - itemmas[i].wt] > mass1[1][j]:
                            mass1[0][j] = itemmas[i].value + mass1[1][j - itemmas[i].wt]
                            t = copy.copy(mass2[1][j - itemmas[i].wt])
                            t.append(itemmas[i])
                            mass2[0][j] = t
                        else:
                            mass1[0][j] = mass1[1][j]
                            mass2[0][j] = mass2[1][j]
                    else:
                        mass1[0][j] = mass1[1][j]
                        mass2[0][j] = mass2[1][j]

            i += 1
        if n % 2 == 0 and i == n:
            for i in mass2[0][W]:
                rowCount = self.frame.ui.tablewidget_2.rowCount()
                self.frame.ui.tablewidget_2.insertRow(rowCount)
                self.frame.ui.tablewidget_2.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(str(i.value)))
                self.frame.ui.tablewidget_2.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(str(i.wt)))
                self.frame.ui.tablewidget_2.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(i.name))
        elif i == n:
            for i in mass2[1][W]:
                rowCount = self.frame.ui.tablewidget_2.rowCount()
                self.frame.ui.tablewidget_2.insertRow(rowCount)
                self.frame.ui.tablewidget_2.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(str(i.value)))
                self.frame.ui.tablewidget_2.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(str(i.wt)))
                self.frame.ui.tablewidget_2.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(i.name))
        _m = 0
        self.valueChanged.emit(_m)


class mywindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(mywindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.init_ui()
        self.fill_thread = None
        self.ui.tablewidget.setColumnCount(3)
        self.ui.tablewidget.setHorizontalHeaderLabels(["Название", "Вес", "Ценность"])
        self.ui.tablewidget_2.setColumnCount(3)
        self.ui.tablewidget_2.setHorizontalHeaderLabels(["Название", "Вес", "Ценность"])
        self.ui.tablewidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.ui.tablewidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ui.tablewidget_2.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Fixed)
        self.ui.tablewidget_2.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.ui.spinBox.setRange(0, 10000)
        self.ui.spinBox_2.setRange(0, 10000)
        self.ui.spinBox_3.setRange(0, 100000)
        self.ui.progressBar.setRange(0, 100)
        self.ui.progressBar.setValue(0)

    def init_ui(self):
        self.ui.pushButton_6.clicked.connect(self.add)
        self.ui.pushButton_5.clicked.connect(self.search)
        self.ui.pushButton_4.clicked.connect(self.delete)
        self.ui.pushButton_3.clicked.connect(self.deletetable)
        self.ui.pushButton.clicked.connect(self.openfill)
        self.ui.pushButton_7.clicked.connect(self.deletetable_2)
        self.ui.pushButton_2.clicked.connect(self.runbackpack)
        self.ui.pushButton_8.clicked.connect(self.savebackpack)
        self.ui.pushButton_9.clicked.connect(self.savelist)
        self.ui.pushButton_10.clicked.connect(self.killprocess)

    def killprocess(self):
        self.ui.progressBar.setValue(0)
        if self.fill_thread != None:
            if _m != 0:
                self.fill_thread.disconnect()  # event unbind
                self.fill_thread.stop_fill = True
                self.fill_thread.wait()
                self.fill_thread.quit()
                self.deletetable_2()

    def runbackpack(self):

        self.ui.progressBar.setValue(0)
        self.fill_thread = CThread(self.ui.progressBar.value(), self)
        self.fill_thread.valueChanged.connect(self.ui.progressBar.setValue)
        self.fill_thread.start()

    def savelist(self):
        if self.ui.tablewidget.rowCount() > 0:
            filePath, _ = QFileDialog.getSaveFileName(self, "Save", "List",
                                                      "TXT(*.txt)")
            if filePath == "":
                return
            f = open(filePath, 'w')
            for i in range(self.ui.tablewidget.rowCount()):
                f.write(self.ui.tablewidget.item(i, 0).text() + ','
                        + self.ui.tablewidget.item(i, 1).text() + ','
                            + self.ui.tablewidget.item(i, 2).text() + ';' + '\n')
            f.close()
        else:
            self.ui.messegbox.setText('Список пуст')
            self.ui.messegbox.exec()

    def savebackpack(self):
        if self.ui.tablewidget_2.rowCount() > 0:
            filePath, _ = QFileDialog.getSaveFileName(self, "Save", "Backpack",
                                                      "TXT(*.txt)")
            if filePath == "":
                return
            f = open(filePath, 'w')
            for i in range(self.ui.tablewidget_2.rowCount()):
                f.write(self.ui.tablewidget_2.item(i, 0).text() + ','
                        + self.ui.tablewidget_2.item(i, 1).text() + ','
                            + self.ui.tablewidget_2.item(i, 2).text() + ';' + '\n')
            f.close()
        else:
            self.ui.messegbox.setText('Рюкзак пуст')
            self.ui.messegbox.exec()

    def findOccurrences(self, s, ch):
        return [i for i, letter in enumerate(s) if letter == ch]

    def openfill(self):
        path, _ = QFileDialog.getOpenFileName(self, "Open file", "",
                                              "TXT(*.txt)")
        if path:
            encoding = ['utf-8', 'windows-1251']
            correct_encoding = ''
            for enc in encoding:
                try:
                    open(path, encoding=enc).read()
                except (UnicodeDecodeError, LookupError):
                    pass
                else:
                    correct_encoding = enc
                    break
            f = open(path, encoding=correct_encoding, mode='r+')
            try:
                name = ''
                wt = ''
                value = ''
                text = f.readlines()
                for ii in text:
                    m = self.findOccurrences(ii, ',')
                    for i in range(len(ii)):
                        if i < m[0]:
                            name = name + ii[i]
                        if m[0] < i < m[1]:
                            chek = ii[i]
                            if chek != '1' and chek != '2' and chek != '3' and chek != '4' and chek \
                                    != '5' and chek != '6' and chek != '7' and chek != '8' and chek \
                                    != '9' and chek != '0':
                                self.ui.messegbox.setText('Файл неправильно заполнен')
                                self.ui.messegbox.exec()
                                self.deletetable()
                                return
                            else:
                                wt = wt + chek
                        if m[-1] < i < ii.find(';'):
                            chek = ii[i]
                            if chek != '1' and chek != '2' and chek != '3' and chek != '4' and chek \
                                    != '5' and chek != '6' and chek != '7' and chek != '8' and chek \
                                    != '9' and chek != '0':
                                self.ui.messegbox.setText('Файл неправильно заполнен')
                                self.ui.messegbox.exec()
                                self.deletetable()
                                return
                            else:
                                value = value + chek

                    if name == '' or wt == '' or value == '' or ' ' in name or ' ' in wt or ' ' in value:
                        self.ui.messegbox.setText('Файл неправильно заполнен')
                        self.ui.messegbox.exec()
                        self.deletetable()
                        return
                    rowCount = self.ui.tablewidget.rowCount()
                    self.ui.tablewidget.insertRow(rowCount)
                    self.ui.tablewidget.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(value))
                    self.ui.tablewidget.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(wt))
                    self.ui.tablewidget.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(name))
                    name, value, wt = '', '', ''
            finally:
                f.close()

    def deletetable_2(self):
        # self.ui.tablewidget_2.clear()
        self.ui.tablewidget_2.clearSelection()
        for i in range(self.ui.tablewidget_2.rowCount()):
            self.ui.tablewidget_2.removeRow(0)

    def deletetable(self):
        self.ui.tablewidget.clearSelection()
        for i in range(self.ui.tablewidget.rowCount()):
            self.ui.tablewidget.removeRow(0)

    def delete(self):
        self.ui.tablewidget.clearSelection()
        if self.ui.spinBox.value() and self.ui.spinBox_2.value() and self.ui.lineEdit.text() != '':
            if ' ' in self.ui.lineEdit.text():
                self.ui.messegbox.setText('В строке найден пробел')
                self.ui.messegbox.exec()
            else:
                for i in range(self.ui.tablewidget.rowCount()):
                    if self.ui.tablewidget.item(i, 0).text() == self.ui.lineEdit.text() and int(
                            self.ui.tablewidget.item(i, 1).text()) == self.ui.spinBox.value() and int(
                                self.ui.tablewidget.item(i, 2).text()) == self.ui.spinBox_2.value():
                        self.ui.tablewidget.removeRow(i)
                        return

                self.ui.messegbox.setText('Такого предмета нету в списке')
                self.ui.messegbox.exec()

        else:
            self.ui.messegbox.setText('Не все поля заполнены')
            self.ui.messegbox.exec()

    def add(self):
        self.ui.tablewidget.clearSelection()
        rowCount = self.ui.tablewidget.rowCount()
        if self.ui.spinBox.value() and self.ui.spinBox_2.value() and self.ui.lineEdit.text() != '':
            if ' ' in self.ui.lineEdit.text():
                self.ui.messegbox.setText('В строке найден пробел')
                self.ui.messegbox.exec()
            else:
                self.ui.tablewidget.insertRow(rowCount)
                self.ui.tablewidget.setItem(rowCount, 2, QtWidgets.QTableWidgetItem(str(self.ui.spinBox_2.value())))
                self.ui.tablewidget.setItem(rowCount, 1, QtWidgets.QTableWidgetItem(str(self.ui.spinBox.value())))
                self.ui.tablewidget.setItem(rowCount, 0, QtWidgets.QTableWidgetItem(self.ui.lineEdit.text()))
        else:
            self.ui.messegbox.setText('Не все поля заполнены')
            self.ui.messegbox.exec()

    def search(self):
        self.ui.tablewidget.clearSelection()
        self.ui.tablewidget.setSelectionMode(QAbstractItemView.MultiSelection)
        flag = 0
        if self.ui.spinBox.value() and self.ui.spinBox_2.value() and self.ui.lineEdit.text() != '':
            if ' ' in self.ui.lineEdit.text():
                self.ui.messegbox.setText('В строке найден пробел')
                self.ui.messegbox.exec()
            else:
                for i in range(self.ui.tablewidget.rowCount()):
                    if self.ui.tablewidget.item(i, 0).text() == self.ui.lineEdit.text() and int(
                            self.ui.tablewidget.item(i, 1).text()) == self.ui.spinBox.value() and int(
                                self.ui.tablewidget.item(i, 2).text()) == self.ui.spinBox_2.value():
                        flag = 1
                        self.ui.tablewidget.selectRow(i)
                if flag == 0:
                    self.ui.messegbox.setText('Такого предмета нету в списке')
                    self.ui.messegbox.exec()
        else:
            self.ui.messegbox.setText('Не все поля заполнены')
            self.ui.messegbox.exec()
        self.ui.tablewidget.setSelectionMode(QAbstractItemView.NoSelection)




app = QtWidgets.QApplication([])
application = mywindow()
application.show()

sys.exit(app.exec())