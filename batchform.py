# Libraries
import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy import  *
from sqlalchemy.orm import *
# My Imports
import ui_forms.ui_batchform
from databaseschema import *
from genericdelegates import *
from functions import *
import modelsandviews
from itemform import BaseAssemblyModel


#==============================================================================
### Model Setup ============== 
(RMID, QTY, DESC, SUPPLIER, SUPPLIER_NO, AVG_COST, TOTAL) = range(7)

def calculate_total(record):
    assert isinstance(record, BatchDetail)
    if not record.bom_qty:
        return 0
    else:
        total = float(getType(record.bom_qty)) * float(getType(record.cost))
        return total

def calculate_qty(record):
    assert isinstance(record, BatchDetail)
    total = record.bom_qty
    if isinstance(record.bom_qty, QString):
        total = record.bom_qty.toFloat()[0]
    elif total is None:
        return 0
    else:
        return float(total)
        

class BaseDetailModel(QAbstractTableModel):
    ### Model Initializer ============== 
    def __init__(self, journal_date=QDate.currentDate().toPyDate(), parent=None):
        super(BaseDetailModel, self).__init__(parent)
        self.records = []
        self.records.append(BatchDetail())
        self.itemModel = modelsandviews.ItemModel('BOM')
        self.formType = 0
        self.journal_date = journal_date
        
    ### Base Implemantations ============== 
    def rowCount(self, index=QModelIndex()):
        return len(self.records)
    
    def columnCount(self, index=QModelIndex()):
        return 7
    
    def flags(self, index):
        flag = QAbstractTableModel.flags(self, index)
        if index.column() not in (DESC, SUPPLIER, SUPPLIER_NO, AVG_COST, TOTAL):
            flag |= Qt.ItemIsEditable
        return flag
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == RMID:
                return QVariant('Item')
            elif section == QTY:
                return QVariant('Qty')
            elif section == DESC:
                return QVariant('Description')
            elif section == SUPPLIER:
                return QVariant('Supplier')
            elif section == SUPPLIER_NO:
                return QVariant('Supplier No.')
            elif section == AVG_COST:
                return QVariant('Avg Cost')
            elif section == TOTAL:
                return QVariant('Total')
        return QVariant(section + 1)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <=index.row() < len(self.records)):
            return QVariant()
        record = self.records[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == RMID:
                bomNo =  dLookup(BOM.bom_no, BOM.bom_id == str(record.bom_id))
                return QVariant(bomNo)
            elif column == QTY:
                if record.bom_qty is not None:                    
                    return QVariant(round(getType(record.bom_qty), 4))
            elif column == DESC:
                bomDesc = dLookup(BOM.bom_desc, BOM.bom_id == str(record.bom_id))
                return QVariant(bomDesc)
            elif column == SUPPLIER:
                supID = dLookup(BOM.supplier_id, BOM.bom_id == str(record.bom_id))
                supName = dLookup(Suppliers.supplier_name, Suppliers.supplier_id==supID)
                return QVariant(supName)
            elif column == SUPPLIER_NO:
                return QVariant(dLookup(BOM.bom_supplier_no, BOM.bom_id == str(record.bom_id)))
            elif column == AVG_COST:
                return QVariant(record.cost)
            elif column == TOTAL:
                total = self.calcTotal(record)
                if total is not None:
                    return QVariant('{:,.2f}'.format(total))
        return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            record = self.records[index.row()]
            column = index.column()
            if column == RMID:
                record.bom_id = value.toInt()[0]
                record.cost = self.cost(record)
                record.total = self.calcTotal(record)
            elif column == QTY:
                record.bom_qty = value.toFloat()[0]
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
            return True
        return False
    
    ### Calculations ============
    def updateDate(self, journal_date):
        self.journal_date = journal_date
    
    def calcTotal(self, record):
        qty = getType(record.bom_qty)
        cost = getType(record.cost)
        total = qty * cost
        return total
    
    def cost(self, record):
        date = self.journal_date
        bom_id = record.bom_id
        cost = avgCost(bom_id, str(date))
        return cost
    
    def getSumTotal(self):
        return sum(map(calculate_total, self.records), 0.0)
    
    def getSumQty(self):
        return sum(map(calculate_qty, self.records), 0.0)
    
    def updateDetailModel(self, multiplier):
        assert isinstance(multiplier, float)
        self.beginResetModel()
        for record in self.records:
            if record.bom_id:
                qty = getType(record.bom_qty)
                record.bom_qty = qty * multiplier
                record.cost = self.cost(record)
                record.total = self.calcTotal(record)
        self.endResetModel()
    
    ### Operations ============== 
    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.records.insert(position + row + 1, BatchDetail())
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        if rows == self.rowCount():
            rows -= 1
        self.beginRemoveRows(QModelIndex(), position, position + rows -1)
        self. records = self.records[:position] + self.records[position + rows:]
        self.endRemoveRows()
        return True
    
    def load(self, formType, itemList, session):
        self.beginResetModel()
        self.records = []
        self.endResetModel()
        for item in itemList:
            bom_id = item.bom_id
            bom_qty = item.bom_qty
            cost = self.cost(item)
            qty = float(nonZero(bom_qty, 0))
            total = getType(qty) * getType(cost)
            self.records.append(BatchDetail(None, bom_id, cost, bom_qty, total))
        self.records.append(BatchDetail())
            
    def save(self, formType, base_id, journal_date):
        records = []
        for record in self.records:
            if record.bom_id:
                bom_id = record.bom_id
                bom_qty = record.bom_qty
                if formType == 0:
                    records = records + [BaseDetail(base_id, bom_id, bom_qty)]
                else:
                    records = records + [BatchDetail(base_id, bom_id, None, bom_qty)]
        return records
    
    def clear(self):
        self.beginResetModel()
        self.records = []
        self.records.append(BatchDetail())
        self.endResetModel()
        
    def copy(self, indexList):
        clipboard = QApplication.clipboard()
        clipText = QString()
        indexList.sort()
        previous = indexList[0]
        for current in indexList:
            text = self.data(current, Qt.DisplayRole).toString()
            if current.row() != previous.row():
                clipText.append('\n')
            else:
                clipText.append('\t')
            clipText.append(text)
            previous = current
        clipText.remove(0, 1)
        clipboard.setText(clipText)
        
    def paste(self, position, index=QModelIndex()):
        myList = []
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        rows = text.split('\n')
        for rec in rows:
            col = rec.split('\t')
            bom_id = dLookup(BOM.bom_id, BOM.bom_no==str(col[0]))
            if bom_id:
                qty = float(getType(col[1])) if len(col) >= 2 else 0
                myList += [BatchDetail(None, bom_id, None, qty)]
        rowCount = len(myList)
        self.beginInsertRows(QModelIndex(), position, position + rowCount - 1)
        for row in range(rowCount):
                self.records.insert(position + row, myList[row])
        self.endInsertRows()
        self.updateDetailModel(1.0)
        return True
            
        
        
#==============================================================================
### Form Setup ============== 
BASE, BATCH, OTHER = range(3)
class BatchForm(QDialog, ui_forms.ui_batchform.Ui_BatchForm):
    localTITLE = 'Base Setup'
    ### Initializer ============= 
    def __init__(self, baseModel, bomModel, formType=BATCH, parent=None):
        super(BatchForm, self).__init__(parent)
        self.setupUi(self)
        
        self.my_parent = parent
        self.dirty = False
        self.editing = False
        self.session = Session()
        self.query = None
        self.current_record = None
        self.record_id = None
        
        if formType == BASE:
            self.baseRadio.setChecked(True)
        else:
            self.batchRadio.setChecked(True)
            
        self.dateEdit.setDate(self.my_parent.getDate())
        baseID = dMax(BaseHeader.base_id) + 1
        self.v_baseID_Label.setText(str(baseID))
        
        self.printButton.setEnabled(False)
        
        self.baseModel = baseModel
        self.baseView = modelsandviews.ItemView(self.baseModel, True)
        self.baseCombo.setModel(self.baseModel)
        self.baseCombo.setView(self.baseView)
        self.baseCombo.setModelColumn(1)
        self.baseCombo.setCurrentIndex(-1)
        self.baseCombo.view().setFixedWidth(200)
        self.baseCombo.setEditable(True)
        self.baseCombo.setInsertPolicy(QComboBox.NoInsert)
        self.baseTypeCombo = QComboBox(self.frame)
        self.baseTypeCombo.addItems(("Base", "Flavor"))
        self.baseTypeCombo.setGeometry(QRect(275, 9, 96, 25))
        
        self.itemModel = bomModel
        self.detailModel = BaseDetailModel()
        self.detailView.setModel(self.detailModel)
        delegate = GenericDelegate(self)
        delegate.insertDelegate(RMID, ComboDelegate(self.itemModel, True))
        delegate.insertDelegate(QTY, NumberDelegate())
        self.detailView.setItemDelegate(delegate)
        
        self.associatedModel = BaseAssemblyModel()
        self.associatedView.setModel(self.associatedModel)
        assoDelegate = GenericDelegate(self)
        assoDelegate.insertDelegate(1, ComboDelegate(self.baseModel, True))
        assoDelegate.insertDelegate(2, NumberDelegate())
        self.associatedView.setColumnHidden(0, True)
        self.associatedView.setItemDelegate(assoDelegate)
        self.associatedView.horizontalHeader().setStretchLastSection(True)                                    
        
        self.changeLayout(False)
        
        self.baseRadio.toggled.connect(lambda: self.changeLayout(True))
        self.detailModel.dataChanged.connect(lambda: self.autoAddRow(self.detailView, self.detailModel))
        self.associatedModel.dataChanged.connect(lambda: self.autoAddRow(self.associatedView, self.associatedModel))
        self.multFactorLineedit.editingFinished.connect(self.updateSumTotal)
        self.baseCombo.currentIndexChanged.connect(self.recallBase)
        self.multLineedit.editingFinished.connect(self.multiplyQty)
        self.dateEdit.dateChanged.connect(self.updateModelDate)
        self.dateEdit.dateChanged.connect(self.setParentDate)
        
        self.newButton.clicked.connect(self.clear)
        self.saveButton.clicked.connect(self.save)
        self.deleteButton.clicked.connect(self.delete)
        self.closeButton.clicked.connect(self.accept)
        self.detailView.doubleClicked.connect(self.findBomID)
        
        self.setupConnection()
        
    ### Form Behaviour setup ==============        
    def setupConnection(self):
        """ connect every widget on form to the data changed function, 
        to set the form to dirty """
        widgets = self.findChildren(QWidget)
        for widget in widgets:
            if isinstance(widget, (QLineEdit, QTextEdit)):
                self.connect(widget, SIGNAL("textEdited(QString)"), self.setDirty)
            elif isinstance(widget, QComboBox):
                self.connect(widget, SIGNAL("activated(int)"), self.setDirty)
            elif isinstance(widget, QCheckBox):
                self.connect(widget, SIGNAL("stateChanged(int)"), self.setDirty)
    
    def changeLayout(self, clrBool):
        """ setup the form layout, based on type of item user wants to enter"""
        if self.baseRadio.isChecked():
            self.baseTypeCombo.setVisible(True)
            self.multLineedit.setVisible(False)
            self.mult_Label.setText('Base Type')
            self.baseID_Label.setText('Base ID')
            self.associatedLabel.setVisible(True)
            self.associatedView.setVisible(True)
            self.header_label.setText('Create New Base:')
            self.setStyleSheet("QDialog {Background-color: lightGray ;}")
            self.localTITLE = 'Base Setup'
        elif self.batchRadio.isChecked():
            self.baseTypeCombo.setVisible(False)
            self.multLineedit.setVisible(True)
            self.mult_Label.setText('Multiply Batch')
            self.baseID_Label.setText('Batch ID')
            self.associatedLabel.setVisible(False)
            self.associatedView.setVisible(False)
            self.header_label.setText('Record Batch:')
            self.setStyleSheet("QDialog {Background-color: ;}")
            self.localTITLE = 'Record Batch'
        self.setWindowTitle(self.localTITLE)
        if clrBool == True:
            self.clear()
        
       
    def setDirty(self):
        if self.baseCombo not in (self.sender(), self.sender().parent()):
            self.dirty = True
            self.setWindowTitle("%s - Editing..." % self.localTITLE)
    
    def setParentDate(self):
        date = self.dateEdit.date().toPyDate()
        self.my_parent.setDate(date) 
         
    def updateModelDate(self):
        date = self.dateEdit.date().toPyDate()
        self.detailModel.updateDate(date)
        
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        if self.detailView.hasFocus() or self.bom_view.hasFocus():
            model = self.detailModel
            view = self.detailView
            copyAction = menu.addAction('Copy')
            pasteAction = menu.addAction('Paste')
            insertAction = menu.addAction('Insert Line')
            deleteAction = menu.addAction('Delete Line')
            copyAction.triggered.connect(self.copy)
            pasteAction.triggered.connect(self.paste)
            insertAction.triggered.connect(lambda: self.insertRow(view, model))
            deleteAction.triggered.connect(lambda: self.removeRow(view, model))
        menu.exec_(event.globalPos())
       
    def copy(self):
        if self.detailModel.rowCount() <= 1:
            return
        selectedItems = self.detailView.selectionModel().selectedIndexes()
        self.detailModel.copy(selectedItems)
        
    def paste(self):
        row = self.detailView.currentIndex().row()
        self.detailModel.paste(row)
        self.updateSumTotal()
            
    def autoAddRow(self, view, model):
        self.updateSumTotal()
        row = view.currentIndex().row()
        if model.rowCount() == row + 1:
            self.insertRow(view, model)
        
                
    def insertRow(self, view, model):
        if view is not None:
            index = view.currentIndex()
            row = index.row()
            model.insertRows(row)
            view.setFocus()
            view.setCurrentIndex(index)
       
    
    def removeRow(self, view, model):
        if model.rowCount() <= 1:
            return
        row = 0
        rowsSelected = view.selectionModel().selectedRows()
        for i in rowsSelected:
            row = i.row()
        rows = len(rowsSelected)
        row = row - rows + 1
        model.removeRows(row, rows)
        self.updateSumTotal()
        self.setDirty()
        
    def findBomID(self):
        row = self.detailView.currentIndex().row()
        index = self.detailModel.index(row, 0)
        self.my_parent.findItem(0, (self, index), self.localTITLE)
    
    def enterBOMNo(self, index, bomID):
        i = 0
        ok = True
        while ok:
            myIndex = self.detailModel.index(index.row() + i, index.column())
            bom = self.detailModel.data(myIndex).toString()
            if not bom:
                ok = False
            i += 1
        self.detailView.setCurrentIndex(myIndex)
        self.detailModel.setData(myIndex, QVariant(bomID))
        
        
    ### Data and calculations ====================================    
    def updateSumTotal(self):
        sum_total = float(self.detailModel.getSumTotal())
        sum_qty = float(self.detailModel.getSumQty())
        inf_factor = str(self.multFactorLineedit.text())
        inf_factor = float(getType(inf_factor))
        self.v_cost_Label.setText(str('{:,.2f}'.format(sum_total)))
        self.v_weight_Label.setText(str('{:,.2f}'.format(sum_qty)))
        self.v_multFlu_Label.setText(str('{:,.2f}'.format(sum_qty)))
        self.v_mult1lt_Label.setText(str('{:,.2f}'.format(sum_qty * inf_factor)))
        self.v_mult15lt_Label.setText(str('{:,.2f}'.format((sum_qty * inf_factor) / 1.5)))
        self.v_mult2lt_Label.setText(str('{:,.2f}'.format((sum_qty * inf_factor) / 2)))
        self.v_mult4lt_Label.setText(str('{:,.2f}'.format((sum_qty * inf_factor) / 4)))
        self.v_mult114lt_Label.setText(str('{:,.2f}'.format((sum_qty * inf_factor) / 11.4)))
    
    def multiplyQty(self):
        # // formula is: newQty = qty (new / old)
        newValue = self.multLineedit.text()
        self.multLineedit.undo()
        oldValue = self.multLineedit.text()
        self.multLineedit.setText(newValue)
        if newValue:
            newValue = float(newValue)
        else:
            newValue = 1
        if oldValue:
            oldValue = float(oldValue)
        else:
            oldValue = 1
        multiplier = newValue / oldValue
        self.detailModel.updateDetailModel(multiplier)
        self.updateSumTotal()
    
        
    ## Operations ==============
    def reject(self):
        self.accept()
        
    def accept(self):
        if self.dirty:
            answer = QMessageBox.question(self, "Editing - %s" % self.localTITLE, "Would you like to save your data?",
                                 QMessageBox.Yes| QMessageBox.No| QMessageBox.Cancel)
            if answer == QMessageBox.Cancel:
                return
            elif answer == QMessageBox.No:
                QDialog.accept(self)
            elif answer == QMessageBox.Yes:
                self.save()
        QDialog.accept(self)
        self.my_parent.formClosed()
        
    
    def checkForJournalID(self):
        j = dLookup(BatchHeader.journal_id, BatchHeader.batch_id==self.record_id)
        if j != 'None':
            return True
        else:
            return False
    
    def save(self):
        # // Prepare the items to be recorded
        qDate = self.dateEdit.date()
        base_date = qDate.toPyDate()
        base_type = str(self.baseTypeCombo.currentText())
        base_desc = str(self.descLineedit.text())
        base_volume = unicode(self.volumeLineedit.text())
        inflation_factor = unicode(self.multFactorLineedit.text())
        base_memo = str(self.memoTextedit.toPlainText())
        base_no = str(self.baseCombo.currentText())
        # // do some checks
        if not base_no:
            QMessageBox.information(self, 'Save - %s' % self.localTITLE, 'Please specify a Base Number before saving', 
                                    QMessageBox.Ok)
            return
        if not base_volume:
            QMessageBox.information(self, 'Save - %s' % self.localTITLE, 'Please sepcify a base volume before saving', 
                                    QMessageBox.Ok)
            return
        # // Continue based on form type
        if self.baseRadio.isChecked():
            # // some more checks
            if not inflation_factor:
                QMessageBox.information(self, 'Save - %s' % self.localTITLE, 'Please specify an inflation factor before saving', 
                                        QMessageBox.Ok)
                return
            # // check if there are details
            if self.detailModel.rowCount() <= 1:
                QMessageBox.information(self, 'Save - %s' % self.localTITLE, 'No details found.', 
                                        QMessageBox.Ok)
                return
            # // do differently if new record or old record
            if self.editing:
                # // of old record, update header, delete and redo detail
                journal_id = self.record_id
                self.current_record = self.session.query(BaseHeader).filter(BaseHeader.base_id==journal_id)
                self.current_record.update({'base_date': base_date, 'base_no': base_no, 'base_type': base_type,
                                            'base_desc': base_desc, 'base_volume': base_volume, 'inflation_factor': inflation_factor,
                                            'base_memo': base_memo})
                self.session.query(BaseDetail).filter(BaseDetail.base_id==journal_id).delete()
                self.session.query(AssociatedBase).filter(AssociatedBase.base_id==journal_id).delete()
            
            elif not self.editing: 
                # // if new record, get new id number and record header
                journal_id = dMax(BaseHeader.base_id) + 1
                self.session.add(BaseHeader(journal_id, base_date, base_no, base_type, base_desc, 
                                            base_volume, inflation_factor, base_memo))
            # // record detail
            items = self.detailModel.save(0, journal_id, base_date)
            associated = self.associatedModel.save(journal_id, 'AssociatedBase')
            self.session.add_all(associated) 
        
        elif self.batchRadio.isChecked():
            # // some items or a bit different if formType is different, like for batch we need base_id
            base_id = dLookup(BaseHeader.base_id, BaseHeader.base_no==base_no)
            multiple = unicode(self.multLineedit.text())
            # // check if batch is being edited, or new record
            if self.editing:
                #// Check if batch was already used on production
                if self.checkForJournalID():
                    if self.checkForJournalID():
                        QMessageBox.information(self, "Save - %s" % self.localTITLE, "Can't save changes," \
                                                "because it was already used on a production", QMessageBox.Ok)
                        return
                # // if edited, update header, delete detail so could be redone.
                journal_id = self.record_id
                self.current_record = self.session.query(BatchHeader).filter(BatchHeader.batch_id==journal_id)
                self.current_record.update({'base_id': base_id, 'batch_date': base_date, 'base_volume': base_volume,
                                            'multiple': multiple, 'inflation_factor': inflation_factor, 'batch_memo': base_memo})
                self.session.query(BatchDetail).filter(BatchDetail.base_id==journal_id).delete()
            else:
                # // if new record, get new id_num, and record new header.
                journal_id = dMax(BatchHeader.batch_id) + 1
                self.session.add(BatchHeader(journal_id, base_id, base_date, base_volume, multiple, inflation_factor, base_memo)) 
            # // record details 
            items = self.detailModel.save(1, journal_id, base_date)
        # // record details no matter on form type
        self.session.add_all(items)                         
        self.sendToDB()
        self.my_parent.refreshModels() # // reloads all the models, including batch list model used on production form
        self.record_id = journal_id
        self.editing = True
        self.dirty = False
        self.setWindowTitle('%s - (Data Saved)' % self.localTITLE)
        
    def recallBase(self):
        """ to fill the detail model when selecting a base,
        used to edit a base, and to start a new batch """
        row = self.baseCombo.currentIndex()
        if row == -1:
            return
        i = self.baseModel.index(row, 0)
        recordID = self.baseModel.data(i).toInt()[0]
        self.recall(OTHER, recordID)

        
    def recall(self, fType, recordID):
        # // first find out if the user is in middle of entering data.
        if self.dirty:
            answer = QMessageBox.question(self, "Editing - %s" % self.localTITLE, "Would you like to save your data?",
                                 QMessageBox.Yes| QMessageBox.Discard| QMessageBox.Cancel)
            if answer == QMessageBox.Cancel:
                return
            elif answer == QMessageBox.Yes:
                self.save()
                
        self.record_id = recordID
        if fType in (BASE, OTHER):
            if fType == BASE:
                self.baseRadio.setChecked(True)
            row = self.baseCombo.currentIndex()
            self.changeLayout(False)
            self.current_record = self.session.query(BaseHeader).filter(BaseHeader.base_id==recordID)
            for record in self.current_record:
                self.v_baseID_Label.setText(str(self.record_id))
                self.baseCombo.setCurrentIndex(row)
                base_type = self.baseTypeCombo.findText(record.base_type, Qt.MatchExactly)
                self.baseTypeCombo.setCurrentIndex(base_type)
                self.descLineedit.setText(str(record.base_desc))
                if fType == BASE:
                    self.dateEdit.setDate(record.base_date)
                self.volumeLineedit.setText(str(record.base_volume))
                self.multFactorLineedit.setText(str(record.inflation_factor))
                self.memoTextedit.setText(str(record.base_memo))
            baseList = self.session.query(AssociatedBase).filter(AssociatedBase.base_id==recordID)
            self.associatedModel.load(baseList, True)
            itemList = self.session.query(BaseDetail).filter(BaseDetail.base_id==recordID)
        elif fType == BATCH:
            self.batchRadio.setChecked(True)
            # // need to block signal, bcs, setChecked triggeres self.clear() where signal is unbocked
            # // and latter when i do set current indes, it combo emits signal
            self.baseCombo.blockSignals(True)
            self.changeLayout(False)
            self.current_record = self.session.query(BatchHeader).filter(BatchHeader.batch_id==recordID)
            for record in self.current_record:
                self.v_baseID_Label.setText(str(self.record_id))
                base_no = dLookup(BaseHeader.base_no, BaseHeader.base_id==record.base_id)
                base_id = self.baseCombo.findText(base_no, Qt.MatchExactly)
                self.baseCombo.setCurrentIndex(base_id)
                baseType = dLookup(BaseHeader.base_type, BaseHeader.base_id==record.base_id)
                base_type = self.baseTypeCombo.findText(baseType, Qt.MatchExactly)
                self.baseTypeCombo.setCurrentIndex(base_type)
                baseDesc = dLookup(BaseHeader.base_desc, BaseHeader.base_id==record.base_id)
                self.descLineedit.setText(str(baseDesc))
                self.dateEdit.setDate(record.batch_date)
                self.volumeLineedit.setText(str(record.base_volume))
                self.multLineedit.setText(str(record.multiple))
                self.multFactorLineedit.setText(str(record.inflation_factor))
                self.memoTextedit.setText(str(record.batch_memo))
            itemList = self.session.query(BatchDetail).filter(BatchDetail.base_id==recordID)
        self.detailModel.load(fType, itemList, self.session)
        self.updateSumTotal()
        if fType in (BASE, BATCH):
            self.editing = True
        self.baseCombo.blockSignals(False)
        
    def delete(self):
        if not self.record_id:
            return
        
        if self.baseRadio.isChecked():
            #need to check if there are batches created with this base, if yes don delete.
            
            answer = QMessageBox.question(self, "Delete - %s" % self.localTITLE, "Are you sure you " \
                                              "want to delete Base: %s" % self.descLineedit.text(), 
                                              QMessageBox.Yes| QMessageBox.No, QMessageBox.NoButton)
            if answer == QMessageBox.No:
                return
            self.session.query(BaseDetail).filter(BaseDetail.base_id==self.record_id).delete()
            self.session.query(AssociatedBase).filter(AssociatedBase.base_id==self.record_id).delete()
        
        elif self.batchRadio.isChecked():    
            if self.editing == True:
                if self.checkForJournalID():
                    QMessageBox.information(self, "Delete - %s" % self.localTITLE, "Can't delete current batch," \
                                            "because it was already used on a production", QMessageBox.Ok)
                    return
            answer = QMessageBox.question(self, "Delete - %s" % self.localTITLE, "Are you sure you " \
                                          "want to delete batch: %s" % self.descLineedit.text(), 
                                          QMessageBox.Yes| QMessageBox.No, QMessageBox.NoButton)
            if answer == QMessageBox.No:
                return
            self.session.query(BatchDetail).filter(BatchDetail.base_id==self.record_id).delete()
        self.current_record.delete()
        self.sendToDB()
        self.clear()
            
    def sendToDB(self):
        try:
            self.session.flush
            self.session.commit()
        except Exception, e:
            self.session.rollback()
            raise e 
            
    def clear(self):
        self.baseCombo.blockSignals(True)
        self.baseModel.select()
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
        self.baseTypeCombo.setCurrentIndex(0)
        self.detailModel.clear()
        self.associatedModel.clear()
        self.my_parent.refreshModels()
        if defaultDate() == 'current':
            self.dateEdit.setDate(QDate.currentDate())
        self.editing = False
        self.dirty = False         
        self.setWindowTitle(self.localTITLE)
        self.baseCombo.blockSignals(False)

            
            
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    setupDatabase("Production.sqlite")
#    supModel = modelsandviews.SupplierModel()
    bomModel = modelsandviews.ItemModel('BOM')
    baseModel = modelsandviews.BaseListModel()
    form = BatchForm(baseModel, bomModel, BATCH)
    form.show()
    app.exec_()