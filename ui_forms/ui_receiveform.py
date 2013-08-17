# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'receiveform.ui'
#
# Created: Sun Jul 07 15:55:47 2013
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

class Ui_ReceiveForm(object):
    def setupUi(self, ReceiveForm):
        ReceiveForm.setObjectName(_fromUtf8("ReceiveForm"))
        ReceiveForm.resize(883, 577)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/inventory")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ReceiveForm.setWindowIcon(icon)
        ReceiveForm.setAutoFillBackground(True)
        self.gridLayout_5 = QtGui.QGridLayout(ReceiveForm)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.label_11 = QtGui.QLabel(ReceiveForm)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_11.setFont(font)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout_5.addWidget(self.label_11, 0, 0, 1, 1)
        self.frame_4 = QtGui.QFrame(ReceiveForm)
        self.frame_4.setAutoFillBackground(False)
        self.frame_4.setStyleSheet(_fromUtf8("border: none;\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #BBBBBB, \n"
"stop: 0.4 #EEEEEE,\n"
"stop: 0.9 #CCCCCC,\n"
" stop: 1 #666666);"))
        self.frame_4.setFrameShape(QtGui.QFrame.Box)
        self.frame_4.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_4.setObjectName(_fromUtf8("frame_4"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_4)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.newButton = QtGui.QPushButton(self.frame_4)
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
        self.horizontalLayout.addWidget(self.newButton)
        self.saveButton = QtGui.QPushButton(self.frame_4)
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
        self.horizontalLayout.addWidget(self.saveButton)
        self.calcButton = QtGui.QPushButton(self.frame_4)
        self.calcButton.setMinimumSize(QtCore.QSize(90, 0))
        self.calcButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.calcButton.setStyleSheet(_fromUtf8("QPushButton {\n"
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
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/delete")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon4)
        self.deleteButton.setIconSize(QtCore.QSize(20, 20))
        self.deleteButton.setFlat(False)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.horizontalLayout.addWidget(self.deleteButton)
        self.findButton = QtGui.QPushButton(self.frame_4)
        self.findButton.setMinimumSize(QtCore.QSize(90, 0))
        self.findButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.findButton.setStyleSheet(_fromUtf8("QPushButton {\n"
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
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/find")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.findButton.setIcon(icon5)
        self.findButton.setIconSize(QtCore.QSize(20, 20))
        self.findButton.setFlat(False)
        self.findButton.setObjectName(_fromUtf8("findButton"))
        self.horizontalLayout.addWidget(self.findButton)
        self.closeButton = QtGui.QPushButton(self.frame_4)
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
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/exit")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon6)
        self.closeButton.setIconSize(QtCore.QSize(20, 20))
        self.closeButton.setFlat(False)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout.addWidget(self.closeButton)
        spacerItem = QtGui.QSpacerItem(259, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.gridLayout_5.addWidget(self.frame_4, 1, 0, 1, 4)
        self.frame_3 = QtGui.QFrame(ReceiveForm)
        self.frame_3.setMinimumSize(QtCore.QSize(500, 180))
        self.frame_3.setAutoFillBackground(True)
        self.frame_3.setFrameShape(QtGui.QFrame.Box)
        self.frame_3.setFrameShadow(QtGui.QFrame.Plain)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.gridLayout_4 = QtGui.QGridLayout(self.frame_3)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.gridLayout_2 = QtGui.QGridLayout()
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label = QtGui.QLabel(self.frame_3)
        self.label.setMinimumSize(QtCore.QSize(46, 0))
        self.label.setMaximumSize(QtCore.QSize(46, 16777215))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.supcom = QtGui.QComboBox(self.frame_3)
        self.supcom.setMinimumSize(QtCore.QSize(197, 25))
        self.supcom.setMaximumSize(QtCore.QSize(197, 25))
        self.supcom.setObjectName(_fromUtf8("supcom"))
        self.gridLayout_2.addWidget(self.supcom, 0, 1, 1, 2)
        self.label_2 = QtGui.QLabel(self.frame_3)
        self.label_2.setMinimumSize(QtCore.QSize(46, 0))
        self.label_2.setMaximumSize(QtCore.QSize(46, 16777215))
        self.label_2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_2.addWidget(self.label_2, 1, 0, 1, 1)
        self.note_textEdit = QtGui.QTextEdit(self.frame_3)
        self.note_textEdit.setMinimumSize(QtCore.QSize(197, 81))
        self.note_textEdit.setMaximumSize(QtCore.QSize(197, 81))
        self.note_textEdit.setTabChangesFocus(True)
        self.note_textEdit.setObjectName(_fromUtf8("note_textEdit"))
        self.gridLayout_2.addWidget(self.note_textEdit, 1, 1, 1, 2)
        self.label_3 = QtGui.QLabel(self.frame_3)
        self.label_3.setMinimumSize(QtCore.QSize(46, 0))
        self.label_3.setMaximumSize(QtCore.QSize(46, 16777215))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_2.addWidget(self.label_3, 2, 0, 1, 1)
        self.curr_lineEdit = QtGui.QLineEdit(self.frame_3)
        self.curr_lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.curr_lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.curr_lineEdit.setInputMask(_fromUtf8(""))
        self.curr_lineEdit.setObjectName(_fromUtf8("curr_lineEdit"))
        self.gridLayout_2.addWidget(self.curr_lineEdit, 2, 1, 1, 1)
        self.frame = QtGui.QFrame(self.frame_3)
        self.frame.setMinimumSize(QtCore.QSize(100, 0))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout_2.addWidget(self.frame, 2, 2, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout_2, 0, 0, 1, 1)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_4 = QtGui.QLabel(self.frame_3)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 0, 1, 1)
        self.transid_lineEdit = QtGui.QLineEdit(self.frame_3)
        self.transid_lineEdit.setEnabled(False)
        self.transid_lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.transid_lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.transid_lineEdit.setObjectName(_fromUtf8("transid_lineEdit"))
        self.gridLayout.addWidget(self.transid_lineEdit, 0, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.frame_3)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 1, 0, 1, 1)
        self.date_dateEdit = QtGui.QDateEdit(self.frame_3)
        self.date_dateEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.date_dateEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.date_dateEdit.setCalendarPopup(True)
        self.date_dateEdit.setObjectName(_fromUtf8("date_dateEdit"))
        self.gridLayout.addWidget(self.date_dateEdit, 1, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.frame_3)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 0, 1, 1)
        self.billno_lineEdit = QtGui.QLineEdit(self.frame_3)
        self.billno_lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.billno_lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.billno_lineEdit.setObjectName(_fromUtf8("billno_lineEdit"))
        self.gridLayout.addWidget(self.billno_lineEdit, 2, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.frame_3)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 3, 0, 1, 1)
        self.shipping_lineEdit = QtGui.QLineEdit(self.frame_3)
        self.shipping_lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.shipping_lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.shipping_lineEdit.setInputMask(_fromUtf8(""))
        self.shipping_lineEdit.setObjectName(_fromUtf8("shipping_lineEdit"))
        self.gridLayout.addWidget(self.shipping_lineEdit, 3, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.frame_3)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)
        self.total_lineEdit = QtGui.QLineEdit(self.frame_3)
        self.total_lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.total_lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.total_lineEdit.setInputMask(_fromUtf8(""))
        self.total_lineEdit.setObjectName(_fromUtf8("total_lineEdit"))
        self.gridLayout.addWidget(self.total_lineEdit, 4, 1, 1, 1)
        self.gridLayout_4.addLayout(self.gridLayout, 0, 1, 1, 1)
        self.gridLayout_5.addWidget(self.frame_3, 2, 0, 1, 2)
        self.frame_6 = QtGui.QFrame(ReceiveForm)
        self.frame_6.setMinimumSize(QtCore.QSize(120, 195))
        self.frame_6.setMaximumSize(QtCore.QSize(120, 16777215))
        self.frame_6.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_6.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_6.setObjectName(_fromUtf8("frame_6"))
        self.gridLayout_6 = QtGui.QGridLayout(self.frame_6)
        self.gridLayout_6.setObjectName(_fromUtf8("gridLayout_6"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.groupBox = QtGui.QGroupBox(self.frame_6)
        self.groupBox.setTitle(_fromUtf8(""))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.verticalLayout = QtGui.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.receive_radioButton = QtGui.QRadioButton(self.groupBox)
        self.receive_radioButton.setObjectName(_fromUtf8("receive_radioButton"))
        self.verticalLayout.addWidget(self.receive_radioButton)
        self.return_radioButton = QtGui.QRadioButton(self.groupBox)
        self.return_radioButton.setObjectName(_fromUtf8("return_radioButton"))
        self.verticalLayout.addWidget(self.return_radioButton)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.export_checkBox = QtGui.QCheckBox(self.frame_6)
        self.export_checkBox.setObjectName(_fromUtf8("export_checkBox"))
        self.verticalLayout_3.addWidget(self.export_checkBox)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_10 = QtGui.QLabel(self.frame_6)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout_3.addWidget(self.label_10, 1, 0, 1, 1)
        self.qst_lineEdit = QtGui.QLineEdit(self.frame_6)
        self.qst_lineEdit.setMinimumSize(QtCore.QSize(71, 25))
        self.qst_lineEdit.setMaximumSize(QtCore.QSize(71, 25))
        self.qst_lineEdit.setInputMask(_fromUtf8(""))
        self.qst_lineEdit.setObjectName(_fromUtf8("qst_lineEdit"))
        self.gridLayout_3.addWidget(self.qst_lineEdit, 1, 1, 1, 1)
        self.gst_lineEdit = QtGui.QLineEdit(self.frame_6)
        self.gst_lineEdit.setMinimumSize(QtCore.QSize(71, 25))
        self.gst_lineEdit.setMaximumSize(QtCore.QSize(71, 25))
        self.gst_lineEdit.setInputMask(_fromUtf8(""))
        self.gst_lineEdit.setObjectName(_fromUtf8("gst_lineEdit"))
        self.gridLayout_3.addWidget(self.gst_lineEdit, 0, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.frame_6)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout_3)
        self.amount_lineEdit = QtGui.QLineEdit(self.frame_6)
        self.amount_lineEdit.setEnabled(False)
        self.amount_lineEdit.setObjectName(_fromUtf8("amount_lineEdit"))
        self.verticalLayout_2.addWidget(self.amount_lineEdit)
        self.verticalLayout_3.addLayout(self.verticalLayout_2)
        self.gridLayout_6.addLayout(self.verticalLayout_3, 0, 0, 1, 1)
        self.gridLayout_5.addWidget(self.frame_6, 2, 2, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(251, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout_5.addItem(spacerItem1, 2, 3, 1, 1)
        spacerItem2 = QtGui.QSpacerItem(20, 19, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout_5.addItem(spacerItem2, 3, 1, 1, 1)
        spacerItem3 = QtGui.QSpacerItem(20, 19, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        self.gridLayout_5.addItem(spacerItem3, 3, 2, 1, 1)
        self.receive_tableView = QtGui.QTableView(ReceiveForm)
        self.receive_tableView.setMinimumSize(QtCore.QSize(840, 240))
        self.receive_tableView.setObjectName(_fromUtf8("receive_tableView"))
        self.gridLayout_5.addWidget(self.receive_tableView, 4, 0, 1, 4)
        self.label.setBuddy(self.supcom)
        self.label_2.setBuddy(self.note_textEdit)
        self.label_3.setBuddy(self.curr_lineEdit)
        self.label_4.setBuddy(self.transid_lineEdit)
        self.label_7.setBuddy(self.date_dateEdit)
        self.label_5.setBuddy(self.billno_lineEdit)
        self.label_6.setBuddy(self.shipping_lineEdit)
        self.label_8.setBuddy(self.total_lineEdit)
        self.label_10.setBuddy(self.qst_lineEdit)
        self.label_9.setBuddy(self.gst_lineEdit)

        self.retranslateUi(ReceiveForm)
        QtCore.QMetaObject.connectSlotsByName(ReceiveForm)
        ReceiveForm.setTabOrder(self.supcom, self.note_textEdit)
        ReceiveForm.setTabOrder(self.note_textEdit, self.date_dateEdit)
        ReceiveForm.setTabOrder(self.date_dateEdit, self.billno_lineEdit)
        ReceiveForm.setTabOrder(self.billno_lineEdit, self.shipping_lineEdit)
        ReceiveForm.setTabOrder(self.shipping_lineEdit, self.gst_lineEdit)
        ReceiveForm.setTabOrder(self.gst_lineEdit, self.qst_lineEdit)
        ReceiveForm.setTabOrder(self.qst_lineEdit, self.total_lineEdit)
        ReceiveForm.setTabOrder(self.total_lineEdit, self.receive_tableView)
        ReceiveForm.setTabOrder(self.receive_tableView, self.receive_radioButton)
        ReceiveForm.setTabOrder(self.receive_radioButton, self.return_radioButton)
        ReceiveForm.setTabOrder(self.return_radioButton, self.amount_lineEdit)
        ReceiveForm.setTabOrder(self.amount_lineEdit, self.transid_lineEdit)
        ReceiveForm.setTabOrder(self.transid_lineEdit, self.curr_lineEdit)

    def retranslateUi(self, ReceiveForm):
        ReceiveForm.setWindowTitle(_translate("ReceiveForm", "Receiving Form", None))
        self.label_11.setText(_translate("ReceiveForm", "Receive Inventory:", None))
        self.newButton.setText(_translate("ReceiveForm", "&New", None))
        self.saveButton.setText(_translate("ReceiveForm", "&Save", None))
        self.calcButton.setText(_translate("ReceiveForm", "&Recalculate", None))
        self.deleteButton.setText(_translate("ReceiveForm", "&Delete", None))
        self.findButton.setText(_translate("ReceiveForm", "&Find", None))
        self.closeButton.setText(_translate("ReceiveForm", "&Close", None))
        self.label.setText(_translate("ReceiveForm", "Supplier", None))
        self.label_2.setText(_translate("ReceiveForm", "Note", None))
        self.label_3.setText(_translate("ReceiveForm", "Currency", None))
        self.label_4.setText(_translate("ReceiveForm", "ID", None))
        self.label_7.setText(_translate("ReceiveForm", "Date", None))
        self.label_5.setText(_translate("ReceiveForm", "Bill No.", None))
        self.label_6.setText(_translate("ReceiveForm", "Shipping", None))
        self.label_8.setText(_translate("ReceiveForm", "Total", None))
        self.receive_radioButton.setText(_translate("ReceiveForm", "Receive", None))
        self.return_radioButton.setText(_translate("ReceiveForm", "Return", None))
        self.export_checkBox.setText(_translate("ReceiveForm", "Export", None))
        self.label_10.setText(_translate("ReceiveForm", "QST", None))
        self.label_9.setText(_translate("ReceiveForm", "GST", None))

import images_rc
