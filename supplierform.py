import os
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy import  *
from sqlalchemy.orm import *
from databaseschema import *
from functions import *
import modelsandviews



localTITLE = "Supplier Setup"

class SupplierForm(QDialog):
    
    def __init__(self, model, parent=None):
        super(SupplierForm, self).__init__(parent)
        
        label_3 = QLabel("Recall Supplier")
        self.model = model
        self.view = modelsandviews.SupplierView(self.model)
        self.recall_supplier = modelsandviews.SupplierComboBox(self.model)
        label_3.setBuddy(self.recall_supplier)
        label_1 = QLabel("Name")
        self.suppliername_lineEdit = QLineEdit()
        label_1.setBuddy(self.suppliername_lineEdit)
        label_2 = QLabel("Currency")
        self.supplier_currency = QComboBox()
        self.supplier_currency.addItems(("CAD", "USD", "EU"))
        label_2.setBuddy(self.supplier_currency)
        frame = QFrame()
        hLine = QFrame()
        hLine.setFrameShape(QFrame.HLine)
        hLine.setFrameShadow(QFrame.Sunken)
        
        self.save_button = QPushButton("&Save New")
        self.delete_button = QPushButton("&Delete")
        self.close_button = QPushButton("C&lose")
        
        self.save_button.setIcon(QIcon(':/icons/save'))
        self.delete_button.setIcon(QIcon(':/icons/delete'))
        self.close_button.setIcon(QIcon(':/icons/exit'))
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.save_button)
        buttonLayout.addWidget(self.delete_button)
        buttonLayout.addWidget(self.close_button)
        spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        buttonLayout.setContentsMargins(11, 25, 11, 11)
        buttonLayout.addSpacerItem(spacer)
        fieldlayout = QGridLayout()
        fieldlayout.addWidget(label_3, 0, 0, 1, 1)
        fieldlayout.addWidget(self.recall_supplier, 0, 1 ,1 ,3)
        fieldlayout.addWidget(frame, 1, 1, 1, 3)
        fieldlayout.addWidget(label_1, 2, 0,1 ,1)
        fieldlayout.addWidget(self.suppliername_lineEdit, 2, 1, 1, 3)
        fieldlayout.addWidget(label_2, 3, 0, 1, 1)
        fieldlayout.addWidget(self.supplier_currency, 3, 1, 1, 3)
        vlayout = QVBoxLayout()
        vlayout.addLayout(fieldlayout)
        vlayout.addWidget(hLine)
        vlayout.addLayout(buttonLayout)
        vlayout.addSpacerItem(spacer)
        layout = QHBoxLayout()
        layout.addLayout(vlayout)
        layout.addSpacerItem(spacer)
        self.setLayout(layout)
   
        self.setWindowIcon(QIcon(':/icons/account'))
        self.setWindowTitle(localTITLE)
        self.dirty = False
        self.editing = False
        self.session = Session()
        self.query = self.session.query(Suppliers)
        self.current_record = None
        self.record_id = None
        self.my_parent = parent
        
        self.connect(self.save_button, SIGNAL("clicked()"), self.save)
        self.connect(self.close_button, SIGNAL("clicked()"), self.accept)
        self.connect(self.delete_button, SIGNAL("clicked()"), self.delete)
        self.connect(self.recall_supplier, SIGNAL("activated(int)"), self.recall)
        self.connect(self.supplier_currency, SIGNAL("currentIndexChanged(int)"), self.dataChanged)
        self.connect(self.suppliername_lineEdit, SIGNAL("textEdited(QString)"), self.dataChanged)
        self.connect(self.recall_supplier, SIGNAL("keyPressEvent(QKeyEvent*)"), self.verify)
        
    def verify(self):
        text = self.recall_supplier.currentText()
        index = self.recall_supplier.findText(text)
        if index == -1:
            print "index not valid"
    
    def dataChanged(self):
        """ set form to dirty, as soon as some data is changed"""
        self.dirty = True
        self.setWindowTitle("%s - Editing..." % localTITLE)
        
    
    def reject(self):
        self.accept()
    
    def accept(self):
        """ close form, and save changes"""
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
        
        

    def save(self):
        """ save record, or clear form if no data has been modified"""
        
        if not self.dirty:
            self.clear()
            return
        # if data was edited, save information
        s_name = str(self.suppliername_lineEdit.text())
        s_curr = str(self.supplier_currency.currentText())
        if not s_name:
            QMessageBox.information(self, "Save - %s" % localTITLE, "Please sepcify a supplier name before saving",
                                    QMessageBox.Ok)
            return
        if self.editing:
            self.current_record.update({'supplier_name': s_name, 'currency': s_curr})
        else:
            # check if supplier already exists.
            supplier = dLookup(Suppliers.supplier_name, Suppliers.supplier_name==s_name)
            if supplier:
                QMessageBox.information(self, 'Save - %s' % localTITLE, 'Supplier already exists in list', QMessageBox.Ok)
                return
            supplier = Suppliers(s_name, s_curr)
            self.session.add(supplier)
        exception = None
        try:
            self.session.flush()
        except ValueError, e:
            exception = e
            self.session.rollback()
        finally:
            self.session.commit()
            if exception is not None:
                raise exception
        self.clear()
        
        
    def recall(self, row):
        """ recall record """
        # // first find out if the user is in middle of entering data.
        if self.dirty:
            answer = QMessageBox.question(self, "Editing - %s" % localTITLE, "Would you like to save your data?",
                                 QMessageBox.Yes| QMessageBox.Discard| QMessageBox.Cancel)
            if answer == QMessageBox.Cancel:
                return
            elif answer == QMessageBox.Yes:
                self.save()
                
        i_index = self.model.index(row, 0)
        record = self.model.data(i_index).toString()
        if not record:
            self.clear()
            return
        record = str(record)
        self.current_record = self.query.filter_by(supplier_id=record)
        for supplier in self.current_record :
            self.suppliername_lineEdit.setText(supplier.supplier_name)
            self.supplier_currency.setCurrentIndex(self.supplier_currency.findText(
                                                supplier.currency, Qt.MatchExactly))
            self.record_id = supplier.supplier_id
        self.editing = True
    
    def delete(self):
        if self.record_id:
            used = dLookup(BOM.supplier_id, BOM.supplier_id==self.record_id)
            rcv = dLookup(ReceiveHeader.supplier_id, ReceiveHeader.supplier_id==self.record_id)
            if used or rcv:
                QMessageBox.information(self, "Delete - %s" % self.localTITLE, "Can't delete supplier," \
                                            "because it was already used elsewhere", QMessageBox.Ok)
                return
            answer = QMessageBox.question(self, "Delete - %s" % localTITLE, "Are you sure you " \
                                          "want to delete item: %s" % self.suppliername_lineEdit.text(), 
                                          QMessageBox.Yes| QMessageBox.No, QMessageBox.NoButton)
            if answer == QMessageBox.No:
                return
            self.current_record.delete()
            exception = None
            try:
                self.session.flush()
            except ValueError, e:
                exception = e
                self.session.rollback()
            finally:
                self.session.commit()
                if exception is not None:
                    raise exception
            self.clear()
            
    def clear(self):
        self.view.resize()
        self.model.select()
        for widget in self.children():
            if isinstance(widget, (QLineEdit, QTextEdit)):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(-1)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(False)
        self.supplier_currency.setCurrentIndex(0)
        self.suppliername_lineEdit.setFocus()
        self.dirty = False
        self.editing = False   
        
        self.setWindowTitle(localTITLE)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    setupDatabase("Production.sqlite")
    model = modelsandviews.SupplierModel()
    form = SupplierForm(model)
    form.resize(200, 200)
    form.show()
    app.exec_()