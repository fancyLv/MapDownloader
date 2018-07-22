# -*- coding: utf-8 -*-
# @File    : mapdownloader.py
# @Author  : LVFANGFANG
# @Time    : 2018/6/7 0007 23:05
# @Desc    :

import os
import re
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import *

from download import DownloadEngine
from province import data


class MainDialog(QDialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)
        self.resize(625, 240)
        self.dir = os.path.split(os.path.realpath(__file__))[0]
        provinceLabel = QLabel('省或直辖市')
        cityLabel = QLabel('市')
        townLabel = QLabel('区县')
        self.provinceCombo = QComboBox()
        self.cityCombo = QComboBox()
        self.townCombo = QComboBox()
        self.add_province_item()
        self.styleCheckBox = QCheckBox('样式')
        self.styleLineEdit = QLineEdit()
        self.styleLineEdit.setPlaceholderText(
            't:water|e:all|c:#246386ff,t:highway|e:g.f|c:#000000,t:highway|e:g.s|c:#147a92,t:arterial|e:g.f|c:#000000,t:arterial|e:g.s|c:#0b3d51,t:local|e:g|c:#000000,t:land|e:g.f|c:#044c71ff,t:railway|e:g.f|c:#000000,t:railway|e:g.s|c:#08304b,t:subway|e:g|l:-70,t:building|e:g.f|c:#000000,t:all|e:l.t.f|c:#857f7f,t:all|e:l.t.s|c:#000000,t:building|e:g|c:#022338,t:green|e:g|c:#0b385fff,t:boundary|e:all|c:#1e1c1c,t:manmade|e:g|c:#022338,t:poi|e:all|v:off,t:all|e:l.i|v:off,t:road|e:g.f|v:on|c:#326081ff|l:-69,t:land|e:g.f|c:#012f50ff|l:3|s:20,t:road|e:g.s|v:on|c:#133b6eff|l:4,t:manmade|e:l|v:on,t:administrative|e:l.t.f|v:on|c:#90d7fbff|l:-51,t:road|e:g.f|c:#09485eff')
        self.styleLineEdit.setEnabled(False)
        levelLabel = QLabel('级别')
        self.comboCheck = ComboCheckBox()
        self.comboCheck.addItems(list(map(lambda x: str(x), range(1, 19))))
        threadLabel = QLabel('线程')
        self.spinBox = QSpinBox()
        self.spinBox.setMaximum(20)
        self.spinBox.setProperty("value", 10)
        pathLabel = QLabel('存储目录')
        self.pathLineEdit = QLineEdit()

        self.pathLineEdit.setEnabled(False)
        self.pathButton = QPushButton('浏览')
        self.pathButton.setObjectName('pathButton')
        self.downloadButton = QPushButton('下载')
        self.downloadButton.setObjectName('downloadButton')
        self.cancelButton = QPushButton('取消')
        self.cancelButton.setObjectName('cancelButton')
        progressLabel = QLabel('下载进度')
        self.progressBar = QProgressBar()

        self.buttonGroup = QButtonGroup()
        self.rb1 = QRadioButton('百度')
        self.rb2 = QRadioButton('谷歌')
        self.rb3 = QRadioButton('高德')
        self.rb4 = QRadioButton('天地图')
        self.rb4.setEnabled(False)
        self.buttonGroup.addButton(self.rb1, 1)
        self.buttonGroup.addButton(self.rb2, 2)
        self.buttonGroup.addButton(self.rb3, 3)
        self.buttonGroup.addButton(self.rb4, 4)
        self.rb1.setChecked(True)
        rbLayout = QHBoxLayout()
        rbLayout.addWidget(self.rb1)
        rbLayout.addWidget(self.rb2)
        rbLayout.addWidget(self.rb3)
        rbLayout.addWidget(self.rb4)

        topLayout = QHBoxLayout()
        topLayout.addWidget(pathLabel)
        topLayout.addWidget(self.pathLineEdit)
        topLayout.addWidget(self.pathButton)

        cityLayout = QHBoxLayout()
        cityLayout.addWidget(provinceLabel)
        cityLayout.addWidget(self.provinceCombo, 1)
        cityLayout.addWidget(cityLabel)
        cityLayout.addWidget(self.cityCombo, 1)
        cityLayout.addWidget(townLabel)
        cityLayout.addWidget(self.townCombo, 1)

        styleLayout = QHBoxLayout()
        styleLayout.addWidget(self.styleCheckBox)
        styleLayout.addWidget(self.styleLineEdit)

        layout1 = QHBoxLayout()
        layout1.addWidget(levelLabel)
        layout1.addWidget(self.comboCheck, 1)
        layout1.addWidget(threadLabel)
        layout1.addWidget(self.spinBox, 1)
        layout1.addWidget(self.downloadButton)
        layout1.addWidget(self.cancelButton)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(progressLabel)
        bottomLayout.addWidget(self.progressBar)

        layout = QVBoxLayout()
        layout.addLayout(rbLayout)
        layout.addLayout(topLayout)
        layout.addLayout(cityLayout)
        layout.addLayout(styleLayout)
        layout.addLayout(layout1)
        layout.addLayout(bottomLayout)

        self.setLayout(layout)
        self.setWindowTitle('Map Downloader v1.0')

        self.reset_state()

        self.provinceCombo.activated.connect(self.add_city_item)
        self.cityCombo.activated.connect(self.add_town_item)

        self.pathButton.clicked.connect(self.on_pathButton_clicked)
        self.downloadButton.clicked.connect(self.on_downloadButton_clicked)
        self.cancelButton.clicked.connect(self.on_cancelButton_clicked)
        self.cancelButton.blockSignals(True)
        self.pathLineEdit.setText(os.path.join(self.dir, '百度地图').replace('\\', '/'))
        self.styleCheckBox.stateChanged.connect(self.on_styleCheckBox_stateChanged)
        self.comboCheck.currentTextChanged.connect(self.reset_state)
        self.rb1.toggled.connect(self.on_radioButton_toggled)
        self.rb2.toggled.connect(self.on_radioButton_toggled)
        self.rb3.toggled.connect(self.on_radioButton_toggled)
        self.rb4.toggled.connect(self.on_radioButton_toggled)

    def add_province_item(self):
        item = '请选择'
        self.provinceCombo.addItem(item)
        self.cityCombo.addItem(item)
        self.townCombo.addItem(item)
        for i in data:
            if i.endswith('0000'):
                self.provinceCombo.addItem(data[i], i)

    def add_city_item(self, index):
        self.cityCombo.clear()
        self.cityCombo.addItem('请选择')
        self.townCombo.clear()
        self.townCombo.addItem('请选择')
        pid = self.provinceCombo.itemData(index)
        if not pid:
            return
        p = re.compile('{}(?!00)\d+00'.format(pid[:2]))
        for i in data:
            if re.match(p, i):
                self.cityCombo.addItem(data[i], i)
        if self.cityCombo.count() == 1:
            for i in data:
                if i.startswith(pid[:2]) and not i.endswith('00'):
                    self.cityCombo.addItem(data[i], i)

    def add_town_item(self, index):
        self.townCombo.clear()
        self.townCombo.addItem('请选择')
        cid = self.cityCombo.itemData(index)
        if not cid or not cid.endswith('00'):
            return
        for i in data:
            if i.startswith(cid[:4]) and not i.endswith('00'):
                self.townCombo.addItem(data[i], i)

    def on_styleCheckBox_stateChanged(self, state):
        if state == Qt.Checked:
            self.styleLineEdit.setEnabled(True)
        else:
            self.styleLineEdit.setEnabled(False)
        self.reset_state()

    def on_radioButton_toggled(self):
        if self.buttonGroup.checkedId() == 1:
            path = os.path.join(self.dir, '百度地图').replace('\\', '/')
            self.styleCheckBox.setEnabled(True)
        elif self.buttonGroup.checkedId() == 2:
            path = os.path.join(self.dir, '谷歌地图').replace('\\', '/')
            self.styleCheckBox.setEnabled(False)
        elif self.buttonGroup.checkedId() == 3:
            path = os.path.join(self.dir, '高德地图').replace('\\', '/')
            self.styleCheckBox.setEnabled(False)
        else:
            path = os.path.join(self.dir, '天地图').replace('\\', '/')
            self.styleCheckBox.setEnabled(False)
        self.pathLineEdit.setText(path)


    def on_cancelButton_clicked(self):
        if hasattr(self.downloadEngine, 'threads'):
            self.downloadEngine.terminate()
        self.reset_state()

    def on_downloadButton_clicked(self):
        self.paused = not self.paused
        if not self.check_option():
            return
        if not self.downloading:
            self.reset_progress()
            self.downloadButton.setText('暂停')
            self.cancelButton.blockSignals(False)
            path = self.pathLineEdit.text() if self.pathLineEdit.text()  else self.pathLineEdit.placeholderText()
            level = self.comboCheck.selectList()
            if self.styleCheckBox.checkState() == Qt.Checked:
                style = self.styleLineEdit.text() if self.styleLineEdit.text() else self.styleLineEdit.placeholderText()
            else:
                style = None
            area = (
                self.provinceCombo.currentText() + self.cityCombo.currentText() + self.townCombo.currentText()).replace(
                '请选择', '')
            thread_num = self.spinBox.text()
            if self.buttonGroup.checkedId() == 1:
                maptype = 'baidu'
            elif self.buttonGroup.checkedId() == 2:
                maptype = 'google'
            elif self.buttonGroup.checkedId() == 3:
                maptype = 'gaode'
            else:
                maptype = 'tiandiyu'
            self.downloadEngine = DownloadEngine(maptype, area, level, path, style, thread_num)
            self.downloadEngine.division_done_signal.connect(self.division_done_slot)
            self.downloadEngine.progressBar_updated_signal.connect(self.progressBar_updated_slot)
            self.downloadEngine.download_done_signal.connect(self.download_done_slot)
            self.downloadEngine.start()
        else:
            if hasattr(self.downloadEngine, 'threads'):
                self.downloadEngine.pause()
            else:
                self.paused = not self.paused
            self.downloadButton.setText('下载' if self.paused else '暂停')
        self.downloading = True

    def on_pathButton_clicked(self):
        dir = QFileDialog.getExistingDirectory(self, '选择存储目录', '.')
        self.pathLineEdit.setText(dir)
        self.reset_state()

    def check_option(self):
        level = self.comboCheck.selectList()
        if not level:
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "请选择下载级别！")
            msg_box.exec_()
            return False
        area = self.provinceCombo.currentText() + self.cityCombo.currentText() + self.townCombo.currentText()
        if area.replace('请选择', '') == "":
            msg_box = QMessageBox(QMessageBox.Warning, "警告", "请选择下载区域！")
            msg_box.exec_()
            return False
        return True

    def reset_progress(self):
        self.count = 0
        self.progressBar.setValue(0)

    def reset_state(self):
        self.downloading = False
        self.paused = True
        self.downloadButton.setText('下载')
        self.reset_progress()

    def division_done_slot(self, total):
        self.progressBar.setMaximum(total)

    def progressBar_updated_slot(self):
        self.count += 1
        self.progressBar.setValue(self.count)

    def download_done_slot(self):
        msg_box = QMessageBox(QMessageBox.Information, "提示", "下载完毕!")
        msg_box.exec_()
        self.reset_state()


class ComboCheckBox(QComboBox):
    def addItems(self, items, p_str=None):  # items==[str,str...]
        self.items = items
        self.items.insert(0, '全部')
        self.row_num = len(self.items)
        self.selectedrow_num = 0
        self.qCheckBox = []
        self.qLineEdit = QLineEdit()
        self.qLineEdit.setReadOnly(True)
        self.qListWidget = QListWidget()
        self.addQCheckBox(0)
        self.qCheckBox[0].stateChanged.connect(self.all)
        for i in range(1, self.row_num):
            self.addQCheckBox(i)
            self.qCheckBox[i].stateChanged.connect(self.show)
        self.setModel(self.qListWidget.model())
        self.setView(self.qListWidget)
        self.setLineEdit(self.qLineEdit)

    def addQCheckBox(self, i):
        self.qCheckBox.append(QCheckBox())
        qItem = QListWidgetItem(self.qListWidget)
        self.qCheckBox[i].setText(self.items[i])
        self.qListWidget.setItemWidget(qItem, self.qCheckBox[i])

    def selectList(self):
        outputList = []
        for i in range(1, self.row_num):
            if self.qCheckBox[i].isChecked() == True:
                outputList.append(self.qCheckBox[i].text())
        self.selectedrow_num = len(outputList)
        return outputList

    def show(self):
        show = ''
        outputList = self.selectList()
        self.qLineEdit.setReadOnly(False)
        self.qLineEdit.clear()
        for i in outputList:
            show += i + ';'
        if self.selectedrow_num == 0:
            self.qCheckBox[0].setCheckState(0)
        elif self.selectedrow_num == self.row_num - 1:
            self.qCheckBox[0].setCheckState(2)
        else:
            self.qCheckBox[0].setCheckState(1)
        self.qLineEdit.setText(show)
        self.qLineEdit.setReadOnly(True)

    def all(self, state):
        if state == Qt.Checked:
            for i in range(1, self.row_num):
                self.qCheckBox[i].setChecked(True)
        elif state == Qt.CaseSensitive:
            if self.selectedrow_num == 0:
                self.qCheckBox[0].setCheckState(2)
        elif state == Qt.CaseInsensitive:
            self.clear()

    def clear(self):
        for i in range(self.row_num):
            self.qCheckBox[i].setChecked(False)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainwindow = MainDialog()
    mainwindow.show()
    app.exec_()
