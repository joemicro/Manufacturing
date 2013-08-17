#// Libraries
import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy import  *
from sqlalchemy.orm import *
#// My Imports
import ui_forms.ui_productionform
from databaseschema import *
from genericdelegates import *
from functions import *
import modelsandviews
import itemform
import receiveform
from reports import *
import reporting

localTITLE = 'Production'

""" Story!!!!!!!
Step 1) get total FG Volume by Batch, by looping through base assembly, and getting the volume of the items attached to it
Step 2) update cost of batch details namely RM for batch, via running an update query.
Step 3) get cost of RM and divide by FG liters being produced (can't divide by rm liters, because FG liters are inflated)
        will get cost by running a sum query on the batch details in the DB.
Step 4) sum Up the packaging cost, for each item.
Step 5) in the base assembly get the total cost for each batch based on volume and percentage of batch used.
        ex. 301 has 50ltrs, has batch BCRM 100%, FRVN 100%, FORG 50%.
        a liter BCRM = .25, FRVN = .10, FORG = .15. then RM for 301 will equal (.25 + .10 +(.15 * .5)) * 50 
"""
def updateCostForBatch(session, date, journalID, batchID=None):
    """ update cost in the batch detail table in the DB, based on a batchID,
    need date and journal_id to pass to avgCost calculator """
    batchIDFilter = BatchDetail.base_id==batchID
    if not batchID:
        batchIDFilter = ""
    batchDetailQuery = session.query(BatchDetail).filter(batchIDFilter)
    for item in batchDetailQuery:
        bom_id = item.bom_id
        cost = avgCost(bom_id, date, journalID)
        item.cost = cost
    session.flush()
    session.commit()
    
#==============================================
### Setup Batches Model========================
class Batch(object):
    def __init__(self, base_id=None, batch_id=None, batch_num=None, batch_desc=None, rm_cost=None, 
                 fg_volume=None, per_lt=None, used=None):
        
        self.base_id = base_id
        self.batch_id = batch_id
        self.batch_num = batch_num
        self.batch_desc = batch_desc
        self.rm_cost = rm_cost
        self.fg_volume = fg_volume
        self.per_lt = per_lt
        self.used = used
        
        
BATCH, NUM, BATCH_DESC, BATCH_COST, FG_VOLUME, PER_LT, USED = range(7)
class ProductionBatchesModel(QAbstractTableModel):
    ### Model Initializer =====================
    def __init__(self, baseModel, parent=None):
        super(ProductionBatchesModel, self).__init__(parent)
        self.records = []
        self.records.append(Batch())
        self.baseAssembly = baseModel
        self.productionDetail = None
    
    ### Base Implementation ===================
    def rowCount(self, index=QModelIndex()):
        return len(self.records)
    
    def columnCount(self, index=QModelIndex()):
        return 7
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            if section == BATCH:
                return QVariant('Batch ID')
            elif section == NUM:
                return QVariant('Batch No.')
            elif section == BATCH_DESC:
                return QVariant('Description')
            elif section == BATCH_COST:
                return QVariant('RM Cost')
            elif section == FG_VOLUME:
                return QVariant('FG Volume')
            elif section == PER_LT:
                return QVariant('Per Lt.')
            elif section == USED:
                return QVariant('Unused')
        return QVariant(section + 1)
    
    def flags(self, index):
        flag = QAbstractTableModel.flags(self, index)
        if index.column() == BATCH:
            flag |= Qt.ItemIsEditable
        return flag
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.records)):
            return QVariant()
        record = self.records[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == BATCH:
                return QVariant(record.batch_id)
            elif column == NUM:
                return QVariant(record.batch_num)
            elif column == BATCH_DESC:
                return QVariant(record.batch_desc)
            elif column == BATCH_COST:
                if not record.rm_cost:
                    return QVariant(record.rm_cost)
                return QVariant(round(record.rm_cost, 4))
            elif column == FG_VOLUME:
                if not record.fg_volume:
                    return QVariant(record.fg_volume)
                return QVariant(round(record.fg_volume, 4))
            elif column == PER_LT:
                cost = float(getType(record.rm_cost))
                volume = float(getType(record.fg_volume))
                per_lt = nonZero(cost, 0) / nonZero(volume, 1)
                return QVariant(round(per_lt, 4))
            elif column == USED:
                if not record.used:
                    return QVariant()
                return QVariant('{:.0%}'.format(record.used))
        elif role == Qt.BackgroundColorRole:
            if (abs(nonZero(record.used, 0)) * 100) > 2:
                return QVariant(QColor(255, 130, 130))
        return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            row = index.row()
            record = self.records[row]
            column = index.column()
            if column == BATCH:
                batch_id = value.toInt()[0]
                record.batch_id = batch_id
                
                base_id = dLookup(BatchHeader.base_id, BatchHeader.batch_id==batch_id)
                record.base_id = base_id
                
                base_num = dLookup(BaseHeader.base_no, BaseHeader.base_id==base_id)
                record.batch_num = base_num
                
                desc = dLookup(BaseHeader.base_desc, BaseHeader.base_id==base_id)
                record.batch_desc = desc
                
                cost = self.calcCost(record)
                record.rm_cost = cost
                
                volume = self.calcVolume(record)
                record.fg_volume = volume
            
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
            return True
        return False
    
    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.records.insert(position + row + 1, Batch())
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.records = self.records[:position] + self.records[position + rows:]
        self.endRemoveRows()
        return True
    
    ### Data and Calculations =====================
    def calcUsed(self, record):
        base_id = record.base_id
        base_assembly_list = self.baseAssembly.filteredList(base_id)
        base_value = 0
        for base in base_assembly_list:
            if base.base_id:
                base_value += getType(base.value)
        batch_value = record.rm_cost
        percent = (float(getType(batch_value)) - float(getType(base_value))) / float(nonZero(batch_value, 1))
        return percent
    
    def calcVolume(self, record):
        base_id = record.base_id
        baseAssemblyList = self.baseAssembly.filteredList(base_id)
        volume = 0
        for base in baseAssemblyList:
            fgd_id = base.item_id
            iterList = self.productionDetail.filteredList(fgd_id)
            if iterList:
                volume += self.productionDetail.getSumVolume(iterList)
                volume = float(getType(volume))
        return volume
    
    def calcCost(self, record):
        batch_id = record.batch_id
        costQuery = Session().query(func.sum(BatchDetail.cost * BatchDetail.bom_qty).label('sumCost')).filter(BatchDetail.base_id == batch_id)
        for i in costQuery:
            sum_cost = i.sumCost
        sum_cost = float(getType(sum_cost))
        return sum_cost
    
    def sumUpCost(self, record):
        assert isinstance(record, Batch)
        rm_cost = float(getType(record.rm_cost))
        return rm_cost
    
    def getSumCost(self):
        sumCost = sum(map(self.sumUpCost, self.records), 0.0)
        return sumCost
    
    def updateModel(self):
        self.beginResetModel()
        for record in self.records:
            record.rm_cost = self.calcCost(record)
            record.fg_volume = self.calcVolume(record)
            record.used = self.calcUsed(record)
        self.endResetModel()
    
    def recordBatchDetailsToRMD(self, session, journal_id, date):
        records_ = []
        adjustments = []
        for record in self.records:
            batch_id = record.batch_id
            batch = session.query(BatchHeader).filter(BatchHeader.batch_id==batch_id)
            batch.update({'journal_id': journal_id})
            batchDetails = session.query(BatchDetail).filter(BatchDetail.base_id==batch_id)
            for item in batchDetails:
                bom_id = item.bom_id
                qty = item.bom_qty
                cost = item.cost
                total = getType(qty) * getType(cost)
                records_ += [BatchRMD(journal_id, bom_id, qty, cost, total, batch_id)]
                adjRmd = adjustAvgCost(session, bom_id, str(date), journal_id)
                if adjRmd:
                    adjustments += adjRmd
        return (records_, adjustments)
    
    def load(self, batchList):
        self.beginResetModel()
        self.records = []
        self.endResetModel()
        for record in batchList:
            batch_id = record.batch_id
            base_id = dLookup(BatchHeader.base_id, BatchHeader.batch_id==batch_id)
            base_num = dLookup(BaseHeader.base_no, BaseHeader.base_id==base_id)
            desc = dLookup(BaseHeader.base_desc, BaseHeader.base_id==base_id)
            self.records.append(Batch(base_id, batch_id, base_num, desc))
        self.updateModel()
    
            
    def clear(self):
        self.beginResetModel()
        self.records = []
        self.records.append(Batch())
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
        
        
    def checkForExtraBatches(self):
        for rec in self.records:
            if not rec.batch_id:
                continue
            base_id = rec.base_id
            base_num = rec.batch_num
            baseList = self.baseAssembly.filteredList(base_id)
            if not baseList:
                QMessageBox.warning(None, 'Calculating Production', 'There is no base-assembly for Batch: %s' % base_num, QMessageBox.Ok)
                return False
        return True
            
            
        
        
    
#==============================================
### Setup Detail Model ========================
FGD_ID, ITEM, QTY, DESC, VOLUME, PACK, RM_COST, DIRECT_COST, COST, TOTAL, QTY_PK = range(11)
class ProductionDetailModel(QAbstractTableModel):
    ### Model Initializer ============
    def __init__(self, batchModel, baseModel, bomModel, parent=None):
        super(ProductionDetailModel, self).__init__(parent)
        self.records = []
        self.records.append(FGD())
        self.headerList = ('ID', 'Item No', 'Qty', 'Description', 'Volume', 'Pack', 'RM Cost', 
                           'Direct Cost', 'Cost', 'Total', 'PK Qty')
        self.directCost = 0
        self.baseAssembly = baseModel
        self.bomAssembly = bomModel
        self.batches = batchModel
        
    ### Base Implementation ============
    def rowCount(self, index=QModelIndex()):
        return len(self.records)
    
    def columnCount(self, index=QModelIndex()):
        return 10
    
    def headerData(self, section, orientation, role):
        if role != Qt.DisplayRole:
            return QVariant()
        if orientation == Qt.Horizontal:
            return QVariant(self.headerList[section])
        return QVariant(section + 1)
    
    def flags(self, index):
        flag = QAbstractTableModel.flags(self, index)
        if index.column() in (ITEM, QTY, DESC):
            flag |= Qt.ItemIsEditable
        return flag
    
    def data(self, index, role=Qt.DisplayRole):
        if not index.isValid() or not (0 <= index.row() < len(self.records)):
            return QVariant()
        record = self.records[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            if column == FGD_ID:
                return QVariant(record.fgd_id)
            elif column == ITEM:
                item_no = dLookup(Items.item_no, Items.item_id==record.item_id)
                return QVariant(item_no)
            elif column == QTY:
                return QVariant(record.fgd_qty)
            elif column == DESC:
                return QVariant(record.fgd_desc)
            elif column == VOLUME:
                volume = self.volume(record.item_id)
                return QVariant(volume)
            elif column == PACK:
                pack = self.pack(record.item_id)
                return QVariant(pack)
            elif column == RM_COST:
                return QVariant(record.rm_cost)
            elif column == DIRECT_COST:
                return QVariant(record.direct_cost)
            elif column == COST:
                return QVariant(record.cost)
            elif column == TOTAL:
                cost = getType(record.cost)
                qty = getType(record.fgd_qty)
                total = qty * cost
                return QVariant(total)
            elif column == QTY_PK:
                pack = self.pack(record.item_id)
                if not pack:
                    return
                pack = float(pack)
                qty = record.fgd_qty
                qty_pk = round(qty / pack, 0)
                return QVariant(qty_pk)
        elif role == Qt.EditRole:
            if column == ITEM:
                return QVariant(record.item_id)
        return QVariant()
    
    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid() and role == Qt.EditRole:
            row = index.row()
            record = self.records[row]
            column = index.column()
            fg_id = dMax(FGD.fgd_id) + 1
            if column == ITEM:
                item = value.toInt()[0]
                record.item_id = item
                if not record.fgd_id:
                    record.fgd_id = fg_id + row
                desc = dLookup(Items.item_desc, Items.item_id==item)
                record.fgd_desc = str(desc)
            elif column == QTY:
                qty, ok = value.toFloat()
                if not ok:
                    return
                record.fgd_qty = qty
                record.rm_cost = self.calc_rmCost(record)
                record.direct_cost = self.calc_directCost(record)
                record.cost = self.calc_cost(record)
            elif column == DESC:
                record.fgd_desc = value.toString()
            self.emit(SIGNAL('dataChanged(QModelIndex, QModelIndex)'), index, index)
            return True
        return False
    
    def insertRows(self, position, rows=1, index=QModelIndex()):
        self.beginInsertRows(QModelIndex(), position, position + rows - 1)
        for row in range(rows):
            self.records.insert(position + row + 1, FGD())
        self.endInsertRows()
        return True
    
    def removeRows(self, position, rows=1, index=QModelIndex()):
        self.beginRemoveRows(QModelIndex(), position, position + rows - 1)
        self.records = self.records[:position] + self.records[position + rows:]
        self.endRemoveRows()
        return True
    
    ### Functions, Data and calculations
    def volume(self, item_id):
        volume = dLookup(Items.volume, Items.item_id==item_id)
        volume = getType(volume)
        return volume
    
    def pack(self, item_id):
        pack = dLookup(Items.pack, Items.item_id==item_id)
        return pack
    
    def sumUpTotal(self, record):
        qty = getType(record.fgd_qty)
        cost = getType(record.cost)
        total = qty * cost
        return float(total)
    
    def sumUpVolume(self, record):
        assert isinstance(record, FGD)
        qty = record.fgd_qty
        item_id = record.item_id
        volume = dLookup(Items.volume, Items.item_id==item_id)
        sumVolume = getType(qty) * getType(volume)
        return float(sumVolume)
    
    def getSumTotal(self, iterable=None):
        if not iterable:
            iterable = self.records
        sumTotal = sum(map(self.sumUpTotal, iterable), 0.0)
        return sumTotal
        
    def getSumVolume(self, iterable=None):
        if not iterable:
            iterable = self.records
        sumVolume = sum(map(self.sumUpVolume, iterable), 0.0)
        return sumVolume
    
    def calc_rmCost(self, record):
        #// sum up the value of the batches associated with fgd_id, and divide it by qty, because its per_lt * item_volume
        #// the percentage is already accounted for in the value
        fgd_id = record.fgd_id
        baseAssemblyList = self.baseAssembly.filteredList(None, fgd_id)
        batch_cost = sum(map(self.baseAssembly.sumUpValue, baseAssemblyList), 0.0)
        rm_cost = nonZero(batch_cost, 0) / getType(record.fgd_qty)
        
        #// simply enter the sum of bom cost, and will be multiplied by qty in the total column
        bomAssemblyList = self.bomAssembly.filteredList(fgd_id)
        bom_cost = sum(map(self.bomAssembly.sumUpCost, bomAssemblyList))
        rm_cost += nonZero(bom_cost, 0)
        rm_cost = round(rm_cost, 4)
        return rm_cost
    
    def calc_directCost(self, record):
        """ calculate direct cost for item
         the formula to calculate direct cost: directCost = volume((filing + labour) / sum(volume))
         """
        _directCost_ = self.directCost
        item_id = record.item_id
        volume = self.volume(item_id)
        sumVolume = self.getSumVolume(self.records)
        directCost = nonZero(volume, 0) * (nonZero(_directCost_, 0) / nonZero(sumVolume, 1))
        directCost = round(nonZero(directCost, 0), 4)
        return directCost
    
    def calc_cost(self, record):
        rmCost = record.rm_cost
        directCost = record.direct_cost
        cost = rmCost + directCost
        return cost
    
    def updateModel(self, directCost=0):
        self.beginResetModel()
        self.directCost = directCost
        for record in self.records:
            if record.item_id:
                record.rm_cost = self.calc_rmCost(record)
                record.direct_cost = self.calc_directCost(record)
                record.cost = self.calc_cost(record)
        self.endResetModel()
        
    def checkForExtraBatches(self):
        pass
        
    def updateBaseAssemblyValue(self):
        """ Goes through all base assemblies attached to the FG item, and calculates the value base on the batch,
        it basically looks up the per liter cost for the batch and multiplies it by total volume used by fg item 
        multiplied by percentage"""
        for record in self.records:
            fgd_id = record.fgd_id # // get the fgd_id, because thats the unique for the base assembly
            if not record.item_id:
                return
            fg_volume = getType(self.volume(record.item_id)) * getType(record.fgd_qty) # // get total volume for item
            # // create a list of indexes that contain base assemblies associated with this fgd_id 
            bIndex = self.batches.index(0, 1) # // specify an address to search in
            beginIndex = self.baseAssembly.index(0, 0) # // specify a beginning index
            baseIndexList = self.baseAssembly.match(beginIndex, Qt.DisplayRole, QVariant(fgd_id), hits=-1) # // create the list
            # // now go through the base assembly list and enter the value
            for i in baseIndexList:
                row = i.row() # // get row number
                base_num_index = self.baseAssembly.index(row, 1) # // specify index, to find the base_num
                base_num = self.baseAssembly.data(base_num_index).toString() # // get base_num, so we could match it to batch
                percentage_index = self.baseAssembly.index(row, 2) 
                percentage = self.baseAssembly.data(percentage_index).toFloat()[0]# // the percentage to be used in calculating value * percent
                index_list = self.batches.match(bIndex, Qt.DisplayRole, QVariant(base_num)) # // get the index of the batch to get the per-lt cost
                if not index_list:
                    QMessageBox.information(None, 'Calculating Production', 'Missing batch for Base: %s' % base_num, QMessageBox.Ok)
                    continue
                per_lt_row = index_list[0].row()
                per_lt_index = self.batches.index(per_lt_row, 5)
                per_lt = self.batches.data(per_lt_index, Qt.DisplayRole).toFloat()[0]
                value = round(fg_volume * per_lt * percentage, 4)
                value_index = self.baseAssembly.index(row, 4)
                if base_num:
                    self.baseAssembly.setData(value_index, QVariant(value), Qt.EditRole)
#                print 'ID: %s, Base: %s, fgVolume: %s, volum: %s, qty: %s, per_lt: %s, percent: %s, value: %s' \
#                % (fgd_id, base_num, fg_volume, self.volume(record.item_id),  record.fgd_qty, per_lt, percentage, value)
#                return
        
                

    ## Operations setup ============
    def clear(self):
        self.beginResetModel()
        self.records = []
        self.records.append(FGD())
        self.endResetModel()
        
        
    def filteredList(self, fgdId):
        records_ = []
        for record in self.records:
            if record.item_id:
                if str(record.fgd_id) == str(fgdId):
                    fgd_id = record.fgd_id
                    item_id = record.item_id
                    fgd_desc = record.fgd_desc
                    fgd_qty = record.fgd_qty
                    cost = record.cost
                    records_ += [FGD(fgd_id, item_id, fgd_desc, fgd_qty, cost)]
        return records_
    
    def save(self, journal_id):
        records_ = []
        for record in self.records:
            if record.item_id:
                fgd_id = int(record.fgd_id)
                item_id = int(record.item_id)
                fgd_desc = str(record.fgd_desc)
                fgd_qty = unicode(record.fgd_qty)
                rm_cost = unicode(record.rm_cost)
                direct_cost = unicode(record.direct_cost)
                cost = unicode(record.cost)
                total = getType(fgd_qty) * getType(cost)
                mix = dLookup(Items.mix_item, Items.item_id==item_id)
                item_no = dLookup(Items.item_no, Items.item_id==item_id)
                bom_id = dLookup(BOM.bom_id, BOM.bom_no==item_no)
                if eval(mix):
                    records_ += [ReceiveRMD(journal_id, bom_id, fgd_desc, fgd_qty, cost, cost, 0, 'Production Detail', total)]
                    records_ += [FGD(fgd_id, item_id, fgd_desc, fgd_qty, cost, journal_id, rm_cost, direct_cost)]
                else:
                    records_ += [FGD(fgd_id, item_id, fgd_desc, fgd_qty, cost, journal_id, rm_cost, direct_cost)]
        return records_
    
    def load(self, objectList, directCost=0):
        self.beginResetModel()
        self.records = []
        self.endResetModel()
        incr = 1
        row_id_list = []
        for item in objectList:
            if isinstance(item, PrepDetail):
                fg_id = dMax(FGD.fgd_id) + incr
                item_id = item.item_id
                fgd_qty = item.qty
                fgd_desc = dLookup(Items.item_desc, Items.item_id==item_id)
                self.records.append(FGD(fg_id, item_id, fgd_desc, fgd_qty))
                incr += 1
                row_id_list += [(item.pd_id, fg_id, item_id)]
            elif isinstance(item, FGD):
                fg_id = item.fgd_id
                item_id = item.item_id
                fgd_desc = item.fgd_desc
                fgd_qty = item.fgd_qty
                cost = item.cost
                journal_id = item.journal_id
                rm_cost = item.rm_cost
                direct_cost = item.direct_cost
                self.records.append(FGD(fg_id, item_id, fgd_desc, fgd_qty, cost, journal_id, rm_cost, direct_cost))
                row_id_list = None
        self.records.append(FGD())
        return row_id_list
        
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
        fgInc = position
        for rec in rows:
            col = rec.split('\t')
            fg_id = dMax(FGD.fgd_id) + 1 + fgInc
            item_id = dLookup(Items.item_id, Items.item_no==str(col[0]))
            if item_id:
                qty = float(getType(col[1])) if len(col) >= 2 else None
                desc = col[2] if len(col) >= 3 else dLookup(Items.item_desc, Items.item_id==item_id)
                myList += [FGD(fg_id, item_id, desc, qty)]
            fgInc += 1
        rowCount = len(myList)
        self.beginInsertRows(QModelIndex(), position, position + rowCount - 1)
        for row in range(rowCount):
            self.records.insert(position + row, myList[row])
        self.endInsertRows()
        self.updateModel()
        return rowCount


#=======================================================================
### Receive Form Setup =====
class ReceiveFormDialog(QDialog):
    def __init__(self, model, bomModel, session, journal_id, parent=None):
        super(ReceiveFormDialog, self).__init__(parent)
        
        self.journal_id = journal_id
        self.journal_date = self.parent().getDate()
        self.session = session
        self.model = model
        
        saveButton = QPushButton('&Save')
        saveButton.setVisible(False)
        clearButton = QPushButton('C&lear')
        closeButton = QPushButton('Close')
        self.date_dateEdit = QDateEdit()
        self.date_dateEdit.setCalendarPopup(True)
        self.date_dateEdit.setDate(self.journal_date)
        label = QLabel('Total')
        self.v_total_label = QLabel()
        self.v_total_label.setMinimumSize(QSize(96, 25))
        self.v_total_label.setFrameShape(QFrame.Box)
        
        
        self.detailView = QTableView()
        self.detailView.setModel(self.model)
        itemModel = bomModel
        delegate = GenericDelegate(self)
        delegate.insertDelegate(receiveform.ITEM, ComboDelegate(itemModel, True))
        delegate.insertDelegate(receiveform.DESCRIPTION, PlainTextDelegate())
        delegate.insertDelegate(receiveform.QTY, NumberDelegate())
        delegate.insertDelegate(receiveform.PRICE, NumberDelegate())
        delegate.insertDelegate(receiveform.MEMO, PlainTextDelegate())
        self.detailView.setItemDelegate(delegate)
        self.detailView.setColumnHidden(receiveform.SHIPPING, True)
        self.detailView.setColumnHidden(receiveform.COST, True)
        self.detailView.setColumnHidden(receiveform.MEMO, True)
        
        spacer = QSpacerItem(20, 10, QSizePolicy.Expanding, QSizePolicy.Minimum)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(saveButton)
        buttonLayout.addWidget(clearButton)
        buttonLayout.addWidget(closeButton)
        buttonLayout.addItem(spacer)
        buttonLayout.addWidget(self.date_dateEdit)
        buttonLayout.addItem(spacer)
        buttonLayout.addWidget(label)
        buttonLayout.addWidget(self.v_total_label)
        
        layout = QVBoxLayout()
        layout.addLayout(buttonLayout)
        layout.addWidget(self.detailView)
        self.setLayout(layout)
        
        self.updateSumTotal()
        
        self.date_dateEdit.dateChanged.connect(self.setParentDate)
        saveButton.clicked.connect(lambda: self.save(self.journal_id, self.journal_date))
        clearButton.clicked.connect(self.clear)
        closeButton.clicked.connect(self.reject)
        
        self.resize(QSize(600, 400))
        self.setWindowTitle(localTITLE)
        
        self.model.dataChanged.connect(self.setDirty)
        self.model.dataChanged.connect(self.autoAddRow)
        
    def setParentDate(self):
        date = self.date_dateEdit.date()
        self.parent().dateDateEdit.setDate(date)
        self.journal_date = date.toPyDate()
        
    def setDirty(self):
        self.parent().setDirty()
        self.updateSumTotal()
    
    def setJournalInfo(self, journal_id, journal_date):
        self.journal_date = journal_date
        self.journal_id = journal_id
        
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        if self.detailView.hasFocus():
            copyAction = menu.addAction('Copy', QObject, 'Ctrl+C')
            pasteAction = menu.addAction('Paste', QObject, 'Ctrl+V')
            insertAction = menu.addAction("Insert Line", QObject, "Ctrl+I")
            deleteAction = menu.addAction("Delete Line", QObject, "Ctrl+D")
            copyAction.triggered.connect(self.copy)
            pasteAction.triggered.connect(self.paste)
            self.connect(insertAction, SIGNAL("triggered()"), self.insertRow)
            self.connect(deleteAction, SIGNAL("triggered()"), self.removeRow)
            addActions(self, self.detailView, (copyAction, pasteAction, insertAction, deleteAction))
        menu.exec_(event.globalPos())
        
    def updateSumTotal(self):
        sum_total = QString('%L1').arg(self.model.getSumTotal(), 0, 'f', 2)
        self.v_total_label.setText(sum_total)
        
    def copy(self):
        if self.model.rowCount() <= 1:
            return
        selectedItems = self.detailView.selectionModel().selectedIndexes()
        self.model.copy(selectedItems)
        
    def paste(self):
        row = self.detailView.currentIndex().row()
        self.model.paste(row)
        self.updateSumTotal()
           
    def autoAddRow(self):
        view = self.detailView
        row = view.currentIndex().row()
        if self.model.rowCount() ==  row + 1:
            self.insertRow()
            
    def insertRow(self):
        view = self.detailView
        index = view.currentIndex()
        row = index.row()
        self.model.insertRows(row)
        view.setFocus()
        view.setCurrentIndex(index)
    
    def removeRow(self):
        if self.model.rowCount() <= 1:
            return
        view = self.detailView
        rowsSelected = view.selectionModel().selectedRows()
        if not rowsSelected:
            row = view.currentIndex().row()
            rows = 1
        else:
            for i in rowsSelected:
                row = i.row()
            rows = len(rowsSelected)
            row = row - rows + 1
        self.model.removeRows(row, rows)
        
    def save(self, journal_id, journal_date):
        details, adjustments = self.model.save(journal_id, journal_date)
        self.session.add_all(details)
        self.session.add_all(adjustments)
        self.sendToDB()
        self.accept()
        
    def delete(self):
        self.session.query(ReceiveRMD).filter(ReceiveRMD.journal_id==self.journal_id).delete()
        self.sendToDB()
        
    def sendToDB(self):
        try:
            self.session.flush
            self.session.commit()
        except Exception, e:
            self.session.rollback()
            raise e
        
    def clear(self):
        self.model.clear()
        
#=======================================================================
### Form Setup =============
class ProductionForm(QDialog, ui_forms.ui_productionform.Ui_ProductionForm):
    
    def __init__(self, baseListModel, batchListModel, itemModel, bomModel, prepModel, parent=None):
        super(ProductionForm, self).__init__(parent)
        self.setupUi(self)
        self.session = Session()
        self.dirty = False
        self.editing = False
        self.record_id = None
        self.current_record = None
        self.directCost = 0
        self.my_parent = parent
        
        ### setup text's and labels
        self.v_prodID_label.setText(str(dMax(JournalHeader.journal_id) + 1))
        self.dateDateEdit.setDate(self.my_parent.getDate())
        
        ### Prep combo box setup ###
        prep_view = modelsandviews.ItemView(prepModel, False, self.prep_comboBox)
        self.prep_comboBox.setModel(prepModel)
        self.prep_comboBox.setView(prep_view)
        self.prep_comboBox.setFixedWidth(150)
        self.prep_comboBox.setCurrentIndex(-1)
        self.prep_comboBox.setModelColumn(0)
        self.prep_comboBox.setEditable(True)
        
        
        
        ### instantiate models
        self.baseAssemblyModel = itemform.BaseAssemblyModel()
        self.bomAssemblyModel = itemform.ItemAssemblyModel()
        self.batchesModel = ProductionBatchesModel(self.baseAssemblyModel)
        self.detailModel = ProductionDetailModel(self.batchesModel, self.baseAssemblyModel, self.bomAssemblyModel)
        self.batchesModel.productionDetail = self.detailModel
        self.receiveModel = receiveform.ReceivingDetailModel(self.session)
        
        ### setup detail view ###
        self.itemModel = itemModel
        tblView = self.productionTableView
        tblView.setModel(self.detailModel)
        delegate = GenericDelegate(self)
        delegate.insertDelegate(ITEM, ComboDelegate(self.itemModel, True))
        delegate.insertDelegate(QTY, NumberDelegate())
        delegate.insertDelegate(DESC, PlainTextDelegate())
        tblView.setItemDelegate(delegate)
        tblView.setColumnWidth(ITEM, 50)
        tblView.setColumnWidth(QTY, 75)
        tblView.setColumnWidth(DESC, 250)
        tblView.setColumnWidth(VOLUME, 50)
        tblView.setColumnWidth(PACK, 50)
        tblView.setColumnWidth(RM_COST, 75)
        tblView.setColumnWidth(DIRECT_COST, 75)
        tblView.setColumnWidth(COST, 75)
        tblView.setColumnHidden(FGD_ID, True)
        
        ### setup Assembly views ###
        self.bsView.setVisible(False)
        baseModel = baseListModel
        self.baseAssemblyProxy = QSortFilterProxyModel()
        self.baseAssemblyProxy.setFilterKeyColumn(0)
        self.baseAssemblyProxy.setSourceModel(self.baseAssemblyModel)
        self.baseAssembly_view = modelsandviews.AssemblyTableView(self.baseAssemblyProxy, baseModel, self)
        self.verticalLayout.addWidget(self.baseAssembly_view)
        
        self.bmView.setVisible(False)
        self.bomModel = bomModel
        self.bomAssemblyProxy = QSortFilterProxyModel()
        self.bomAssemblyProxy.setSourceModel(self.bomAssemblyModel)
        self.bomAssemblyProxy.setFilterKeyColumn(0)
        self.bomAssembly_view = modelsandviews.AssemblyTableView(self.bomAssemblyProxy, self.bomModel, self)
        self.verticalLayout.addWidget(self.label_15)
        self.verticalLayout.addWidget(self.bomAssembly_view)
        
        ### setup batches view ###
        self.batchList = batchListModel
        self.batchesTableView.setModel(self.batchesModel)
        delegate = GenericDelegate(self)
        delegate.insertDelegate(BATCH, ComboDelegate(self.batchList, False))
        self.batchesTableView.setItemDelegate(delegate)
        self.batchesTableView.setColumnWidth(BATCH, 50)
        self.batchesTableView.setColumnWidth(NUM, 75)
        self.batchesTableView.setColumnWidth(BATCH_DESC, 150)
        self.batchesTableView.setColumnWidth(FG_VOLUME, 75)
        self.batchesTableView.setColumnWidth(PER_LT, 75)
        self.batchesTableView.setColumnWidth(USED, 50)
        
        
        ### setup receive form
        self.dialog = ReceiveFormDialog(self.receiveModel, self.bomModel, self.session, None, self)
        
        ### Signal and Slot Setup ###
        self.dateDateEdit.dateChanged.connect(self.setParentDate)
        self.detailModel.dataChanged.connect(lambda: self.autoAddRow(self.productionTableView, self.detailModel))
        self.batchesModel.dataChanged.connect(lambda: self.autoAddRow(self.batchesTableView, self.batchesModel))
        self.detailModel.dataChanged.connect(self.addAssemblies)
        self.productionTableView.selectionModel().currentRowChanged.connect(self.setFilter)
        self.productionTableView.doubleClicked.connect(self.editItem)
        self.prep_comboBox.currentIndexChanged.connect(self.fillWithPrep)
        
        self.calcButton.clicked.connect(self.recalc)
        self.saveButton.clicked.connect(self.save)
        self.newButton.clicked.connect(self.clear)
        self.receiveButton.clicked.connect(self.openReceive)
        self.printButton.clicked.connect(self.printReport)
        self.deleteButton.clicked.connect(lambda: self.delete(header=True))
        self.closeButton.clicked.connect(self.accept)
        
        self.setupConnection()

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
        date = self.dateDateEdit.date().toPyDate()
        self.my_parent.setDate(date) 
    
    def getDate(self):
        date = self.dateDateEdit.date()
        date = date.toPyDate()
        return date
        
    def contextMenuEvent(self, event):
        menu = QMenu(self)
        if self.productionTableView.hasFocus():
            view = self.productionTableView
            model = self.detailModel
            copyAction = menu.addAction('Copy', QObject)
            pasteAction = menu.addAction('Paste', QObject)
            insertAction = menu.addAction("Insert Line", QObject)
            deleteAction = menu.addAction("Delete Line", QObject)
            copyAction.triggered.connect(lambda: self.copy(view, model))
            pasteAction.triggered.connect(lambda: self.paste(view, model))
            insertAction.triggered.connect(lambda: self.insertRow(view, model))
            deleteAction.triggered.connect(lambda: self.removeRow(view, model))
        elif self.batchesTableView.hasFocus():
            view = self.batchesTableView
            model = self.batchesModel
            copyAction = menu.addAction('Copy', QObject)
            insertAction = menu.addAction("Insert Line", QObject)
            deleteAction = menu.addAction("Delete Line", QObject)
            copyAction.triggered.connect(lambda: self.copy(view, model))
            insertAction.triggered.connect(lambda: self.insertRow(view, model))
            deleteAction.triggered.connect(lambda: self.removeRow(view, model))
        elif self.bomAssembly_view.hasFocus():
            view = self.bomAssembly_view
            model = self.bomAssemblyModel
            copyAction = menu.addAction('Copy', QObject)
            insertAction = menu.addAction("Insert Line", QObject)
            deleteAction = menu.addAction("Delete Line", QObject)
            copyAction.triggered.connect(lambda: self.copy(view, model))
            insertAction.triggered.connect(lambda: self.insertRow(view, model))
            deleteAction.triggered.connect(lambda: self.removeRow(view, model))
        elif self.baseAssembly_view.hasFocus():
            view = self.baseAssembly_view
            model = self.baseAssemblyModel
            copyAction = menu.addAction('Copy', QObject)
            insertAction = menu.addAction("Insert Line", QObject)
            deleteAction = menu.addAction("Delete Line", QObject)
            copyAction.triggered.connect(lambda: self.copy(view, model))
            insertAction.triggered.connect(lambda: self.insertRow(view, model))
            deleteAction.triggered.connect(lambda: self.removeRow(view, model))
        menu.exec_(event.globalPos())
        
    def fgd_id(self):
        index = self.productionTableView.currentIndex()
        row = index.row()
        idIndex = self.detailModel.index(row, 0)
        fgd_id, ok = self.detailModel.data(idIndex, Qt.DisplayRole).toInt()
        return (fgd_id, ok)
    
    def copy(self, view, model):
        if model.rowCount() <= 1:
            return
        selectedItems = view.selectionModel().selectedIndexes()
        model.copy(selectedItems)
        
    def paste(self, view, model):
        row = view.currentIndex().row()
        rows = model.paste(row)
        return
        for i in range(rows):
            index = view.model().index(i + row, 1)
            view.setCurrentIndex(index)
            self.addAssemblies(recall=False)
        self.updateSumTotals()
        
    def autoAddRow(self, view, model):
        self.setDirty()
        row = view.currentIndex().row()
        if model.rowCount() == row + 1:
            self.insertRow(view, model)
        
    def insertRow(self, view, model):
        if view is not None:
            index = view.currentIndex()
            row = index.row() + 1
            if model in (self.bomAssemblyModel, self.baseAssemblyModel):
                fgd_id, ok = self.fgd_id()
                if ok:
                    model.insertRows(row, item_id=fgd_id)
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
            
        if model in (self.baseAssemblyModel, self.bomAssemblyModel):
            if model == self.baseAssemblyModel:
                proxy_index = self.baseAssemblyProxy.index(view.currentIndex().row(), 0)
                row = self.baseAssemblyProxy.mapToSource(proxy_index).row()
            elif model == self.bomAssemblyModel:
                proxy_index = self.bomAssemblyProxy.index(view.currentIndex().row(), 0)
                row = self.bomAssemblyProxy.mapToSource(proxy_index).row()
            rows = 1
        model.removeRows(row, rows)
        if model.rowCount() < 1:
            self.insertRow(view, model)
        self.updateSumTotals()
        self.setDirty()
        
    def deleteAssemblies(self, fgd_id):
        beginIndex = self.baseAssemblyModel.index(0, 0)
        baseIndexList = self.baseAssemblyModel.match(beginIndex, Qt.DisplayRole, QVariant(fgd_id), hits=-1)
        beginIndex = self.bomAssemblyModel.index(0, 0)
        bomIndexList = self.bomAssemblyModel.match(beginIndex, Qt.DisplayRole, QVariant(fgd_id), hits=-1)
        if not baseIndexList:
            return
        if not bomIndexList:
            return
        while baseIndexList:
            position = baseIndexList[0].row()
            self.baseAssemblyModel.removeRows(position)
            baseIndexList = self.baseAssemblyModel.match(beginIndex, Qt.DisplayRole, QVariant(fgd_id))
        while bomIndexList:
            position = bomIndexList[0].row()
            self.bomAssemblyModel.removeRows(position)
            bomIndexList = self.bomAssemblyModel.match(beginIndex, Qt.DisplayRole, QVariant(fgd_id))
            
    def addAssemblies(self, recall=False):
        if recall == True:
            baseList = self.session.query(FGDBatchAssembly).join(FGD).filter(FGD.journal_id==self.record_id)
            itemList = self.session.query(FGDBOMAssembly).join(FGD).join(AssemblyRMD) \
                                            .filter(FGD.journal_id==self.record_id)
            clear = True
            fgd_id = None
        else:
            index = self.productionTableView.currentIndex()
            if not index.column() == 1:
                return
            row = index.row()
            myIndex = self.detailModel.index(row, 1)
            fgd_id = self.fgd_id()[0]
            fg_num = str(self.detailModel.data(myIndex, Qt.DisplayRole).toString())
            fg_id = dLookup(Items.item_id, Items.item_no==fg_num)
            self.deleteAssemblies(fgd_id)
            baseList = self.session.query(BaseAssembly).filter(BaseAssembly.item_id==fg_id)
            itemList = self.session.query(ItemAssembly).filter(ItemAssembly.item_id==fg_id)
            clear = False
        self.baseAssemblyModel.load(baseList, clear, fgd_id)
        self.bomAssemblyModel.load(itemList, clear, fgd_id)
        self.baseAssemblyProxy.reset()
        self.bomAssemblyProxy.reset()

    def setFilter(self):
        fgd_id = self.fgd_id()[0]
        self.bomAssemblyProxy.setFilterFixedString(str(fgd_id))
        self.baseAssemblyProxy.setFilterFixedString(str(fgd_id))
    
    def editItem(self):
        row = self.productionTableView.currentIndex().row()
        index = self.detailModel.index(row, ITEM)
        item_id = self.detailModel.data(index, Qt.EditRole).toString()
        if not item_id:
            return
        form = self.my_parent.itemForm()
        form.recall(1, str(item_id))
        
    
    def fillWithPrep(self):
        self.clearModels()
        #// get prep id
        prep_id = str(self.prep_comboBox.currentText())
        #// get batch list, and load it into batch model
        batch_list = self.session.query(BatchHeader).filter(BatchHeader.prep_id==prep_id)
        self.batchesModel.load(batch_list)
        #// now lets load items and assemblies
        #// first w'ill load items then w'ill loop through it to get the fgd and load assemblies for each one
        details = self.session.query(PrepDetail).filter(PrepDetail.header_id==prep_id)
        row_id_list = self.detailModel.load(details)
        for row in row_id_list:
            pd_id, fgd_id, fg_id = row
            clear = False
            base_list = self.session.query(PrepAssembly).filter(PrepAssembly.pd_id==pd_id)
            itemList = self.session.query(ItemAssembly).filter(ItemAssembly.item_id==fg_id)
            self.baseAssemblyModel.load(base_list, clear, fgd_id)
            self.bomAssemblyModel.load(itemList, clear, fgd_id)
        self.baseAssemblyProxy.reset()
        self.bomAssemblyProxy.reset()
        self.setFilter()
        self.editing = False
            
        
    ### Calculations
    def updateSumTotals(self):
        fg_volume = round(nonZero(self.detailModel.getSumVolume(), 0), 2)
        rm_cost = round(nonZero(self.batchesModel.getSumCost(), 0), 2)
        fg_total_cost = self.detailModel.getSumTotal()
        filing = float(getType(self.filingChargeLineEdit.text()))
        labour = float(getType(self.labourChargeLineEdit.text()))
        self.directCost = filing + labour
        per_lt = round(nonZero(filing, 0) / nonZero(fg_volume, 1), 2)
        self.v_fgVolume_label.setText(str('{:,.2f}'.format(fg_volume)))
        self.v_rmCost_label.setText(str('{:,.2f}'.format(rm_cost)))
        self.v_totalFGCost_label.setText(str('{:,.2f}'.format(fg_total_cost)))
        self.v_costPerLT_label.setText(str('{:,.2f}'.format(per_lt)))
        self.v_totalFees_label.setText(str('{:,.2f}'.format(self.directCost)))
        

    def recalc(self):
        date = self.dateDateEdit.date()
        date = date.toPyDate()
        date = str(date)
        journal_id = str(self.v_prodID_label.text())
        updateCostForBatch(self.session, date, journal_id)
        self.bomAssemblyModel.updateCost(journal_id, date)
        self.batchesModel.updateModel()
        self.detailModel.updateBaseAssemblyValue()
        self.detailModel.updateModel(self.directCost)
        self.batchesModel.updateModel() #// need to update batches model again because the used column is based on data from baseAssembly
        self.updateSumTotals()
        
    ### Form operations
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
        
        
    
    def openReceive(self):
        journal_id = int(self.v_prodID_label.text()) if self.v_prodID_label.text() else None
        journal_date = self.dateDateEdit.date().toPyDate()
        self.dialog.setJournalInfo(journal_id, journal_date)
        self.dialog.updateSumTotal()
        self.dialog.exec_()
        
        
    def save(self):
        #// make sure there are details to be recorded
        if self.detailModel.rowCount() <= 1 :
            QMessageBox.information(self, 'Save Production - %s' % localTITLE, 'No details found', QMessageBox.Ok)
            return
        #// check if all batches are being used
        ok = self.batchesModel.checkForExtraBatches()
        if not ok:
            return
        #// prepare the values to be saved for the header
        journal_type = 'Production'
        qDate = self.dateDateEdit.date()
        journal_date = qDate.toPyDate()
        journal_no = str(self.refnoLineEdit.text())
        journal_memo = str(self.notesTextEdit.toPlainText())
        filing_charge = unicode(self.filingChargeLineEdit.text())
        labour_charge = unicode(self.labourChargeLineEdit.text())
        mix = False
        modified_date = QDateTime().currentDateTime().toPyDateTime()
        log_memo = 'Created'
        progress = QProgressDialog('Recording Production...', 'Abort Record', 0, 4)
        progress.setCancelButton(None)
        progress.setValue(1)
        progress.show()
        progress.setLabelText('Calculating')
        QApplication.processEvents()
        #// if journal is being edited, then update header, delete details and repost a new.
        if self.editing:
            #// check for closing date issues
            old_date = dLookup(JournalHeader.journal_date, JournalHeader.journal_id==self.record_id)
            if not closingDate(old_date):
                return
            if not closingDate(journal_date):
                return
            log_memo = 'Modified'
            #// update journal header info
            journal_id = self.record_id
            self.current_record = self.session.query(ProductionHeader).filter(ProductionHeader.journal_id==self.record_id)
            self.current_record.update({'journal_date': journal_date, 'journal_no': journal_no, 'journal_memo': journal_memo,
                                        'filing_charge': filing_charge, 'labour_charge': labour_charge, 'mix': mix,
                                         'modified_date': modified_date})
            #// delete old details from db
            self.delete(header=False)
        #// if its a new journal
        else:
            #// check for closing issues
            if not closingDate(journal_date):
                return
            #// make sure to get correct journal_id
            journal_id = dMax(JournalHeader.journal_id) + 1
            #// post header info
            self.session.add(ProductionHeader(journal_id, journal_type, journal_date, journal_no, journal_memo,
                                              filing_charge, labour_charge, mix, modified_date))
        #// update the journal_id on the prep
        prep_id = str(self.prep_comboBox.currentText())
        if prep_id:
            self.session.query(PrepHeader).filter(PrepHeader.prep_id==prep_id).update({'prod_id': journal_id})
        #// but before reporting details recalculate
        #// recalculate
        self.recalc()
        progress.setLabelText('Posting')
        progress.setValue(2)
        #// post-repost details
        if self.receiveModel.rowCount() > 1:
            self.dialog.save(journal_id, journal_date)
        details = self.detailModel.save(journal_id)
        rmDetails, batchAdjustments = self.batchesModel.recordBatchDetailsToRMD(self.session, journal_id, journal_date)
        baseAssemblies = self.baseAssemblyModel.save(None, 'FGDBatchAssembly')
        bomAssemblies = self.bomAssemblyModel.save(journal_id, 'FGDBOMAssembly', None, journal_date)
        bomRM, smAdjustments = self.bomAssemblyModel.save(journal_id, 'AssemblyRMD', self.session, journal_date, self.detailModel)
        progress.setLabelText('Saving')
        progress.setValue(3)
        self.session.add_all(details)
        self.session.add_all(rmDetails)
        self.session.add_all(batchAdjustments)
        self.session.add_all(baseAssemblies)
        self.session.add_all(bomAssemblies)
        self.session.add_all(bomRM)
        self.session.add_all(smAdjustments)
        self.session.add(Logs(journal_id, self.my_parent.user_id, modified_date, log_memo))
        self.sendToDB()
        self.v_prodID_label.setText(str(journal_id))
        self.editing = True
        self.dirty = False
        self.record_id = journal_id
        progress.setValue(4)
        self.setWindowTitle('%s - (Data Saved)' % localTITLE)
        self.session.close()
        
    def delete(self, header):
        if not self.record_id:
            return
        journal_id = self.record_id
        if header:
            #// check for closing date issues
            old_date = dLookup(JournalHeader.journal_date, JournalHeader.journal_id==self.record_id)
            if not closingDate(old_date):
                return
            answer = QMessageBox.question(self, "Delete - %s" % localTITLE, "Are you sure you " \
                                                  "want to delete Production: %s:, %s" % (self.v_prodID_label.text(),
                                                                                    self.dateDateEdit.date().toPyDate()), 
                                                  QMessageBox.Yes| QMessageBox.No, QMessageBox.NoButton)
            if answer == QMessageBox.No:
                return
            self.session.query(ProductionHeader).filter(ProductionHeader.journal_id==journal_id).delete()
            self.session.query(BatchHeader).filter(BatchHeader.journal_id==journal_id).update({'journal_id': None})
            prep_id = str(self.prep_comboBox.currentText())
            if prep_id:
                self.session.query(PrepHeader).filter(PrepHeader.prod_id==journal_id).update({'prod_id': None})
            
        self.deleteDBAssemblies(journal_id)
        self.session.query(FGD).filter(FGD.journal_id==journal_id).delete()
        self.session.query(RMD).filter(RMD.journal_id==journal_id).delete()
        
            
        if header:
            log_memo = 'Deleted - ProdID: %s, Date: %s, ProdNo: %s' % (self.record_id, 
                                                                       self.dateDateEdit.date().toPyDate(),
                                                                       str(self.refnoLineEdit.text()))
            self.session.add(Logs(self.record_id, self.my_parent.user_id, QDateTime().currentDateTime().toPyDateTime(), log_memo))
            self.sendToDB()
            self.clear()
    
    def deleteDBAssemblies(self, journal_id):
        fgdQry = self.session.query(FGD.fgd_id).filter(FGD.journal_id==journal_id).subquery()
        self.session.query(FGDBatchAssembly).filter(FGDBatchAssembly.item_id.in_(fgdQry)).delete('fetch')
        self.session.query(FGDBOMAssembly).filter(FGDBOMAssembly.item_id.in_(fgdQry)).delete('fetch')
        
    
    def sendToDB(self):
        try:
            self.session.flush
            self.session.commit()
        except Exception, e:
            self.session.rollback()
            raise e
    
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
        self.current_record = self.session.query(ProductionHeader).filter(ProductionHeader.journal_id==journal_id)
        for record in self.current_record:
            self.v_prodID_label.setText(str(journal_id))
            self.dateDateEdit.setDate(record.journal_date)
            self.refnoLineEdit.setText(str(record.journal_no))
            self.notesTextEdit.setText(str(record.journal_memo))
            self.filingChargeLineEdit.setText(str(record.filing_charge))
            self.labourChargeLineEdit.setText(str(record.labour_charge))
            self.directCost = getType(record.filing_charge) + getType(record.labour_charge)
        prep_id = dLookup(PrepHeader.prep_id, PrepHeader.prod_id==journal_id)
        if prep_id:
            self.prep_comboBox.lineEdit().setText(prep_id)
        batch_list = self.session.query(BatchHeader).filter(BatchHeader.journal_id==journal_id)
        details = self.session.query(FGD).filter(FGD.journal_id==journal_id)
        receive = self.session.query(ReceiveRMD).join(BOM).filter(ReceiveRMD.journal_id==journal_id).filter(BOM.mix_item==False)
        self.detailModel.load(details)
        self.batchesModel.load(batch_list)
        self.receiveModel.load(receive)
        self.addAssemblies(True)
        self.setFilter()
        self.updateSumTotals()
        self.editing = True
    
    def clearModels(self):
        self.batchesModel.clear()
        self.detailModel.clear()
        self.baseAssemblyModel.clear()
        self.bomAssemblyModel.clear()
        self.receiveModel.clear()
        
    def clear(self):
        self.prep_comboBox.blockSignals(True)
        self.clearModels()
        self.my_parent.refreshModels()
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
        
        if defaultDate() == 'current':
            self.dateDateEdit.setDate(QDate.currentDate())
        self.v_prodID_label.setText(str(dMax(JournalHeader.journal_id) + 1))
        
        self.editing = False
        self.dirty = False         
        self.setWindowTitle(localTITLE)
        
        self.prep_comboBox.blockSignals(False)

        
    def printReport(self):
        journal_id = str(self.v_prodID_label.text())
        if not journal_id:
            return
        reportModel = reporting.ReportModel('Production')
        self.refreshReport(reportModel)
        self.my_parent.reportForm(reportModel, self)
        
    def refreshReport(self, model, report=None):
        journal_id = str(self.v_prodID_label.text())
        productionQuery(self.session, journal_id, model)
        
    def formClosed(self):
        self.my_parent.formClosed()
        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    setupDatabase("Production.sqlite")

    form = ProductionForm()
    form.show()
    app.exec_()