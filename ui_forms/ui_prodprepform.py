# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'prodprepform.ui'
#
# Created: Thu Aug 15 15:51:30 2013
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

class Ui_ProdPrep(object):
    def setupUi(self, ProdPrep):
        ProdPrep.setObjectName(_fromUtf8("ProdPrep"))
        ProdPrep.resize(602, 551)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/prep")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ProdPrep.setWindowIcon(icon)
        self.verticalLayout_2 = QtGui.QVBoxLayout(ProdPrep)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame = QtGui.QFrame(ProdPrep)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_11 = QtGui.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame)
        self.frame_4 = QtGui.QFrame(ProdPrep)
        self.frame_4.setAutoFillBackground(False)
        self.frame_4.setStyleSheet(_fromUtf8("QFrame {border: none;\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #BBBBBB, \n"
"stop: 0.4 #EEEEEE,\n"
"stop: 0.9 #CCCCCC,\n"
" stop: 1 #666666);}"))
        self.frame_4.setFrameShape(QtGui.QFrame.Box)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.newButton = QtGui.QPushButton(self.frame_4)
        self.newButton.setMinimumSize(QtCore.QSize(90, 0))
        self.newButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.newButton.setStyleSheet(_fromUtf8("QPushButton {\n"
"background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(0, 0, 0, 050), stop:1 rgba(255, 255, 255, 255));\n"
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
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/new")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newButton.setIcon(icon1)
        self.newButton.setIconSize(QtCore.QSize(20, 20))
        self.newButton.setFlat(False)
        self.newButton.setObjectName(_fromUtf8("newButton"))
        self.horizontalLayout.addWidget(self.newButton)
        self.saveButton = QtGui.QPushButton(self.frame_4)
        self.saveButton.setMinimumSize(QtCore.QSize(90, 0))
        self.saveButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.saveButton.setStyleSheet(_fromUtf8("QPushButton {\n"
"background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(0, 0, 0, 050), stop:1 rgba(255, 255, 255, 255));\n"
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
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/save")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveButton.setIcon(icon2)
        self.saveButton.setIconSize(QtCore.QSize(20, 20))
        self.saveButton.setFlat(False)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout.addWidget(self.saveButton)
        self.calcButton = QtGui.QPushButton(self.frame_4)
        self.calcButton.setMinimumSize(QtCore.QSize(90, 0))
        self.calcButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.calcButton.setStyleSheet(_fromUtf8("QPushButton {\n"
"background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(0, 0, 0, 050), stop:1 rgba(255, 255, 255, 255));\n"
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
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/recalc")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.calcButton.setIcon(icon3)
        self.calcButton.setIconSize(QtCore.QSize(20, 20))
        self.calcButton.setFlat(False)
        self.calcButton.setObjectName(_fromUtf8("calcButton"))
        self.horizontalLayout.addWidget(self.calcButton)
        self.deleteButton = QtGui.QPushButton(self.frame_4)
        self.deleteButton.setMinimumSize(QtCore.QSize(90, 0))
        self.deleteButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.deleteButton.setStyleSheet(_fromUtf8("QPushButton {\n"
"background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(0, 0, 0, 050), stop:1 rgba(255, 255, 255, 255));\n"
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
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/delete")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon4)
        self.deleteButton.setIconSize(QtCore.QSize(20, 20))
        self.deleteButton.setFlat(False)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.horizontalLayout.addWidget(self.deleteButton)
        self.closeButton = QtGui.QPushButton(self.frame_4)
        self.closeButton.setMinimumSize(QtCore.QSize(90, 0))
        self.closeButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.closeButton.setStyleSheet(_fromUtf8("QPushButton {\n"
"background-color: qlineargradient(spread:pad, x1:1, y1:1, x2:1, y2:0, stop:0 rgba(0, 0, 0, 050), stop:1 rgba(255, 255, 255, 255));\n"
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
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/exit")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon5)
        self.closeButton.setIconSize(QtCore.QSize(20, 20))
        self.closeButton.setFlat(False)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout.addWidget(self.closeButton)
        spacerItem = QtGui.QSpacerItem(259, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addWidget(self.frame_4)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label = QtGui.QLabel(ProdPrep)
        self.label.setMinimumSize(QtCore.QSize(0, 25))
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.v_prepNo_label = QtGui.QLabel(ProdPrep)
        self.v_prepNo_label.setMinimumSize(QtCore.QSize(75, 25))
        self.v_prepNo_label.setFrameShape(QtGui.QFrame.Box)
        self.v_prepNo_label.setText(_fromUtf8(""))
        self.v_prepNo_label.setObjectName(_fromUtf8("v_prepNo_label"))
        self.horizontalLayout_2.addWidget(self.v_prepNo_label)
        self.label_3 = QtGui.QLabel(ProdPrep)
        self.label_3.setMinimumSize(QtCore.QSize(0, 25))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.date_dateEdit = QtGui.QDateEdit(ProdPrep)
        self.date_dateEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.date_dateEdit.setCalendarPopup(True)
        self.date_dateEdit.setObjectName(_fromUtf8("date_dateEdit"))
        self.horizontalLayout_2.addWidget(self.date_dateEdit)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.label_7 = QtGui.QLabel(ProdPrep)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setTextFormat(QtCore.Qt.PlainText)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.verticalLayout_2.addWidget(self.label_7)
        self.detail_tableView = QtGui.QTableView(ProdPrep)
        self.detail_tableView.setMinimumSize(QtCore.QSize(0, 195))
        self.detail_tableView.setObjectName(_fromUtf8("detail_tableView"))
        self.verticalLayout_2.addWidget(self.detail_tableView)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_5 = QtGui.QLabel(ProdPrep)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_3.addWidget(self.label_5)
        self.note_lineEdit = QtGui.QLineEdit(ProdPrep)
        self.note_lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.note_lineEdit.setObjectName(_fromUtf8("note_lineEdit"))
        self.horizontalLayout_3.addWidget(self.note_lineEdit)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.label_4 = QtGui.QLabel(ProdPrep)
        self.label_4.setMinimumSize(QtCore.QSize(0, 25))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_3.addWidget(self.label_4)
        self.v_totalQty_label = QtGui.QLabel(ProdPrep)
        self.v_totalQty_label.setMinimumSize(QtCore.QSize(100, 25))
        self.v_totalQty_label.setFrameShape(QtGui.QFrame.Box)
        self.v_totalQty_label.setText(_fromUtf8(""))
        self.v_totalQty_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v_totalQty_label.setObjectName(_fromUtf8("v_totalQty_label"))
        self.horizontalLayout_3.addWidget(self.v_totalQty_label)
        self.label_2 = QtGui.QLabel(ProdPrep)
        self.label_2.setMinimumSize(QtCore.QSize(0, 25))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_3.addWidget(self.label_2)
        self.v_totalLiters_label = QtGui.QLabel(ProdPrep)
        self.v_totalLiters_label.setMinimumSize(QtCore.QSize(100, 25))
        self.v_totalLiters_label.setFrameShape(QtGui.QFrame.Box)
        self.v_totalLiters_label.setText(_fromUtf8(""))
        self.v_totalLiters_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v_totalLiters_label.setObjectName(_fromUtf8("v_totalLiters_label"))
        self.horizontalLayout_3.addWidget(self.v_totalLiters_label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.label_6 = QtGui.QLabel(ProdPrep)
        font = QtGui.QFont()
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.label_6.setFont(font)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.verticalLayout_2.addWidget(self.label_6)
        self.batch_tableView = QtGui.QTableView(ProdPrep)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.batch_tableView.sizePolicy().hasHeightForWidth())
        self.batch_tableView.setSizePolicy(sizePolicy)
        self.batch_tableView.setObjectName(_fromUtf8("batch_tableView"))
        self.verticalLayout_2.addWidget(self.batch_tableView)

        self.retranslateUi(ProdPrep)
        QtCore.QMetaObject.connectSlotsByName(ProdPrep)

    def retranslateUi(self, ProdPrep):
        ProdPrep.setWindowTitle(_translate("ProdPrep", "Production Prep", None))
        self.label_11.setText(_translate("ProdPrep", "Prep Production:", None))
        self.newButton.setText(_translate("ProdPrep", "&New", None))
        self.saveButton.setText(_translate("ProdPrep", "&Save", None))
        self.calcButton.setText(_translate("ProdPrep", "&Recalculate", None))
        self.deleteButton.setText(_translate("ProdPrep", "&Delete", None))
        self.closeButton.setText(_translate("ProdPrep", "&Close", None))
        self.label.setText(_translate("ProdPrep", "Prep No", None))
        self.label_3.setText(_translate("ProdPrep", "Date", None))
        self.label_7.setText(_translate("ProdPrep", "Items To Produce", None))
        self.label_5.setText(_translate("ProdPrep", "Note", None))
        self.label_4.setText(_translate("ProdPrep", "Total Qty", None))
        self.label_2.setText(_translate("ProdPrep", "Total Liters", None))
        self.label_6.setText(_translate("ProdPrep", "Assembly Batches", None))

import images_rc
