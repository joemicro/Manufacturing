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
import ui_forms.ui_batchadjform

class BatchAdjModel(QAbstractTableModel):
    
    def __init__(self, parent=None):
        super(BatchAdjModel, self).__init__(parent)
        self.summarized = []
        self.detail = []
        self.session = Session()
#        self.load()
        
    def rowCount(self, index=QModelIndex()):
        return len(self.summarized)
    
    def columnCount(self, index=QModelIndex):
        return 4
    
    def headerData(self, section, orientation, role):
        if role == Qt.DisplayRole:
            if orientation == Qt.Horizontal:
                if section == 0:
                    return QVariant('ID')
                elif section == 1:
                    return QVariant('Item')
                elif section == 2:
                    return QVariant('Description')
                elif section == 3:
                    return QVariant('Total')
        else:
            return QVariant()
        return QVariant(section + 1)
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.summarized)):
            return QVariant()
        record = self.summarized[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            return QVariant(record[column])
        return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        record = self.summarized[index.row()]
        column = index.column()
        if index.isValid() and role == Qt.EditRole:
            if column == 3:
                record[column] = round(value.toFloat()[0], 4)
            self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True
        return False

    def flags(self, index):
        flag = QAbstractTableModel.flags(self, index)
        if index.column() == 3:
            flag |= Qt.ItemIsEditable
        return flag
    
    def load(self, critList=[]):
        self.clear()
        or_string = ''.join(i for i in critList)[:-2]
        batch_filter = eval("or_(%s)" % or_string) if critList else ""
#        batch_filter = or_(BatchHeader.batch_id=="10", BatchHeader.batch_id=="11")
        
        detail_query = self.session.query(BatchDetail.id, BatchDetail.base_id, BatchDetail.bom_id, BatchDetail.bom_qty,
                                     BOM.bom_no, BOM.bom_desc).join(BOM).join(BatchHeader) \
                                     .filter(batch_filter)
        
        detail_subQuery = detail_query.subquery()
        sum_query = self.session.query(detail_subQuery.c.bom_id, detail_subQuery.c.bom_no, detail_subQuery.c.bom_desc,
                                   func.sum(detail_subQuery.c.bom_qty).label('total')).group_by(detail_subQuery.c.bom_id) \
                                   .order_by(detail_subQuery.c.bom_no)
        for i in detail_query:
            self.detail.append([i[0], i[1], i[2], i[3], i[4], i[5]])
        
        for i in sum_query:
            self.summarized.append([i[0], i[1], i[2], i[3]])
            
    def save(self):
        # // from the summary get the bom_id needing to be changed 
        # // and the fraction by which to multiply in order to get the new amount
        # // fraction == new_total / old_total, and new amount  = (new_total / old_total) * bom_qty
        for i in self.summarized:
            bom_id = i[0]
            new_total = i[3]
            old_total = sum(float(k[3]) for k in self.detail if k[2] == bom_id)
            fraction = float(nonZero(new_total, 0) / nonZero(old_total, 1))
            # // new update amount in detail
            for j in self.detail:
                if j[2] == bom_id:
                    j[3] = float(getType(j[3])) * fraction
                
                
        # // now lets update the database
        for i in self.detail:
            b_id = i[0]
            bom_qty = i[3]
            query = self.session.query(BatchDetail).filter(BatchDetail.id==b_id)
            query.update({'bom_qty': bom_qty})
        
        # // flush session to database
        try:
            self.session.flush
            self.session.commit()
        except Exception, e:
            self.session.rollback()
            raise e
            
    def clear(self):
        self.beginResetModel()
        self.summarized = []
        self.detail = []
        self.endResetModel()
            
       



class BatchAdjForm(QDialog, ui_forms.ui_batchadjform.Ui_batchadjform):
    
    def __init__(self, parent=None):
        super(BatchAdjForm, self).__init__(parent)
        self.setupUi(self)
        self.my_parent = parent
        
        self.refresh_pushButton.setVisible(False)
        
        self.batchListModel = modelsandviews.BatchCkListModel()
        self.batchList_tableView.setModel(self.batchListModel)
        self.batchList_tableView.resizeColumnsToContents()
        self.batchList_tableView.setSelectionMode(QTableView.SingleSelection)
        self.batchList_tableView.setSelectionBehavior(QTableView.SelectRows)
        self.batchList_tableView.clicked.connect(self.checkItem)
        
        delegate = GenericDelegate(self)
        delegate.insertDelegate(3, NumberDelegate())
        
        self.adjModel = BatchAdjModel()
        self.adj_tableView.setModel(self.adjModel)
        self.adj_tableView.setItemDelegate(delegate)
        self.adj_tableView.verticalHeader().setVisible(False)
        self.adj_tableView.setColumnHidden(0, True)
        self.resizeAdjView()
        
        self.saveButton.clicked.connect(self.save)
        self.clearButton.clicked.connect(self.clear)
        self.closeButton.clicked.connect(self.accept)
        self.populate_pushButton.clicked.connect(self.populateAdj)
    
    def reject(self):
        self.accept()
        
    def accept(self):
        QDialog.accept(self)
        self.my_parent.formClosed()
        
    def resizeAdjView(self):
        self.adj_tableView.resizeColumnsToContents()
        self.adj_tableView.setColumnWidth(2, 200)
            
    def checkItem(self, index):
        model = self.batchListModel
        row = index.row()
        i = model.index(row, 0)
        if index.model().data(i, Qt.DisplayRole).toString() != 'P':
            model.setData(i, QVariant('P'), role=Qt.EditRole)
        else:
            model.setData(i, QVariant(), role=Qt.EditRole)
    
    def populateAdj(self):
        crit_list = self.batchListModel.getList()
        self.adjModel.load(crit_list)
        self.resizeAdjView()
                
    def save(self):
        self.adjModel.save()
        
        
    def clear(self):
        self.adjModel.clear()
        self.batchListModel.load()
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    setupDatabase("Production.sqlite")

    form = BatchAdjForm()
    form.show()
    app.exec_()