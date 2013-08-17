import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy import  *
from sqlalchemy.orm import *

from databaseschema import *
from functions import *
import modelsandviews
import ui_forms.ui_finditemform
import itemform
import reporting


RAW_MATERIAL = 0
FINISHED_GOOD = 1

localTITLE = 'Find Item'

class FindItemForm(QDialog, ui_forms.ui_finditemform.Ui_FindItemForm):
    
    def __init__(self, supModel, itemType=0, parent=None, ascForm=None):
        super(FindItemForm, self).__init__(parent)
        self.setupUi(self)
        self.typeCombo.setCurrentIndex(itemType)
        self.session = Session()
        self.query = None
        self.fieldList = []
        self.reportName = None
        self.columnsToTotal = []
        self.model = None
        self.proxyModel = QSortFilterProxyModel()
        self.myParent = parent
        self.ascForm = ascForm
        
        
        self.sup_comb.setVisible(False)
        self.supplierCombo = modelsandviews.SupplierComboBox(supModel, self)
        self.supplierCombo.setGeometry(QRect(70, 99, 285, 25))
        self.supplierCombo.setTabOrder(self.descLineedit, self.supplierCombo)
        
        catModel = QSqlTableModel(self)
        db = QSqlDatabase.database('prod')
        catModel.setQuery(QSqlQuery('SELECT item FROM lists WHERE type = "itemCategory"', db))
        catModel.select()
        self.category_combo = QComboBox(self)
        self.category_combo.setModel(catModel)
        self.category_combo.setEditable(False)
        self.category_combo.setCurrentIndex(-1)
        self.category_combo.setGeometry(QRect(70, 99, 150, 25))
        self.category_combo.setTabOrder(self.descLineedit, self.supplierCombo)
        
        
        view = self.resultsView
        view.verticalHeader().setVisible(False)
        view.setSelectionMode(QTableView.SingleSelection)
        view.setSelectionBehavior(QTableView.SelectRows)
        
        self.changeLayout()
        
        self.typeCombo.currentIndexChanged.connect(self.changeLayout)
        self.resultsView.doubleClicked.connect(self.edit)
        self.findButton.clicked.connect(self.find)
        self.clearButton.clicked.connect(self.clear)
        self.editButton.clicked.connect(self.edit)
        self.reportButton.clicked.connect(self.printReport)
        self.closeButton.clicked.connect(self.reject)
        
        self.setWindowTitle(localTITLE)
        
    def reject(self):
        QDialog.reject(self)
        self.myParent.formClosed()

        
    def changeType(self, itemType):
        self.typeCombo.setCurrentIndex(itemType)
            
    def changeLayout(self):
        self.clear()
        if self.typeCombo.currentIndex() == RAW_MATERIAL:
            self.supplierLabel.setText('Supplier')
            self.supplierCombo.setVisible(True)
            self.category_combo.setVisible(False)
            self.supplierNumLabel.setVisible(True)
            self.supplierNoLineedit.setVisible(True)
            self.volumeLabel.setVisible(False)
            self.volumeLineedit.setVisible(False)
        elif self.typeCombo.currentIndex() == FINISHED_GOOD:
            self.supplierLabel.setText('Category')
            self.supplierCombo.setVisible(False)
            self.category_combo.setVisible(True)
            self.supplierNumLabel.setVisible(False)
            self.supplierNoLineedit.setVisible(False)
            self.volumeLabel.setVisible(True)
            self.volumeLineedit.setVisible(True)
            
    def resizeView(self):
        self.resultsView.resizeColumnsToContents()
        self.resultsView.horizontalHeader().setStretchLastSection(True)
        self.resultsView.setColumnHidden(0, True)
      
    def find(self):
        tIndex = self.typeCombo.currentIndex()
        desc = str(self.descLineedit.text())
        supplier = dLookup(Suppliers.supplier_id, Suppliers.supplier_name==str(self.supplierCombo.currentText()))
        category_txt = str(self.category_combo.currentText())
        category = dLookup(Lists.id, Lists.item==category_txt)
        item = str(self.itemNumLineedit.text())
        supplierNum = str(self.supplierNoLineedit.text())
        volume = unicode(self.volumeLineedit.text())
        pack = unicode(self.packLineedit.text())
        inactive = self.inactiveCheckbox.isChecked()
        if tIndex == RAW_MATERIAL:
            descFilter = BOM.bom_desc.ilike('%'+desc+'%') if desc else ""
            supplierFilter = BOM.supplier_id == supplier if supplier else ""
            itemFilter = BOM.bom_no.like(item + '%') if item else ""
            supplierNoFilter = BOM.bom_supplier_no == supplierNum if supplierNum else ""
            packFilter = BOM.pack == pack if pack else ""
            
            self.query = self.session.query(BOM).filter(descFilter).filter(supplierFilter).filter(itemFilter) \
                                            .filter(supplierNoFilter).filter(packFilter).filter(BOM.inactive==inactive)
            self.fieldList = [('ID', 'bom_id', 25, 'string'), ('No', 'bom_no', 50, 'string'), ('Description', 'bom_desc', 250, 'string'), 
                              ('Supplier', 'supplier_name', 75, 'string'), ('Pack', 'pack', 25, 'string'), ('Our UOM', 'uom', 25, 'string')]
            self.reportName = 'Bill Of Material List'
            
        elif tIndex == FINISHED_GOOD:
            descFilter = Items.item_desc.ilike('%'+desc+'%') if desc else ""
            itemFilter = Items.item_no.like(item) if item else ""
            categoryFilter = Items.category == category if category else ""
            packFilter = Items.pack == pack if pack else ""
            volumeFilter = Items.volume == volume if volume else ""
            
            self.query = self.session.query(Items).filter(descFilter).filter(itemFilter).filter(packFilter) \
                                            .filter(volumeFilter).filter(categoryFilter).filter(Items.inactive==inactive)
            self. fieldList = [('ID', 'item_id', 25, 'string'), ('No', 'item_no', 50, 'string'), ('Description', 'item_desc', 250, 'string'), 
                         ('Category',' category_txt', 50, 'string'), ('Pack', 'pack', 25, 'string'), ('Volume', 'volume', 50, 'string')]
            self.reportName = 'Item List'
            
        self.model = modelsandviews.FindResultModel(self.fieldList)
        self.model.load(self.query)
        self.proxyModel.setSourceModel(self.model)
        self.resultsView.setModel(self.proxyModel)
        self.resultsView.setSortingEnabled(True)
        self.resultsLabel.setText('%s - Results' % len(self.model.results))
        self.resizeView()
    
    def edit(self):
        if not self.model:
            return
        row = self.resultsView.currentIndex().row()
        recordIndex = self.proxyModel.index(row, 0)
        recordID = self.proxyModel.data(recordIndex).toInt()[0]
        itemType = self.typeCombo.currentIndex() 
        if self.ascForm:
            form, index = self.ascForm
            form.enterBOMNo(index, recordID)
#            self.reject()
        else:
            self.editTransaction(itemType, recordID)
         
    def editTransaction(self, itemType, recordID):
        form = self.myParent.itemForm(itemType)
        form.recall(itemType, recordID)

    
    def printReport(self):
        if not self.model:
            return
        reportModel = reporting.ReportModel('Simple List')
        self.refreshReport(reportModel)
        report_type = 'raw_material' if self.typeCombo.currentIndex() == RAW_MATERIAL else 'finished_good'
        self.myParent.reportForm(reportModel, self, report_type)
        
    def refreshReport(self, model, report=None):
        period = ''
        model.load(self.reportName, period, self.query, self.fieldList, self.columnsToTotal)
            
    def clear(self):
        widgets = self.findChildren(QWidget)
        for widget in widgets:
            if isinstance(widget, (QLineEdit, QTextEdit)):
                widget.clear()
            elif isinstance(widget, QComboBox):
                if widget != self.typeCombo:
                    widget.setCurrentIndex(-1)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(False)
        if self.model is not None:
            self.model.clear()
            
    def formClosed(self):
        self.myParent.formClosed()
                    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    setupDatabase("Production.sqlite")
    supModel = modelsandviews.SupplierModel()
    form = FindItemForm(supModel)
    form.show()
    app.exec_()
        
        
        