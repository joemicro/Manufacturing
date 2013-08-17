# Libraries
import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy import  *
from sqlalchemy.orm import *
# My Imports
from databaseschema import *
from genericdelegates import *
from functions import *
import modelsandviews
import ui_forms.ui_inventoryadjform

localTITLE = 'Inventory Adjustment'
BOM_ID, DESC, QTY, COST, VALUE, MEMO = range(6)
class InventoryAdjustmentDetailModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(InventoryAdjustmentDetailModel, self).__init__(parent)
        self.records = []
        self.records.append(AdjRMD())
        self.journal_date = None
        self.journal_id = None
    
    def rowCount(self, index=QModelIndex()):
        return len(self.records)
    
    def columnCount(self, index=QModelIndex()):
        return 6
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == BOM_ID:
                return QVariant('Item')
            elif section == DESC:
                return QVariant('Description')
            elif section == QTY:
                return QVariant('New Qty')
            elif section == COST:
                return QVariant('Cost')
            elif section == VALUE:
                return QVariant('New Value')
            elif section == MEMO:
                return QVariant('Memo')
        return QVariant(section + 1)
    
    def flags(self, index):
        flag = QAbstractTableModel.flags(self, index)
        if not index.column() in (DESC, COST):
            flag |= Qt.ItemIsEditable
        return flag
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.records)):
            return QVariant()
        record = self.records[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == BOM_ID:
                bom_id = record.bom_id
                bom_num = dLookup(BOM.bom_no, BOM.bom_id==bom_id)
                return QVariant(bom_num)
            elif column == DESC:
                bom_id = record.bom_id
                desc = dLookup(BOM.bom_desc, BOM.bom_id==bom_id)
                return QVariant(desc)
            elif column == QTY:
                return QVariant(record.new_qty)
            elif column == COST:
                return QVariant(record.cost)
            elif column == VALUE:
                return QVariant(record.new_value)
            elif column == MEMO:
                return QVariant(record.rmd_memo)
        return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            record = self.records[index.row()]
            column = index.column()
            if column == BOM_ID:
                record.bom_id = value.toInt()[0]
            elif column == QTY:
                new_qty, ok = value.toFloat()
                if ok:
                    record.new_qty = new_qty
            elif column == VALUE:
                new_value, ok = value.toFloat()
                if ok:
                    record.new_value = new_value
                qty = getType(record.new_qty)
                value = getType(record.new_value)
                cost = value / nonZero(qty, 1)
                record.cost = float(cost)
            elif column == MEMO:
                record.rmd_memo = value.toString()
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
            return True
        return False
    
    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.records.insert(position + row + 1, AdjRMD())
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        if rows == self.rowCount():
            rows -= 1
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.records = self.records[:position] + self.records[position + rows:]
        self.endRemoveRows()
        return True
    
    ## Calculations ================
    def calcAdj(self, record):
        bom_id = record.bom_id
        new_qty = getType(record.new_qty)
        new_value = getType(record.new_value)
        qty, value = lookupValue(None, bom_id, str(self.journal_date), str(self.journal_id))
        adj_qty = new_qty - nonZero(qty, 0)
        adj_value = new_value - nonZero(value, 0)
        return (adj_qty, adj_value)
    
    def UpdateModel(self, journalDate, journalID=None):
        self.beginResetModel()
        self.journal_date = journalDate
        self.journal_id = journalID
        for record in self.records:
            record.qty, record.total = self.calcAdj(record)
        self.endResetModel()
        
    def sumUpAdj(self, record):
        assert isinstance(record, AdjRMD)
        total = getType(record.total)
        return total
    
    def sumUpValue(self, record):
        assert isinstance(record, AdjRMD)
        value = getType(record.new_value)
        return value
    
    def getAdjValue(self):
        adjValue = sum(map(self.sumUpAdj, self.records), 0.0)
        return adjValue
    
    def getValue(self):
        value = sum(map(self.sumUpValue, self.records), 0.0)
        return value
    
    ## Operations setup ============
    def clear(self):
        self.beginResetModel()
        self.records = []
        self.records.append(AdjRMD())
        self.endResetModel()
        
    def save(self, journal_id):
        self.UpdateModel(self.journal_date, self.journal_id)
        records_ = []
        for record in self.records:
            if record.bom_id:
                bom_id = int(record.bom_id)
                qty = unicode(record.qty)
                cost = unicode(record.cost)
                new_qty = unicode(record.new_qty)
                new_value = unicode(record.new_value)
                total = unicode(record.total)
                rmd_memo = str(record.rmd_memo)
                records_ = records_ + [AdjRMD(bom_id, new_qty, new_value, cost, rmd_memo, qty, total, journal_id)]
        return records_
    
    def load(self, objectList, journalDate, journalID):
        self.beginResetModel()
        self.records = []
        self.endResetModel()
        for item in objectList:
            bom_id = item.bom_id
            new_qty = item.new_qty
            cost = item.cost
            new_value = item.new_value
            rmd_memo = item.rmd_memo
            self.records.append(AdjRMD(bom_id, new_qty, new_value, cost, rmd_memo))
        self.records.append(AdjRMD())
        self.UpdateModel(journalDate, journalID)
            
                
class InventoryAdjForm(QDialog, ui_forms.ui_inventoryadjform.Ui_InventoryAdjustment):
    def __init__(self, bomModel, parent=None):
        super(InventoryAdjForm, self).__init__(parent)
        self.setupUi(self)
        
        self.session = Session()
        self.my_parent = parent
        self.dirty = False
        self.editing = False
        self.record_id = None
        self.current_record = None
        
        dtlTableView = self.detail_tableView
        self.detailModel = InventoryAdjustmentDetailModel()
        dtlTableView.setModel(self.detailModel)
        delegate = GenericDelegate(self)
        delegate.insertDelegate(BOM_ID, ComboDelegate(bomModel, True))
        delegate.insertDelegate(QTY, NumberDelegate())
        delegate.insertDelegate(VALUE, NumberDelegate())
        delegate.insertDelegate(MEMO, PlainTextDelegate())
        dtlTableView.setItemDelegate(delegate)
        
        self.adj_dateEdit.setDate(self.my_parent.getDate())
    
        self.adj_dateEdit.dateChanged.connect(self.setParentDate)
        self.detailModel.dataChanged.connect(lambda: self.autoAddRow(dtlTableView, self.detailModel))
        self.newButton.clicked.connect(self.clear)
        self.saveButton.clicked.connect(self.save)
        self.deleteButton.clicked.connect(self.delete)
        self.closeButton.clicked.connect(self.accept)
        
    
    ## == Form Behaviour Setup
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
                
    def setDirty(self):
        self.updateSumTotals()
        self.dirty = True
        self.setWindowTitle("%s - Editing..." % localTITLE) 
        
    def setParentDate(self):
        date = self.adj_dateEdit.date().toPyDate()
        self.my_parent.setDate(date)  
        
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        if self.detail_tableView.hasFocus():
            insertAction = menu.addAction("Insert Line", QObject, "Ctrl+I")
            deleteAction = menu.addAction("Delete Line", QObject, "Ctrl+D")
            self.connect(insertAction, SIGNAL("triggered()"), lambda: self.insertRow(self.dtl_tableView, self.detailModel))
            self.connect(deleteAction, SIGNAL("triggered()"), lambda: self.removeRow(self.dtl_tableView, self.detailModel))
            addActions(self, self.detail_tableView, (insertAction, deleteAction))
        menu.exec_(event.globalPos())
            
    def autoAddRow(self, view, model):
        index = view.currentIndex()
        self.setDirty()
        view.setFocus()
        view.setCurrentIndex(index)
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
        rowsSelected = view.selectionModel().selectedRows()
        if not rowsSelected:
            row = view.currentIndex().row()
            rows = 1
        else:
            for i in rowsSelected:
                row = i.row()
            rows = len(rowsSelected)
            row = row - rows + 1
        model.removeRows(row, rows)
        
    
    def updateSumTotals(self):
        journalDate = self.adj_dateEdit.date()
        journalDate = journalDate.toPyDate()
        journalID = self.v_adjID_label.text()
        self.detailModel.UpdateModel(journalDate, journalID)
        value_total = nonZero(self.detailModel.getValue(), 0)
        value_total = '{:,.2f}'.format(float(value_total))
        adj_total = nonZero(self.detailModel.getAdjValue(), 0)
        adj_total = '{:,.2f}'.format(float(adj_total))
        self.v_value_label.setText(value_total)
        self.v_adjValue_label.setText(adj_total)
    
    ### Operations =============   
    def reject(self):
        self.accept()
        
    def accept(self):
        if self.dirty:
            answer = QMessageBox.question(self, "Editing - %s" % localTITLE, "Would you like to save your data?",
                                 QMessageBox.Yes| QMessageBox.No| QMessageBox.Cancel)
            if answer == QMessageBox.Cancel:
                return
            elif answer == QMessageBox.No:
                QDialog.accept(self)
            elif answer == QMessageBox.Yes:
                self.save()
        QDialog.accept(self)
        self.my_parent.formClosed()
        
    def recall(self, journal_id):
        # // first find out if the user is in middle of entering data.
        if self.dirty:
            answer = QMessageBox.question(self, "Editing - %s" % localTITLE, "Would you like to save your data?",
                                 QMessageBox.Yes| QMessageBox.Discard| QMessageBox.Cancel)
            if answer == QMessageBox.Cancel:
                return
            elif answer == QMessageBox.Yes:
                self.save()
                
        self.record_id = journal_id
        self.current_record = self.session.query(AdjustmentHeader).filter(AdjustmentHeader.journal_id==journal_id)
        for field in self.current_record:
            self.adj_dateEdit.setDate(field.journal_date)
            self.v_adjID_label.setText(str(journal_id))
            self.note_textEdit.setText(str(field.journal_memo))
        detailList = self.session.query(AdjRMD).filter(AdjRMD.journal_id==journal_id)
        self.detailModel.load(detailList, field.journal_date, journal_id)
        self.updateSumTotals()
        self.editing = True
        
        
    def save(self):
        journal_id = self.record_id
        journal_type = 'Adjustment'
        qDate = self.adj_dateEdit.date()
        journal_date = qDate.toPyDate()
        journal_memo = str(self.note_textEdit.toPlainText())
        modified_date = QDateTime().currentDateTime().toPyDateTime()
        log_memo = 'Created'
        if self.detailModel.rowCount() <= 1:
            QMessageBox.information(self, 'Save adjustment - %s' % localTITLE, 'No details found.', QMessageBox.Ok)
            return
        if self.editing:
            #// check for closing date issues
            old_date = dLookup(JournalHeader.journal_date, JournalHeader.journal_id==self.record_id)
            if not closingDate(old_date):
                return
            if not closingDate(journal_date):
                return
            log_memo = 'Modified'
            self.current_record = self.session.query(AdjustmentHeader).filter(AdjustmentHeader.journal_id==journal_id)
            self.current_record.update({'journal_date': journal_date, 'journal_memo': journal_memo, 'modified_date': modified_date})
            self.session.query(AdjRMD).filter(AdjRMD.journal_id==journal_id).delete()
        else:
            if not closingDate(journal_date):
                return
            journal_id = dMax(JournalHeader.journal_id) + 1
            self.session.add(AdjustmentHeader(journal_id, journal_type, journal_date, journal_memo, modified_date))
        details = self.detailModel.save(journal_id)
        self.session.add_all(details)
        self.session.add(Logs(journal_id, self.my_parent.user_id, modified_date, log_memo))
        self.sendToDB()
        self.editing = True
        self.record_id = journal_id
        self.dirty = False
        self.setWindowTitle('%s - (Data Saved)' % localTITLE)
    
    def delete(self):
        if not self.record_id:
            return
        old_date = dLookup(JournalHeader.journal_date, JournalHeader.journal_id==self.record_id)
        if not closingDate(old_date):
            return
        answer = QMessageBox.question(self, "Delete - %s" % localTITLE, "Are you sure you " \
                                              "want to delete adjustment: %s, %s ?" % (self.v_adjID_label.text(),
                                                                                self.adj_dateEdit.date()), 
                                              QMessageBox.Yes| QMessageBox.No, QMessageBox.NoButton)
        if answer == QMessageBox.No:
            return
        self.session.query(AdjRMD).filter(AdjRMD.journal_id==self.record_id).delete()
        self.current_record.delete()
        log_memo = 'Deleted - Date: %s, Memo: %s' % (self.adj_dateEdit.date().toPyDate(),
                                                     str(self.note_textEdit.toPlainText()))
        self.session.add(Logs(self.record_id, self.my_parent.user_id, QDateTime().currentDateTime().toPyDateTime(), log_memo))
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
        self.detailModel.clear()
        if self.default_date == 'current':
            self.adj_dateEdit.setDate(QDate.currentDate())
        self.editing = False
        self.dirty = False         
        self.setWindowTitle(localTITLE)
        
        
        


if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    setupDatabase("Production.sqlite")

    form = InventoryAdjForm()
    form.show()
    app.exec_()