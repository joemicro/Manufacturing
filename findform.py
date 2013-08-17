import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy import  *
from sqlalchemy.orm import *

from databaseschema import *
from genericdelegates import *
from functions import *
import modelsandviews
import ui_forms.ui_findform
import receiveform
import batchform
import productionform
import inventoryadjform
import reporting

localTITLE = 'Find'
RECEIVE, BATCH, PRODUCTION, ADJUSTMENT, PREP = range(5)
class FilterList(object):
    def __init__(self, filter, criteria, setTo):
        self.filter = filter
        self.criteria = criteria  
        self.setTo = setTo
        
                          
class FilterModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(FilterModel, self).__init__(parent)
        self.records = []
        
    def rowCount(self, index=QModelIndex()):
        return len(self.records)
    
    def columnCount(self, index=QModelIndex()):
        return 3
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.records)):
            return QVariant()
        record = self.records[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == 0:
                return QVariant(record.filter)
            elif column == 1:
                return QVariant(record.criteria)
            elif column == 2:
                return QVariant(record.setTo)
        return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            record = self.records[index.row()]
            column = index.column()
            if column == 0:
                record.filter = value.toString()
            elif column == 1:
                record.criteria = value.toString()
            elif column == 2 :
                record.setTo = value.toString()
            self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True
        return False
    
    def insertRows(self, position, object, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.records.insert(position + row + 1, object)
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.records = self.records[:position] + self.records[position + rows:]
        self.endRemoveRows()
        return True
    
    def getFilterCriteria(self):
        records_ = []
        for rec in self.records:
            crit = rec.filter
            records_ += [str(crit)]
        return records_
            
    def clear(self):
        self.beginResetModel()
        self.items = []
        self.items.append(ItemAssembly())
        self.endResetModel()
 
#==================================================================
### Form setup ==============       
class FindForm(QDialog, ui_forms.ui_findform.Ui_FindForm):
    ### Initializer ==============
    def __init__(self, supplierModel, parent=None):
        super(FindForm, self).__init__(parent)
        self.setupUi(self)
        self.tabWidget.setCurrentIndex(0)
        self.session = Session()
        self.query = None
        self.model = None
        self.reportName = QString()
        self.fieldList = []
        self.columnsToTotal = []
        self.proxyModel = QSortFilterProxyModel()
        self.myParent = parent
        
        ## == Standard tab GUI setup ==
        journalList = QStringList()
        journalList << 'Receive' << 'Batch' << 'Production' << 'Adjustment' << 'Preparation'
        self.journal_combo.addItems(journalList)
        
        self.supCom.setVisible(False)
        self.supplierModel = supplierModel
        self.supplier_combo = modelsandviews.SupplierComboBox(self.supplierModel)
        self.supplier_combo.setMinimumSize(QSize(218, 25))
        self.supplier_combo.setMaximumSize(QSize(218, 25))
        self.gridLayout.addWidget(self.supplier_combo, 2, 1, 1, 2)
        
        self.batchDesc_lineEdit = QLineEdit()
        self.batchDesc_lineEdit.setMinimumSize(QSize(218, 25))
        self.batchDesc_lineEdit.setMaximumSize(QSize(218, 85))
        self.gridLayout.addWidget(self.batchDesc_lineEdit, 2, 1, 1, 2)
        self.batchDesc_lineEdit.setVisible(False)
        
        validator = QDoubleValidator()
        validator.StandardNotation
        self.amountHi_lineEdit.setValidator(validator)
        self.amountLow_lineEdit.setValidator(validator)
        
        self.dtcom.setVisible(False)
        self.dateRange_combo = modelsandviews.DateRangeComboBox(self.layoutWidget)
        self.dateRange_combo.setCurrentIndex(0)
        self.dateRange_combo.setMinimumSize(QSize(96, 25))
        self.dateRange_combo.setMaximumSize(QSize(96, 25))
        self.gridLayout.addWidget(self.dateRange_combo, 4, 1, 1, 1)
        self.dateLow_dateEdit.setDate(QDate.currentDate())
        self.dateHi_dateEdit.setDate(QDate.currentDate())
        
        self.results_tableView.setSelectionMode(QTableView.SingleSelection)
        self.results_tableView.setSelectionBehavior(QTableView.SelectRows)
        
        ## == Detail tab GUI setup ==
        self.filter_stackedWidget.setCurrentIndex(0)
        crtList = QStringList()
        crtList << 'Journal Number' << 'Journal ID' << 'Supplier' << 'Items' << 'Description' << 'Journal Type' \
        << 'Item Type' << 'Date' << 'Date Modified'
        crtView = self.criteriaList_listWidget
        crtView.addItems(crtList)
        crtView.setEditTriggers(QListView.NoEditTriggers)
        
        self.filterModel = FilterModel()
        fltView = self.criteria_tableView
        fltView.setModel(self.filterModel)
        fltView.hideColumn(0)
        fltView.horizontalHeader().setStretchLastSection(True)
        fltView.horizontalHeader().setVisible(False)
        fltView.verticalHeader().setVisible(False)
        fltView.setSelectionMode(QTableView.SingleSelection)
        fltView.setSelectionBehavior(QTableView.SelectRows)
        fltView.resizeColumnsToContents()
        
        self.dateLowFilter_dateEdit.setDate(QDate.currentDate())
        self.dateHiFilter_dateEdit.setDate(QDate.currentDate())
        self.modDateLowFilter_dateEdit.setDate(QDate.currentDate())
        self.modDateHiFilter_dateEdit.setDate(QDate.currentDate())
                                                                                  
        ## == stackWidget items setup ==
        self.journalStart_lineEdit.setValidator(validator)
        self.journalEnd_lineEdit.setValidator(validator)
        
        self.supplier_list = modelsandviews.SupplierListModel()
        self.supplierFilter_tableView.setModel(self.supplier_list)
        supplier_view = self.supplierFilter_tableView
        supplier_view.hideColumn(1)
        supplier_view.setColumnWidth(0, 25)
        supplier_view.verticalHeader().setVisible(False)
        supplier_view.setSelectionMode(QTableView.SingleSelection)
        supplier_view.setSelectionBehavior(QTableView.SelectRows)
        
        self.ItemList = modelsandviews.UnionItemListModel()
        itemView = self.itemFilter_tableView
        itemView.setModel(self.ItemList)
        itemView.hideColumn(1)
        itemView.verticalHeader().setVisible(False)
        itemView.setSelectionMode(QTableView.SingleSelection)
        itemView.setSelectionBehavior(QTableView.SelectRows)
        itemView.resizeColumnsToContents()
        
        
        self.journalFilter_combo.addItems(journalList)
        self.journalFilter_combo.removeItem(1)
        self.journalFilter_combo.setCurrentIndex(-1)
        
        self.bothItemTypeFilter_checkBox.setChecked(True)
        
        self.dtfilcom.setVisible(False)
        self.dateFilter_combo = modelsandviews.DateRangeComboBox(self.layoutWidget6)
        self.dateFilter_combo.setMinimumSize(QSize(96, 25))
        self.dateFilter_combo.setMaximumSize(QSize(96, 25))
        self.gridLayout_7.addWidget(self.dateFilter_combo, 1, 1, 1, 1)
        self.dtfilcom_2.setVisible(False)
        self.modfiedDateFilter_combo = modelsandviews.DateRangeComboBox(self.layoutWidget_10)
        self.modfiedDateFilter_combo.setMinimumSize(QSize(96, 25))
        self.modfiedDateFilter_combo.setMaximumSize(QSize(96, 25))
        self.gridLayout_8.addWidget(self.modfiedDateFilter_combo, 1, 1, 1, 1)
        
        self.amountLow_lineEdit.editingFinished.connect(self.standardAmount)
        self.amountHi_lineEdit.editingFinished.connect(self.standardAmount)
        self.dateRange_combo.currentIndexChanged.connect(lambda: 
                                                          self.dateRangeSelection(self.dateRange_combo, 
                                                                                  self.dateLow_dateEdit, 
                                                                                  self.dateHi_dateEdit))
        self.dateFilter_combo.currentIndexChanged.connect(lambda: 
                                                          self.dateRangeSelection(self.dateFilter_combo, 
                                                                                  self.dateLowFilter_dateEdit, 
                                                                                  self.dateHiFilter_dateEdit))
        self.modfiedDateFilter_combo.currentIndexChanged.connect(lambda: 
                                                          self.dateRangeSelection(self.modfiedDateFilter_combo, 
                                                                                  self.modDateLowFilter_dateEdit, 
                                                                                  self.modDateHiFilter_dateEdit))
        self.connect(crtView, SIGNAL('currentRowChanged(int)'),
                     self.filter_stackedWidget, SLOT('setCurrentIndex(int)'))
        self.journal_combo.currentIndexChanged.connect(self.layoutChange)
        self.findButton.clicked.connect(self.find)
        self.editButton.clicked.connect(self.edit)
        self.results_tableView.doubleClicked.connect(self.edit)
        self.reportButton.clicked.connect(self.printReport)
        self.clearButton.clicked.connect(self.clear)
        self.closeButton.clicked.connect(self.reject)
        
        ## == Setup stackedWidget operations == 
        self.journalRef_lineEdit.editingFinished.connect(self.journalNum)
        self.journalStart_lineEdit.editingFinished.connect(self.journalIDRange)
        self.journalEnd_lineEdit.editingFinished.connect(self.journalIDRange)
        self.itemDesc_lineEdit.editingFinished.connect(self.itemDesc)
        self.journalFilter_combo.currentIndexChanged.connect(self.journalType)
        self.rmFilter_checkBox.stateChanged.connect(self.itemType)
        self.fgFilter_checkBox.stateChanged.connect(self.itemType)
        self.dateLowFilter_dateEdit.dateChanged.connect(self.dateRange)
        self.dateHiFilter_dateEdit.dateChanged.connect(self.dateRange)
        self.modDateLowFilter_dateEdit.dateChanged.connect(self.modDateRange)
        self.modDateHiFilter_dateEdit.dateChanged.connect(self.modDateRange)
        
        self.removeFilter_button.clicked.connect(self.removeFilter)
        itemView.clicked.connect(self.checkItem)
        supplier_view.clicked.connect(self.checkItem)
        
        self.setWindowTitle(localTITLE)
        
    def reject(self):
        QDialog.reject(self)
        self.myParent.formClosed()
        
    def standardAmount(self):
        amount_low = str(self.amountLow_lineEdit.text())
        amount_hi = str(self.amountHi_lineEdit.text())
        if not amount_low:
            return
        amount_low = float(amount_low)
        if not amount_hi:
            return
        amount_hi = float(amount_hi)
        if amount_hi < amount_low:
            self.amountLow_lineEdit.setText(str(amount_hi))
            self.amountHi_lineEdit.setText(str(amount_low))
        
    def standardDate(self):
        fromDate = self.dateLow_dateEdit.date()
        fromDate = fromDate.toPyDate()
        toDate = self.dateHi_dateEdit.date()
        toDate = toDate.toPyDate()
        if toDate < fromDate:
            self.dateLow_dateEdit.setDate(toDate)
            self.dateHi_dateEdit.setDate(fromDate)
    
    ## == setup detail filter function calls
    def checkItem(self, index):
        model = self.supplier_list
        if self.sender() == self.itemFilter_tableView:
            model = self.ItemList
        row = index.row()
        i = model.index(row, 0)
        if index.model().data(i, Qt.DisplayRole).toString() != 'P':
            model.setData(i, QVariant('P'), role=Qt.EditRole)
        else:
            model.setData(i, QVariant(), role=Qt.EditRole)
    
    def removeFilter(self):
        row = self.criteria_tableView.currentIndex().row()
        self.filterModel.removeRows(row)
            
    def dateRangeSelection(self, rangeCombo, dateFrom, dateTo):
        dateFrom.blockSignals(True)
        dateTo.blockSignals(True)
        selection = rangeCombo.currentText()
        date_from, date_to = dateRange(selection)
        dateFrom.setDate(date_from)
        dateTo.setDate(date_to)
        dateFrom.blockSignals(False)
        dateTo.blockSignals(False)
        dateFrom.emit(SIGNAL('dateChanged(QDate)'), date_from)
        dateTo.emit(SIGNAL('dateChanged(QDate)'), date_to)
        
    def journalNum(self):
        fType = 'Journal Num'
        start = str(self.journalRef_lineEdit.text())
        self.updateFilterModel(fType, 'JournalHeader.journal_no==%s' % start, start)
        
    def journalIDRange(self):
        fType = 'Journal ID'
        start = str(self.journalStart_lineEdit.text())
        if not start:
            return
        start = int(start)
        end  = str(self.journalEnd_lineEdit.text())
        if not end:
            return
        end = int(end)
        if end < start:
            self.journalStart_lineEdit.setText(str(end))
            self.journalEnd_lineEdit.setText(str(start))
            self.journalIDRange()
            return
        self.updateFilterModel(fType, 'JournalHeader.journal_id.between(%i,%i)' % (start, end), 'Between(%i,%i)' % (start, end))
    
    def itemDesc(self):
        fType = 'Item Description'
        desc = str(self.itemDesc_lineEdit.text())
        self.updateFilterModel(fType, 'unionQuery.c.itemDesc.ilike("%%%s%%"))' % (desc, desc), desc)
        
    def journalType(self):
        fType = 'Journal Type'
        jType = str(self.journalFilter_combo.currentText())
        crit = 'JournalHeader.journal_type=="%s"' % jType
        if jType == 'Receive':
            crit = 'or_(JournalHeader.journal_type=="Bill", JournalHeader.journal_type=="Credit")'
        self.updateFilterModel(fType, crit, jType)
        
    def itemType(self):
        fType = 'Item Type'
        rmdType = self.rmFilter_checkBox.isChecked()
        fgdType = self.fgFilter_checkBox.isChecked()
        if rmdType == 1:
            self.updateFilterModel(fType, 'unionQuery.c.itemType=="RMD"', 'Raw Materials')
        elif fgdType == 1:
            self.updateFilterModel(fType, 'unionQuery.c.itemType=="FGD"', 'Finished Goods')
        
    def dateRange(self):
        fType = 'Date range'
        fromDate = self.dateLowFilter_dateEdit.date()
        fromDate = fromDate.toPyDate()
        toDate = self.dateHiFilter_dateEdit.date()
        toDate = toDate.toPyDate()
        if toDate < fromDate:
            self.dateLowFilter_dateEdit.setDate(toDate)
            self.dateHiFilter_dateEdit.setDate(fromDate)
            self.dateRange()
            return
        self.updateFilterModel(fType, 'JournalHeader.journal_date.between("%s", "%s")' % (fromDate, toDate), 
                               'Between(%s, %s)' % (fromDate, toDate))
        
    def modDateRange(self):
        fType = 'Modified Range'
        fromDate = self.modDateLowFilter_dateEdit.date()
        fromDate = fromDate.toPyDate()
        toDate = self.modDateHiFilter_dateEdit.date()
        toDate = toDate.toPyDate()
        if toDate < fromDate:
            self.modDateLowFilter_dateEdit.setDate(toDate)
            self.modDateHiFilter_dateEdit.setDate(fromDate)
            self.modDateRange()
            return
        self.updateFilterModel(fType, 'JournalHeader.modified_date.between("%s", "%s")' % (fromDate, toDate), 
                               'Between(%s, %s)' % (fromDate, toDate))
            
    def updateFilterModel(self, fType, filter, setTo):
        index = self.filterModel.index(0, 1)
        m = self.filterModel.match(index, Qt.DisplayRole, QVariant(fType), 1)
        if len(m) <= 0:
            position = self.ItemList.rowCount() + 1
            self.filterModel.insertRows(position, FilterList(QString(filter), QString(fType), QString(setTo)))
            
        else:
            for i in m:
                row = i.row()
            index = self.filterModel.index(row, 0)
            self.filterModel.setData(index, QVariant(filter), Qt.EditRole)
            index = self.filterModel.index(row, 2)
            self.filterModel.setData(index, QVariant(setTo), Qt.EditRole)
            
        self.criteria_tableView.resizeColumnsToContents()
        
    
    ## == Form layout setup
    def layoutChange(self):
        jType = self.journal_combo.currentIndex()
        if jType == RECEIVE:
            self.supplier_combo.setVisible(True)
            self.supplier_label.setVisible(True)
            self.amount_label.setVisible(True)
            self.amountLow_lineEdit.setVisible(True)
            self.amount_and_label.setVisible(True)
            self.amountHi_lineEdit.setVisible(True)
            self.batchDesc_lineEdit.setVisible(False)
            self.supplier_label.setText('Supplier')
        elif jType == BATCH:
            self.supplier_combo.setVisible(False)
            self.amount_label.setVisible(False)
            self.amountLow_lineEdit.setVisible(False)
            self.amount_and_label.setVisible(False)
            self.amountHi_lineEdit.setVisible(False)
            self.batchDesc_lineEdit.setVisible(True)
            self.supplier_label.setText('Description')
        elif jType in (PRODUCTION, ADJUSTMENT, PREP):
            self.supplier_combo.setVisible(False)
            self.amount_label.setVisible(False)
            self.amountLow_lineEdit.setVisible(False)
            self.amount_and_label.setVisible(False)
            self.amountHi_lineEdit.setVisible(False)
            self.batchDesc_lineEdit.setVisible(False)
            self.supplier_label.setVisible(False)
            
    def getDate(self):
        if self.dateRange_combo.currentText() == 'All':
            return ("", "")
        else:
            date_low = self.dateLow_dateEdit.date()
            date_low = date_low.toPyDate()
            date_hi = self.dateHi_dateEdit.date()
            date_hi = date_hi.toPyDate()
            dateTupple = (date_low, date_hi)
            return dateTupple
            
    ## == Form operations  
    def find(self):
        if self.tabWidget.currentIndex() == 0:
            self.standardFind()
        elif self.tabWidget.currentIndex() == 1:
            self.detailFind()
              
    def standardFind(self):
        jType = self.journal_combo.currentIndex()
        journal_no = str(self.number_lineEdit.text())
        supplier_id = dLookup(Suppliers.supplier_id, Suppliers.supplier_name==str(self.supplier_combo.currentText()))
        amount_low = str(self.amountLow_lineEdit.text())
        amount_hi = str(self.amountHi_lineEdit.text())
        batch_desc = str(self.batchDesc_lineEdit.text())
        date_low, date_hi = self.getDate()
        if jType == RECEIVE:
            journalNo_filter = ReceiveHeader.journal_no.ilike('%%%s%%' % journal_no) \
                                if journal_no else ""

            supplierId_filter = ReceiveHeader.supplier_id == supplier_id \
                                if supplier_id else ""

            if amount_low and amount_hi:
                amount_low = int(amount_low)
                amount_hi = int(amount_hi)
                amount_filter = ReceiveHeader.journal_total.between(amount_low, amount_hi)
            elif not amount_low or not amount_hi:
                amount_filter = ""
            if self.dateRange_combo.currentText() == 'All':
                date_filter = ""
            elif not self.dateRange_combo.currentText() == 'All':
                date_filter = ReceiveHeader.journal_date.between(date_low, date_hi)

            self.query = self.session.query(ReceiveHeader).filter(or_(ReceiveHeader.journal_type=='Bill', ReceiveHeader.journal_type=='Credit')) \
                                  .filter(journalNo_filter).filter(supplierId_filter).filter(amount_filter).filter(date_filter)
            self.fieldList = [('ID', 'journal_id', 50, 'string'), ('Type', 'journal_type', 50, 'string'), ('No', 'journal_no', 75, 'string'), 
                       ('Date', 'journal_date', 150, 'date'), ('Supplier', 'supplier_name', 150, 'string'), 
                       ('Amount', 'journal_total', 50, 'number'), ('Modified', 'modified_date', 150, 'date'),
                       ('Memo', 'journal_memo', 150, 'string')]
            self.reportName = 'Receiving List'
            self.columnsToTotal = [(5,)]
      
        elif jType == BATCH:
            journalNo_filter = or_(BatchHeader.batch_id==journal_no, BatchHeader.base_no==journal_no) \
                                if journal_no else ""

            batchDesc_filter = BatchHeader.base_desc == batch_desc \
                                if batch_desc else ""
         
            if self.dateRange_combo.currentText() == 'All':
                date_filter = ""
            elif not self.dateRange_combo.currentText() == 'All':
                date_filter = BatchHeader.batch_date.between(date_low, date_hi)
          
            self.query = self.session.query(BatchHeader).filter(journalNo_filter).filter(batchDesc_filter).filter(date_filter)
            self.fieldList = [('ID', 'batch_id', 50, 'string'), ('Base No.', 'base_no', 50, 'string'), ('Date', 'batch_date', 75, 'date'),
                             ('Journal', 'journal_id', 50, 'string'), ('Memo', 'batch_memo', 150, 'string')]
            self.reportName = 'Batch List'
            self.columnsToTotal = []
          
        elif jType == PRODUCTION:
            journalNo_filter = or_(ProductionHeader.journal_no.ilike('%%%s%%' % journal_no),
                                   ProductionHeader.journal_id == journal_no) \
                                   if journal_no else ""
            if self.dateRange_combo.currentText() == 'All':
                date_filter = ""
            elif not self.dateRange_combo.currentText() == 'All':
                date_filter = ProductionHeader.journal_date.between(date_low, date_hi)
          
            self.query = self.session.query(ProductionHeader).filter(journalNo_filter).filter(date_filter)
            self.fieldList = [('ID', 'journal_id', 50, 'string'), ('Production No', 'journal_id', 50, 'string'), 
                              ('Ref No', 'journal_no', 50, 'string'), ('Date', 'journal_date', 75, 'date'), 
                              ('Modified', 'modified_date', 150, 'date'), ('Memo', 'journal_memo', 150, 'string')]
            self.reportName = 'Production List'
            self.columnsToTotal = []
        
        elif jType == ADJUSTMENT:
            journalNo_filter = or_(AdjustmentHeader.journal_no.ilike('%%%s%%' % journal_no),
                                   AdjustmentHeader.journal_id == journal_no) \
                                   if journal_no else ""
            if self.dateRange_combo.currentText() == 'All':
                date_filter = ""
            elif not self.dateRange_combo.currentText() == 'All':
                date_filter = AdjustmentHeader.journal_date.between(date_low, date_hi)
          
            self.query = self.session.query(AdjustmentHeader).filter(journalNo_filter).filter(date_filter)
            self.fieldList = [('ID', 'journal_id', 0, 'string'), ('No', 'journal_id', 50 ,'string'), ('Date', 'journal_date', 75, 'date'), 
                              ('Modified', 'modified_date', 150, 'date'), ('Memo', 'journal_memo', 150, 'string')]
            self.reportName = 'Adjustment List'
            self.columnsToTotal = []
        
        elif jType == PREP:
            journalNo_filter = PrepHeader.prep_id.ilike('%%%s%%' % journal_no) if journal_no else ""
            if self.dateRange_combo.currentText() == 'All':
                date_filter = ""
            elif not self.dateRange_combo.currentText() == 'All':
                date_filter = AdjustmentHeader.journal_date.between(date_low, date_hi)
            self.query = self.session.query(PrepHeader).filter(journalNo_filter).filter(date_filter)
            self.fieldList = [('ID', 'prep_id', 0, 'string'), ('Date', 'prep_date', 75, 'date'), ('Memo', 'prep_memo', 150, 'string')]
            self.reportName = 'Preparation List'
            self.columnsToTotal = []
            
        self.populateView()
        
        
    def detailFind(self):
        rmd_list = self.session.query(RMD.journal_id, (RMD.bom_id).label('itemID'), (RMD.total / RMD.qty).label('rmdCost'), 
                                      (BOM.bom_no).label('itemNo'), (BOM.bom_desc).label('itemDesc'), 
                                      BOM.supplier_id.label('supplierId'), JournalHeader.journal_id, JournalHeader.journal_no, 
                                      JournalHeader.journal_date, JournalHeader.journal_type, literal_column('"RMD"').label('itemType')) \
                                      .join(BOM).join(JournalHeader)
        
        fgd_list = self.session.query(FGD.journal_id, (FGD.item_id).label('itemID'), FGD.cost, (Items.item_no).label('itemNo'), 
                                      (Items.item_desc).label('itemDesc'), literal_column('"AW Products"').label('supplierId'), 
                                      JournalHeader.journal_id, JournalHeader.journal_no, JournalHeader.journal_date, 
                                      JournalHeader.journal_type, literal_column('"FGD"').label('itemType')) \
                                      .join(Items).join(JournalHeader)

        unionQuery = rmd_list.union(fgd_list).subquery()
        
        query = self.session.query(unionQuery).join(JournalHeader)
       
        itemCrit = self.ItemList.getList()
        itemLine = ''.join(i for i in itemCrit)[:-2]
        itemFilter = "or_(%s)" % itemLine
        query = query.filter(eval(itemFilter)) if itemCrit else query
        
        supCrit = self.supplier_list.getList()
        supLine = ''.join(i for i in supCrit)[:-2]
        supFilter = "or_(%s)" % supLine
        query = query.filter(eval(supFilter)) if supCrit else query
        
        critList = self.filterModel.getFilterCriteria()
        for crit in critList:
            query = query.filter(eval(crit))
        

        self.fieldList = [('ID', 'journal_id', 25, 'string'), ('Journal', 'journal_type', 70, 'string'), ('No', 'journal_no', 75, 'string'),
                          ('Date', 'journal_date', 75, 'date'), ('Item', 'item_no', 50, 'string'), 
                          ('Description', 'item_desc', 200, 'string'), ('Cost', 'item_cost', 50, 'number')]
        self.reportName = 'Detail Find List'
        self.columnsToTotal = []
            
        self.query = []
        for i in query:
            journal_id = i[0]
            item_no = i[3]
            item_desc = i[4]
            item_cost = nonZero(i[2], 0)
            journal_no = i[7]
            journal_date = i[8]
            journal_type = i[9]
            self.query += [DetailFind(journal_id, item_no, item_desc, item_cost, journal_no, journal_date, journal_type)]
        
        self.populateView()
        
    def populateView(self):    
        self.model = modelsandviews.FindResultModel(self.fieldList)
        self.model.load(self.query)
        self.proxyModel.setSourceModel(self.model)
        self.results_tableView.setModel(self.proxyModel)
        self.results_tableView.setSortingEnabled(True)
        self.v_results_label.setText('%s - Results' % len(self.model.results))
        self.resizeView()
    
    def resizeView(self):
        self.results_tableView.resizeColumnsToContents()
        self.results_tableView.horizontalHeader().setStretchLastSection(True)
#        self.results_tableView.setColumnHidden(0, True)
    
    def edit(self):
        if not self.model:
            return
        jType = self.journal_combo.currentIndex()
        row = self.results_tableView.currentIndex().row()
        recordIndex = self.proxyModel.index(row, 0)
        recordID = self.proxyModel.data(recordIndex).toInt()[0]
        self.editTransaction(jType, recordID)
        
    def editTransaction(self, jType, recordID):
        if jType == RECEIVE:
            form = self.myParent.receiveForm()
            form.recall(recordID)
        
        elif jType == BATCH:
            form = self.myParent.batchForm()
            form.recall(1, recordID)
            
        elif jType == PRODUCTION:
            form = self.myParent.productionForm()
            form.recall(recordID)
            
        elif jType == ADJUSTMENT:
            form = self.myParent.invAdjustment()
            form.recall(recordID)
            
        elif jType == PREP:
            form = self.myParent.prodprepForm()
            form.recall(recordID)
            
    
    def clear(self):
        widgets = self.findChildren(QWidget)
        for widget in widgets:
            if isinstance(widget, (QLineEdit, QTextEdit)):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(-1)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(False)
            elif isinstance(widget, QLabel):
                if widget.objectName()[:2] == 'v_':
                    widget.clear()
        self.dateRange_combo.setCurrentIndex(0)
        self.dateFilter_combo.setCurrentIndex(0)
        if self.model is not None:
            self.model.clear()
    
    def printReport(self):
        if not self.model:
            return
        reportModel = reporting.ReportModel('Simple List')
        self.refreshReport(reportModel)
        report_type = 'trans_header_report' if self.tabWidget.currentIndex() == 0 else 'trans_detail_report'
        self.myParent.reportForm(reportModel, self, report_type)
    
    def refreshReport(self, model, report=None):
        fromDate, toDate = self.getDate()
        if fromDate and toDate:
            period = 'From %s To %s.' % (fromDate, toDate)
        elif toDate:
            period = 'As of %s.' % toDate
        else:
            period = 'All available dates.'
        model.load(self.reportName, period, self.query, self.fieldList, self.columnsToTotal)
        
    def formClosed(self):
        self.myParent.formClosed()
   

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    setupDatabase("Production.sqlite")
    supModel = modelsandviews.SupplierModel()
#    itmModel = modelsandviews.ItemModel()
#    bsModel = modelsandviews.BaseListModel()
    form = FindForm(supModel)
    form.show()
    app.exec_()
        