# Libraries
import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy import  *
from sqlalchemy.orm import *
# My Imports
import ui_forms.ui_homeform
from functions import *
import modelsandviews

class HomeForm(QDialog, ui_forms.ui_homeform.Ui_homeform):
    
    def __init__(self, batchModel, parent=None):
        super(HomeForm, self).__init__(parent)
        self.setupUi(self)
        
        self.my_parent = parent
        self.batchModel = batchModel
        self.tableView.setModel(self.batchModel)
        self.tableView.setEditTriggers(QTableView.NoEditTriggers)
        self.tableView.setSelectionMode(QTableView.SingleSelection)
        self.tableView.setSelectionBehavior(QTableView.SelectRows)
        
        
        self.supplier_pushButton.clicked.connect(self.supplier)
        self.item_pushButton.clicked.connect(self.item)
        self.receive_pushButton.clicked.connect(self.receive)
        self.batch_pushButton.clicked.connect(self.batch)
        self.production_pushButton.clicked.connect(self.production)
        self.adj_pushButton.clicked.connect(self.adj)
        self.tableView.doubleClicked.connect(self.editBatch)
    
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        if self.tableView.hasFocus():
            refreshAction = menu.addAction("Refresh", QObject)
            refreshAction.triggered.connect(self.refresh)
        menu.exec_(event.globalPos())
        
    def refresh(self):
        self.my_parent.refreshModels()
    
    def reject(self):
        QDialog.reject(self)
        self.my_parent.formClosed()
        
    def editBatch(self):
        row = self.tableView.currentIndex().row()
        index = self.tableView.model().index(row, 0)
        batch_id = self.batchModel.data(index).toInt()[0]
        form = self.my_parent.batchForm()
        form.recall(1, batch_id)
        
    def supplier(self):
        self.my_parent.supplierForm()
    
    def item(self):
        self.my_parent.itemForm()
        
    def receive(self):
        self.my_parent.receiveForm()
    
    def batch(self):
        self.my_parent.batchForm()
        
    def production(self):
        self.my_parent.productionForm()
        
    def adj(self):
        self.my_parent.invAdjustment()
        
        
        
        
        
