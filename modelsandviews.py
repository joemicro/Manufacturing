import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from sqlalchemy import  *
from sqlalchemy.orm import *
from databaseschema import *
import genericdelegates



## Quick Model =======================
class QuickModel(QAbstractTableModel):
    """ header_data format = ('header', 'True') True/False if editable"""
    
    def __init__(self, headerData, parent=None):
        super(QuickModel, self).__init__(parent)
        self.records = []
        self.header_data = headerData
        
    def rowCount(self, index=QModelIndex()):
        return len(self.records)
    
    def columnCount(self, index=QModelIndex()):
        return len(self.header_data)
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            return QVariant(self.header_data[section][0])
        return QVariant(section + 1)
        
    def flags(self, index):
        flag = QAbstractTableModel.flags(self, index)
        if self.header_data[index.column()][1]:
            flag |= Qt.ItemIsEditable
        return flag
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.records)):
            return QVariant()
        row = index.row()
        column = index.column()
        if role == Qt.DisplayRole:
            if len(self.records[row]) > 1:
                return QVariant(self.records[row][column])
            else:
                return QVariant(self.records[row])
        return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            row = index.row()
            column = index.column()
            self.records[row][column] = value.toString()
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
            return True
        return False
    
    def insertRows(self, position, rows=1, value=None, index=QModelIndex()):
        """ value most be list, with amount of fields equaling the amount of fields in header list """
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.records.insert(position + row + 1, value)
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        if rows == self.rowCount():
            rows -= 1
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.records = self.records[:position] + self.records[position + rows:]
        self.endRemoveRows()
        return True
    
    def clear(self):
        self.beginResetModel()
        self.records = []
        self.endResetModel()
        
    def save(self):
        return self.records
    
    def load(self, objectList):
        self.clear()
        for i in objectList:
            self.records.append(i)
            
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
        
    
    
## Date Range ComboBox ===============
class DateRangeComboBox(QComboBox):
    def __init__(self, parent=None):
        super(DateRangeComboBox, self).__init__(parent)
        dateRange = QStringList()
        dateRange << 'All' << 'Today' << 'This Month' << 'This Year' << 'Last Month' << 'Last Year'
        self.addItems(dateRange)
        self.setCurrentIndex(-1)

## User Model ComboBox ===============        
class UserComboBox(QComboBox):

    def __init__(self, model, parent=None):
        super(UserComboBox, self).__init__(parent)
        self.view = UserView(model)
        self.setModel(model)
        self.setView(self.view)
        self.setModelColumn(1)
        self.setCurrentIndex(-1)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.lineEdit().editingFinished.connect(self.validate)
        
    def validate(self):
        text = self.lineEdit().text()
        if self.findText(text, Qt.MatchRegExp) == -1:
            self.lineEdit().setText("")
            
        

class UserModel(QSqlTableModel):
              
    def __init__(self, parent=None):
        super(UserModel, self).__init__(parent)
        self.select()
        self.setHeaderData(0, Qt.Horizontal, QVariant("ID"))
        self.setHeaderData(1, Qt.Horizontal, QVariant("Name"))
    
    def select(self):
        db = QSqlDatabase.database('prod')
        query = QSqlQuery('SELECT user_id, user_name FROM users ' \
                          'ORDER BY users.user_name', db)
        self.setQuery(query)
        self.setSort(1, Qt.AscendingOrder)
    



class UserView(QTableView):
    
    def __init__(self, model, parent=None):
        super(UserView, self).__init__(parent)
    
        self.setModel(model)
        self.verticalHeader().setVisible(False)
        self.setSelectionMode(QTableView.SingleSelection)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setColumnHidden(0, True)
        self.setColumnHidden(2, True)
        self.resize()
        self.horizontalHeader().setStretchLastSection(True)
        
    def resize(self):
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
    
    def index(self):
        return self.currentIndex()
        
        
## Supplier Model ComboBox ===============        
class SupplierComboBox(QComboBox):

    def __init__(self, model, parent=None):
        super(SupplierComboBox, self).__init__(parent)
        self._view = SupplierView(model)
        self.setModel(model)
        self.setView(self._view)
        self.setModelColumn(1)
        self.setCurrentIndex(-1)
        self.setEditable(True)
        self.setInsertPolicy(QComboBox.NoInsert)
        self.view().setFixedWidth(300)
        self.lineEdit().editingFinished.connect(self.validate)
        
        
    def validate(self):
        text = self.lineEdit().text()
        if self.findText(text, Qt.MatchRegExp) == -1:
            self.lineEdit().setText("")
            
        
class SupplierModel(QSqlTableModel):
    
    def __init__(self, parent=None):
        super(SupplierModel, self).__init__(parent)
        self.select()
        self.setHeaderData(0, Qt.Horizontal, QVariant("ID"))
        self.setHeaderData(1, Qt.Horizontal, QVariant("Name"))
        self.setHeaderData(2, Qt.Horizontal, QVariant('Currency'))
        
    def select(self):
        db = QSqlDatabase.database('prod')
        query = QSqlQuery('SELECT supplier_id, supplier_name, currency FROM supplier_list ' \
                          'ORDER BY supplier_list.supplier_name', db)
        self.setQuery(query)
        

class SupplierView(QTableView):
    
    def __init__(self, model, parent=None):
        super(SupplierView, self).__init__(parent)
        self.setModel(model)
        self.verticalHeader().setVisible(False)
        self.setSelectionMode(QTableView.SingleSelection)
        self.setSelectionBehavior(QTableView.SelectRows)
        self.setColumnHidden(0, True)
        self.resize()
        self.horizontalHeader().setStretchLastSection(True)
        
    def resize(self):
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
    
    def index(self):
        return self.currentIndex()
    

## Base List Model ===============  
class BaseListModel(QSqlTableModel):
    
    def __init__(self, parent=None):
        super(BaseListModel, self).__init__(parent)
        self.select()
        self.setHeaderData(1, Qt.Horizontal, QVariant('Base No'))
        self.setHeaderData(2, Qt.Horizontal, QVariant('Description'))
        
    def select(self):
        db = QSqlDatabase.database('prod')
        query = QSqlQuery('SELECT base_id, base_no, base_desc FROM base_header ' \
                          'ORDER BY base_header.base_no', db)
        self.setQuery(query)

## Prep List Model ========================
class PrepListModel(QSqlTableModel):
    def __init__(self, parent=None):
        super(PrepListModel, self).__init__(parent)
        self.select()
        self.setHeaderData(0, Qt.Horizontal, QVariant('Prep ID'))
        self.setHeaderData(1, Qt.Horizontal, QVariant('Date'))
        
    def select(self):
        db = QSqlDatabase.database('prod')
        query = QSqlQuery('SELECT prep_id, prep_date FROM prep_header ' \
                          'WHERE prep_header.prod_id IS NULL ' \
                          'ORDER BY prep_header.prep_date', db)
        self.setQuery(query)
        
                
## Outstanding Batch List Model ===========
class BatchListModel(QSqlTableModel):
    
    def __init__(self, parent=None):
        super(BatchListModel, self).__init__(parent)
        self.select()
        self.setHeaderData(0, Qt.Horizontal, QVariant('Batch ID'))
        self.setHeaderData(1, Qt.Horizontal, QVariant('Base No.'))
        self.setHeaderData(2, Qt.Horizontal, QVariant('Date'))
        self.setHeaderData(3, Qt.Horizontal, QVariant('Description'))
        
    def select(self):
        sql = 'SELECT batch_header.batch_id, base_header.base_no, batch_header.batch_date, base_header.base_desc ' \
                'FROM batch_header ' \
                'LEFT JOIN base_header ON batch_header.base_id = base_header.base_id ' \
                'WHERE batch_header.journal_id isNull ' \
                'ORDER BY batch_header.batch_id'
        db = QSqlDatabase.database('prod')
        query = QSqlQuery(sql, db)
        self.setQuery(query)
        self.setSort(0, Qt.AscendingOrder)
        

## Item List Model and view ===============        
class ItemModel(QSqlTableModel):
    
    def __init__(self, itemType, parent=None):
        super(ItemModel, self).__init__(parent)
        self.itemType = itemType
        self.select()
        self.setHeaderData(0, Qt.Horizontal, QVariant("ID"))
        self.setHeaderData(1, Qt.Horizontal, QVariant("Item"))
        self.setHeaderData(2, Qt.Horizontal, QVariant("Description"))
        self.removeColumns(3, 9)
        
    def select(self):
        if self.itemType == 'BOM':
            sql = 'SELECT bom_id, bom_no, bom_desc FROM bom WHERE bom.inactive == 0 ORDER BY bom.bom_no'
        elif self.itemType == 'Items':
            sql = 'SELECT item_id, item_no, item_desc FROM item_list WHERE item_list.inactive == 0 ORDER BY item_list.item_no'
        db = QSqlDatabase.database('prod')
        query = QSqlQuery(sql, db)
        self.setQuery(query)
        self.setSort(1, Qt.AscendingOrder)
        
        

class ItemView(QTableView):
    
    def __init__(self, model, hide=True, parent=None):
        super(ItemView, self).__init__(parent)
        self.model = model
        self.setModel(self.model)
        self.verticalHeader().setVisible(False)
        self.setSelectionMode(QTableView.SingleSelection)
        self.setSelectionBehavior(QTableView.SelectRows)
        if hide:
            self.setColumnHidden(0, True)
        self.resize()
        self.horizontalHeader().setStretchLastSection(True)
        
    def resize(self):
        self.resizeColumnsToContents()
        self.resizeRowsToContents()
    
    def index(self):
        return self.currentIndex()
    

## Union Item list model With checkable column ===============
class UnionItemList(object):
    def __init__(self, iBool, iId, iNum, iDesc, iType):
        self.iBool = iBool
        self.iId = iId
        self.iNum = iNum
        self.iDesc = iDesc
        self.iType = iType
           
class UnionItemListModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(UnionItemListModel, self).__init__(parent)
        self.records = []
        self.session = Session()
        self.load()
        
    def rowCount(self, index=QModelIndex()):
        return len(self.records)
    
    def columnCount(self, index=QModelIndex()):
        return 5
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return QVariant('P')
                elif section == 1:
                    return QVariant('ID')
                elif section == 2:
                    return QVariant('Item')
                elif section == 3:
                    return QVariant('Description')
                elif section == 4:
                    return QVariant('Type')
        elif role == Qt.FontRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return QVariant(QFont('Wingdings 2', 12))
        else:
            return QVariant()
        return QVariant(section + 1)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.records)):
            return QVariant()
        record = self.records[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == 0:
                return QVariant(record.iBool)
            elif column == 1:
                return QVariant(record.iId)
            elif column == 2:
                return QVariant(record.iNum)
            elif column == 3:
                return QVariant(record.iDesc)
            elif column == 4:
                return QVariant(record.iType)
        if role == Qt.FontRole:
            if column == 0:
                return QVariant(QFont('Wingdings 2', 12))
        return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            record = self.records[index.row()]
            column = index.column()
            if column == 0:
                record.iBool = value.toString()
            self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True
        return False
    
    def load(self):
        self.clear()
        bomItem = self.session.query(BOM.bom_id, BOM.bom_no, BOM.bom_desc, literal_column('"BOM"').label('Type')) \
                                        .filter(BOM.inactive==False)
        FGItem = self.session.query(Items.item_id, Items.item_no, Items.item_desc, literal_column('"Item"').label('Type')) \
                                    .filter(Items.inactive==False)
        union = bomItem.union(FGItem).order_by('Type').order_by(BOM.bom_no)
        for i in union:
            self.records.append(UnionItemList(None, i.bom_id, i.bom_no, i.bom_desc, i.Type))
            
    def getList(self):
        records_ = []
        for rec in self.records:
            if rec.iBool == 'P':
                records_ += ['unionQuery.c.itemNo=="%s", ' % rec.iNum]
        return records_
    
    def clear(self):
        self.beginResetModel()
        self.records = []
        self.endResetModel()


### Batch List model with checkable column ===================       
class BatchCkListModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(BatchCkListModel, self).__init__(parent)
        self.records = []
        self.session = Session()
        self.load()
        
    def rowCount(self, index=QModelIndex()):
        return len(self.records)
    
    def columnCount(self, index=QModelIndex()):
        return 5
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return QVariant('P')
                elif section == 1:
                    return QVariant('ID')
                elif section == 2:
                    return QVariant('Base')
                elif section == 3:
                    return QVariant('Description')
                elif section == 4:
                    return QVariant('Date')
        elif role == Qt.FontRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return QVariant(QFont('Wingdings 2', 12))
        else:
            return QVariant()
        return QVariant(section + 1)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.records)):
            return QVariant()
        record = self.records[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == 4:
                return QVariant(QDate(record[4]))
            else:
                return QVariant(record[column])
        if role == Qt.FontRole:
            if column == 0:
                return QVariant(QFont('Wingdings 2', 12))
        return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            record = self.records[index.row()]
            column = index.column()
            if column == 0:
                record[0] = value.toString()
            self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True
        return False
    
    def load(self):
        self.clear()
        query = self.session.query(BatchHeader.batch_id, BaseHeader.base_no, BaseHeader.base_desc, BatchHeader.batch_date) \
                                    .join(BaseHeader).filter(BatchHeader.journal_id==None)
        for i in query:
            self.records.append([None, i[0], i[1], i[2], i[3]]) # // needs to be a list because can't change value if tuple
        
            
    def getList(self):
        records_ = []
        for rec in self.records:
            if rec[0] == 'P':
                records_ += ['BatchHeader.batch_id=="%s", ' % rec[1]]
        return records_
    
    def clear(self):
        self.beginResetModel()
        self.records = []
        self.endResetModel()
                
### Supplier model with checkable column ===================       
class SupplierListModel(QAbstractTableModel):
    def __init__(self, parent=None):
        super(SupplierListModel, self).__init__(parent)
        self.records = []
        self.session = Session()
        self.load()
        
    def rowCount(self, index=QModelIndex()):
        return len(self.records)
    
    def columnCount(self, index=QModelIndex()):
        return 4
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return QVariant('P')
                elif section == 1:
                    return QVariant('ID')
                elif section == 2:
                    return QVariant('Name')
                elif section == 3:
                    return QVariant('Currency')
        elif role == Qt.FontRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return QVariant(QFont('Wingdings 2', 12))
        else:
            return QVariant()
        return QVariant(section + 1)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.records)):
            return QVariant()
        record = self.records[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == 0:
                return QVariant(record.selected)
            elif column == 1:
                return QVariant(record.suppler_id)
            elif column == 2:
                return QVariant(record.supplier_name)
            elif column == 3:
                return QVariant(record.currency)
        if role == Qt.FontRole:
            if column == 0:
                return QVariant(QFont('Wingdings 2', 12))
        return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            record = self.records[index.row()]
            column = index.column()
            if column == 0:
                record.selected = value.toString()
            self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True
        return False
    
    def load(self):
        self.clear()
        query = self.session.query(Suppliers)
        for i in query:
            self.records.append(Suppliers(i.supplier_name, i.currency, i.supplier_id, None))
        
            
    def getList(self):
        records_ = []
        for rec in self.records:
            if rec.selected == 'P':
                records_ += ['unionQuery.c.supplierId=="%s", ' % rec.supplier_id]
        return records_
    
    def clear(self):
        self.beginResetModel()
        self.records = []
        self.endResetModel()
        
               
## Assembly TableView Subclass (used for item assembly, and base assembly)
class AssemblyTableView(QTableView):
    ID, ITEM, QTY, DESC = range(4)
    def __init__(self, model, itemModel, parent=None):
        super(AssemblyTableView, self).__init__(parent)
        
        self.setModel(model)
        delegate = genericdelegates.GenericDelegate(self)
        delegate.insertDelegate(self.ITEM, genericdelegates.ComboDelegate(itemModel, True))
        delegate.insertDelegate(self.QTY, genericdelegates.NumberDelegate())
        self.setItemDelegate(delegate)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setStretchLastSection(True)
        self.setColumnHidden(self.ID, True)
        self.setColumnWidth(self.ITEM, 75)
        self.setColumnWidth(self.QTY, 50)
        self.setColumnWidth(self.DESC, 100)

        
### Delegate Widgets, reimplemented for keyPress event purposes.
class ItemComboBox(QComboBox):
    def __init__(self, parent=None):
        super(ItemComboBox, self).__init__(parent)
        self.widget_parent = parent.parent()
        
    def keyPressEvent(self, event):
        key = event.key()
        if self.widget_parent:
            index = self.widget_parent.currentIndex()
            row = index.row()
            col = index.column()
            if key == Qt.Key_Down:
                self.close()
                index = self.widget_parent.model().index(row + 1, col)
                focusChange = self.changeFocus(index)
                if not focusChange:
                    index = self.widget_parent.model().index(row, col)
                    self.changeFocus(index)
            elif key == Qt.Key_Up:
                self.close()
                index = self.widget_parent.model().index(row - 1, col)
                focusChange = self.changeFocus(index)
                if not focusChange:
                    index = self.widget_parent.model().index(row, col)
                    self.changeFocus(index)
            elif key == Qt.Key_Right:
                self.close()
                index = self.widget_parent.model().index(row, col + 1)
                focusChange = self.changeFocus(index)
                if not focusChange:
                    for i in range(self.widget_parent.model().columnCount() - col):
                        index = self.widget_parent.model().index(row, col + i + 1)
                        focusChange = self.changeFocus(index)
                        if focusChange:
                            break
                    if not focusChange:
                        index = self.widget_parent.model().index(row + 1, 0)
                        self.changeFocus(index)
                        if not focusChange:
                            index = self.widget_parent.model().index(row + 1, 1)
                            self.changeFocus(index)
            elif key == Qt.Key_Left:
                self.close()
                index = self.widget_parent.model().index(row, col - 1)
                focusChange = self.changeFocus(index)
                if not focusChange:
                    index = self.widget_parent.model().index(row, col - 2)
                    focusChange = self.changeFocus(index)
                    if not focusChange:
                        index = self.widget_parent.model().index(row, col)
                        self.changeFocus(index)
            else:
                QComboBox.keyPressEvent(self, event)
        else:
            QComboBox.keyPressEvent(self, event)
    
    def changeFocus(self, index):
        if index.isValid():
            self.widget_parent.setFocus()
            self.widget_parent.setCurrentIndex(index)
            flags = self.widget_parent.model().flags(index)
            if flags & Qt.ItemIsEditable:
                self.widget_parent.edit(index)
                return True
        return False
    
class MyLineEdit(QLineEdit):
    def __init__(self, parent=None):
        super(MyLineEdit, self).__init__(parent)
        self.widget_parent = parent.parent()
        
    def keyPressEvent(self, event):
        key = event.key()
        if self.widget_parent:
            index = self.widget_parent.currentIndex()
            row = index.row()
            col = index.column()
            if key == Qt.Key_Down:
                self.close()
                index = self.widget_parent.model().index(row + 1, col)
                self.changeFocus(index)
            elif key == Qt.Key_Up:
                self.close()
                index = self.widget_parent.model().index(row - 1, col)
                focusChange = self.changeFocus(index)
                if not focusChange:
                    index = self.widget_parent.model().index(row, col)
                    self.changeFocus(index)
            elif key == Qt.Key_Right:
                self.close()
                index = self.widget_parent.model().index(row, col + 1)
                focusChange = self.changeFocus(index)
                if not focusChange:
                    for i in range(self.widget_parent.model().columnCount() - col):
                        index = self.widget_parent.model().index(row, col + i + 1)
                        focusChange = self.changeFocus(index)
                        if focusChange:
                            break
                    if not focusChange:
                        index = self.widget_parent.model().index(row + 1, 0)
                        self.changeFocus(index)
                        if not focusChange:
                            index = self.widget_parent.model().index(row + 1, 1)
                            self.changeFocus(index)
            elif key == Qt.Key_Left:
                self.close()
                index = self.widget_parent.model().index(row, col - 1)
                focusChange = self.changeFocus(index)
                if not focusChange:
                    index = self.widget_parent.model().index(row, col - 2)
                    focusChange = self.changeFocus(index)
                    if not focusChange:
                        index = self.widget_parent.model().index(row, col)
                        self.changeFocus(index)
            else:
                QLineEdit.keyPressEvent(self, event)
        else:
            QLineEdit.keyPressEvent(self, event)
    
    def changeFocus(self, index):
        if index.isValid():
            self.widget_parent.setFocus()
            self.widget_parent.setCurrentIndex(index)
            flags = self.widget_parent.model().flags(index)
            if flags & Qt.ItemIsEditable:
                self.widget_parent.edit(index)
                return True
        return False
        
            
## Find results model ===============
class FindResultModel(QAbstractTableModel):
    def __init__(self, fieldList, parent=None):
        super(FindResultModel, self).__init__(parent)
        self.results = []
        self.columns = len(fieldList)
        self.fieldList = fieldList
        
    def rowCount(self, index=QModelIndex()):
        return len(self.results)
    
    def columnCount(self, index=QModelIndex()):
        return self.columns
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            i = 0
            while i < self.columns:
                key = self.fieldList[i][0]
                if section == i:
                    return QVariant(key)
                i += 1
        return QVariant(section + 1)
                
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.results)):
            return QVariant()
        result = self.results[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            i = 0
            while i <= self.columns:
                field = self.fieldList[i][1]
                field = 'result.' + field
                if column == i:
                    value = unicode(eval(field))
                    if self.fieldList[i][3] == 'number':
                        value = '{:,.2f}'.format(float(value))
                    return QVariant(value)
                i += 1
        return QVariant()
    
    def load(self, objectList):
        for object in objectList:
            self.results.append(object)
        
    def clear(self):
        self.beginResetModel()
        self.results = []
        self.endResetModel()