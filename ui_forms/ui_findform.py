# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'findform.ui'
#
# Created: Sun Jul 07 15:54:00 2013
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

class Ui_FindForm(object):
    def setupUi(self, FindForm):
        FindForm.setObjectName(_fromUtf8("FindForm"))
        FindForm.resize(702, 592)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/search")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FindForm.setWindowIcon(icon)
        self.frame = QtGui.QFrame(FindForm)
        self.frame.setGeometry(QtCore.QRect(0, 50, 711, 37))
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
        self.clearButton = QtGui.QPushButton(self.frame)
        self.clearButton.setGeometry(QtCore.QRect(111, 5, 90, 27))
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
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/clear")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.clearButton.setIcon(icon1)
        self.clearButton.setIconSize(QtCore.QSize(20, 20))
        self.clearButton.setFlat(False)
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.findButton = QtGui.QPushButton(self.frame)
        self.findButton.setGeometry(QtCore.QRect(15, 5, 90, 27))
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
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/find")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.findButton.setIcon(icon2)
        self.findButton.setIconSize(QtCore.QSize(20, 20))
        self.findButton.setFlat(False)
        self.findButton.setObjectName(_fromUtf8("findButton"))
        self.reportButton = QtGui.QPushButton(self.frame)
        self.reportButton.setGeometry(QtCore.QRect(303, 5, 90, 27))
        self.reportButton.setMinimumSize(QtCore.QSize(90, 0))
        self.reportButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.reportButton.setStyleSheet(_fromUtf8("QPushButton {\n"
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
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/report")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.reportButton.setIcon(icon3)
        self.reportButton.setIconSize(QtCore.QSize(20, 20))
        self.reportButton.setFlat(False)
        self.reportButton.setObjectName(_fromUtf8("reportButton"))
        self.editButton = QtGui.QPushButton(self.frame)
        self.editButton.setGeometry(QtCore.QRect(207, 5, 90, 27))
        self.editButton.setMinimumSize(QtCore.QSize(90, 0))
        self.editButton.setMaximumSize(QtCore.QSize(90, 16777215))
        self.editButton.setStyleSheet(_fromUtf8("QPushButton {\n"
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
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/edit")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.editButton.setIcon(icon4)
        self.editButton.setIconSize(QtCore.QSize(20, 20))
        self.editButton.setFlat(False)
        self.editButton.setObjectName(_fromUtf8("editButton"))
        self.closeButton = QtGui.QPushButton(self.frame)
        self.closeButton.setGeometry(QtCore.QRect(399, 5, 90, 27))
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
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/exit")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.closeButton.setIcon(icon5)
        self.closeButton.setIconSize(QtCore.QSize(20, 20))
        self.closeButton.setFlat(False)
        self.closeButton.setObjectName(_fromUtf8("closeButton"))
        self.label_2 = QtGui.QLabel(FindForm)
        self.label_2.setGeometry(QtCore.QRect(85, 8, 259, 32))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(20)
        font.setBold(True)
        font.setItalic(True)
        font.setUnderline(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.tabWidget = QtGui.QTabWidget(FindForm)
        self.tabWidget.setGeometry(QtCore.QRect(10, 93, 680, 229))
        self.tabWidget.setAutoFillBackground(True)
        self.tabWidget.setStyleSheet(_fromUtf8(""))
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.standard_tab = QtGui.QWidget()
        self.standard_tab.setObjectName(_fromUtf8("standard_tab"))
        self.layoutWidget = QtGui.QWidget(self.standard_tab)
        self.layoutWidget.setGeometry(QtCore.QRect(18, 12, 290, 186))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 0, 0, 1, 1)
        self.journal_combo = QtGui.QComboBox(self.layoutWidget)
        self.journal_combo.setMinimumSize(QtCore.QSize(96, 25))
        self.journal_combo.setMaximumSize(QtCore.QSize(96, 25))
        self.journal_combo.setEditable(False)
        self.journal_combo.setObjectName(_fromUtf8("journal_combo"))
        self.gridLayout.addWidget(self.journal_combo, 0, 1, 1, 1)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 0, 1, 1)
        self.number_lineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.number_lineEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.number_lineEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.number_lineEdit.setObjectName(_fromUtf8("number_lineEdit"))
        self.gridLayout.addWidget(self.number_lineEdit, 1, 1, 1, 1)
        self.supplier_label = QtGui.QLabel(self.layoutWidget)
        self.supplier_label.setObjectName(_fromUtf8("supplier_label"))
        self.gridLayout.addWidget(self.supplier_label, 2, 0, 1, 1)
        self.supCom = QtGui.QComboBox(self.layoutWidget)
        self.supCom.setMinimumSize(QtCore.QSize(218, 25))
        self.supCom.setMaximumSize(QtCore.QSize(218, 25))
        self.supCom.setEditable(True)
        self.supCom.setInsertPolicy(QtGui.QComboBox.NoInsert)
        self.supCom.setObjectName(_fromUtf8("supCom"))
        self.gridLayout.addWidget(self.supCom, 2, 1, 1, 2)
        self.amount_label = QtGui.QLabel(self.layoutWidget)
        self.amount_label.setObjectName(_fromUtf8("amount_label"))
        self.gridLayout.addWidget(self.amount_label, 3, 0, 1, 1)
        self.amountLow_lineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.amountLow_lineEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.amountLow_lineEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.amountLow_lineEdit.setObjectName(_fromUtf8("amountLow_lineEdit"))
        self.gridLayout.addWidget(self.amountLow_lineEdit, 3, 1, 1, 1)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.amount_and_label = QtGui.QLabel(self.layoutWidget)
        self.amount_and_label.setObjectName(_fromUtf8("amount_and_label"))
        self.horizontalLayout_2.addWidget(self.amount_and_label)
        self.amountHi_lineEdit = QtGui.QLineEdit(self.layoutWidget)
        self.amountHi_lineEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.amountHi_lineEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.amountHi_lineEdit.setObjectName(_fromUtf8("amountHi_lineEdit"))
        self.horizontalLayout_2.addWidget(self.amountHi_lineEdit)
        self.gridLayout.addLayout(self.horizontalLayout_2, 3, 2, 1, 1)
        self.label_8 = QtGui.QLabel(self.layoutWidget)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 4, 0, 1, 1)
        self.dtcom = QtGui.QComboBox(self.layoutWidget)
        self.dtcom.setMinimumSize(QtCore.QSize(96, 25))
        self.dtcom.setMaximumSize(QtCore.QSize(96, 25))
        self.dtcom.setEditable(False)
        self.dtcom.setObjectName(_fromUtf8("dtcom"))
        self.gridLayout.addWidget(self.dtcom, 4, 1, 1, 1)
        self.label_9 = QtGui.QLabel(self.layoutWidget)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 5, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_10 = QtGui.QLabel(self.layoutWidget)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.horizontalLayout.addWidget(self.label_10)
        self.dateHi_dateEdit = QtGui.QDateEdit(self.layoutWidget)
        self.dateHi_dateEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.dateHi_dateEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.dateHi_dateEdit.setCalendarPopup(True)
        self.dateHi_dateEdit.setObjectName(_fromUtf8("dateHi_dateEdit"))
        self.horizontalLayout.addWidget(self.dateHi_dateEdit)
        self.gridLayout.addLayout(self.horizontalLayout, 5, 2, 1, 1)
        self.dateLow_dateEdit = QtGui.QDateEdit(self.layoutWidget)
        self.dateLow_dateEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.dateLow_dateEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.dateLow_dateEdit.setCalendarPopup(True)
        self.dateLow_dateEdit.setObjectName(_fromUtf8("dateLow_dateEdit"))
        self.gridLayout.addWidget(self.dateLow_dateEdit, 5, 1, 1, 1)
        self.tabWidget.addTab(self.standard_tab, _fromUtf8(""))
        self.detail_tab = QtGui.QWidget()
        self.detail_tab.setObjectName(_fromUtf8("detail_tab"))
        self.layoutWidget1 = QtGui.QWidget(self.detail_tab)
        self.layoutWidget1.setGeometry(QtCore.QRect(9, 10, 654, 192))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.horizontalLayout_3 = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_3.setMargin(0)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.verticalLayout_9 = QtGui.QVBoxLayout()
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.label_45 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Calibri"))
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_45.setFont(font)
        self.label_45.setAlignment(QtCore.Qt.AlignCenter)
        self.label_45.setObjectName(_fromUtf8("label_45"))
        self.verticalLayout_9.addWidget(self.label_45)
        self.criteriaList_listWidget = QtGui.QListWidget(self.layoutWidget1)
        self.criteriaList_listWidget.setObjectName(_fromUtf8("criteriaList_listWidget"))
        self.verticalLayout_9.addWidget(self.criteriaList_listWidget)
        self.horizontalLayout_3.addLayout(self.verticalLayout_9)
        self.filter_stackedWidget = QtGui.QStackedWidget(self.layoutWidget1)
        self.filter_stackedWidget.setMinimumSize(QtCore.QSize(280, 182))
        self.filter_stackedWidget.setMaximumSize(QtCore.QSize(280, 182))
        self.filter_stackedWidget.setAutoFillBackground(False)
        self.filter_stackedWidget.setFrameShape(QtGui.QFrame.NoFrame)
        self.filter_stackedWidget.setObjectName(_fromUtf8("filter_stackedWidget"))
        self.journalNumber_page = QtGui.QWidget()
        self.journalNumber_page.setObjectName(_fromUtf8("journalNumber_page"))
        self.layoutWidget2 = QtGui.QWidget(self.journalNumber_page)
        self.layoutWidget2.setGeometry(QtCore.QRect(66, 49, 142, 77))
        self.layoutWidget2.setObjectName(_fromUtf8("layoutWidget2"))
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget2)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.label_6 = QtGui.QLabel(self.layoutWidget2)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout_2.addWidget(self.label_6, 1, 0, 1, 1)
        self.journalRef_lineEdit = QtGui.QLineEdit(self.layoutWidget2)
        self.journalRef_lineEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.journalRef_lineEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.journalRef_lineEdit.setObjectName(_fromUtf8("journalRef_lineEdit"))
        self.gridLayout_2.addWidget(self.journalRef_lineEdit, 1, 1, 1, 1)
        self.label = QtGui.QLabel(self.layoutWidget2)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 2)
        self.filter_stackedWidget.addWidget(self.journalNumber_page)
        self.journalID_page = QtGui.QWidget()
        self.journalID_page.setObjectName(_fromUtf8("journalID_page"))
        self.layoutWidget3 = QtGui.QWidget(self.journalID_page)
        self.layoutWidget3.setGeometry(QtCore.QRect(66, 49, 142, 77))
        self.layoutWidget3.setObjectName(_fromUtf8("layoutWidget3"))
        self.gridLayout_3 = QtGui.QGridLayout(self.layoutWidget3)
        self.gridLayout_3.setMargin(0)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_13 = QtGui.QLabel(self.layoutWidget3)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout_3.addWidget(self.label_13, 0, 0, 1, 2)
        self.label_14 = QtGui.QLabel(self.layoutWidget3)
        self.label_14.setObjectName(_fromUtf8("label_14"))
        self.gridLayout_3.addWidget(self.label_14, 1, 0, 1, 1)
        self.journalStart_lineEdit = QtGui.QLineEdit(self.layoutWidget3)
        self.journalStart_lineEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.journalStart_lineEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.journalStart_lineEdit.setObjectName(_fromUtf8("journalStart_lineEdit"))
        self.gridLayout_3.addWidget(self.journalStart_lineEdit, 1, 1, 1, 1)
        self.label_15 = QtGui.QLabel(self.layoutWidget3)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_3.addWidget(self.label_15, 2, 0, 1, 1)
        self.journalEnd_lineEdit = QtGui.QLineEdit(self.layoutWidget3)
        self.journalEnd_lineEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.journalEnd_lineEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.journalEnd_lineEdit.setObjectName(_fromUtf8("journalEnd_lineEdit"))
        self.gridLayout_3.addWidget(self.journalEnd_lineEdit, 2, 1, 1, 1)
        self.filter_stackedWidget.addWidget(self.journalID_page)
        self.supplier_page = QtGui.QWidget()
        self.supplier_page.setObjectName(_fromUtf8("supplier_page"))
        self.layoutWidget_11 = QtGui.QWidget(self.supplier_page)
        self.layoutWidget_11.setGeometry(QtCore.QRect(20, 7, 235, 165))
        self.layoutWidget_11.setObjectName(_fromUtf8("layoutWidget_11"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget_11)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_46 = QtGui.QLabel(self.layoutWidget_11)
        self.label_46.setObjectName(_fromUtf8("label_46"))
        self.verticalLayout_2.addWidget(self.label_46)
        self.supplierFilter_tableView = QtGui.QTableView(self.layoutWidget_11)
        self.supplierFilter_tableView.setObjectName(_fromUtf8("supplierFilter_tableView"))
        self.verticalLayout_2.addWidget(self.supplierFilter_tableView)
        self.filter_stackedWidget.addWidget(self.supplier_page)
        self.item_page = QtGui.QWidget()
        self.item_page.setObjectName(_fromUtf8("item_page"))
        self.layoutWidget4 = QtGui.QWidget(self.item_page)
        self.layoutWidget4.setGeometry(QtCore.QRect(20, 7, 235, 165))
        self.layoutWidget4.setObjectName(_fromUtf8("layoutWidget4"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label_17 = QtGui.QLabel(self.layoutWidget4)
        self.label_17.setObjectName(_fromUtf8("label_17"))
        self.verticalLayout.addWidget(self.label_17)
        self.itemFilter_tableView = QtGui.QTableView(self.layoutWidget4)
        self.itemFilter_tableView.setObjectName(_fromUtf8("itemFilter_tableView"))
        self.verticalLayout.addWidget(self.itemFilter_tableView)
        self.filter_stackedWidget.addWidget(self.item_page)
        self.page = QtGui.QWidget()
        self.page.setObjectName(_fromUtf8("page"))
        self.layoutWidget5 = QtGui.QWidget(self.page)
        self.layoutWidget5.setGeometry(QtCore.QRect(32, 65, 213, 46))
        self.layoutWidget5.setObjectName(_fromUtf8("layoutWidget5"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.layoutWidget5)
        self.verticalLayout_7.setMargin(0)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.label_44 = QtGui.QLabel(self.layoutWidget5)
        self.label_44.setObjectName(_fromUtf8("label_44"))
        self.verticalLayout_7.addWidget(self.label_44)
        self.itemDesc_lineEdit = QtGui.QLineEdit(self.layoutWidget5)
        self.itemDesc_lineEdit.setMinimumSize(QtCore.QSize(0, 25))
        self.itemDesc_lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.itemDesc_lineEdit.setObjectName(_fromUtf8("itemDesc_lineEdit"))
        self.verticalLayout_7.addWidget(self.itemDesc_lineEdit)
        self.filter_stackedWidget.addWidget(self.page)
        self.journalType_page = QtGui.QWidget()
        self.journalType_page.setObjectName(_fromUtf8("journalType_page"))
        self.layoutWidget_2 = QtGui.QWidget(self.journalType_page)
        self.layoutWidget_2.setGeometry(QtCore.QRect(19, 62, 235, 46))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label_18 = QtGui.QLabel(self.layoutWidget_2)
        self.label_18.setObjectName(_fromUtf8("label_18"))
        self.verticalLayout_3.addWidget(self.label_18)
        self.journalFilter_combo = QtGui.QComboBox(self.layoutWidget_2)
        self.journalFilter_combo.setMinimumSize(QtCore.QSize(0, 25))
        self.journalFilter_combo.setMaximumSize(QtCore.QSize(16777215, 25))
        self.journalFilter_combo.setObjectName(_fromUtf8("journalFilter_combo"))
        self.verticalLayout_3.addWidget(self.journalFilter_combo)
        self.filter_stackedWidget.addWidget(self.journalType_page)
        self.itemType_page = QtGui.QWidget()
        self.itemType_page.setObjectName(_fromUtf8("itemType_page"))
        self.itemFilter_groupBox = QtGui.QGroupBox(self.itemType_page)
        self.itemFilter_groupBox.setGeometry(QtCore.QRect(20, 18, 241, 144))
        self.itemFilter_groupBox.setObjectName(_fromUtf8("itemFilter_groupBox"))
        self.rmFilter_checkBox = QtGui.QCheckBox(self.itemFilter_groupBox)
        self.rmFilter_checkBox.setGeometry(QtCore.QRect(47, 35, 151, 17))
        self.rmFilter_checkBox.setObjectName(_fromUtf8("rmFilter_checkBox"))
        self.buttonGroup = QtGui.QButtonGroup(FindForm)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.rmFilter_checkBox)
        self.fgFilter_checkBox = QtGui.QCheckBox(self.itemFilter_groupBox)
        self.fgFilter_checkBox.setGeometry(QtCore.QRect(47, 64, 151, 17))
        self.fgFilter_checkBox.setObjectName(_fromUtf8("fgFilter_checkBox"))
        self.buttonGroup.addButton(self.fgFilter_checkBox)
        self.bothItemTypeFilter_checkBox = QtGui.QCheckBox(self.itemFilter_groupBox)
        self.bothItemTypeFilter_checkBox.setGeometry(QtCore.QRect(47, 94, 151, 17))
        self.bothItemTypeFilter_checkBox.setObjectName(_fromUtf8("bothItemTypeFilter_checkBox"))
        self.buttonGroup.addButton(self.bothItemTypeFilter_checkBox)
        self.filter_stackedWidget.addWidget(self.itemType_page)
        self.date_page = QtGui.QWidget()
        self.date_page.setObjectName(_fromUtf8("date_page"))
        self.layoutWidget6 = QtGui.QWidget(self.date_page)
        self.layoutWidget6.setGeometry(QtCore.QRect(57, 35, 161, 108))
        self.layoutWidget6.setObjectName(_fromUtf8("layoutWidget6"))
        self.gridLayout_7 = QtGui.QGridLayout(self.layoutWidget6)
        self.gridLayout_7.setMargin(0)
        self.gridLayout_7.setObjectName(_fromUtf8("gridLayout_7"))
        self.label_39 = QtGui.QLabel(self.layoutWidget6)
        self.label_39.setObjectName(_fromUtf8("label_39"))
        self.gridLayout_7.addWidget(self.label_39, 0, 0, 1, 2)
        self.label_37 = QtGui.QLabel(self.layoutWidget6)
        self.label_37.setObjectName(_fromUtf8("label_37"))
        self.gridLayout_7.addWidget(self.label_37, 1, 0, 1, 1)
        self.dtfilcom = QtGui.QComboBox(self.layoutWidget6)
        self.dtfilcom.setMinimumSize(QtCore.QSize(96, 25))
        self.dtfilcom.setMaximumSize(QtCore.QSize(96, 25))
        self.dtfilcom.setEditable(False)
        self.dtfilcom.setObjectName(_fromUtf8("dtfilcom"))
        self.gridLayout_7.addWidget(self.dtfilcom, 1, 1, 1, 1)
        self.label_36 = QtGui.QLabel(self.layoutWidget6)
        self.label_36.setObjectName(_fromUtf8("label_36"))
        self.gridLayout_7.addWidget(self.label_36, 2, 0, 1, 1)
        self.dateLowFilter_dateEdit = QtGui.QDateEdit(self.layoutWidget6)
        self.dateLowFilter_dateEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.dateLowFilter_dateEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.dateLowFilter_dateEdit.setCalendarPopup(True)
        self.dateLowFilter_dateEdit.setObjectName(_fromUtf8("dateLowFilter_dateEdit"))
        self.gridLayout_7.addWidget(self.dateLowFilter_dateEdit, 2, 1, 1, 1)
        self.label_38 = QtGui.QLabel(self.layoutWidget6)
        self.label_38.setObjectName(_fromUtf8("label_38"))
        self.gridLayout_7.addWidget(self.label_38, 3, 0, 1, 1)
        self.dateHiFilter_dateEdit = QtGui.QDateEdit(self.layoutWidget6)
        self.dateHiFilter_dateEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.dateHiFilter_dateEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.dateHiFilter_dateEdit.setCalendarPopup(True)
        self.dateHiFilter_dateEdit.setObjectName(_fromUtf8("dateHiFilter_dateEdit"))
        self.gridLayout_7.addWidget(self.dateHiFilter_dateEdit, 3, 1, 1, 1)
        self.filter_stackedWidget.addWidget(self.date_page)
        self.modifiedDate_page = QtGui.QWidget()
        self.modifiedDate_page.setObjectName(_fromUtf8("modifiedDate_page"))
        self.layoutWidget_10 = QtGui.QWidget(self.modifiedDate_page)
        self.layoutWidget_10.setGeometry(QtCore.QRect(57, 35, 161, 108))
        self.layoutWidget_10.setObjectName(_fromUtf8("layoutWidget_10"))
        self.gridLayout_8 = QtGui.QGridLayout(self.layoutWidget_10)
        self.gridLayout_8.setMargin(0)
        self.gridLayout_8.setObjectName(_fromUtf8("gridLayout_8"))
        self.label_40 = QtGui.QLabel(self.layoutWidget_10)
        self.label_40.setObjectName(_fromUtf8("label_40"))
        self.gridLayout_8.addWidget(self.label_40, 0, 0, 1, 2)
        self.label_41 = QtGui.QLabel(self.layoutWidget_10)
        self.label_41.setObjectName(_fromUtf8("label_41"))
        self.gridLayout_8.addWidget(self.label_41, 1, 0, 1, 1)
        self.dtfilcom_2 = QtGui.QComboBox(self.layoutWidget_10)
        self.dtfilcom_2.setMinimumSize(QtCore.QSize(96, 25))
        self.dtfilcom_2.setMaximumSize(QtCore.QSize(96, 25))
        self.dtfilcom_2.setEditable(False)
        self.dtfilcom_2.setObjectName(_fromUtf8("dtfilcom_2"))
        self.gridLayout_8.addWidget(self.dtfilcom_2, 1, 1, 1, 1)
        self.label_42 = QtGui.QLabel(self.layoutWidget_10)
        self.label_42.setObjectName(_fromUtf8("label_42"))
        self.gridLayout_8.addWidget(self.label_42, 2, 0, 1, 1)
        self.modDateLowFilter_dateEdit = QtGui.QDateEdit(self.layoutWidget_10)
        self.modDateLowFilter_dateEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.modDateLowFilter_dateEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.modDateLowFilter_dateEdit.setCalendarPopup(True)
        self.modDateLowFilter_dateEdit.setObjectName(_fromUtf8("modDateLowFilter_dateEdit"))
        self.gridLayout_8.addWidget(self.modDateLowFilter_dateEdit, 2, 1, 1, 1)
        self.label_43 = QtGui.QLabel(self.layoutWidget_10)
        self.label_43.setObjectName(_fromUtf8("label_43"))
        self.gridLayout_8.addWidget(self.label_43, 3, 0, 1, 1)
        self.modDateHiFilter_dateEdit = QtGui.QDateEdit(self.layoutWidget_10)
        self.modDateHiFilter_dateEdit.setMinimumSize(QtCore.QSize(96, 25))
        self.modDateHiFilter_dateEdit.setMaximumSize(QtCore.QSize(96, 25))
        self.modDateHiFilter_dateEdit.setCalendarPopup(True)
        self.modDateHiFilter_dateEdit.setObjectName(_fromUtf8("modDateHiFilter_dateEdit"))
        self.gridLayout_8.addWidget(self.modDateHiFilter_dateEdit, 3, 1, 1, 1)
        self.filter_stackedWidget.addWidget(self.modifiedDate_page)
        self.horizontalLayout_3.addWidget(self.filter_stackedWidget)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.criteria_tableView = QtGui.QTableView(self.layoutWidget1)
        self.criteria_tableView.setMinimumSize(QtCore.QSize(202, 150))
        self.criteria_tableView.setMaximumSize(QtCore.QSize(202, 150))
        self.criteria_tableView.setObjectName(_fromUtf8("criteria_tableView"))
        self.verticalLayout_8.addWidget(self.criteria_tableView)
        self.frame_2 = QtGui.QFrame(self.layoutWidget1)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 32))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 32))
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName(_fromUtf8("frame_2"))
        self.removeFilter_button = QtGui.QPushButton(self.frame_2)
        self.removeFilter_button.setGeometry(QtCore.QRect(56, 4, 90, 23))
        self.removeFilter_button.setMinimumSize(QtCore.QSize(90, 0))
        self.removeFilter_button.setMaximumSize(QtCore.QSize(90, 16777215))
        self.removeFilter_button.setObjectName(_fromUtf8("removeFilter_button"))
        self.verticalLayout_8.addWidget(self.frame_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_8)
        self.tabWidget.addTab(self.detail_tab, _fromUtf8(""))
        self.results_tableView = QtGui.QTableView(FindForm)
        self.results_tableView.setGeometry(QtCore.QRect(10, 332, 679, 217))
        self.results_tableView.setObjectName(_fromUtf8("results_tableView"))
        self.v_results_label = QtGui.QLabel(FindForm)
        self.v_results_label.setGeometry(QtCore.QRect(599, 558, 90, 25))
        self.v_results_label.setMinimumSize(QtCore.QSize(0, 25))
        self.v_results_label.setMaximumSize(QtCore.QSize(192, 25))
        self.v_results_label.setFrameShape(QtGui.QFrame.Box)
        self.v_results_label.setFrameShadow(QtGui.QFrame.Raised)
        self.v_results_label.setText(_fromUtf8(""))
        self.v_results_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.v_results_label.setObjectName(_fromUtf8("v_results_label"))

        self.retranslateUi(FindForm)
        self.tabWidget.setCurrentIndex(0)
        self.filter_stackedWidget.setCurrentIndex(8)
        QtCore.QMetaObject.connectSlotsByName(FindForm)

    def retranslateUi(self, FindForm):
        FindForm.setWindowTitle(_translate("FindForm", "Find Transactions", None))
        self.clearButton.setText(_translate("FindForm", "Clear", None))
        self.findButton.setText(_translate("FindForm", "&Find", None))
        self.reportButton.setText(_translate("FindForm", "Report", None))
        self.editButton.setText(_translate("FindForm", "Edit", None))
        self.closeButton.setText(_translate("FindForm", "Close", None))
        self.label_2.setText(_translate("FindForm", "Find Transactions:", None))
        self.label_3.setText(_translate("FindForm", "Journal", None))
        self.label_5.setText(_translate("FindForm", "Number", None))
        self.supplier_label.setText(_translate("FindForm", "Supplier", None))
        self.amount_label.setText(_translate("FindForm", "Amount", None))
        self.amount_and_label.setText(_translate("FindForm", "And", None))
        self.label_8.setText(_translate("FindForm", "Date Range", None))
        self.label_9.setText(_translate("FindForm", "From", None))
        self.label_10.setText(_translate("FindForm", "To", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.standard_tab), _translate("FindForm", "Standard", None))
        self.label_45.setText(_translate("FindForm", "Criteria List", None))
        self.label_6.setText(_translate("FindForm", "Starting", None))
        self.label.setText(_translate("FindForm", "Enter journal number.", None))
        self.label_13.setText(_translate("FindForm", "Enter journal ID range.", None))
        self.label_14.setText(_translate("FindForm", "Starting", None))
        self.label_15.setText(_translate("FindForm", "Ending", None))
        self.label_46.setText(_translate("FindForm", "Select the suppliers you want to filter by.", None))
        self.label_17.setText(_translate("FindForm", "Select The items you want to filter by.", None))
        self.label_44.setText(_translate("FindForm", "Item description as recorded on journal line.", None))
        self.label_18.setText(_translate("FindForm", "Select journal type, to filter.", None))
        self.itemFilter_groupBox.setTitle(_translate("FindForm", "Item Type", None))
        self.rmFilter_checkBox.setText(_translate("FindForm", "Raw Material item", None))
        self.fgFilter_checkBox.setText(_translate("FindForm", "Finished Good Item", None))
        self.bothItemTypeFilter_checkBox.setText(_translate("FindForm", "Both Item Types", None))
        self.label_39.setText(_translate("FindForm", "Select Date Range", None))
        self.label_37.setText(_translate("FindForm", "Date Range", None))
        self.label_36.setText(_translate("FindForm", "From", None))
        self.label_38.setText(_translate("FindForm", "To", None))
        self.label_40.setText(_translate("FindForm", "Select Modified date Range", None))
        self.label_41.setText(_translate("FindForm", "Date Range", None))
        self.label_42.setText(_translate("FindForm", "From", None))
        self.label_43.setText(_translate("FindForm", "To", None))
        self.removeFilter_button.setText(_translate("FindForm", "Remove filter", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.detail_tab), _translate("FindForm", "Detail", None))

import images_rc
