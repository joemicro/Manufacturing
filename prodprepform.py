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
import ui_forms.ui_prodprepform

# if pack in volume are changed here ask if should be updated in database

localTITLE = 'Production Prep'
(PD_ID) = 0 #// brackets are only for looks here
(BATCH_ID, BASE) = (ITEM, QTY) = range(1, 3)
(DESC) = 3
(PERCENT, INFL) = (PACK, VOLUME) = range(4, 6)
(TOTAL) = WEIGHT = 6

### BaseAssembly Model =======================   
class BaseAssemblyModel(QAbstractTableModel):
    
    def __init__(self, session, parent=None):
        super(BaseAssemblyModel, self).__init__(parent)
        self.records = []
        self.records.append(PrepAssembly())
        self.session = session
    
    def rowCount(self, index=QModelIndex()):
        return len(self.records)
    
    def columnCount(self, index=QModelIndex()):
        return 7
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == PD_ID:
                return QVariant('PD ID')
            elif section == BATCH_ID:
                return QVariant('Batch ID')
            elif section == BASE:
                return QVariant('Base No')
            elif section == DESC:
                return QVariant('Description')
            elif section == PERCENT:
                return QVariant('Percent')
            elif section == INFL:
                return QVariant('Inflation')
            elif section == WEIGHT:
                return QVariant('Weight')
        return QVariant(section + 1)
    
    def flags(self, index):
        flag = QAbstractTableModel.flags(self, index)
        if index.column() not in (PD_ID, BATCH_ID, DESC, WEIGHT):
            flag |=Qt.ItemIsEditable
        return flag
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.records)):
            return QVariant()
        record = self.records[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == PD_ID:
                return QVariant(record.pd_id)
            elif column == BATCH_ID:
                return QVariant(record.batch_id)
            elif column == BASE:
                base_no = dLookup(BaseHeader.base_no, BaseHeader.base_id == str(record.base_id))
                return QVariant(base_no)
            elif column == PERCENT:
                if not record.percentage:
                    return QVariant(record.percentage)
                return QVariant(round(float(getType(record.percentage)), 4))
            elif column == DESC:
                base_desc = dLookup(BaseHeader.base_desc, BaseHeader.base_id==record.base_id)
                return QVariant(base_desc)
            elif column == INFL:
                if not record.inflation:
                    return QVariant(record.inflation)
                return QVariant(round(float(getType(record.inflation)), 4))
            elif column == WEIGHT:
                if not record.weight:
                    return QVariant(record.weight)
                return QVariant(round(float(getType(record.weight)), 4))
        return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            record = self.records[index.row()]
            column = index.column()
            if column == PD_ID:
                record.pd_id = value.toInt()[0]
            elif column == BATCH_ID:
                record.batch_id = value.toInt()[0]
            elif column == BASE:
                base_id = value.toInt()[0]
                record.base_id = base_id
                record.inflation = float(getType(dLookup(BaseHeader.inflation_factor, BaseHeader.base_id==base_id)))
            elif column == PERCENT:
                percent, ok = value.toFloat()
                if ok:
                    percent = (percent / 100) if percent > 1 else percent
                record.percentage = percent
            elif column == INFL:
                record.inflation = value.toFloat()[0]
            elif column == WEIGHT:
                record.weight = value.toFloat()[0]
            self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True
        return False
    
    def insertRows(self, position, rows=1, index=QModelIndex(), item_id=None):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.records.insert(position + row + 1, PrepAssembly(item_id))
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.records = self.records[:position] + self.records[position + rows:]
        self.endRemoveRows()
        return True
    
    ### Data and Calculations =============
    def getWeight(self, baseId):
        """ takes a base id to use for the criteria, and returns a sum of the weight for the base. """
        weight_query = self.session.query(func.sum(BaseDetail.bom_qty).label('sumQty')).join(BaseHeader).filter(BaseHeader.base_id==baseId)
        for i in weight_query:
            weight = float(getType(i.sumQty))
        return weight
    
    def calcIndWeight(self, literNeeded, pdId):
        """ Create an array that looks like this:
        BaseAssembly:
        Base ID    Base    %    factor  Value      |infl    Weight
        ----------------------------------------   |-------------
        3          BSRB    50    1.7    1364.5     |850     500    1000 for 1lt
        53         FORG    100   1.7    6.8225     |4.25    2.5    2.5 for 500lt
        1          BCRM    50    1.95   1364.5     |975     500    1000 for 1lt
        23         FRVN    100   1.95   4.0935     |2.925   1.5    .75 for 250lt
        ---------------------------------------------------------
                                    2739.92    1832.175    2008  - > if we multiply the value column by the inflation factor column we get 5000
                              liters needed    5000
                                 multiplier    2.729
        then we post the value column to the model
            """
        calc_array = {}
        base_id_list = []
        row_index = 0
        #// construct a list of bases to work with, add an index so we know where to post the resulting value
        for i in self.records:
            if i.pd_id == pdId:
                base_id_list += [(row_index, i.base_id, i.percentage, i.inflation)]
            row_index += 1
        #// construct the above array
        for line in base_id_list:
            row_index, base_id, percent, inflation = line
            percent = 1 if not percent else float(getType(percent))
            inflation = 1 if not inflation else float(getType(inflation))
            if base_id:
                where_cond = BaseHeader.base_id==base_id
                calc_array.setdefault(row_index, {})
                internal = calc_array[row_index]
                base_no = dLookup(BaseHeader.base_no, where_cond)
                internal['base_id'] = base_id
                internal['base'] = base_no
                internal['percent'] = percent
                internal['inflation'] = inflation
                #// lets make the base a default arbitrary value of 1000 so we know how much flavour to use.
                weight = 1000 * percent
                #// get base weight for flavour
                weight_flavor = self.getWeight(base_id)
                #// lets check to see if base is a flavour base, in that case w'ill calculate the weight as follows:
                #// the actual weight times the intended weight divided by the base weight which is 1000 * percent
                #// Ex. actual weight = 2.5 and its intended for 250lt of mix but we r doing it for a 1000lt so = 2.5 * (1000/250)
                base_type = dLookup(BaseHeader.base_type, where_cond)
                if base_type == 'Flavor':
                    base_volume = dLookup(BaseHeader.base_volume, where_cond)
                    weight = weight_flavor * (weight / float(getType(base_volume)))
                inf_weight = weight * inflation
                internal['weight'] = weight
                internal['inf_weight'] = inf_weight
                print row_index, internal
        liter_got = sum(calc_array[i]['inf_weight'] for i in calc_array.keys())
        multiplier = literNeeded / nonZero(liter_got, 1)
        
        #// now that we have the multiplier, lets post the value to model
        for key in calc_array.keys():
            weight_needed = round(calc_array[key]['weight'] * multiplier, 4)
            index = self.index(key, WEIGHT)
            self.setData(index, QVariant(weight_needed))
        print 'Result: ', liter_got, multiplier
        
    def createBatches(self, date, prep_id):
        """ returns a list of batch headers and details to record to database. """
        batches = details = []
        to_create_list = []
        got_it = []
        #// condense the list into a single base and sum of weight
        #// have a list where u store the bases already in the new list, for reference not take it again
        for i in self.records:
            if i.base_id and i.base_id not in got_it:
                total_volume = sum(r.weight for r in self.records if r.base_id==i.base_id)
                inflation = i.inflation
                to_create_list += [(i.base_id, total_volume, inflation)]
                got_it += [i.base_id]
        #// now that we have the list of what we need to create, lets create batches.
        id_increment = 1
        for base in to_create_list:
            #// create header instance
            base_id = base[0]
            where_cond = BaseHeader.base_id==base_id
            batch_id = dMax(BatchHeader.batch_id) + id_increment
            batch_date = date
            base_volume = dLookup(BaseHeader.base_volume, where_cond)
            multiple = 1
            inflation_factor = base[2]
            batch_memo = None
            batches += [BatchHeader(batch_id, base_id, batch_date, unicode(base_volume), unicode(multiple),
                                     unicode(inflation_factor), batch_memo, None, prep_id)]
            #// create detail instance, first get the details from base table, then transfer it to batch table
            #// but first lets get a multiplier to use to multiply qty
            base_weight = self.getWeight(base_id)
            weight_needed = base[1]
            multiplier = weight_needed / nonZero(base_weight, 1)
            detail_query = self.session.query(BaseDetail).filter(BaseDetail.base_id==base_id)
            for item in detail_query:
                bom_id = item.bom_id
                cost = None
                bom_qty = float(getType(item.bom_qty)) * multiplier
                details += [BatchDetail(batch_id, bom_id, cost, unicode(bom_qty))]
            #// update the model with batch id
            base_no = dLookup(BaseHeader.base_no, BaseHeader.base_id==base_id)
            begin_index = self.index(0, BASE)
            index_list = self.match(begin_index, Qt.DisplayRole, QVariant(base_no), hits=-1)
            for i in index_list:
                index = self.index(i.row(), BATCH_ID)
                self.setData(index, QVariant(batch_id))
            id_increment += 1
        return (batches, details)
    
    ### Operations ============
    def sort(self):
        self.records.sort(key=lambda item: item.pd_id, reverse=True)
        
    def load(self, itemList, clear=True, itemId=None):
        """ loads data in BaseAssembly Model.
        Takes 'ItemList' a list of data to load
        Takes 'Clear' a boolean if True will clear all data already in the model, Default is True
        Takes 'ItemId' to load into item_id column """
        #// Prepare variables for later use
        item_id = itemId
        add = added = False
        
        #// clear is True then clear the model properly.
        if clear:
            self.beginResetModel()
            self.records = []
            self.endResetModel()
        #// if the list to load comes with an itemId,
        #// it means that its a detial id for instances pd_id. in that case delete all records that don't have an id
        #// as not to accumulate empty rows, looks ugly on table view
        if itemId:
            for rec in self.records:
                if not rec.pd_id:
                    i = self.records.index(rec)
                    self.records.pop(i)
        #// now lets load up the model    
        for item in itemList:
            #// if no itemId was passed
            if not itemId:
                #// then check if the item_id was changed
                if item_id != item.pd_id:
                    #// if it changed add a new empty line
                    add = True 
                #// keep track of the item_id for verification later if change
                item_id = item.pd_id
            #// finally lets get the list elements and get them ready for importing into the model
            
            #// if the list comes when a new item is added to detail, then it will be a list from base assembly,
            #// then there wont be a batch id
            try:
                batch_id = item.batch_id
            except AttributeError:
                batch_id = None
            
            #// if the list is being passed when doing a recall, then it will come from prepAssembly table,
            #// then it wont have a base id, and w'ill need to look it up from the batch_header table    
            try:
                base_id = item.base_id
            except AttributeError:
                if batch_id:
                    base_id = dLookup(BatchHeader.base_id, BatchHeader.batch_id==batch_id)
                else:
                    base_id = None
            try:
                infl = item.inflation
            except AttributeError:
                if base_id:
                    infl = float(getType(dLookup(BaseHeader.inflation_factor, BaseHeader.base_id==base_id)))
                else:
                    infl = None
            percentage = item.percentage
            self.records.append(PrepAssembly(item_id, batch_id, percentage, infl, base_id))
           
            #// we said before to add an empty line, here is where we actually listen
            if add:
                self.records.append(PrepAssembly(item_id)) # add an empty line, every time the item_id changes  
                add = False
                #// we tell him that we have already added a line, so he doesnt need to do it later
                added = True
            
        #// there are no individual empty lines for each item_id, add one empty line at the end
        if not added:
            self.records.append(PrepAssembly(item_id))
        
        self.sort()
    
    
    def save(self):
        records_ = []
        for rec in self.records:
            if rec.base_id:
                records_ += [PrepAssembly(rec.pd_id, rec.batch_id, unicode(rec.percentage), unicode(rec.inflation))]
        return records_
            
    
    def clear(self):
        self.beginResetModel()
        self.records = []
        self.records.append(PrepAssembly())
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
        
        
### Detail Model Setup ===========================================
class PrepDetailModel(QAbstractTableModel):
    def __init__(self, assemModel, parent=None):
        super(PrepDetailModel, self).__init__(parent)
        self.records = []
        self.records.append(PrepDetail())
        self.assemblyModel = assemModel
    
    def rowCount(self, index=QModelIndex()):
        return len(self.records)
    
    def columnCount(self, index=QModelIndex()):
        return 7
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == PD_ID:
                return QVariant('PD ID')
            elif section == ITEM:
                return QVariant('Item')
            elif section == QTY:
                return QVariant('Qty')
            elif section == DESC:
                return QVariant('Description')
            elif section == PACK:
                return QVariant('Pack')
            elif section == VOLUME:
                return QVariant('Volume')
            elif section == TOTAL:
                return QVariant('Total')
        return QVariant(section + 1)
    
    def flags(self, index):
        flag = QAbstractTableModel.flags(self, index)
        if index.column() not in (PD_ID, DESC, TOTAL):
            flag |=Qt.ItemIsEditable
        return flag
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.records)):
            return QVariant()
        record = self.records[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == PD_ID:
                return QVariant(record.pd_id)
            elif column == ITEM:
                item_id = record.item_id
                item_no = dLookup(Items.item_no, Items.item_id==item_id)
                return QVariant(item_no)
            elif column == QTY:
                if not record.qty:
                    return QVariant(record.qty)
                return QVariant(round(record.qty, 2))
            elif column == DESC:
                item_desc = dLookup(Items.item_desc, Items.item_id==record.item_id)
                return QVariant(item_desc)
            elif column == PACK:
                if not record.pack:
                    return QVariant()
                return QVariant(round(record.pack, 2))
            elif column == VOLUME:
                if not record.volume:
                    return QVariant()
                return QVariant(round(record.volume, 2))
            elif column == TOTAL:
                if not record.total:
                    return QVariant()
                return QVariant(round(record.total, 2))
        elif role == Qt.EditRole:
            if column == ITEM:
                return QVariant(record.item_id)
        return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role==Qt.EditRole:
            record = self.records[index.row()]
            column = index.column()
            pd_id = dMax(PrepDetail.pd_id) + 1
            if column == PD_ID:
                record.pd_id = value.toInt()[0]
            elif column == ITEM:
                if not record.pd_id:
                    record.pd_id = pd_id + index.row()
                item_id = value.toInt()[0]
                record.item_id = item_id
                record.pack = float(getType(dLookup(Items.pack, Items.item_id==item_id)))
                record.volume = float(getType(dLookup(Items.volume, Items.item_id==item_id)))
            elif column == QTY:
                qty, ok = value.toFloat()
                if ok:
                    record.qty = qty
                    record.total = self.calcTotal(record)
            elif column == PACK:
                record.pack = value.toFloat()[0]
            elif column == VOLUME:
                record.volume = value.toFloat()[0]
                record.total = self.calcTotal(record)
            self.emit(SIGNAL("dataChanged(QModelIndex, QModelIndex)"), index, index)
            return True
        return False
    
    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.records.insert(position + row + 1, PrepDetail())
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.records = self.records[:position] + self.records[position + rows:]
        self.endRemoveRows()
        return True
    
    ### Data and Calculations =============
    def calcTotal(self, record):
        qty = float(getType(record.qty))
        volume = float(getType(record.volume))
        total = qty * volume
        return total
    
    def recalcModel(self):
        self.beginResetModel()
        for rec in self.records:
            rec.total = self.calcTotal(rec)
        self.endResetModel()
        
    def getTotals(self):
        sum_qty = sum(nonZero(i.qty) for i in self.records)
        sum_total = sum(nonZero(i.qty) * nonZero(i.volume) for i in self.records)
        return (sum_qty, sum_total)
        
    ### Model Operations ==================
    def calcAssemblyWeight(self):
        for record in self.records:
            if record.item_id:
                pdId = record.pd_id
                literNeeded = record.total if record.total else 1
                self.assemblyModel.calcIndWeight(literNeeded, pdId)
                
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
        id_count = position
        for rec in rows:
            col = rec.split('\t')
            id_count += 1
            pd_id = dMax(PrepAssembly.pd_id) + id_count
            item_id = dLookup(Items.item_id, Items.item_no==str(col[0]))
            qty = pack = volume = None
            var_list = [qty, pack, volume]
            if item_id:
                for i in range(len(var_list)):
                    try:
                        var_list[i] = float(getType(col[i + 1]))
                    except ValueError:
                        var_list[i] = None
                    except IndexError:
                        continue
                qty, pack, volume = var_list
                pack = float(getType(dLookup(Items.pack, Items.item_id==item_id))) if not pack else pack
                volume = float(getType(dLookup(Items.volume, Items.item_id==item_id))) if not volume else volume
                myList += [PrepDetail(pd_id, item_id, qty, pack, volume)]
                
        rowCount = len(myList)
        self.beginInsertRows(QModelIndex(), position, position + rowCount - 1)
        for row in range(rowCount):
                self.records.insert(position + row, myList[row])
        self.endInsertRows()
        self.recalcModel()
        return rowCount
    
    
    def load(self, recordList):
        self.beginResetModel()
        self.records = []
        self.endResetModel()
        for record in recordList:
            self.records.append(PrepDetail(record.pd_id, record.item_id, float(getType(record.qty)), 
                                        float(getType(record.pack)), float(getType(record.volume))))
        self.recalcModel()
            
    
    def save(self, header_id):
        records_ = []
        for record in self.records:
            if record.item_id:
                records_ += [PrepDetail(record.pd_id, record.item_id, unicode(record.qty), 
                                        unicode(record.pack), unicode(record.volume), header_id)]
        return records_
    
    def clear(self):
        self.beginResetModel()
        self.records = []
        self.records.append(PrepDetail())
        self.endResetModel()
        
            
        
        
                
### Form Setup ===================================================
class ProductionPrep(QDialog, ui_forms.ui_prodprepform.Ui_ProdPrep):
    
    def __init__(self, itemModel, baseModel, parent=None):
        super(ProductionPrep, self).__init__(parent)
        self.setupUi(self)
        self.my_parent = parent
        self.record_id = None
        self.dirty = False
        self.editing = False
        self.session = Session()
        
        if self.my_parent:
            self.date_dateEdit.setDate(self.my_parent.getDate())
        self.v_prepNo_label.setText(str(dMax(PrepHeader.prep_id) + 1))
        
        self.assemblyModel = BaseAssemblyModel(self.session)
        
        self.detailModel = PrepDetailModel(self.assemblyModel)
        self.detail_tableView.setModel(self.detailModel)
        delegate = GenericDelegate(self)
        delegate.insertDelegate(ITEM, ComboDelegate(itemModel, True))
        delegate.insertDelegate(QTY, NumberDelegate())
        delegate.insertDelegate(PACK, NumberDelegate())
        delegate.insertDelegate(VOLUME, NumberDelegate())
        self.detail_tableView.setItemDelegate(delegate)
        self.detail_tableView.setColumnHidden(PD_ID, True)
        self.detail_tableView.setColumnWidth(ITEM, 75)
        self.detail_tableView.setColumnWidth(QTY, 75)
        self.detail_tableView.setColumnWidth(DESC, 250)
        self.detail_tableView.setColumnWidth(PACK, 50)
        self.detail_tableView.setColumnWidth(VOLUME, 50)
        self.detail_tableView.horizontalHeader().setStretchLastSection(True)
        
        self.assemblyProxyModel = QSortFilterProxyModel()
        self.assemblyProxyModel.setFilterKeyColumn(0)
        self.assemblyProxyModel.setSourceModel(self.assemblyModel)
        self.batch_tableView.setModel(self.assemblyProxyModel)
        batch_dlg = GenericDelegate(self)
        batch_dlg.insertDelegate(BASE, ComboDelegate(baseModel, True))
        batch_dlg.insertDelegate(PERCENT, NumberDelegate())
        batch_dlg.insertDelegate(INFL, NumberDelegate())
        self.batch_tableView.setItemDelegate(batch_dlg)
        self.batch_tableView.verticalHeader().setVisible(False)
        self.batch_tableView.setColumnHidden(PD_ID, True)
        self.batch_tableView.setColumnHidden(BATCH_ID, True)
        self.batch_tableView.setColumnWidth(BASE, 75)
        self.batch_tableView.setColumnWidth(DESC, 300)
        self.batch_tableView.setColumnWidth(PERCENT, 50)
        self.batch_tableView.setColumnWidth(INFL, 50)
        self.batch_tableView.horizontalHeader().setStretchLastSection(True)
        
        self.detailModel.dataChanged.connect(self.addAssemblies)
        self.detailModel.dataChanged.connect(lambda: self.autoAddRow(self.detail_tableView, self.detailModel))
        self.detail_tableView.selectionModel().currentRowChanged.connect(self.setFilter)
        self.detail_tableView.doubleClicked.connect(self.editItem)
        
        self.date_dateEdit.dateChanged.connect(self.setParentDate)
        
        self.newButton.clicked.connect(self.clear)
        self.calcButton.clicked.connect(self.recalc)
        self.saveButton.clicked.connect(self.save)
        self.deleteButton.clicked.connect(lambda: self.delete(header=True))
        self.closeButton.clicked.connect(self.accept)
     
    ### Form Behaviour ============================================   
    def setDirty(self):
        self.updateSumTotals()
        self.dirty = True
        self.setWindowTitle("%s - Editing..." % localTITLE) 
        
    def setParentDate(self):
        date = self.date_dateEdit.date().toPyDate()
        self.my_parent.setDate(date) 
    
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        if self.detail_tableView.hasFocus():
            view = self.detail_tableView
            model = self.detailModel
            
            copyAction = menu.addAction('Copy', QObject, 'Ctrl+C')
            pasteAction = menu.addAction('Paste', QObject, 'Ctrl+V')
            insertAction = menu.addAction("Insert Line", QObject, "Ctrl+I")
            deleteAction = menu.addAction("Delete Line", QObject, "Ctrl+D")
            
            copyAction.triggered.connect(lambda: self.copy(view, model))
            pasteAction.triggered.connect(lambda: self.paste(view, model))
            insertAction.triggered.connect(lambda: self.insertRow(view, model))
            deleteAction.triggered.connect(lambda: self.removeRow(view, model))
            
            addActions(self, view, (insertAction, deleteAction))
            
        elif self.batch_tableView.hasFocus():
            view = self.batch_tableView
            model = self.assemblyModel
            
            copyAction = menu.addAction('Copy', QObject, 'Ctrl+C')
            insertAction = menu.addAction("Insert Line", QObject, "Ctrl+I")
            deleteAction = menu.addAction("Delete Line", QObject, "Ctrl+D")
            
            copyAction.triggered.connect(lambda: self.copy(view, model))
            insertAction.triggered.connect(lambda: self.insertRow(view, model))
            deleteAction.triggered.connect(lambda: self.removeRow(view, model))
        menu.exec_(event.globalPos())
    
    def autoAddRow(self, view, model):
        self.setDirty()
        row = view.currentIndex().row()
        if model.rowCount() == row + 1:
            self.insertRow(view, model)
        
    def insertRow(self, view, model):
        if view is not None:
            index = view.currentIndex()
            row = index.row() + 1
            if model == self.assemblyModel:
                pd_id, ok = self.fgd_id()
                if ok:
                    model.insertRows(row, item_id=pd_id)
                    self.setFilter()
            else:
                model.insertRows(row)
            view.setFocus()
            view.setCurrentIndex(index)
    
    def removeRow(self, view, model):
        rowsSelected = view.selectionModel().selectedRows()
        if not rowsSelected:
            row = view.currentIndex().row()
            rows = 1
        else:
            for i in rowsSelected:
                row = i.row()
            rows = len(rowsSelected)
            row = row - rows + 1
        if model == self.assemblyModel:
            proxy_index = self.assemblyProxyModel.index(view.currentIndex().row(), 0)
            row = self.assemblyProxyModel.mapToSource(proxy_index).row()
            rows = 1
        model.removeRows(row, rows)
        if model.rowCount() < 1:
            self.insertRow(view, model)
        self.setDirty()
        self.updateSumTotals()
        
    def copy(self, view, model):
        if model.rowCount() <= 1:
            return
        selectedItems = view.selectionModel().selectedIndexes()
        model.copy(selectedItems)
        
    def paste(self, view, model):
        row = view.currentIndex().row()
        rows = model.paste(row)
        for i in range(rows):
            index = view.model().index(i + row, 1)
            view.setCurrentIndex(index)
            self.addAssemblies(recall=False)
        self.updateSumTotals()
    
    def fgd_id(self):
        index = self.detail_tableView.currentIndex()
        row = index.row()
        idIndex = self.detailModel.index(row, 0)
        fgd_id, ok = self.detailModel.data(idIndex, Qt.DisplayRole).toInt()
        return (fgd_id, ok)
        
        
    def deleteAssemblies(self, fgd_id):
        beginIndex = self.assemblyModel.index(0, 0)
        baseIndexList = self.assemblyModel.match(beginIndex, Qt.DisplayRole, QVariant(fgd_id), hits=-1)
        if not baseIndexList:
            return
        while baseIndexList:
            position = baseIndexList[0].row()
            self.assemblyModel.removeRows(position)
            baseIndexList = self.assemblyModel.match(beginIndex, Qt.DisplayRole, QVariant(fgd_id))

    def addAssemblies(self, recall=False):
        if recall == True:
            baseList = self.session.query(PrepAssembly).join(PrepDetail).filter(PrepDetail.header_id==self.record_id)
            clear = True
            fgd_id = None
        else:
            index = self.detail_tableView.currentIndex()
            if not index.column() == 1:
                return
            row = index.row()
            myIndex = self.detailModel.index(row, 1)
            fgd_id = self.fgd_id()[0]
            fg_num = str(self.detailModel.data(myIndex, Qt.DisplayRole).toString())
            fg_id = dLookup(Items.item_id, Items.item_no==fg_num)
            self.deleteAssemblies(fgd_id)
            baseList = self.session.query(BaseAssembly).filter(BaseAssembly.item_id==fg_id)
            clear = False
        self.assemblyModel.load(baseList, clear, fgd_id)
        self.assemblyProxyModel.reset()
        self.setFilter()

    def setFilter(self):
        fgd_id = self.fgd_id()[0]
        self.assemblyProxyModel.setFilterFixedString(str(fgd_id))
        
    
    def editItem(self):
        row = self.detail_tableView.currentIndex().row()
        index = self.detailModel.index(row, ITEM)
        item_id = self.detailModel.data(index, Qt.EditRole).toString()
        if not item_id:
            return
        form = self.my_parent.itemForm()
        form.recall(1, str(item_id))
        
    
    
    
    ### Data and calculations ==================================
    def updateModel(self):
        self.detailModel.recalcModel()
    
    def updateSumTotals(self):
        sum_qty, sum_total = self.detailModel.getTotals()
        self.v_totalQty_label.setText(str(sum_qty))
        self.v_totalLiters_label.setText(str(sum_total))
        
    def recalc(self):
        self.detailModel.calcAssemblyWeight()
        
    
    ### Form Operations ========================================
    def recall(self, prep_id):
        if self.dirty:
            answer = QMessageBox.question(self, "Editing - %s" % localTITLE, "Would you like to save your data?",
                                 QMessageBox.Yes| QMessageBox.Discard| QMessageBox.Cancel)
            if answer == QMessageBox.Cancel:
                return
            elif answer == QMessageBox.Yes:
                self.save()
                
        self.record_id = prep_id
        self.v_prepNo_label.setText(str(prep_id))
        records = self.session.query(PrepHeader).filter(PrepHeader.prep_id==prep_id)
        for record in records:
            self.date_dateEdit.setDate(record.prep_date)
            self.note_lineEdit.setText(str(record.prep_memo))
        
        details = self.session.query(PrepDetail).filter(PrepDetail.header_id==prep_id)
        self.detailModel.load(details)
        self.addAssemblies(recall=True)
        self.editing = True
        self.updateSumTotals()
        
        
    def save(self):
        self.recalc()
        if not self.assemblyModel.save():
            QMessageBox.information(self, 'Saving - %s' % localTITLE, 'No assemblies found', QMessageBox.Ok)
            self.dirty = False
            return
        prep_id = self.record_id
        prep_date = self.date_dateEdit.date().toPyDate()
        prep_memo = str(self.note_lineEdit.text())
        if self.editing:
            self.delete(header=False)
            self.session.query(PrepHeader).filter(PrepHeader.prep_id==prep_id).update({'prep_date': prep_date, 'prep_memo': prep_memo})
        else:
            prep_id = dMax(PrepHeader.prep_id) + 1
            self.session.add(PrepHeader(prep_id, prep_date, prep_memo))
            
        batches, details = self.assemblyModel.createBatches(prep_date, prep_id)
        prep_details = self.detailModel.save(prep_id)
        assembly_details = self.assemblyModel.save()
        self.session.add_all(prep_details)
        self.session.add_all(assembly_details)
        self.session.add_all(batches)
        self.session.add_all(details)
        self.sendToDB()
        self.dirty = False
        self.editing = True
        self.my_parent.refreshModels()
        self.setWindowTitle('%s - (Data Saved)' % localTITLE)
        
    
    def delete(self, header=True):
        if not self.record_id:
            return
        prep_id = self.record_id
        #// if function was called by user, header is probably true, ask if user is sure you never know.
        if header:
            prod_id = dLookup(PrepHeader.prod_id, PrepHeader.prep_id==prep_id)
            if prod_id != 'None':
                QMessageBox.information(self, "Delete - %s" % localTITLE, "This preparation is already used for a production \n Can't Delete",
                                        QMessageBox.Ok)
                return
            answer = QMessageBox.question(self, "Delete - %s" % localTITLE, "Are you sure you " \
                                                  "want to delete Prep: %s:, %s" % (self.v_prepNo_label.text(),
                                                                                    self.date_dateEdit.date().toPyDate()), 
                                                  QMessageBox.Yes| QMessageBox.No, QMessageBox.NoButton)
            if answer == QMessageBox.No:
                return
            self.session.query(PrepHeader).filter(PrepHeader.prep_id==prep_id).delete()
        #// delete the assemblies
        dtl_qry = self.session.query(PrepDetail.pd_id).filter(PrepDetail.header_id==prep_id)
        self.session.query(PrepAssembly).filter(PrepAssembly.pd_id.in_(dtl_qry)).delete('fetch')
        #// lets delete the details
        self.session.query(PrepDetail).filter(PrepDetail.header_id==prep_id).delete()
        #//  lets delete the batches that was created by this prep
        btch_qry = self.session.query(BatchHeader.batch_id).filter(BatchHeader.prep_id==prep_id).subquery()
        self.session.query(BatchDetail).filter(BatchDetail.base_id.in_(btch_qry)).delete('fetch')
        self.session.query(BatchHeader).filter(BatchHeader.prep_id==prep_id).delete()
        if header:
            self.sendToDB()
            self.my_parent.refreshModels()
            self.clear()
        
                
    def sendToDB(self):
        try:
            self.session.flush
            self.session.commit()
        except Exception, e:
            self.session.rollback()
            raise e
        
        
    def clear(self):
        self.v_prepNo_label.setText(str(dMax(PrepHeader.prep_id) + 1))
        self.v_totalLiters_label.clear()
        self.v_totalQty_label.clear()
        self.note_lineEdit.clear()
        self.detailModel.clear()
        self.assemblyModel.clear()
        if defaultDate() == 'current':
            self.date_dateEdit.setDate(QDate.currentDate())
        self.dirty = False
        self.editing = False
        self.setWindowTitle(localTITLE)
        
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
        
        
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    setupDatabase("Production.sqlite")
    item = modelsandviews.ItemModel('Items')
    base = modelsandviews.BaseListModel()
    form = ProductionPrep(item, base)
    form.show()
    app.exec_()