# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'finditemform.ui'
#
# Created: Wed Jul 17 15:39:22 2013
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

class Ui_FindItemForm(object):
    def setupUi(self, FindItemForm):
        FindItemForm.setObjectName(_fromUtf8("FindItemForm"))
        FindItemForm.resize(655, 435)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/search")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FindItemForm.setWindowIcon(icon)
        self.resultsView = QtGui.QTableView(FindItemForm)
        self.resultsView.setGeometry(QtCore.QRect(9, 200, 640, 192))
        self.resultsView.setObjectName(_fromUtf8("resultsView"))
        self.resultsLabel = QtGui.QLabel(FindItemForm)
        self.resultsLabel.setGeometry(QtCore.QRect(550, 401, 100, 25))
        self.resultsLabel.setMinimumSize(QtCore.QSize(100, 25))
        self.resultsLabel.setMaximumSize(QtCore.QSize(100, 25))
        self.resultsLabel.setFrameShape(QtGui.QFrame.Box)
        self.resultsLabel.setFrameShadow(QtGui.QFrame.Sunken)
        self.resultsLabel.setText(_fromUtf8(""))
        self.resultsLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.resultsLabel.setObjectName(_fromUtf8("resultsLabel"))
        self.frame = QtGui.QFrame(FindItemForm)
        self.frame.setGeometry(QtCore.QRect(271, 10, 16, 27))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.label = QtGui.QLabel(FindItemForm)
        self.label.setGeometry(QtCore.QRect(11, 11, 53, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.typeCombo = QtGui.QComboBox(FindItemForm)
        self.typeCombo.setGeometry(QtCore.QRect(64, 11, 200, 25))
        self.typeCombo.setMinimumSize(QtCore.QSize(200, 25))
        self.typeCombo.setMaximumSize(QtCore.QSize(200, 25))
        self.typeCombo.setObjectName(_fromUtf8("typeCombo"))
        self.typeCombo.addItem(_fromUtf8(""))
        self.typeCombo.addItem(_fromUtf8(""))
        self.layoutWidget = QtGui.QWidget(FindItemForm)
        self.layoutWidget.setGeometry(QtCore.QRect(560, 10, 88, 178))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.line = QtGui.QFrame(self.layoutWidget)
        self.line.setFrameShape(QtGui.QFrame.VLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.horizontalLayout.addWidget(self.line)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.findButton = QtGui.QPushButton(self.layoutWidget)
        self.findButton.setMinimumSize(QtCore.QSize(0, 30))
        self.findButton.setMaximumSize(QtCore.QSize(16777215, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/find")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.findButton.setIcon(icon1)
        self.findButton.setIconSize(QtCore.QSize(20, 20))
        self.findButton.setObjectName(_fromUtf8("findButton"))
        self.verticalLayout.addWidget(self.findButton)
        self.clearButton = QtGui.QPushButton(self.layoutWidget)
        self.clearButton.setMinimumSize(QtCore.QSize(0, 30))
        self.clearButton.setMaximumSize(QtCore.QSize(16777215, 30))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/clear")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearButton.setIcon(icon2)
        self.clearButton.setIconSize(QtCore.QSize(20, 20))
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.verticalLayout.addWidget(self.clearButton)
        self.editButton = QtGui.QPushButton(self.layoutWidget)
        self.editButton.setMinimumSize(QtCore.QSize(0, 30))
        self.editButton.setMaximumSize(QtCore.QSize(16777215, 30))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/edit")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editButton.setIcon(icon3)
        self.editButton.setIconSize(QtCore.QSize(20, 20))
        self.editButton.setObjectName(_fromUtf8("editButton"))
        self.verticalLayout.addWidget(self.editButton)
        self.reportButton = QtGui.QPushButton(self.layoutWidget)
        self.reportButton.setMinimumSize(QtCore.QSize(0, 30))
        self.reportButton.setMaximumSize(QtCore.QSize(16777215, 30))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/report")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reportButton.setIcon(icon4)
        self.reportButton.setIconSize(QtCore.QSize(20, 20))
        self.reportButton.setObjectName(_fromUtf8("reportButton"))
        self.verticalLayout.addWidget(self.reportButton)
        self.closeButton = QtGui.QPushButton(self.layoutWidget)
        self.closeButton.setMinimumSize(QtCore.QSize(0, 30))
        self.closeButton.setMaximumSize(QtCore.QSize(16777215, 30))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/exit")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon5)
        self.closeButton.setIconSize(QtCore.QSize(20, 20))
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.verticalLayout.addWidget(self.closeButton)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.frame_2 = QtGui.QFrame(FindItemForm)
        self.frame_2.setGeometry(QtCore.QRect(9, 57, 544, 130))
        self.frame_2.setFrameShape(QtGui.QFrame.Box)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.packLabel = QtGui.QLabel(self.frame_2)
        self.packLabel.setGeometry(QtCore.QRect(389, 90, 34, 16))
        self.packLabel.setObjectName(_fromUtf8("packLabel"))
        self.itemNumLineedit = QtGui.QLineEdit(self.frame_2)
        self.itemNumLineedit.setGeometry(QtCore.QRect(68, 90, 100, 25))
        self.itemNumLineedit.setMinimumSize(QtCore.QSize(100, 25))
        self.itemNumLineedit.setMaximumSize(QtCore.QSize(100, 25))
        self.itemNumLineedit.setObjectName(_fromUtf8("itemNumLineedit"))
        self.itemNumLabel = QtGui.QLabel(self.frame_2)
        self.itemNumLabel.setGeometry(QtCore.QRect(9, 90, 51, 16))
        self.itemNumLabel.setObjectName(_fromUtf8("itemNumLabel"))
        self.volumeLabel = QtGui.QLabel(self.frame_2)
        self.volumeLabel.setGeometry(QtCore.QRect(389, 49, 33, 16))
        self.volumeLabel.setObjectName(_fromUtf8("volumeLabel"))
        self.inactiveCheckbox = QtGui.QCheckBox(self.frame_2)
        self.inactiveCheckbox.setGeometry(QtCore.QRect(429, 15, 91, 25))
        self.inactiveCheckbox.setMinimumSize(QtCore.QSize(0, 25))
        self.inactiveCheckbox.setMaximumSize(QtCore.QSize(16777215, 25))
        self.inactiveCheckbox.setObjectName(_fromUtf8("inactiveCheckbox"))
        self.sup_comb = QtGui.QComboBox(self.frame_2)
        self.sup_comb.setGeometry(QtCore.QRect(68, 49, 285, 25))
        self.sup_comb.setMinimumSize(QtCore.QSize(285, 25))
        self.sup_comb.setMaximumSize(QtCore.QSize(285, 25))
        self.sup_comb.setObjectName(_fromUtf8("sup_comb"))
        self.supplierNoLineedit = QtGui.QLineEdit(self.frame_2)
        self.supplierNoLineedit.setGeometry(QtCore.QRect(251, 90, 100, 25))
        self.supplierNoLineedit.setMinimumSize(QtCore.QSize(100, 25))
        self.supplierNoLineedit.setMaximumSize(QtCore.QSize(100, 25))
        self.supplierNoLineedit.setObjectName(_fromUtf8("supplierNoLineedit"))
        self.supplierNumLabel = QtGui.QLabel(self.frame_2)
        self.supplierNumLabel.setGeometry(QtCore.QRect(174, 90, 71, 16))
        self.supplierNumLabel.setObjectName(_fromUtf8("supplierNumLabel"))
        self.descLineedit = QtGui.QLineEdit(self.frame_2)
        self.descLineedit.setGeometry(QtCore.QRect(68, 15, 285, 25))
        self.descLineedit.setMinimumSize(QtCore.QSize(285, 25))
        self.descLineedit.setMaximumSize(QtCore.QSize(285, 25))
        self.descLineedit.setObjectName(_fromUtf8("descLineedit"))
        self.supplierLabel = QtGui.QLabel(self.frame_2)
        self.supplierLabel.setGeometry(QtCore.QRect(9, 49, 53, 16))
        self.supplierLabel.setObjectName(_fromUtf8("supplierLabel"))
        self.volumeLineedit = QtGui.QLineEdit(self.frame_2)
        self.volumeLineedit.setGeometry(QtCore.QRect(429, 49, 100, 25))
        self.volumeLineedit.setMinimumSize(QtCore.QSize(100, 25))
        self.volumeLineedit.setMaximumSize(QtCore.QSize(100, 25))
        self.volumeLineedit.setObjectName(_fromUtf8("volumeLineedit"))
        self.label_2 = QtGui.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(9, 15, 53, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.packLineedit = QtGui.QLineEdit(self.frame_2)
        self.packLineedit.setGeometry(QtCore.QRect(429, 90, 100, 25))
        self.packLineedit.setMinimumSize(QtCore.QSize(100, 25))
        self.packLineedit.setMaximumSize(QtCore.QSize(100, 25))
        self.packLineedit.setObjectName(_fromUtf8("packLineedit"))
        self.resultsLabel.setBuddy(self.resultsView)
        self.label.setBuddy(self.typeCombo)
        self.packLabel.setBuddy(self.packLineedit)
        self.itemNumLabel.setBuddy(self.itemNumLineedit)
        self.volumeLabel.setBuddy(self.volumeLineedit)
        self.supplierNumLabel.setBuddy(self.supplierNoLineedit)
        self.supplierLabel.setBuddy(self.sup_comb)
        self.label_2.setBuddy(self.descLineedit)

        self.retranslateUi(FindItemForm)
        QtCore.QMetaObject.connectSlotsByName(FindItemForm)
        FindItemForm.setTabOrder(self.typeCombo, self.findButton)
        FindItemForm.setTabOrder(self.findButton, self.editButton)
        FindItemForm.setTabOrder(self.editButton, self.reportButton)
        FindItemForm.setTabOrder(self.reportButton, self.clearButton)
        FindItemForm.setTabOrder(self.clearButton, self.closeButton)
        FindItemForm.setTabOrder(self.closeButton, self.resultsView)

    def retranslateUi(self, FindItemForm):
        FindItemForm.setWindowTitle(_translate("FindItemForm", "Dialog", None))
        self.label.setText(_translate("FindItemForm", "Type          ", None))
        self.typeCombo.setItemText(0, _translate("FindItemForm", "Raw Material", None))
        self.typeCombo.setItemText(1, _translate("FindItemForm", "Finished Good", None))
        self.findButton.setText(_translate("FindItemForm", "&Find", None))
        self.clearButton.setText(_translate("FindItemForm", "C&lear", None))
        self.editButton.setText(_translate("FindItemForm", "&Edit", None))
        self.reportButton.setText(_translate("FindItemForm", "&Report", None))
        self.closeButton.setText(_translate("FindItemForm", "Close", None))
        self.packLabel.setText(_translate("FindItemForm", "Pack    ", None))
        self.itemNumLabel.setText(_translate("FindItemForm", "Item num  ", None))
        self.volumeLabel.setText(_translate("FindItemForm", "Volume", None))
        self.inactiveCheckbox.setText(_translate("FindItemForm", "Show Inactive", None))
        self.supplierNumLabel.setText(_translate("FindItemForm", "   Supplier Num", None))
        self.supplierLabel.setText(_translate("FindItemForm", "Supplier     ", None))
        self.label_2.setText(_translate("FindItemForm", "Description", None))

import images_rc
