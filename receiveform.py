import sys
import os
from PyQt4.QtSql import *
import ui_forms.ui_receiveform
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy import  *
from sqlalchemy.orm import *
from databaseschema import *
import modelsandviews
import genericdelegates
from functions import *

localTITLE = "Receiving"

#==============================================================================
### Model Setup ============== 
(ITEM, DESCRIPTION, QTY, PRICE, SHIPPING, COST, TOTAL, CAD_TOTAL, MEMO) = range(9)

class ReceivingDetailModel(QAbstractTableModel):
 
### Model Initializer ==============    
    def __init__(self, session, parent=None):
        super(ReceivingDetailModel, self).__init__(parent)
        self.records = []
        self.records.append(ReceiveRMD())
        self.shippingRate = 0
        self.currencyRate = 1
        self.journal_date = None
        self.session = session
        
    def setDate(self, date):
        self.journal_date = date

### Base Implemantations ==============   
    def rowCount(self, index=QModelIndex()):
        return len(self.records)
    
    def columnCount(self, index=QModelIndex()):
        return 9
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == ITEM:
                return QVariant("Item")
            elif section == DESCRIPTION:
                return QVariant("Description")
            elif section == QTY:
                return QVariant('Qty (KG,LT)')
            elif section == PRICE:
                return QVariant("Price")
            elif section == SHIPPING:
                return QVariant("Shipping")
            elif section == COST:
                return QVariant("Cost")
            elif section == TOTAL:
                return QVariant("Total")
            elif section == MEMO:
                return QVariant("Memo")
            elif section == CAD_TOTAL:
                return QVariant('CAD Total')
        return QVariant(section + 1)
    
    def flags(self, index):
        flag = QAbstractTableModel.flags(self, index)
        if index.column() not in (COST, SHIPPING, CAD_TOTAL):
            flag |= Qt.ItemIsEditable
        return flag
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.records)):
            return QVariant()
        record = self.records[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == ITEM:
                item_no = dLookup(BOM.bom_no, BOM.bom_id==record.bom_id)
                return QVariant(item_no)
            elif column == DESCRIPTION:
                return QVariant(record.rmd_desc)
            elif column == QTY:
                if not record.qty:
                    return QVariant(record.qty)
                return QVariant(round(record.qty, 4))
            elif column == PRICE:
                if not record.cost_native:
                    return QVariant(record.cost_native)
                return QVariant(round(getType(record.cost_native), 4))
            elif column == SHIPPING:
                if not record.rmd_shipping:
                    return QVariant(record.rmd_shipping)
                return QVariant(round(getType(record.rmd_shipping), 2))
            elif column == COST:
                if not record.cost:
                    return QVariant(record.cost)
                return QVariant(round(getType(record.cost), 2))
            elif column == TOTAL:
                if not record.native_total:
                    return QVariant(record.native_total)
                return QVariant(round(getType(record.native_total), 2))
            elif column == CAD_TOTAL:
                if not record.total:
                    return QVariant(record.total)
                return QVariant(round(getType(record.total), 2))
            elif column == MEMO:
                return QVariant(record.rmd_memo)
        return QVariant()
        
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            record = self.records[index.row()]
            column = index.column()
            if column == ITEM:
                item = value.toInt()[0]
                record.bom_id = item
                record.rmd_desc = dLookup(BOM.bom_desc, 
                                                     BOM.bom_id==item)
                record.cost_native = dLookup(BOM.bom_cost, 
                                                 BOM.bom_id==item)
                self.checkPrice(record)
            elif column == DESCRIPTION:
                record.rmd_desc = value.toString()
            elif column == QTY:
                qty, ok = value.toFloat()
                if not ok:
                    return False
                record.qty = qty
                record.rmd_shipping = self.calcShipping(record)
                record.cost = self.calcCost(record)
                record.native_total = self.calcNTotal(record)
                record.total = self.calcTotal(record)
            elif column == PRICE:
                price, ok = value.toFloat()
                if not ok:
                    return False
                record.cost_native = price
                record.rmd_shipping = self.calcShipping(record)
                record.cost = self.calcCost(record)
                record.native_total = self.calcNTotal(record)
                record.total = self.calcTotal(record)
                self.checkPrice(record)
            elif  column == TOTAL:
                total, ok = value.toFloat()
                if not ok:
                    return
                record.cost_native = self.calcPrice(record, total)
                record.rmd_shipping = self.calcShipping(record)
                record.cost = self.calcCost(record)
                record.native_total = self.calcNTotal(record)
                record.total = self.calcTotal(record)
                self.checkPrice(record)
            elif column == MEMO:
                record.rmd_memo = value.toString()
            self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True
        return False
    
    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.records.insert(position + row + 1, ReceiveRMD())
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.records = self.records[:position] + self.records[position + rows:]
        self.endRemoveRows()
        return True
   
### Data and Calculations ==============         
    def calcPrice(self, record, total):
        qty = getType(record.qty)
        return abs(total / qty)
    
    def calcCost(self, record):
        price = getType(record.cost_native)
        shipping = getType(record.rmd_shipping)
        return price + shipping
    
    def calcShipping(self, record):
        price = getType(record.cost_native)
        rate = self.shippingRate
        return price * rate
    
    def calcNTotal(self, record):
        price = getType(record.cost_native)
        shipping = getType(record.rmd_shipping)
        qty = getType(record.qty)
        return (price + shipping) * qty
    
    def calcTotal(self, record):
        price = getType(record.cost_native)
        shipping = getType(record.rmd_shipping)
        qty = getType(record.qty)
        exRate = getType(nonZero(self.currencyRate, 1))
        return (price + shipping) * qty * exRate
    
    def updateDetailModel(self, shipping=1, currency=1):
        assert isinstance(shipping, float)
        self.beginResetModel()
        for record in self.records:
            if record.bom_id:
                record.rmd_shipping = getType(record.cost_native) * shipping
                record.cost = self.calcCost(record)
                record.native_total = self.calcNTotal(record)
                record.total = self.calcTotal(record)
        self.shippingRate = shipping
        self.currencyRate = currency
        self.endResetModel()
    
    def getSumTotal(self):
        return sum(map(calculate_total, self.records), 0.0)
    
    def checkPrice(self, record):
        if not self.journal_date:
            return
        where = Settings.setting=='check_price'
        on = dLookup(Settings.bool_value, where) # // this returns a string, so we need to eval to convert to binery
        if not eval(on):
            return
        price_query = self.session.query(ReceiveRMD.id, ReceiveRMD.bom_id, ReceiveRMD.cost_native, JournalHeader.journal_date) \
                                        .join(JournalHeader) \
                                        .filter(JournalHeader.journal_date<=self.journal_date) \
                                        .filter(ReceiveRMD.bom_id==record.bom_id) \
                                        .order_by(JournalHeader.journal_date.desc()).first()
        if not price_query:
            return
        price_diff = dLookup(Settings.value_1, where)
        price_diff = float(getType(price_diff))
        price = float(getType(price_query[2]))
        if abs(price - float(getType(record.cost_native))) >= price_diff:
            QMessageBox.information(None, 'Check Price', 'Last price i have for this item is: %s, \n ' \
                                    'please make sure your price is correct' % price, 
                                    QMessageBox.Ok)
    
### Operations ============== 
    def clear(self):
        self.beginResetModel()
        self.records = []
        self.records.append(ReceiveRMD())
        self.endResetModel()
        
    def save(self, journal_id, date, journal_type='Bill'):
        #// update price on bom_table if setting is on
        update_price = dLookup(Settings.bool_value, Settings.setting=='update_price')
        if eval(update_price):
            for record in self.records:
                self.session.query(BOM).filter(BOM.bom_id==record.bom_id).update({'bom_cost': unicode(record.cost_native)})
        
        records_ = []
        adjustments = []
        for record in self.records:
            if record.bom_id:
                bom_id = int(record.bom_id)
                rmd_desc = str(record.rmd_desc)
                qty = float(record.qty)
                price = unicode(record.cost_native)
                cost = unicode(record.cost)
                shipping = unicode(record.rmd_shipping)
                rmd_memo = str(record.rmd_memo) if record.rmd_memo else ""
                total = unicode(record.total)
                native_total = unicode(record.native_total)
                records_ += [ReceiveRMD(journal_id, bom_id, rmd_desc, qty, cost, price, shipping, rmd_memo, total, native_total)]
                if journal_type == 'Credit':
                    cost = None
                adjRmd = adjustAvgCost(self.session, bom_id, str(date), journal_id, cost)
                if adjRmd:
                    adjustments += adjRmd
        return (records_, adjustments)
    
    def load(self, objectList):
        self.beginResetModel()
        self.records = []
        self.endResetModel()
        for item in objectList:
            bom_id = item.bom_id
            rmd_desc = item.rmd_desc
            qty = float(item.qty)
            rmd_shipping = float(nonZero(item.rmd_shipping, 0))
            cost = float(item.cost)
            cost_native = cost * (1 - (rmd_shipping / cost))
            total = float(getType(item.total))
            native_total = float(getType(item.native_total))
            memo = item.rmd_memo
            self.records.append(ReceiveRMD(None, bom_id, rmd_desc, qty, cost, cost_native, rmd_shipping, memo, total, native_total))
        self.records.append(ReceiveRMD())
    
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
                desc = col[1] if len(col) >= 2 else dLookup(BOM.bom_desc, BOM.bom_id==bom_id)
                qty = float(getType(col[2])) if len(col) >= 3 else None
                price = float(getType(col[3])) if len(col) >= 4 else None
                myList += [ReceiveRMD(None, bom_id, desc, qty, price)]
        rowCount = len(myList)
        self.beginInsertRows(QModelIndex(), position, position + rowCount - 1)
        for row in range(rowCount):
                self.records.insert(position + row, myList[row])
        self.endInsertRows()
        self.updateDetailModel(1.0)
        return True

        
    
#==============================================================================
### Form Setup ==============             
def calculate_total(record):
    assert isinstance(record, ReceiveRMD)
    total = record.native_total
    if isinstance(total, QString):
        total = record.native_total.toFloat()[0]
    elif not total:
        total = 0
    return float(total)

   
class ReceiveForm(QDialog, ui_forms.ui_receiveform.Ui_ReceiveForm):

### Initializer =============   
    def __init__(self, supplierModel, bomModel, parent=None):
        super(ReceiveForm, self).__init__(parent)
        self.setupUi(self)
        self.session = Session()
        self.my_parent = parent
        
        self.supplierModel = supplierModel
        self.supcom.setVisible(False)
        self.supplier_comboBox = modelsandviews.SupplierComboBox(self.supplierModel)
        self.supplier_comboBox.setMaximumSize(QSize(197, 25))
        self.supplier_comboBox.setMinimumSize(QSize(197, 25))
        self.gridLayout_2.addWidget(self.supplier_comboBox, 0, 1, 1, 2)
        self.setTabOrder(self.note_textEdit, self.supplier_comboBox)
        
        self.date_dateEdit.setDate(self.my_parent.getDate())
        self.curr_lineEdit.setText("1")
        self.amount_lineEdit.setText('0.00')
        self.receive_radioButton.setChecked(True)
        self.export_checkBox.setChecked(True)
        self.supplier_comboBox.setFocus()

        self.itemModel = bomModel
        self.itemView = modelsandviews.SupplierView(self.supplierModel)
        
        self.detailModel = ReceivingDetailModel(self.session)
        self.receive_tableView.setModel(self.detailModel)
        delegate = genericdelegates.GenericDelegate(self)
        delegate.insertDelegate(ITEM, genericdelegates.ComboDelegate(self.itemModel, True))
        delegate.insertDelegate(DESCRIPTION, genericdelegates.PlainTextDelegate())
        delegate.insertDelegate(QTY, genericdelegates.NumberDelegate())
        delegate.insertDelegate(PRICE, genericdelegates.NumberDelegate())
        delegate.insertDelegate(MEMO, genericdelegates.PlainTextDelegate())
        tblView = self.receive_tableView
        tblView.setItemDelegate(delegate)
        tblView.setColumnWidth(ITEM, 50)
        tblView.setColumnWidth(DESCRIPTION, 200)
        tblView.setColumnWidth(QTY, 70)
        tblView.setColumnWidth(PRICE, 70)
        tblView.setColumnWidth(SHIPPING, 70)
        tblView.setColumnWidth(COST, 100)
        tblView.setColumnWidth(TOTAL, 100)
        tblView.setColumnWidth(MEMO, 200)
        self.receive_tableView.setColumnHidden(CAD_TOTAL, True)
        tblView.horizontalHeader().setStretchLastSection(True)
        
    
        self.detailModel.dataChanged.connect(self.autoAddRow)
        self.shipping_lineEdit.editingFinished.connect(self.updateDetailModel)
        self.curr_lineEdit.editingFinished.connect(self.updateDetailModel)
        self.detailModel.dataChanged.connect(self.updateSumTotal)
        self.billno_lineEdit.editingFinished.connect(self.checkBillNo)
        self.supplier_comboBox.currentIndexChanged.connect(self.changeLayout)
        self.date_dateEdit.dateChanged.connect(self.setModelDate)
        self.date_dateEdit.dateChanged.connect(self.setParentDate)
        
        self.newButton.clicked.connect(self.clear)
        self.saveButton.clicked.connect(self.save)
        self.deleteButton.clicked.connect(self.delete)
        self.calcButton.clicked.connect(self.updateDetailModel)
        self.findButton.clicked.connect(self.find)
        self.closeButton.clicked.connect(self.accept)
        self.receive_tableView.doubleClicked.connect(self.findBomID)

        self.setupConnection()
        self.setModelDate()
        self.dirty = False
        self.editing = False
        self.record_id = None
        self.current_record = None
        
        
        
### Form Behaviour =============
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
        self.updateDetailModel()
        self.dirty = True
        self.setWindowTitle("%s - Editing..." % localTITLE) 
        
    def setParentDate(self):
        date = self.date_dateEdit.date().toPyDate()
        self.my_parent.setDate(date)   
        
    def setModelDate(self):
        date = self.date_dateEdit.date().toPyDate()
        self.detailModel.setDate(date)
        
    def changeLayout(self):
        supplier = str(self.supplier_comboBox.currentText())
        if not supplier:
            cur = 'CAD'
        else:
            cur = dLookup(Suppliers.currency, Suppliers.supplier_name==supplier)
            
        if cur == 'USD':
            self.receive_tableView.setColumnHidden(CAD_TOTAL, False)
        else:
            self.receive_tableView.setColumnHidden(CAD_TOTAL, True)
                 
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        if self.receive_tableView.hasFocus():
            copyAction = menu.addAction('Copy', QObject, 'Ctrl+C')
            pasteAction = menu.addAction('Paste', QObject, 'Ctrl+V')
            insertAction = menu.addAction("Insert Line", QObject, "Ctrl+I")
            deleteAction = menu.addAction("Delete Line", QObject, "Ctrl+D")
            copyAction.triggered.connect(self.copy)
            pasteAction.triggered.connect(self.paste)
            self.connect(insertAction, SIGNAL("triggered()"), self.insertRow)
            self.connect(deleteAction, SIGNAL("triggered()"), self.removeRow)
            addActions(self, self.receive_tableView, (insertAction, deleteAction))
        menu.exec_(event.globalPos())
    
    
    def copy(self):
        if self.detailModel.rowCount() <= 1:
            return
        selectedItems = self.receive_tableView.selectionModel().selectedIndexes()
        self.detailModel.copy(selectedItems)
        
    def paste(self):
        row = self.receive_tableView.currentIndex().row()
        self.detailModel.paste(row)
        self.updateSumTotal()
             
    def autoAddRow(self):
        view = self.receive_tableView
        row = view.currentIndex().row()
        if self.detailModel.rowCount() ==  row + 1:
            self.insertRow()
            
    def insertRow(self):
        view = self.receive_tableView
        index = view.currentIndex()
        row = index.row()
        self.detailModel.insertRows(row)
        view.setFocus()
        view.setCurrentIndex(index)
    
    def removeRow(self):
        view = self.receive_tableView
        rowsSelected = view.selectionModel().selectedRows()
        if not rowsSelected:
            row = view.currentIndex().row()
            rows = 1
        else:
            for i in rowsSelected:
                row = i.row()
            rows = len(rowsSelected)
            row = row - rows + 1
        self.detailModel.removeRows(row, rows)
        if self.detailModel.rowCount() < 1:
            self.insertRow()
        
    def findBomID(self):
        row = self.receive_tableView.currentIndex().row()
        index = self.detailModel.index(row, 0)
        self.my_parent.findItem(0, (self, index), localTITLE)
    
    def enterBOMNo(self, index, bomID):
        i = 0
        ok = True
        while ok:
            myIndex = self.detailModel.index(index.row() + i, index.column())
            bom = self.detailModel.data(myIndex).toString()
            if not bom:
                ok = False
            i += 1
        self.receive_tableView.setCurrentIndex(myIndex)
        self.detailModel.setData(myIndex, QVariant(bomID))
        
        
### Data and Calculations =============  
    def updateDetailModel(self):
        shipping_str = str(self.shipping_lineEdit.text()) if not self.shipping_lineEdit.text() == "" else 0
        gst_str = str(self.gst_lineEdit.text()) if not self.gst_lineEdit.text() == "" else 0
        qst_str = str(self.qst_lineEdit.text()) if not self.qst_lineEdit.text() == "" else 0
        total_str = str(self.total_lineEdit.text()) if not self.total_lineEdit.text() == "" else 0
        currency_str = str(self.curr_lineEdit.text()) if not self.curr_lineEdit.text() == "" else 1
        try:
            shipping = float(shipping_str) / nonZero(nonZero(float(total_str), 0
                                              ) - nonZero(float(gst_str), 0
                                              ) - nonZero(float(qst_str), 0
                                              ) - nonZero(float(shipping_str), 0), 1)
            currency = float(currency_str)
        except ValueError:
            return
        self.detailModel.updateDetailModel(shipping, currency)
        self.updateSumTotal()
        
    def updateSumTotal(self):
        sum_total = QString('%L1').arg(self.detailModel.getSumTotal(), 0, 'f', 2)
        self.amount_lineEdit.setText(sum_total)


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
        
        
    def checkBillNo(self):
        if not self.billno_lineEdit.isModified():
            return
        self.billno_lineEdit.setModified(False)
        billNo = str(self.billno_lineEdit.text())
        supplier = str(self.supplier_comboBox.currentText())
        supplier_id = dLookup(Suppliers.supplier_id, Suppliers.supplier_name==supplier)
        ckBillNo = dLookup(ReceiveHeader.journal_no, 
                           (ReceiveHeader.journal_no==billNo and ReceiveHeader.supplier_id==supplier_id))
        if ckBillNo:
            QMessageBox.information(self, localTITLE, 'Bill Number already exists for this vendor.', buttons=QMessageBox.Ok)
        
             
    def save(self):
        #// Prepare the items to be recorded
        journal_id = self.record_id
        journal_type = 'Bill'
        if self.return_radioButton.isChecked():
            journal_type = 'Credit'
        qDate = self.date_dateEdit.date()
        journal_date = qDate.toPyDate()
        journal_no = str(self.billno_lineEdit.text())
        journal_memo = str(self.note_textEdit.toPlainText())
        supplier = str(self.supplier_comboBox.currentText())
        supplier_id = dLookup(Suppliers.supplier_id, Suppliers.supplier_name==supplier)
        journal_total = unicode(self.total_lineEdit.text())
        currency_rate = unicode(self.curr_lineEdit.text())
        shipping = unicode(self.shipping_lineEdit.text())
        gst = unicode(self.gst_lineEdit.text())
        qst = unicode(self.qst_lineEdit.text())
        export = self.export_checkBox.isChecked()
        modified_date = QDateTime().currentDateTime().toPyDateTime()
        log_memo = 'Created'
        #//  do some checks
        if not supplier_id:
            QMessageBox.information(self, 'Save bill - %s' % localTITLE, 'Please specify a supplier.', QMessageBox.Ok)
            return
        if self.detailModel.rowCount() <= 1:
            QMessageBox.information(self, 'Save bill - %s' % localTITLE, 'No details found.', QMessageBox.Ok)
            return
        detailTotal = float(unicode(self.amount_lineEdit.text().replace(',','')))
        detailTotal = float(detailTotal + getType(gst) + getType(qst))
        totalDiff = float(getType(journal_total)) - detailTotal
        if abs(totalDiff) > .05:
            QMessageBox.information(self, 'Save bill - %s' % localTITLE, "Total doesn't match.")
            return
        #// do differently if new record or old record
        if self.editing:
            #// check for closing date issues
            old_date = dLookup(JournalHeader.journal_date, JournalHeader.journal_id==self.record_id)
            if not closingDate(old_date):
                return
            if not closingDate(journal_date):
                return
            log_memo = 'Modified'
            self.current_record = self.session.query(ReceiveHeader).filter(ReceiveHeader.journal_id==journal_id)
            self.current_record.update({'journal_type': journal_type, 'journal_date': journal_date, 'journal_no': journal_no,
                                        'journal_memo': journal_memo, 'supplier_id': supplier_id, 'journal_total': journal_total,
                                        'currency_rate': currency_rate, 'shipping': shipping, 'gst': gst, 'qst': qst,
                                        'export': export, 'modified_date': modified_date})
            self.session.query(ReceiveRMD).filter(ReceiveRMD.journal_id==self.record_id).delete()
        else:
            if not closingDate(journal_date):
                return
            journal_id = dMax(JournalHeader.journal_id) + 1
            self.session.add(ReceiveHeader(journal_id, journal_type, journal_date, journal_no, journal_memo,
                                           supplier_id, journal_total, currency_rate, shipping, gst, qst, modified_date, export))
        details, adjustments = self.detailModel.save(journal_id, journal_date, journal_type)
        self.session.add_all(details)
        self.session.add_all(adjustments)
        self.session.add(Logs(journal_id, self.my_parent.user_id, modified_date, log_memo))
        self.sendToDB()
        self.editing = True
        self.record_id = journal_id
        self.dirty = False
        self.setWindowTitle('%s - (Data Saved)' % localTITLE)
    
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
        self.current_record = self.session.query(ReceiveHeader).filter(ReceiveHeader.journal_id==journal_id)
        for field in self.current_record:
            text = dLookup(Suppliers.supplier_name, Suppliers.supplier_id==field.supplier_id)
            if text:
                index = self.supplier_comboBox.findText(text, Qt.MatchExactly)
                self.supplier_comboBox.setCurrentIndex(index)
            self.note_textEdit.setText(field.journal_memo)
            self.curr_lineEdit.setText(str(field.currency_rate))
            self.transid_lineEdit.setText(str(journal_id))
            self.date_dateEdit.setDate(field.journal_date)
            self.billno_lineEdit.setText(str(field.journal_no))
            self.shipping_lineEdit.setText(str(field.shipping))
            self.total_lineEdit.setText(str(field.journal_total))
            self.receive_radioButton.setChecked(True)
            if field.journal_type == 'Credit':
                self.return_radioButton.setChecked(True)
            self.gst_lineEdit.setText(str(field.gst))
            self.qst_lineEdit.setText(str(field.qst))
            self.export_checkBox.setChecked(field.export)
        objectList = self.session.query(ReceiveRMD).filter(ReceiveRMD.journal_id==journal_id)
        self.detailModel.load(objectList)
        self.updateSumTotal()
        self.editing = True
        
    
    def delete(self):
        if not self.record_id:
            return
        #// check for closing date issues
        old_date = dLookup(JournalHeader.journal_date, JournalHeader.journal_id==self.record_id)
        if not closingDate(old_date):
            return
        answer = QMessageBox.question(self, "Delete - %s" % localTITLE, "Are you sure you " \
                                              "want to delete bill: %s:, %s" % (self.supplier_comboBox.currentText(),
                                                                                self.billno_lineEdit.text()), 
                                              QMessageBox.Yes| QMessageBox.No, QMessageBox.NoButton)
        if answer == QMessageBox.No:
            return
        self.session.query(ReceiveRMD).filter(ReceiveRMD.journal_id==self.record_id).delete()
        self.current_record.delete()
        log_memo = 'Deleted - Supplier: %s, Date: %s, Bill: %s Amount %s' % (str(self.supplier_comboBox.currentText()),
                                                                    self.date_dateEdit.date().toPyDate(),
                                                                    str(self.billno_lineEdit.text()),
                                                                    str(self.total_lineEdit.text()))
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
        
    def find(self):
        self.my_parent.findForm()
        
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
        if defaultDate() == 'current':
            self.date_dateEdit.setDate(QDate.currentDate())
        self.editing = False
        self.dirty = False         
        self.setWindowTitle(localTITLE)
            
            
             
    
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    setupDatabase("Production.sqlite")
    form = ReceiveForm()
    form.show()
    app.exec_()