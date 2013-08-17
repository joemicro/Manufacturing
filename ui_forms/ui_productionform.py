# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'productionform.ui'
#
# Created: Thu Aug 15 15:51:50 2013
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

class Ui_ProductionForm(object):
    def setupUi(self, ProductionForm):
        ProductionForm.setObjectName(_fromUtf8("ProductionForm"))
        ProductionForm.resize(1030, 586)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ProductionForm.sizePolicy().hasHeightForWidth())
        ProductionForm.setSizePolicy(sizePolicy)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/production")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        ProductionForm.setWindowIcon(icon)
        self.gridLayout_2 = QtGui.QGridLayout(ProductionForm)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.frame_3 = QtGui.QFrame(ProductionForm)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 40))
        self.frame_3.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.label_14 = QtGui.QLabel(self.frame_3)
        self.label_14.setGeometry(QtCore.QRect(77, 5, 259, 32))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.verticalLayout_2.addWidget(self.frame_3)
        self.frame_2 = QtGui.QFrame(ProductionForm)
        self.frame_2.setAutoFillBackground(False)
        self.frame_2.setStyleSheet(_fromUtf8("QFrame {border: none;\n"
"background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"stop: 0 #BBBBBB, \n"
"stop: 0.4 #EEEEEE,\n"
"stop: 0.9 #CCCCCC,\n"
" stop: 1 #666666);}"))
        self.frame_2.setFrameShape(QtGui.QFrame.Box)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.frame_2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.newButton = QtGui.QPushButton(self.frame_2)
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
        self.saveButton = QtGui.QPushButton(self.frame_2)
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
        self.calcButton = QtGui.QPushButton(self.frame_2)
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
        self.receiveButton = QtGui.QPushButton(self.frame_2)
        self.receiveButton.setMinimumSize(QtCore.QSize(90, 0))
        self.receiveButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.receiveButton.setStyleSheet(_fromUtf8("QPushButton {\n"
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
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/item")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.receiveButton.setIcon(icon4)
        self.receiveButton.setIconSize(QtCore.QSize(20, 20))
        self.receiveButton.setFlat(False)
        self.receiveButton.setObjectName(_fromUtf8("receiveButton"))
        self.horizontalLayout.addWidget(self.receiveButton)
        self.deleteButton = QtGui.QPushButton(self.frame_2)
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
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/delete")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.deleteButton.setIcon(icon5)
        self.deleteButton.setIconSize(QtCore.QSize(20, 20))
        self.deleteButton.setFlat(False)
        self.deleteButton.setObjectName(_fromUtf8("deleteButton"))
        self.horizontalLayout.addWidget(self.deleteButton)
        self.printButton = QtGui.QPushButton(self.frame_2)
        self.printButton.setMinimumSize(QtCore.QSize(90, 0))
        self.printButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.printButton.setStyleSheet(_fromUtf8("QPushButton {\n"
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
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/print")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.printButton.setIcon(icon6)
        self.printButton.setIconSize(QtCore.QSize(20, 20))
        self.printButton.setFlat(False)
        self.printButton.setObjectName(_fromUtf8("printButton"))
        self.horizontalLayout.addWidget(self.printButton)
        self.closeButton = QtGui.QPushButton(self.frame_2)
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
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/exit")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon7)
        self.closeButton.setIconSize(QtCore.QSize(20, 20))
        self.closeButton.setFlat(False)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.horizontalLayout.addWidget(self.closeButton)
        self.prep_comboBox = QtGui.QComboBox(self.frame_2)
        self.prep_comboBox.setMinimumSize(QtCore.QSize(75, 25))
        self.prep_comboBox.setObjectName(_fromUtf8("prep_comboBox"))
        self.horizontalLayout.addWidget(self.prep_comboBox)
        spacerItem = QtGui.QSpacerItem(342, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_2.addWidget(self.frame_2)
        self.gridLayout_2.addLayout(self.verticalLayout_2, 0, 0, 1, 2)
        self.label_12 = QtGui.QLabel(ProductionForm)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout_2.addWidget(self.label_12, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.frame = QtGui.QFrame(ProductionForm)
        self.frame.setMinimumSize(QtCore.QSize(379, 170))
        self.frame.setMaximumSize(QtCore.QSize(379, 170))
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.gridLayout = QtGui.QGridLayout(self.frame)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(self.frame)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.v_prodID_label = QtGui.QLabel(self.frame)
        self.v_prodID_label.setMinimumSize(QtCore.QSize(96, 25))
        self.v_prodID_label.setMaximumSize(QtCore.QSize(96, 25))
        self.v_prodID_label.setFrameShape(QtGui.QFrame.Box)
        self.v_prodID_label.setText(_fromUtf8(""))
        self.v_prodID_label.setObjectName(_fromUtf8("v_prodID_label"))
        self.gridLayout.addWidget(self.v_prodID_label, 0, 1, 1, 1)
        self.label_11 = QtGui.QLabel(self.frame)
        self.label_11.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 0, 2, 1, 1)
        self.notesTextEdit = QtGui.QTextEdit(self.frame)
        self.notesTextEdit.setObjectName(_fromUtf8("notesTextEdit"))
        self.gridLayout.addWidget(self.notesTextEdit, 0, 3, 2, 2)
        self.label_2 = QtGui.QLabel(self.frame)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.dateDateEdit = QtGui.QDateEdit(self.frame)
        self.dateDateEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.dateDateEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.dateDateEdit.setCalendarPopup(True)
        self.dateDateEdit.setObjectName(_fromUtf8("dateDateEdit"))
        self.gridLayout.addWidget(self.dateDateEdit, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.frame)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.refnoLineEdit = QtGui.QLineEdit(self.frame)
        self.refnoLineEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.refnoLineEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.refnoLineEdit.setObjectName(_fromUtf8("refnoLineEdit"))
        self.gridLayout.addWidget(self.refnoLineEdit, 2, 1, 1, 1)
        self.label_4 = QtGui.QLabel(self.frame)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 2, 2, 1, 2)
        self.filingChargeLineEdit = QtGui.QLineEdit(self.frame)
        self.filingChargeLineEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.filingChargeLineEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.filingChargeLineEdit.setObjectName(_fromUtf8("filingChargeLineEdit"))
        self.gridLayout.addWidget(self.filingChargeLineEdit, 2, 4, 1, 1)
        self.label_10 = QtGui.QLabel(self.frame)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 3, 0, 1, 1)
        self.v_fgVolume_label = QtGui.QLabel(self.frame)
        self.v_fgVolume_label.setMinimumSize(QtCore.QSize(96, 25))
        self.v_fgVolume_label.setMaximumSize(QtCore.QSize(96, 25))
        self.v_fgVolume_label.setFrameShape(QtGui.QFrame.Box)
        self.v_fgVolume_label.setText(_fromUtf8(""))
        self.v_fgVolume_label.setObjectName(_fromUtf8("v_fgVolume_label"))
        self.gridLayout.addWidget(self.v_fgVolume_label, 3, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.frame)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 3, 2, 1, 2)
        self.labourChargeLineEdit = QtGui.QLineEdit(self.frame)
        self.labourChargeLineEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.labourChargeLineEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.labourChargeLineEdit.setObjectName(_fromUtf8("labourChargeLineEdit"))
        self.gridLayout.addWidget(self.labourChargeLineEdit, 3, 4, 1, 1)
        self.label_9 = QtGui.QLabel(self.frame)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 4, 0, 1, 1)
        self.v_rmCost_label = QtGui.QLabel(self.frame)
        self.v_rmCost_label.setMinimumSize(QtCore.QSize(96, 25))
        self.v_rmCost_label.setMaximumSize(QtCore.QSize(96, 25))
        self.v_rmCost_label.setFrameShape(QtGui.QFrame.Box)
        self.v_rmCost_label.setText(_fromUtf8(""))
        self.v_rmCost_label.setObjectName(_fromUtf8("v_rmCost_label"))
        self.gridLayout.addWidget(self.v_rmCost_label, 4, 1, 1, 1)
        self.label_7 = QtGui.QLabel(self.frame)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 4, 2, 1, 2)
        self.v_costPerLT_label = QtGui.QLabel(self.frame)
        self.v_costPerLT_label.setMinimumSize(QtCore.QSize(96, 25))
        self.v_costPerLT_label.setMaximumSize(QtCore.QSize(96, 25))
        self.v_costPerLT_label.setFrameShape(QtGui.QFrame.Box)
        self.v_costPerLT_label.setText(_fromUtf8(""))
        self.v_costPerLT_label.setObjectName(_fromUtf8("v_costPerLT_label"))
        self.gridLayout.addWidget(self.v_costPerLT_label, 4, 4, 1, 1)
        self.label_8 = QtGui.QLabel(self.frame)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 5, 0, 1, 1)
        self.v_totalFGCost_label = QtGui.QLabel(self.frame)
        self.v_totalFGCost_label.setMinimumSize(QtCore.QSize(96, 25))
        self.v_totalFGCost_label.setMaximumSize(QtCore.QSize(96, 25))
        self.v_totalFGCost_label.setFrameShape(QtGui.QFrame.Box)
        self.v_totalFGCost_label.setText(_fromUtf8(""))
        self.v_totalFGCost_label.setObjectName(_fromUtf8("v_totalFGCost_label"))
        self.gridLayout.addWidget(self.v_totalFGCost_label, 5, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.frame)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 5, 2, 1, 2)
        self.v_totalFees_label = QtGui.QLabel(self.frame)
        self.v_totalFees_label.setMinimumSize(QtCore.QSize(96, 25))
        self.v_totalFees_label.setMaximumSize(QtCore.QSize(96, 25))
        self.v_totalFees_label.setFrameShape(QtGui.QFrame.Box)
        self.v_totalFees_label.setText(_fromUtf8(""))
        self.v_totalFees_label.setObjectName(_fromUtf8("v_totalFees_label"))
        self.gridLayout.addWidget(self.v_totalFees_label, 5, 4, 1, 1)
        self.horizontalLayout_2.addWidget(self.frame)
        self.batchesTableView = QtGui.QTableView(ProductionForm)
        self.batchesTableView.setObjectName(_fromUtf8("batchesTableView"))
        self.horizontalLayout_2.addWidget(self.batchesTableView)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 2, 0, 1, 2)
        self.productionTableView = QtGui.QTableView(ProductionForm)
        self.productionTableView.setMinimumSize(QtCore.QSize(743, 0))
        self.productionTableView.setObjectName(_fromUtf8("productionTableView"))
        self.gridLayout_2.addWidget(self.productionTableView, 3, 0, 1, 1)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_13 = QtGui.QLabel(ProductionForm)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.verticalLayout.addWidget(self.label_13)
        self.bsView = QtGui.QTableView(ProductionForm)
        self.bsView.setObjectName(_fromUtf8("bsView"))
        self.verticalLayout.addWidget(self.bsView)
        self.label_15 = QtGui.QLabel(ProductionForm)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.verticalLayout.addWidget(self.label_15)
        self.bmView = QtGui.QTableView(ProductionForm)
        self.bmView.setObjectName(_fromUtf8("bmView"))
        self.verticalLayout.addWidget(self.bmView)
        self.gridLayout_2.addLayout(self.verticalLayout, 3, 1, 1, 1)
        self.label_12.setBuddy(self.batchesTableView)
        self.label_11.setBuddy(self.notesTextEdit)
        self.label_2.setBuddy(self.dateDateEdit)
        self.label_3.setBuddy(self.refnoLineEdit)
        self.label_4.setBuddy(self.filingChargeLineEdit)
        self.label_5.setBuddy(self.labourChargeLineEdit)
        self.label_13.setBuddy(self.bsView)
        self.label_15.setBuddy(self.bsView)

        self.retranslateUi(ProductionForm)
        QtCore.QMetaObject.connectSlotsByName(ProductionForm)
        ProductionForm.setTabOrder(self.dateDateEdit, self.refnoLineEdit)
        ProductionForm.setTabOrder(self.refnoLineEdit, self.filingChargeLineEdit)
        ProductionForm.setTabOrder(self.filingChargeLineEdit, self.labourChargeLineEdit)
        ProductionForm.setTabOrder(self.labourChargeLineEdit, self.batchesTableView)
        ProductionForm.setTabOrder(self.batchesTableView, self.productionTableView)
        ProductionForm.setTabOrder(self.productionTableView, self.calcButton)
        ProductionForm.setTabOrder(self.calcButton, self.receiveButton)
        ProductionForm.setTabOrder(self.receiveButton, self.saveButton)
        ProductionForm.setTabOrder(self.saveButton, self.newButton)
        ProductionForm.setTabOrder(self.newButton, self.closeButton)
        ProductionForm.setTabOrder(self.closeButton, self.printButton)
        ProductionForm.setTabOrder(self.printButton, self.deleteButton)
        ProductionForm.setTabOrder(self.deleteButton, self.notesTextEdit)
        ProductionForm.setTabOrder(self.notesTextEdit, self.bsView)
        ProductionForm.setTabOrder(self.bsView, self.bmView)

    def retranslateUi(self, ProductionForm):
        ProductionForm.setWindowTitle(_translate("ProductionForm", "Production Form", None))
        self.label_14.setText(_translate("ProductionForm", "Production:", None))
        self.newButton.setText(_translate("ProductionForm", "&New", None))
        self.saveButton.setText(_translate("ProductionForm", "&Save", None))
        self.calcButton.setText(_translate("ProductionForm", "&Recalculate", None))
        self.receiveButton.setText(_translate("ProductionForm", "Receive", None))
        self.deleteButton.setText(_translate("ProductionForm", "Delete", None))
        self.printButton.setText(_translate("ProductionForm", "Print", None))
        self.closeButton.setText(_translate("ProductionForm", "Close", None))
        self.label_12.setText(_translate("ProductionForm", "                                                                                                                                   Batches", None))
        self.label.setText(_translate("ProductionForm", "Production ID", None))
        self.label_11.setText(_translate("ProductionForm", "Notes", None))
        self.label_2.setText(_translate("ProductionForm", "Date", None))
        self.label_3.setText(_translate("ProductionForm", "Ref no:", None))
        self.label_4.setText(_translate("ProductionForm", "Filing Charge", None))
        self.label_10.setText(_translate("ProductionForm", "FG Volume", None))
        self.label_5.setText(_translate("ProductionForm", "Labour Charge", None))
        self.label_9.setText(_translate("ProductionForm", "RM Cost", None))
        self.label_7.setText(_translate("ProductionForm", "Per Lt Cost", None))
        self.label_8.setText(_translate("ProductionForm", "Total FG Cost", None))
        self.label_6.setText(_translate("ProductionForm", "Total Fees", None))
        self.label_13.setText(_translate("ProductionForm", "Batches Applied To the item", None))
        self.label_15.setText(_translate("ProductionForm", "BOM Applied To Item", None))

import images_rc
