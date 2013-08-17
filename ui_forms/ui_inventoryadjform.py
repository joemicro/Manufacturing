# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inventoryadjform.ui'
#
# Created: Sun Jul 07 15:54:40 2013
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

class Ui_InventoryAdjustment(object):
    def setupUi(self, InventoryAdjustment):
        InventoryAdjustment.setObjectName(_fromUtf8("InventoryAdjustment"))
        InventoryAdjustment.resize(553, 467)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/settings")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        InventoryAdjustment.setWindowIcon(icon)
        self.verticalLayout = QtGui.QVBoxLayout(InventoryAdjustment)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.frame_2 = QtGui.QFrame(InventoryAdjustment)
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
        self.frame = QtGui.QFrame(InventoryAdjustment)
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
        self.newButton = QtGui.QPushButton(self.frame)
        self.newButton.setMinimumSize(QtCore.QSize(90, 0))
        self.newButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.newButton.setStyleSheet(_fromUtf8("QPushButton {\n"
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
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/new")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.newButton.setIcon(icon1)
        self.newButton.setIconSize(QtCore.QSize(20, 20))
        self.newButton.setFlat(False)
        self.newButton.setObjectName(_fromUtf8("newButton"))
        self.horizontalLayout_4.addWidget(self.newButton)
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/save")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.saveButton.setIcon(icon2)
        self.saveButton.setIconSize(QtCore.QSize(20, 20))
        self.saveButton.setFlat(False)
        self.saveButton.setObjectName(_fromUtf8("saveButton"))
        self.horizontalLayout_4.addWidget(self.saveButton)
        self.deleteButton = QtGui.QPushButton(self.frame)
        self.deleteButton.setMinimumSize(QtCore.QSize(90, 0))
        self.deleteButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.deleteButton.setStyleSheet(_fromUtf8("QPushButton {\n"
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
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/delete")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon3)
        self.deleteButton.setIconSize(QtCore.QSize(20, 20))
        self.deleteButton.setFlat(False)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.horizontalLayout_4.addWidget(self.deleteButton)
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
        self.frame_3 = QtGui.QFrame(InventoryAdjustment)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 70))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 70))
        self.frame_3.setFrameShape(QtGui.QFrame.Box)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.frame_3)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.adj_dateEdit = QtGui.QDateEdit(self.frame_3)
        self.adj_dateEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.adj_dateEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.adj_dateEdit.setCalendarPopup(True)
        self.adj_dateEdit.setObjectName(_fromUtf8("adj_dateEdit"))
        self.gridLayout.addWidget(self.adj_dateEdit, 0, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.frame_3)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.v_adjID_label = QtGui.QLabel(self.frame_3)
        self.v_adjID_label.setMinimumSize(QtCore.QSize(96, 25))
        self.v_adjID_label.setMaximumSize(QtCore.QSize(96, 25))
        self.v_adjID_label.setFrameShape(QtGui.QFrame.Box)
        self.v_adjID_label.setText(_fromUtf8(""))
        self.v_adjID_label.setObjectName(_fromUtf8("v_adjID_label"))
        self.gridLayout.addWidget(self.v_adjID_label, 1, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.label_6 = QtGui.QLabel(self.frame_3)
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout.addWidget(self.label_6)
        self.note_textEdit = QtGui.QTextEdit(self.frame_3)
        self.note_textEdit.setFrameShape(QtGui.QFrame.StyledPanel)
        self.note_textEdit.setFrameShadow(QtGui.QFrame.Plain)
        self.note_textEdit.setTabChangesFocus(True)
        self.note_textEdit.setAcceptRichText(False)
        self.note_textEdit.setObjectName(_fromUtf8("note_textEdit"))
        self.horizontalLayout.addWidget(self.note_textEdit)
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_4 = QtGui.QLabel(self.frame_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout_2.addWidget(self.label_4, 0, 0, 1, 1)
        self.v_value_label = QtGui.QLabel(self.frame_3)
        self.v_value_label.setMinimumSize(QtCore.QSize(96, 25))
        self.v_value_label.setMaximumSize(QtCore.QSize(96, 25))
        self.v_value_label.setFrameShape(QtGui.QFrame.Box)
        self.v_value_label.setText(_fromUtf8(""))
        self.v_value_label.setObjectName(_fromUtf8("v_value_label"))
        self.gridLayout_2.addWidget(self.v_value_label, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.frame_3)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout_2.addWidget(self.label_5, 1, 0, 1, 1)
        self.v_adjValue_label = QtGui.QLabel(self.frame_3)
        self.v_adjValue_label.setMinimumSize(QtCore.QSize(96, 25))
        self.v_adjValue_label.setMaximumSize(QtCore.QSize(96, 25))
        self.v_adjValue_label.setFrameShape(QtGui.QFrame.Box)
        self.v_adjValue_label.setText(_fromUtf8(""))
        self.v_adjValue_label.setObjectName(_fromUtf8("v_adjValue_label"))
        self.gridLayout_2.addWidget(self.v_adjValue_label, 1, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_2)
        self.verticalLayout.addWidget(self.frame_3)
        self.detail_tableView = QtGui.QTableView(InventoryAdjustment)
        self.detail_tableView.setObjectName(_fromUtf8("detail_tableView"))
        self.verticalLayout.addWidget(self.detail_tableView)

        self.retranslateUi(InventoryAdjustment)
        QtCore.QMetaObject.connectSlotsByName(InventoryAdjustment)
        InventoryAdjustment.setTabOrder(self.adj_dateEdit, self.note_textEdit)
        InventoryAdjustment.setTabOrder(self.note_textEdit, self.detail_tableView)
        InventoryAdjustment.setTabOrder(self.detail_tableView, self.saveButton)
        InventoryAdjustment.setTabOrder(self.saveButton, self.newButton)
        InventoryAdjustment.setTabOrder(self.newButton, self.closeButton)
        InventoryAdjustment.setTabOrder(self.closeButton, self.deleteButton)

    def retranslateUi(self, InventoryAdjustment):
        InventoryAdjustment.setWindowTitle(_translate("InventoryAdjustment", "Inventory Adjustment", None))
        self.label_2.setText(_translate("InventoryAdjustment", "Inventory Adjustment:", None))
        self.newButton.setText(_translate("InventoryAdjustment", "&New", None))
        self.saveButton.setText(_translate("InventoryAdjustment", "&Save", None))
        self.deleteButton.setText(_translate("InventoryAdjustment", "&Delete", None))
        self.closeButton.setText(_translate("InventoryAdjustment", "Close", None))
        self.label.setText(_translate("InventoryAdjustment", "Date:", None))
        self.label_3.setText(_translate("InventoryAdjustment", "Adjustment ID:", None))
        self.label_6.setText(_translate("InventoryAdjustment", "Notes", None))
        self.label_4.setText(_translate("InventoryAdjustment", "Inventory Value", None))
        self.label_5.setText(_translate("InventoryAdjustment", "Adjustment Value", None))

import images_rc
