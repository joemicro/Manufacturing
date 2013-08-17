# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'batchadjform.ui'
#
# Created: Wed Jul 10 16:07:22 2013
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_batchadjform(object):
    def setupUi(self, batchadjform):
        batchadjform.setObjectName(_fromUtf8("batchadjform"))
        batchadjform.resize(543, 412)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/settings")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        batchadjform.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(batchadjform)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame_2 = QtGui.QFrame(batchadjform)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 40))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_2 = QtGui.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(18)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame = QtGui.QFrame(batchadjform)
        self.frame.setMinimumSize(QtCore.QSize(0, 45))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 45))
        self.frame.setAutoFillBackground(False)
        self.frame.setStyleSheet(_fromUtf8("border: none;\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #BBBBBB, \n"
"stop: 0.4 #EEEEEE,\n"
"stop: 0.9 #CCCCCC,\n"
" stop: 1 #666666);"))
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout(self.frame)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.saveButton = QtGui.QPushButton(self.frame)
        self.saveButton.setMinimumSize(QtCore.QSize(90, 0))
        self.saveButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.saveButton.setStyleSheet(_fromUtf8("QPushButton {\n"
"background-color: rgb(250, 250, 250);\n"
"color: #333;\n"
"border: 2px solid #555;\n"
"padding: 5px;}\n"
"QPushButton:hover {\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #ccc);}\n"
"QPushButton:pressed {\n"
"background: qradialgradient(cx: 0.4, cy: -0.1,\n"
"fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #eee);}"))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/save")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveButton.setIcon(icon1)
        self.saveButton.setIconSize(QtCore.QSize(20, 20))
        self.saveButton.setFlat(False)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout_4.addWidget(self.saveButton)
        self.clearButton = QtGui.QPushButton(self.frame)
        self.clearButton.setMinimumSize(QtCore.QSize(90, 0))
        self.clearButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.clearButton.setStyleSheet(_fromUtf8("QPushButton {\n"
"background-color: rgb(250, 250, 250);\n"
"color: #333;\n"
"border: 2px solid #555;\n"
"padding: 5px;}\n"
"QPushButton:hover {\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #ccc);}\n"
"QPushButton:pressed {\n"
"background: qradialgradient(cx: 0.4, cy: -0.1,\n"
"fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #eee);}"))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/clear")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearButton.setIcon(icon2)
        self.clearButton.setIconSize(QtCore.QSize(20, 20))
        self.clearButton.setFlat(False)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.horizontalLayout_4.addWidget(self.clearButton)
        self.refresh_pushButton = QtGui.QPushButton(self.frame)
        self.refresh_pushButton.setMinimumSize(QtCore.QSize(90, 0))
        self.refresh_pushButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.refresh_pushButton.setStyleSheet(_fromUtf8("QPushButton {\n"
"background-color: rgb(250, 250, 250);\n"
"color: #333;\n"
"border: 2px solid #555;\n"
"padding: 5px;}\n"
"QPushButton:hover {\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #ccc);}\n"
"QPushButton:pressed {\n"
"background: qradialgradient(cx: 0.4, cy: -0.1,\n"
"fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #eee);}"))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/refresh")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.refresh_pushButton.setIcon(icon3)
        self.refresh_pushButton.setIconSize(QtCore.QSize(20, 20))
        self.refresh_pushButton.setFlat(False)
        self.refresh_pushButton.setObjectName(_fromUtf8("refresh_pushButton"))
        self.horizontalLayout_4.addWidget(self.refresh_pushButton)
        self.closeButton = QtGui.QPushButton(self.frame)
        self.closeButton.setMinimumSize(QtCore.QSize(90, 0))
        self.closeButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.closeButton.setStyleSheet(_fromUtf8("QPushButton {\n"
"background-color: rgb(250, 250, 250);\n"
"color: #333;\n"
"border: 2px solid #555;\n"
"padding: 5px;}\n"
"QPushButton:hover {\n"
"background: qradialgradient(cx: 0.3, cy: -0.4,\n"
"fx: 0.3, fy: -0.4,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #ccc);}\n"
"QPushButton:pressed {\n"
"background: qradialgradient(cx: 0.4, cy: -0.1,\n"
"fx: 0.4, fy: -0.1,\n"
"radius: 1.35, stop: 0 #fff, stop: 1 #eee);}"))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/exit")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon4)
        self.closeButton.setIconSize(QtCore.QSize(20, 20))
        self.closeButton.setFlat(False)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout_4.addWidget(self.closeButton)
        spacerItem = QtGui.QSpacerItem(34, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout.addWidget(self.frame)
        self.frame_3 = QtGui.QFrame(batchadjform)
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.verticalLayout.addWidget(self.frame_3)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.adj_tableView = QtGui.QTableView(batchadjform)
        self.adj_tableView.setObjectName(_fromUtf8("adj_tableView"))
        self.horizontalLayout.addWidget(self.adj_tableView)
        self.populate_pushButton = QtGui.QPushButton(batchadjform)
        self.populate_pushButton.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/arrow-l")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.populate_pushButton.setIcon(icon5)
        self.populate_pushButton.setIconSize(QtCore.QSize(50, 50))
        self.populate_pushButton.setFlat(True)
        self.populate_pushButton.setObjectName(_fromUtf8("populate_pushButton"))
        self.horizontalLayout.addWidget(self.populate_pushButton)
        self.batchList_tableView = QtGui.QTableView(batchadjform)
        self.batchList_tableView.setObjectName(_fromUtf8("batchList_tableView"))
        self.batchList_tableView.verticalHeader().setVisible(False)
        self.horizontalLayout.addWidget(self.batchList_tableView)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(batchadjform)
        QtCore.QMetaObject.connectSlotsByName(batchadjform)

    def retranslateUi(self, batchadjform):
        batchadjform.setWindowTitle(_translate("batchadjform", "Batch Adjustment", None))
        self.label_2.setText(_translate("batchadjform", "Adjust Total Raw Materials Used:", None))
        self.saveButton.setText(_translate("batchadjform", "&Save", None))
        self.clearButton.setText(_translate("batchadjform", "Clear", None))
        self.refresh_pushButton.setText(_translate("batchadjform", "&Refresh", None))
        self.closeButton.setText(_translate("batchadjform", "Close", None))

import images_rc
