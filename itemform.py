# Libraries
import sys
import os
from PyQt4.QtSql import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy import  *
from sqlalchemy.orm import *
# My Imports
import ui_forms.ui_itemform
from databaseschema import *
from genericdelegates import *
from functions import *
import modelsandviews
import finditemform

localTITLE = "Item Setup"

### Models setup ==============
RAW_MATERIAL, FINISHED_GOOD = range(2)
ID, BOM_NO, QTY, DESC, COST = range(5)
ID, BASE, PERCENT, DESC, VALUE = range(5)

### Item Assembly Model =====================
class ItemAssemblyModel(QAbstractTableModel):
    
    def __init__(self, parent=None):
        super(ItemAssemblyModel, self).__init__(parent)
        self.items = []
        self.items.append(ItemAssembly())
    
    def rowCount(self, index=QModelIndex()):
        return len(self.items)
    
    def columnCount(self, index=QModelIndex()):
        return 5
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == BOM_NO:
                return QVariant('Item No')
            elif section == QTY:
                return QVariant('Qty')
            elif section == DESC:
                return QVariant('Description')
            elif section == COST:
                return QVariant('Cost')
        return QVariant(section + 1)
    
    def flags(self, index):
        flag = QAbstractTableModel.flags(self, index)
        if index.column() not in (DESC, COST):
            flag |=Qt.ItemIsEditable
        return flag
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.items)):
            return QVariant()
        item = self.items[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == ID:
                return QVariant(item.item_id)
            if column == BOM_NO:
                item_no = dLookup(BOM.bom_no, BOM.bom_id == str(item.bom_id))
                return QVariant(item_no)
            elif column == QTY:
                return QVariant(item.bom_qty)
            elif column == DESC:
                desc = dLookup(BOM.bom_desc, BOM.bom_id==item.bom_id)
                return QVariant(desc)
            elif column == COST:
                return QVariant(item.cost)
        return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            item = self.items[index.row()]
            column = index.column()
            if column == BOM_NO:
                item.bom_id = value.toInt()[0]
                item.cost = self.calcCost(item, None)
            elif column == QTY:
                item.bom_qty = value.toFloat()[0]
            self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True
        return False
    
    ## Calculations
    def filteredList(self, fgdID=None):
        records_ = []
        for record in self.items:
            if record.bom_id:
                if record.item_id == fgdID:
                    item_id = record.item_id
                    bom_id = record.bom_id
                    qty = record.bom_qty
                    cost = record.cost
                    records_ = records_ + [ItemAssembly(item_id, bom_id, qty, cost)]
        return records_
    
    def sumUpCost(self, record):
        cost = getType(record.cost) * getType(record.bom_qty)
        return cost
    
    def getSumCost(self, iterable=None):
        if not iterable:
            iterable = self.items
        sumCost = sum(map(self.sumUpCost, iterable), 0.0)
        return sumCost
    
    def calcCost(self, record, journal_id=None, date=None):
        bom_id = record.bom_id
        if not date:
            date = str(currentDate().date())
        cost = avgCost(bom_id, date, journal_id)
        return cost
    
    def updateCost(self, journal_id=None, date=None):
        self.beginResetModel()
        for record in self.items:
            if record.bom_id:
                record.cost = self.calcCost(record, journal_id, date)
        self.endResetModel()
    
    ## Model operations    
    def insertRows(self, position, rows=1, index=QModelIndex(), item_id=None):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.items.insert(position + row + 1, ItemAssembly(item_id))
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.items = self.items[:position] + self.items[position + rows:]
        self.endRemoveRows()
        return True
    
    def load(self, itemList, clear, itemId=None):
        item_id = itemId
        add = added = False
        if clear:
            self.beginResetModel()
            self.items = []
            self.endResetModel()
        
        if itemId:
            for rec in self.items:
                if not rec.item_id:
                    i = self.items.index(rec)
                    self.items.pop(i)    
        
        for item in itemList:
            if not itemId:
                if item_id != item.item_id:
                    add = True 
                item_id = item.item_id
            try:
                cost = item.cost
            except AttributeError:
                cost = None
            try:
                cost = item.rmds.cost
            except AttributeError:
                cost = None
            bom_id = item.bom_id
            bom_qty = dLookup(ItemAssembly.bom_qty, ItemAssembly.bom_id==bom_id)
            self.items.append(ItemAssembly(item_id, bom_id, bom_qty, cost))
            if add:
                self.items.append(ItemAssembly(item_id)) # add an empty line, every time the item_id changes  
                add = False
                added = True
        if not added:
            self.items.append(ItemAssembly(item_id))
        self.sort()
        
    def sort(self):
        self.items.sort(key=lambda item: item.bom_id, reverse=True)
    
        
    def save(self, itemID=None, instance='ItemAssembly', session=None, date=None, model=None):
        items = []
        adjustments = []
        if instance == 'ItemAssembly':
            evalObject = instance + '(item_id, bom_id, bom_qty)'
        elif instance == 'AssemblyRMD':
            evalObject = instance + '(item_id, bom_id, bom_qty, cost, total)'
            self.updateCost(itemID, str(date))
        elif instance == 'FGDBOMAssembly':
            evalObject = instance + '(item_id, bom_id)'
            self.updateCost(itemID, str(date))
            itemID = None
        for item in self.items:
            if item.bom_id:
                item_id = item.item_id if not itemID else itemID
                bom_id = item.bom_id
                bom_qty = item.bom_qty
                if model:
                    begin_i = model.index(0, 0)
                    indexList = model.match(begin_i, Qt.DisplayRole, QVariant(item.item_id), 1)
                    index = model.index(indexList[0].row(), 2)
                    qty, ok = model.data(index, Qt.DisplayRole).toFloat()
                    if ok:
                        bom_qty = getType(bom_qty) * qty
                cost = item.cost
                total = getType(bom_qty) * getType(cost)
                items = items + [eval(evalObject)]
                if instance == 'AssemblyRMD':
                    adjRmd = adjustAvgCost(session, bom_id, str(date), item_id)
                    if adjRmd:
                        adjustments = adjustments + adjRmd
        if instance == 'AssemblyRMD':
            return (items, adjustments)
        else:
            return items
    
    def clear(self):
        self.beginResetModel()
        self.items = []
        self.items.append(ItemAssembly())
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
    
### BaseAssembly Model =======================   
class BaseAssemblyModel(QAbstractTableModel):
    
    def __init__(self, parent=None):
        super(BaseAssemblyModel, self).__init__(parent)
        self.bases = []
        self.bases.append(BaseAssembly())
    
    def rowCount(self, index=QModelIndex()):
        return len(self.bases)
    
    def columnCount(self, index=QModelIndex()):
        return 5
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == BASE:
                return QVariant('Base No')
            elif section == PERCENT:
                return QVariant('Percent')
            elif section == DESC:
                return QVariant('Description')
            elif section == VALUE:
                return QVariant('Value')
        return QVariant(section + 1)
    
    def flags(self, index):
        flag = QAbstractTableModel.flags(self, index)
        if index.column() not in (DESC, VALUE):
            flag |=Qt.ItemIsEditable
        return flag
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.bases)):
            return QVariant()
        base = self.bases[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == ID:
                return QVariant(base.item_id)
            elif column == BASE:
                base_no = dLookup(BaseHeader.base_no, BaseHeader.base_id == str(base.base_id))
                return QVariant(base_no)
            elif column == PERCENT:
                return QVariant(base.percentage)
            elif column == DESC:
                base_desc = dLookup(BaseHeader.base_desc, BaseHeader.base_id==base.base_id)
                return QVariant(base_desc)
            elif column == VALUE:
                if not base.value:
                    return QVariant(base.value)
                return QVariant(round(base.value, 2))
        return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            base = self.bases[index.row()]
            column = index.column()
            if column == BASE:
                base.base_id = value.toInt()[0]
            elif column == PERCENT:
                percent, ok = value.toFloat()
                if ok:
                    percent = (percent / 100) if percent > 1 else percent
                base.percentage = percent
            elif column == VALUE:
                base.value = value.toFloat()[0]
            self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True
        return False
    
    def insertRows(self, position, rows=1, index=QModelIndex(), item_id=None):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.bases.insert(position + row + 1, BaseAssembly(item_id))
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.bases = self.bases[:position] + self.bases[position + rows:]
        self.endRemoveRows()
        return True
    
    ### Data and Calculations =============
    def filteredList(self, baseID=None, fgdID=None):
        records_ = []
        match = False
        for record in self.bases:
            if record.base_id:
                if baseID or fgdID:
                    if str(record.base_id) == str(baseID) or str(record.item_id) == str(fgdID):
                        match = True
                elif baseID and fgdID:
                    if str(record.base_id) == str(baseID) and str(record.item_id) == str(fgdID):
                        match = True
                        
                if match:
                    item_id = record.item_id
                    base_id = record.base_id
                    percentage = record.percentage
                    value = record.value
                    records_ = records_ + [BaseAssembly(item_id, base_id, percentage, value)]
                    match = False
        return records_
    
    def sumUpValue(self, record):
        assert isinstance(record, BaseAssembly)
        value = getType(record.value)
        return value
        
        
    
    ### Operations ============
    def sort(self):
        self.bases.sort(key=lambda item: item.base_id, reverse=True)
        
    def load(self, itemList, clear=True, itemId=None):
        """ loads data in BaseAssembly Model.
        Takes 'ItemList' a list of data to load
        Takes 'Clear' a boolean if True will clear all data already in the model, Default is True
        Takes 'ItemId' to load into item_id column """
        item_id = itemId
        add = added = False
        
        if clear:
            self.beginResetModel()
            self.bases = []
            self.endResetModel()
        
        if itemId:
            for rec in self.bases:
                if not rec.item_id:
                    i = self.bases.index(rec)
                    self.bases.pop(i)    
        
        for item in itemList:
            if not itemId:
                if item_id != item.item_id:
                    add = True 
                item_id = item.item_id
            
            try:
                value = item.value
            except AttributeError:
                value = None
            
            if isinstance(item, PrepAssembly):
                base_id = dLookup(BatchHeader.base_id, BatchHeader.batch_id == item.batch_id)
            else:
                base_id = item.base_id
                
            percentage = item.percentage

            self.bases.append(BaseAssembly(item_id, base_id, percentage, value))
            
            if add:
                self.bases.append(BaseAssembly(item_id)) # add an empty line, every time the item_id changes  
                add = False
                added = True
        
        if not added:
            self.bases.append(BaseAssembly(item_id))
        self.sort()
    
   
    
    def save(self, itemID=None, instance='BaseAssembly'):
        items = []
        evalObject = instance + '(item_id, base_id, percentage)'
        for base in self.bases:
            if base.base_id:
                item_id = base.item_id if not itemID else itemID
                base_id = base.base_id
                percentage = base.percentage
                items = items + [eval(evalObject)]
        return items
            
    def clear(self):
        self.beginResetModel()
        self.bases = []
        self.bases.append(BaseAssembly())
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
        
#==================================================================
### Form setup ==============
class ItemForm(QDialog, ui_forms.ui_itemform.Ui_ItemForm):
### Initializer ==============
    def __init__(self, supplierModel, itemModel, baseModel, itemType=0, parent=None):
        super(ItemForm, self).__init__(parent)
        self.setupUi(self)
        self.type_comboBox.setCurrentIndex(itemType)
        self.setWindowFlags(Qt.WindowMinMaxButtonsHint)
        
        self.season_combo = QComboBox(self.frame_5)
        self.season_combo.setEditable(False)
        self.season_combo.setCurrentIndex(-1)
        self.season_combo.setGeometry(QRect(70, 198, 150, 25))
        self.setTabOrder(self.price_lineEdit, self.season_combo)
        db = QSqlDatabase.database('prod')
        seasonModel = QSqlTableModel(self)
        seasonModel.setQuery(QSqlQuery('SELECT item FROM lists WHERE type = "season"', db))
        seasonModel.select()
        self.season_combo.setModel(seasonModel)
        
        catModel = QSqlTableModel(self)
        catModel.setQuery(QSqlQuery('SELECT item FROM lists WHERE type = "itemCategory"', db))
        catModel.select()
        self.category_combo = QComboBox()
        self.category_combo.setModel(catModel)
        self.category_combo.setEditable(False)
        self.category_combo.setCurrentIndex(-1)
        self.category_combo.setMinimumSize(QSize(150, 25))
        self.category_combo.setMaximumSize(QSize(150, 25))
        self.gridLayout_2.addWidget(self.category_combo, 0, 1, 1, 1)
        self.setTabOrder(self.season_combo, self.category_combo)

        self.supplierModel = supplierModel
        self.sup_combo.setVisible(False)
        self.supplier_combo = modelsandviews.SupplierComboBox(self.supplierModel)
        self.supplier_combo.setMinimumSize(QSize(150, 25))
        self.supplier_combo.setMaximumSize(QSize(150, 25))
        self.gridLayout_2.addWidget(self.supplier_combo, 1, 1, 1, 1)
        self.setTabOrder(self.supplierno_lineEdit, self.supplier_combo)
        
        self.base = baseModel
        self.baseModel = BaseAssemblyModel()
        self.bsView.setVisible(False)
        self.baseAssembly_view = modelsandviews.AssemblyTableView(self.baseModel, self.base, self.assembly_frame)
        self.baseAssembly_view.setColumnHidden(VALUE, True)
        self.baseAssembly_view.setGeometry(QRect(10, 29, 273, 149))
        
        self.itemModel = itemModel
        self.bomModel = ItemAssemblyModel()
        self.bmView.setVisible(False)
        self.bom_view = modelsandviews.AssemblyTableView(self.bomModel, self.itemModel, self.assembly_frame)
        self.bom_view.setGeometry(QRect(289, 29, 272, 149))


        validator = QDoubleValidator()
        validator.StandardNotation
        self.price_lineEdit.setValidator(validator)
        self.pack_lineEdit.setValidator(validator)
        
        self.dirty = False
        self.editing = False
        self.session = Session()
        self.query = None
        self.current_record = None
        self.record_id = None
        self.mixItem = False
        self.itemType = itemType
        self.myParent = parent
        self.setupConnection()
        
        self.type_comboBox.currentIndexChanged.connect(self.changeLayout)
        self.baseModel.dataChanged.connect(lambda: self.autoAddRow(self.baseAssembly_view, self.baseModel))
        self.bomModel.dataChanged.connect(lambda: self.autoAddRow(self.bom_view, self.bomModel))
        self.itemno_pushButton.clicked.connect(self.itemNum)
        self.connect(self.save_pushButton, SIGNAL("clicked()"), self.save)
        self.connect(self.new_pushButton, SIGNAL("clicked()"), lambda: self.clear(self.type_comboBox.currentIndex()))
        self.connect(self.delete_pushButton, SIGNAL("clicked()"), self.delete)
        self.connect(self.find_pushButton, SIGNAL("clicked()"), self.findItem)
        self.connect(self.close_pushButton, SIGNAL("clicked()"), self.accept)
        
        self.setWindowTitle(localTITLE)
        
        self.changeLayout()
        
### Form Behaviour setup ==============        
    def setupConnection(self):
        """ connect every widget on form to the data changed function, 
        to set the form to dirty """
        widgets = self.findChildren(QWidget)
        for widget in widgets:
            if isinstance(widget, (QLineEdit, QTextEdit)):
                self.connect(widget, SIGNAL("textEdited(QString)"), self.dataChanged)
            elif isinstance(widget, QComboBox):
                self.connect(widget, SIGNAL("currentIndexChanged(int)"), self.dataChanged)
            elif isinstance(widget, QCheckBox):
                self.connect(widget, SIGNAL("stateChanged(int)"), self.dataChanged)
    
    def changeLayout(self):
        """ setup the form layout, based on type of item user wants to enter"""
        cIndex = self.type_comboBox.currentIndex()
        if self.type_comboBox.currentIndex() == FINISHED_GOOD:
            self.itemno_pushButton.setVisible(False)
            self.mixitem_checkBox.setVisible(False)
            self.hachsher_label.setText('Season')
            self.hachsher_lineEdit.setVisible(False)
            self.season_combo.setVisible(True)
            self.supplierNo_label.setText('Category')
            self.supplierno_lineEdit.setVisible(False)
            self.supplier_label.setVisible(False)
            self.supplier_combo.setVisible(False)
            self.measure_label.setVisible(False)
            self.measure_lineEdit.setVisible(False)  
            self.category_combo.setVisible(True)
            self.uom_label.setText('Volume')
            self.assembly_frame.setVisible(True)
            self.qbFrame.setVisible(False)
        else:
            self.itemno_pushButton.setVisible(True)
            self.mixitem_checkBox.setVisible(True)
            self.hachsher_label.setText('Hachsher')
            self.hachsher_lineEdit.setVisible(True)
            self.season_combo.setVisible(False)
            self.supplierNo_label.setText('Supplier No.')
            self.supplierno_lineEdit.setVisible(True)
            self.supplier_label.setVisible(True)
            self.supplier_combo.setVisible(True)
            self.measure_label.setVisible(True)
            self.measure_lineEdit.setVisible(True)
            self.category_combo.setVisible(False)
            self.uom_label.setText('Our UOM')
            self.assembly_frame.setVisible(False)
            self.qbFrame.setVisible(True)
        self.clear(cIndex)
        
    def dataChanged(self):
        self.dirty = True
        self.setWindowTitle("%s - Editing..." % localTITLE)
        
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        if self.baseAssembly_view.hasFocus() or self.bom_view.hasFocus():
            if self.baseAssembly_view.hasFocus():
                view = self.baseAssembly_view
                model = self.baseModel
            elif self.bom_view.hasFocus():
                view = self.bom_view
                model = self.bomModel
            else:
                view = None
                model = None
            insertAction = menu.addAction('Insert Line')
            deleteAction = menu.addAction('Delete Line')
            insertAction.triggered.connect(lambda: self.insertRow(view, model))
            deleteAction.triggered.connect(lambda: self.removeRow(view, model))
        menu.exec_(event.globalPos())
        
    def autoAddRow(self, view, model):
        row = view.currentIndex().row()
        if model.rowCount() == row + 1:
            self.insertRow(view, model)
                
    def insertRow(self, view=None, model=None):
        if view is not None:
            index = view.currentIndex()
            row = index.row()
            model.insertRows(row)
            view.setFocus()
            view.setCurrentIndex(index)
    
    def removeRow(self, view=None, model=None):
        row = view.currentIndex().row()
        model.removeRows(row)
        if model.rowCount() < 1:
            self.insertRow(view, model)
    
    def itemNum(self):
        """ creates an item number by taking the letter passed in by the user
        and returns the letter plus a max number from the database"""
        code, ok = QInputDialog.getText(self, 'Create Item Number - %s' % localTITLE, 'Please type your item code letter:', 
                                    QLineEdit.Normal, "")
        if not ok:
            return
        if not code:
            return
        code = str(code)
        stmt = self.session.query(func.substr(BOM.bom_no, 2), BOM.bom_no).filter(func.substr(BOM.bom_no, 1, 1).ilike(code))
        code_list = []
        for i in stmt:
            code_list += [int(getType(i[0]))]
        if code_list:
            n = max(code_list) + 1
        else:
            n = 1
        itemCode = code.upper() + str(n)
        self.itemno_lineEdit.setText(itemCode)
            
### Form Operations setup ==============    
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
        self.myParent.formClosed()
        
    def save(self):
        if self.type_comboBox.currentIndex() == RAW_MATERIAL:
            supplier = str(self.supplier_combo.currentText())
            supplier_id = dLookup(Suppliers.supplier_id, Suppliers.supplier_name == supplier)
            bom_no = str(self.itemno_lineEdit.text())
            bom_desc = str(self.desc_textEdit.toPlainText())
            bom_cost = unicode(self.price_lineEdit.text())
            hachsher = str(self.hachsher_lineEdit.text())
            bom_supplier_no = str(self.supplierno_lineEdit.text())
            measure = str(self.measure_lineEdit.text())
            pack = unicode(self.pack_lineEdit.text())
            uom = str(self.uom_lineEdit.text())
            inactive = self.inactive_checkBox.isChecked()
            mix_item = self.mixitem_checkBox.isChecked()
            qb_parent_path = str(self.qbParent_lineEdit.text())
            qb_account = unicode(self.qbAccount_lineEdit.text())
            if not bom_no:
                QMessageBox.information(self, "Save - " % localTITLE, "Please sepcify an item number before saving",
                                        QMessageBox.Ok)
                return
            if self.editing:
                self.current_record.update({'supplier_id': supplier_id, 'bom_no': bom_no, 'bom_desc': bom_desc,
                                            'bom_cost': bom_cost, 'hachsher': hachsher, 'bom_supplier_no': bom_supplier_no,
                                            'measure': measure, 'pack': pack, 'uom': uom, 'inactive': inactive, 'mix_item': mix_item,
                                            'qb_parent_path': qb_parent_path, 'qb_account': qb_account})
                if mix_item:
                    old_bom_no = dLookup(BOM.bom_no, BOM.bom_id==self.record_id)
                    self.session.query(Items).filter(Items.item_no==old_bom_no).update({'item_no': bom_no, 'item_desc': bom_desc})
            else:
                bomNum = dLookup(BOM.bom_no, BOM.bom_no == bom_no)
                if bomNum:
                    QMessageBox.information(self, 'Save - %s' % localTITLE, 'Item %s already exists' % bomNum, QMessageBox.Ok)
                    return
                bom = BOM(None, supplier_id, bom_no, bom_desc, bom_cost, hachsher, bom_supplier_no, 
                           measure, pack, uom, inactive, mix_item, qb_parent_path, qb_account)
                self.session.add(bom)
                
                if mix_item:
                    item_id = dMax(Items.item_id) + 1
                    item = Items(item_id, bom_no, bom_desc, "", '', '', '', '', inactive, mix_item)
                    self.session.add(item)
            i = 0 #provide index for clear function
            
        elif self.type_comboBox.currentIndex() == FINISHED_GOOD:
            item_no = str(self.itemno_lineEdit.text())
            item_desc = str(self.desc_textEdit.toPlainText())
            volume = unicode(self.uom_lineEdit.text())
            pack = unicode(self.pack_lineEdit.text())
            item_cost = unicode(self.price_lineEdit.text())
            season_txt = str(self.season_combo.currentText())
            category_txt = str(self.category_combo.currentText())
            season = dLookup(Lists.id, Lists.item==season_txt)
            category = dLookup(Lists.id, Lists.item==category_txt)
            inactive = self.inactive_checkBox.isChecked()
            mix_item = self.mixitem_checkBox.isChecked()
            if not item_no:
                QMessageBox.information(self, 'Save - %s' % localTITLE, 'Please specify an item number before saving', QMessageBox.Ok)
                return
            if self.editing:
                item_id = self.record_id
                self.session.query(ItemAssembly).filter(ItemAssembly.item_id==item_id).delete(False)
                self.session.query(BaseAssembly).filter(BaseAssembly.item_id==item_id).delete(False)
                if mix_item:
                    self.current_record.update({'volume': volume, 'pack': pack, 'item_cost': item_cost, 'season': season, 'category': category})
                else:
                    self.current_record.update({'item_no': item_no, 'item_desc': item_desc, 'volume': volume,
                                                'pack': pack, 'item_cost': item_cost, 'season': season, 'category': category,
                                                'inactive': inactive, 'mix_item': mix_item})
            else:
                item_id = dMax(Items.item_id) + 1
                itemNum = dLookup(Items.item_no, Items.item_no==item_no)
                if itemNum:
                    QMessageBox.information(self, 'Save - %s' % localTITLE, 'Item already exists', QMessageBox.Ok)
                    return
                item = Items(item_id, item_no, item_desc, volume, pack, item_cost, season, category, inactive, mix_item)
                self.session.add(item)
            boms = self.bomModel.save(item_id)
            bases = self.baseModel.save(item_id, 'BaseAssembly')
            self.session.add_all(boms)
            self.session.add_all(bases)
            i = 1
        try:
            self.session.flush()
            self.session.commit()
        except Exception, e:
            self.session.rollback()
            raise e
        self.clear(i)
        
    def findItem(self):
        itemType = self.type_comboBox.currentIndex()
        self.myParent.findItem(itemType)
    
    def recall(self, itemType, itemId):
        # // first find out if the user is in middle of entering data.
        if self.dirty:
            answer = QMessageBox.question(self, "Editing - %s" % localTITLE, "Would you like to save your data?",
                                 QMessageBox.Yes| QMessageBox.Discard| QMessageBox.Cancel)
            if answer == QMessageBox.Cancel:
                return
            elif answer == QMessageBox.Yes:
                self.save()
                
        self.type_comboBox.setCurrentIndex(itemType)
        if itemType == RAW_MATERIAL:
            self.current_record = self.session.query(BOM).filter(BOM.bom_id==itemId)
            for item in self.current_record:
                text = dLookup(Suppliers.supplier_name, Suppliers.supplier_id==item.supplier_id)
                if text:
                    index = self.supplier_combo.findText(text, Qt.MatchExactly)
                    self.supplier_combo.setCurrentIndex(index)
                self.itemno_lineEdit.setText(str(item.bom_no))
                self.desc_textEdit.setText(str(item.bom_desc))
                self.price_lineEdit.setText(str(item.bom_cost))
                self.hachsher_lineEdit.setText(str(item.hachsher))
                self.supplierno_lineEdit.setText(str(item.bom_supplier_no))
                self.measure_lineEdit.setText(str(item.measure))
                self.pack_lineEdit.setText(str(item.pack))
                self.uom_lineEdit.setText(str(item.uom))
                self.inactive_checkBox.setChecked(item.inactive)
                self.mixitem_checkBox.setChecked(item.mix_item)
                self.qbParent_lineEdit.setText(str(item.qb_parent_path))
                self.qbAccount_lineEdit.setText(str(item.qb_account))
                if item.mix_item:
                    self.mixItem= True
        elif itemType == FINISHED_GOOD:
            self.current_record = self.session.query(Items).filter(Items.item_id==itemId)
            for item in self.current_record:
                self.itemno_lineEdit.setText(str(item.item_no))
                self.desc_textEdit.setText(str(item.item_desc))
                self.price_lineEdit.setText(str(item.item_cost))
                season = dLookup(Lists.item, Lists.id==item.season)
                index = self.season_combo.findText(str(season), Qt.MatchExactly)
                self.season_combo.setCurrentIndex(index)
                category = dLookup(Lists.item, Lists.id==item.category)
                index = self.category_combo.findText(str(category), Qt.MatchExactly)
                self.category_combo.setCurrentIndex(index)
                self.pack_lineEdit.setText(str(item.pack))
                self.uom_lineEdit.setText(str(item.volume))
                self.inactive_checkBox.setChecked(item.inactive)
                self.mixitem_checkBox.setChecked(item.mix_item)
                if item.mix_item:
                    self.mixItem = True
            baseList = self.session.query(BaseAssembly).filter(BaseAssembly.item_id==itemId)
            itemList = self.session.query(ItemAssembly).filter(ItemAssembly.item_id==itemId)
            self.baseModel.load(baseList, True)
            self.bomModel.load(itemList, True)
        self.record_id = itemId
        self.itemType = itemType
        self.editing = True
        self.dirty = False
        self.setWindowTitle(localTITLE)
    
    def checkItemUsed(self):
        if self.itemType == 1:
            fgd = dLookup(FGD.item_id, FGD.item_id==self.record_id)
            if fgd:
                return True
        elif self.itemType == 0:
            base = dLookup(BaseDetail.bom_id, BaseDetail.bom_id==self.record_id)
            batch = dLookup(BatchDetail.bom_id, BatchDetail.bom_id==self.record_id)
            fgd_bom = dLookup(FGDBOMAssembly.bom_id, FGDBOMAssembly.bom_id==self.record_id)
            rmd = dLookup(RMD.bom_id, RMD.bom_id==self.record_id)
            item_assem = dLookup(ItemAssembly.bom_id, ItemAssembly.bom_id==self.record_id)
            if base or batch or fgd_bom or rmd or item_assem:
                return True
        return False
    
    def delete(self):
        if self.editing == True:
            used = self.checkItemUsed()
            if used:
                QMessageBox.information(self, "Delete - %s" % localTITLE, 'Item is used, can\'t delete', 
                                            QMessageBox.Ok)
                return
            if self.mixItem:
                if self.itemType == 1:
                    QMessageBox.information(self, "Delete - %s" % localTITLE, 'Please delete mix items from the raw material form', 
                                            QMessageBox.Ok)
                    return
            answer = QMessageBox.question(self, "Delete - %s" % localTITLE, "Are you sure you " \
                                          "want to delete item: %s" % self.desc_textEdit.toPlainText(), 
                                          QMessageBox.Yes| QMessageBox.No, QMessageBox.NoButton)
            if answer == QMessageBox.No:
                return
            bom_no = dLookup(BOM.bom_no, BOM.bom_id==self.record_id)
            self.session.query(Items).filter(Items.item_no==bom_no).delete()
            self.current_record.delete()
            try:
                self.session.flush
                self.session.commit()
            except Exception, e:
                self.session.rollback()
                raise e
            self.clear()
            
    def clear(self, cIndex=0):
        widgets = self.findChildren(QWidget)
        for widget in widgets:
            if isinstance(widget, (QLineEdit, QTextEdit)):
                widget.clear()
            elif isinstance(widget, QComboBox):
                if widget.objectName() != self.type_comboBox.objectName():
                    widget.setCurrentIndex(-1)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(False)
        self.type_comboBox.setCurrentIndex(cIndex)
        self.baseModel.clear()
        self.bomModel.clear()
        self.myParent.refreshModels()
        self.dirty = False
        self.editing = False     
        self.mixItem = False    
        self.setWindowTitle(localTITLE)
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    setupDatabase("Production.sqlite")
    supModel = modelsandviews.SupplierModel()
    itmModel = modelsandviews.ItemModel('BOM')
    bsModel = modelsandviews.BaseListModel()
    form = ItemForm(supModel, itmModel, bsModel, 0)
    form.show()
    app.exec_()