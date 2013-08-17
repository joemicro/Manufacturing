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
import ui_forms.ui_settingsform


localTITLE = 'Settings'

class SettingsForm(QDialog, ui_forms.ui_settingsform.Ui_SettingsForm):
    
    def __init__(self, bomModel, parent=None):
        super(SettingsForm, self).__init__(parent)
        self.setupUi(self)
        self.session = Session()
        self.my_parent = parent
        self.def_value = None
        self.dirty = False
        self.settings_tabWidget.setCurrentIndex(0)
        
        bom_price = dLookup(Settings.bool_value, Settings.setting=='update_price')
        bom_price = True if bom_price == 'True' else False
        self.bomPrice_checkBox.setChecked(bom_price)
        
        price_check = dLookup(Settings.bool_value, Settings.setting=='check_price')
        price_check = True if price_check == 'True' else False
        self.priceCheck_checkBox.setChecked(price_check)
        
        price_diff = dLookup(Settings.value_1, Settings.setting=='check_price')
        price_diff = price_diff if price_diff != 'None' else ""
        self.priceDiff_lineEdit.setText(price_diff)
        
        def_date = dLookup(Settings.value_1, Settings.setting=='default_date')
        if def_date == 'last':
            self.lastDate_radioButton.setChecked(True)
        else:
            self.currDate_radioButton.setChecked(True)
            
        closing_ck = dLookup(Settings.bool_value, Settings.setting=='closing_date')
        closing_ck = True if closing_ck == 'True' else False
        closing_date = dLookup(Settings.date_value, Settings.setting=='closing_date')
        closing_date = closing_date if closing_date != 'None' else '01/01/00'
        closing_date = parser.parse(closing_date).date()
        closing_pass = dLookup(Settings.value_1, Settings.setting=='closing_date')
        closing_pass = closing_pass if closing_pass != 'None' else ""
        self.closingDate_checkBox.setChecked(closing_ck)
        self.closingDate_dateEdit.setDate(closing_date)
        self.closingDate_lineEdit.setText(closing_pass)
        
        bomView1 = modelsandviews.ItemView(bomModel)
        self.del_comboBox.setModel(bomModel)
        self.del_comboBox.setView(bomView1)
        self.del_comboBox.setModelColumn(1)
        self.del_comboBox.setCurrentIndex(-1)
        
        bomView2 = modelsandviews.ItemView(bomModel)
        self.cont_comboBox.setModel(bomModel)
        self.cont_comboBox.setView(bomView2)
        self.cont_comboBox.setModelColumn(1)
        self.cont_comboBox.setCurrentIndex(-1)
        
        export_accounts = dLookup(Settings.value_1, Settings.setting=='export_accounts')
        accounts = export_accounts.split('|')
        self.ap_lineEdit.setText(accounts[0])
        self.apUSD_lineEdit.setText(accounts[1])
        self.inv_lineEdit.setText(accounts[2])
        self.class_lineEdit.setText(accounts[3])
        
        header_list = [('ID', False), ('Type', False), ('Value', True)]
        self.list_model = modelsandviews.QuickModel(header_list)
        self.list_tableView.setModel(self.list_model)
        lists = ['Category', 'Season']
        self.list_comboBox.addItems(lists)
        self.list_comboBox.setCurrentIndex(-1)
        delegate = GenericDelegate(self)
        delegate.insertDelegate(1, PlainTextDelegate())
        self.list_tableView.setItemDelegate(delegate)
        self.list_tableView.setColumnHidden(0, True)
        self.list_tableView.setColumnHidden(1, True)
        
        
        field_list = ['Date', 'Time', 'User', 'Memo', 'Journal', 'Type']
        self.logField_comboBox.addItems(field_list)
        log_header = [('Date', False), ('Time', False), ('User', False), ('Memo', False), ('Journal', False), ('Type', False)]
        self.log_model = modelsandviews.QuickModel(log_header)
        log_query = self.session.query(Logs.log_date, Users.user_name, Logs.log_memo, Logs.journal_id, JournalHeader.journal_type) \
                                        .outerjoin(Users).outerjoin(JournalHeader)
                                        
        object_list = []
        for i in log_query:
            object_list += [[str(i[0].date()), str(i[0].time()), i[1], i[2], i[3], i[4]]]
        self.log_model.load(object_list)
        self.log_proxy = QSortFilterProxyModel()
        self.log_proxy.setSourceModel(self.log_model)
        self.log_tableView.setModel(self.log_proxy)
        self.log_tableView.setSortingEnabled(True)
        self.log_tableView.resizeColumnsToContents()
        
        self.list_comboBox.currentIndexChanged.connect(self.loadList)
        self.list_model.dataChanged.connect(self.autoAddRow)
        self.logFilter_lineEdit.textEdited.connect(self.filterLog)
        self.merge_pushButton.clicked.connect(self.mergeItem)
        self.save_pushButton.clicked.connect(self.save)
        self.close_pushButton.clicked.connect(self.accept)
        
        self.setupConnection()
        
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
            elif isinstance(widget, QRadioButton):
                self.connect(widget, SIGNAL("toggled(bool)"), self.setDirty)
    
    def setDirty(self):
        if self.sender() in (self.logFilter_lineEdit, self.logField_comboBox,
                             self.del_comboBox, self.cont_comboBox, self.list_comboBox):
            return
        self.dirty = True
        self.setWindowTitle('%s - (Unsaved)' % localTITLE)
        
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        if self.list_tableView.hasFocus():
            model = self.list_model
            view = self.list_tableView
            copyAction = menu.addAction('Copy', QObject, 'Ctrl+C')
            copyAction.triggered.connect(lambda: self.copy(model, view))
            insertAction = menu.addAction('Insert Line')
            deleteAction = menu.addAction('Delete Line') 
            insertAction.triggered.connect(self.insertRow)
            deleteAction.triggered.connect(self.removeRow)
        elif self.log_tableView.hasFocus():
            model = self.log_model
            view = self.log_tableView
            copyAction = menu.addAction('Copy', QObject, 'Ctrl+C')
            copyAction.triggered.connect(lambda: self.copy(model, view))
        menu.exec_(event.globalPos())
              
    def loadList(self):
        list_type = self.list_comboBox.currentIndex()
        if  list_type == 0:
            self.def_value = 'itemCategory'
        elif list_type == 1:
            self.def_value = 'season'
        
        item_list = self.session.query(Lists).filter(Lists.type==self.def_value)    
        object_list = [[i.id, i.type, i.item] for i in item_list]
        self.list_model.load(object_list)
        position = self.list_model.rowCount()
        self.list_model.insertRows(position, 1, ['', self.def_value, ''])
     
    def autoAddRow(self):
        row = self.list_tableView.currentIndex().row()
        if self.list_model.rowCount() == row + 1:
            self.insertRow()
            
    def insertRow(self):
        row = self.list_tableView.currentIndex().row()
        self.list_model.insertRows(row, 1, ['', self.def_value, ''])
    
    def removeRow(self):
        row = self.list_tableView.currentIndex().row()
        self.list_model.removeRows(row)
        
    def filterLog(self):
        string = str(self.logFilter_lineEdit.text())
        reg_filter = QRegExp(string, Qt.CaseInsensitive, QRegExp.FixedString)
        self.log_proxy.setFilterRegExp(reg_filter)
        
        self.log_proxy.setFilterKeyColumn(self.logField_comboBox.currentIndex())
        
    def copy(self, model, view):
        if model.rowCount() <= 1:
            return
        selectedItems = view.selectionModel().selectedIndexes()
        model.copy(selectedItems)
        
          
    def save(self):
        bom_price = self.bomPrice_checkBox.isChecked()
        price_check = self.priceCheck_checkBox.isChecked()
        price_diff = str(self.priceDiff_lineEdit.text())
        def_date = 'last' if self.lastDate_radioButton.isChecked() else 'current'
        c_ck = self.closingDate_checkBox.isChecked()
        c_date = self.closingDate_dateEdit.date().toPyDate()
        c_pass = str(self.closingDate_lineEdit.text())
        accounts = unicode('%s|%s|%s|%s') % (self.ap_lineEdit.text(),
                                              self.apUSD_lineEdit.text(),
                                              self.inv_lineEdit.text(),
                                              self.class_lineEdit.text())
        
        settings = self.session.query(Settings)
        update_price = settings.get('update_price')
        update_price.bool_value = bom_price
        
        check_price = settings.get('check_price')
        check_price.bool_value = price_check
        check_price.value_1 = price_diff
        
        default_date = settings.get('default_date')
        default_date.value_1 = def_date
        
        closing_date = settings.get('closing_date')
        closing_date.date_value = c_date
        closing_date.bool_value = c_ck
        closing_date.value_1 = c_pass
        
        export_accounts = settings.get('export_accounts')
        export_accounts.value_1 = accounts
        

        new_list = self.list_model.save()
#        save_list = [Lists(x[0], x[1], str(x[2])) for x in new_list if str(x[2])]
        list_query = self.session.query(Lists)
        for l in new_list:
            if l[2]:
                list_item = list_query.get(l[0])
                if list_item:
                    list_item.item = str(l[2])
                else:
                    self.session.add(Lists(str(l[1]), str(l[2])))
            
        self.sendToDB()
        
        self.setWindowTitle('%s - (Saved)' % localTITLE)
        self.dirty = False
        
    def mergeItem(self):
        d_item = str(self.del_comboBox.currentText())
        c_item = str(self.cont_comboBox.currentText())
        if not d_item or not c_item:
            return
        
        delete_id = dLookup(BOM.bom_id, BOM.bom_no==d_item)
        d_desc = dLookup(BOM.bom_desc, BOM.bom_id==delete_id)
        continue_id = dLookup(BOM.bom_id, BOM.bom_no==c_item)
        c_desc = dLookup(BOM.bom_desc, BOM.bom_id==continue_id)
        
        answer = QMessageBox.question(self, 'Merge BOM', 'Are you sure you want to delete %s: %s' % (d_item, d_desc),
                                      QMessageBox.Yes |QMessageBox.No)
        if answer == QMessageBox.No:
            return
        
        list_to_query = (BaseDetail, BatchDetail, FGDBOMAssembly, RMD, ItemAssembly)
        for q_object in list_to_query:
            self.session.query(q_object).filter(q_object.bom_id==delete_id).update({'bom_id': continue_id})
        
        mix_item = dLookup(BOM.mix_item, BOM.bom_id==delete_id)
        if mix_item:
            self.session.query(Items).filter(Items.item_no==d_item).update({'item_no': c_item})
            self.session.query(BOM).filter(BOM.bom_id==continue_id).update({'mix_item': True})
        self.session.query(BOM).filter(BOM.bom_id==delete_id).delete()
        log_memo = '%s: %s was merged with %s: %s' % (d_item, d_desc, c_item, c_desc)
        
        self.session.add(Logs(None, self.my_parent.user_id, QDateTime().currentDateTime().toPyDateTime(), log_memo))
        self.sendToDB()
        self.del_comboBox.setCurrentIndex(-1)
        self.cont_comboBox.setCurrentIndex(-1)
        self.my_parent.refreshModels()
        
    def sendToDB(self):
        try:
            self.session.flush
            self.session.commit()
        except Exception, e:
            self.session.rollback()
            raise e 
        
        
    def reject(self):
        self.accept()
        
    def accept(self):
        if self.dirty:
            answer = QMessageBox.question(self, '%s - Close' % localTITLE, 'You have unsaved changes, would you like to save?',
                                           QMessageBox.Yes |QMessageBox.No |QMessageBox.Cancel)
            if answer == QMessageBox.Cancel:
                return
            elif answer == QMessageBox.Yes:
                self.save()
        QDialog.accept(self)

                
        
        
        
        
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    setupDatabase("Production.sqlite")
    form = SettingsForm()
    form.show()
    app.exec_()
    