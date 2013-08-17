# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'homeform.ui'
#
# Created: Tue Jul 09 20:52:17 2013
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

class Ui_homeform(object):
    def setupUi(self, homeform):
        homeform.setObjectName(_fromUtf8("homeform"))
        homeform.resize(569, 458)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/home")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        homeform.setWindowIcon(icon)
        self.verticalLayout_4 = QtGui.QVBoxLayout(homeform)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.frame = QtGui.QFrame(homeform)
        self.frame.setMinimumSize(QtCore.QSize(170, 212))
        self.frame.setFrameShape(QtGui.QFrame.Box)
        self.frame.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.verticalLayout = QtGui.QVBoxLayout(self.frame)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.supplier_pushButton = QtGui.QPushButton(self.frame)
        self.supplier_pushButton.setMinimumSize(QtCore.QSize(144, 50))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/account")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.supplier_pushButton.setIcon(icon1)
        self.supplier_pushButton.setIconSize(QtCore.QSize(50, 50))
        self.supplier_pushButton.setObjectName(_fromUtf8("supplier_pushButton"))
        self.verticalLayout.addWidget(self.supplier_pushButton)
        self.item_pushButton = QtGui.QPushButton(self.frame)
        self.item_pushButton.setMinimumSize(QtCore.QSize(144, 50))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/item")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.item_pushButton.setIcon(icon2)
        self.item_pushButton.setIconSize(QtCore.QSize(50, 50))
        self.item_pushButton.setObjectName(_fromUtf8("item_pushButton"))
        self.verticalLayout.addWidget(self.item_pushButton)
        self.receive_pushButton = QtGui.QPushButton(self.frame)
        self.receive_pushButton.setMinimumSize(QtCore.QSize(144, 50))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/inventory")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.receive_pushButton.setIcon(icon3)
        self.receive_pushButton.setIconSize(QtCore.QSize(50, 50))
        self.receive_pushButton.setObjectName(_fromUtf8("receive_pushButton"))
        self.verticalLayout.addWidget(self.receive_pushButton)
        self.horizontalLayout.addWidget(self.frame)
        self.frame_2 = QtGui.QFrame(homeform)
        self.frame_2.setMinimumSize(QtCore.QSize(170, 212))
        self.frame_2.setFrameShape(QtGui.QFrame.Box)
        self.frame_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.frame_2)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.batch_pushButton = QtGui.QPushButton(self.frame_2)
        self.batch_pushButton.setMinimumSize(QtCore.QSize(144, 50))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/batch")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.batch_pushButton.setIcon(icon4)
        self.batch_pushButton.setIconSize(QtCore.QSize(50, 50))
        self.batch_pushButton.setObjectName(_fromUtf8("batch_pushButton"))
        self.verticalLayout_2.addWidget(self.batch_pushButton)
        self.production_pushButton = QtGui.QPushButton(self.frame_2)
        self.production_pushButton.setMinimumSize(QtCore.QSize(144, 50))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/production")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.production_pushButton.setIcon(icon5)
        self.production_pushButton.setIconSize(QtCore.QSize(50, 50))
        self.production_pushButton.setObjectName(_fromUtf8("production_pushButton"))
        self.verticalLayout_2.addWidget(self.production_pushButton)
        self.adj_pushButton = QtGui.QPushButton(self.frame_2)
        self.adj_pushButton.setMinimumSize(QtCore.QSize(144, 50))
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/journal")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.adj_pushButton.setIcon(icon6)
        self.adj_pushButton.setIconSize(QtCore.QSize(50, 50))
        self.adj_pushButton.setObjectName(_fromUtf8("adj_pushButton"))
        self.verticalLayout_2.addWidget(self.adj_pushButton)
        self.horizontalLayout.addWidget(self.frame_2)
        self.frame_3 = QtGui.QFrame(homeform)
        self.frame_3.setMinimumSize(QtCore.QSize(170, 212))
        self.frame_3.setFrameShape(QtGui.QFrame.Box)
        self.frame_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.frame_3.setObjectName(_fromUtf8("frame_3"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.frame_3)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout.addWidget(self.frame_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.tableView = QtGui.QTableView(homeform)
        self.tableView.setObjectName(_fromUtf8("tableView"))
        self.verticalLayout_4.addWidget(self.tableView)

        self.retranslateUi(homeform)
        QtCore.QMetaObject.connectSlotsByName(homeform)

    def retranslateUi(self, homeform):
        homeform.setWindowTitle(_translate("homeform", "Home", None))
        self.supplier_pushButton.setText(_translate("homeform", "New Supplier", None))
        self.item_pushButton.setText(_translate("homeform", "New Item", None))
        self.receive_pushButton.setText(_translate("homeform", "Receive Inventory", None))
        self.batch_pushButton.setText(_translate("homeform", "Prepare Batch", None))
        self.production_pushButton.setText(_translate("homeform", "Record Production", None))
        self.adj_pushButton.setText(_translate("homeform", "Adjust Inventory", None))

import images_rc
