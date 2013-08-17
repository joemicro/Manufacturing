import os
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from databaseschema import *
from functions import *
import modelsandviews

class ReportDialog(QDialog):
    def __init__(self, bomModel, parent=None):
        super(ReportDialog, self).__init__(parent)
        dRange_label = QLabel('Range')
        self.range_comboBox = modelsandviews.DateRangeComboBox()
        from_label = QLabel('From')
        self.from_date = QDateEdit()
        self.from_date.setCalendarPopup(True)
        to_label = QLabel('To')
        self.to_date = QDateEdit()
        self.to_date.setCalendarPopup(True)
        bom_label = QLabel('Item')
        self.bom_comboBox = QComboBox()
        view = modelsandviews.ItemView(bomModel)
        self.bom_comboBox.setModel(bomModel)
        self.bom_comboBox.setView(view)
        self.bom_comboBox.setModelColumn(1)
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok| QDialogButtonBox.Cancel)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        
        layout = QGridLayout()
        layout.addWidget(dRange_label, 0, 0)
        layout.addWidget(self.range_comboBox, 0, 1)
        layout.addWidget(from_label, 1, 0)
        layout.addWidget(self.from_date, 1, 1)
        layout.addWidget(to_label, 1, 2)
        layout.addWidget(self.to_date, 1, 3)
        layout.addWidget(bom_label, 2, 0)
        layout.addWidget(self.bom_comboBox, 2 ,1, 1, 2)
        layout.addWidget(buttonBox, 3, 0, 1, 3)
        self.setLayout(layout)
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
        self.setWindowTitle('Report Settings')
        self.setWindowIcon(QIcon(':/icons/settings'))
        
        self.range_comboBox.currentIndexChanged.connect(lambda: 
                                                          self.dateRangeSelection(self.range_comboBox, 
                                                                                  self.from_date, 
                                                                                  self.to_date))
    
    def dateRangeSelection(self, rangeCombo, dateFrom, dateTo):
        selection = self.range_comboBox.currentText()
        date_from, date_to = dateRange(selection)
        dateFrom.setDate(date_from)
        dateTo.setDate(date_to)
        

def productionQuery(session, journal_id, model):
                                     
    inv_qty = case([(JournalHeader.journal_type == 'Bill', RMD.qty), 
                    (and_(JournalHeader.journal_type == 'Production', RMD.rec_type == 'rcv'), RMD.qty),],
                    else_ = - RMD.qty).label('inv_qty')
    inv_value = case([(JournalHeader.journal_type == 'Bill', RMD.total), 
                    (and_(JournalHeader.journal_type == 'Production', RMD.rec_type == 'rcv'), RMD.total),],
                    else_ = - RMD.total).label('inv_value')                
    rmSum_query = session.query(RMD.bom_id, func.sum(inv_qty).label('sumQty'), func.sum(inv_value).label('sumValue')) \
                    .group_by(RMD.bom_id).join(JournalHeader) \
                    .filter(RMD.journal_id==journal_id).subquery()
    
    rm_sum_detail = session.query(BOM.bom_no, rmSum_query.c.sumQty, BOM.bom_desc, 
                                  (rmSum_query.c.sumValue / rmSum_query.c.sumQty).label('rmCost'), rmSum_query.c.sumValue) \
                                  .join(rmSum_query)
    
    journal_header = session.query(ProductionHeader).filter(ProductionHeader.journal_id==journal_id)
    
    fgd_detail = session.query(Items.item_no, (FGD.fgd_qty / Items.pack).label('pkQty'), Items.item_cost, Items.item_desc, 
                                     FGD.fgd_qty, FGD.rm_cost, FGD.direct_cost, FGD.cost, (Items.pack * FGD.cost).label('pkCost')) \
                                     .join(FGD) \
                                     .filter(FGD.journal_id==journal_id).filter(Items.mix_item==False)
    headerNames = [('Production', 'journal_id', 25, 'string'), ('Date', 'journal_date', 25, 'date'), ('Ref No', 'journal_no', 25, 'string'),
                   ('Filing', 'filing_charge', 50, 'number'), ('Labour', 'labour_charge', 50, 'number')]
    
    mainData = []
    mainNames = []
    mainTotals = []
    subData = []
    subNames = []
    subTotals = []
    
    volume_query = session.query(func.sum(FGD.fgd_qty * Items.volume).label('sumVolume')).join(Items).filter(FGD.journal_id==journal_id)
#    rmCost_total = session.query(func.sum(RMD.total).label('rmTotal')).filter(RMD.journal_id==journal_id)
    rmCost_total = session.query(func.sum(rmSum_query.c.sumValue).label('rmTotal'))
    fgCost_total = session.query(func.sum(FGD.fgd_qty * FGD.cost).label('fgTotal')).filter(FGD.journal_id==journal_id)
    
    for i in volume_query:
        volume = i.sumVolume
        
    for i in rmCost_total:
        rmTotal = i.rmTotal
        
    for i in fgCost_total:
        fgTotal = i.fgTotal
    
    headerData = {}
    for i in journal_header:
        filling = float(nonZero(i.filing_charge))
        labour = float(nonZero(i.labour_charge))
        headerData['Production ID'] = i.journal_id
        headerData['Date'] = i.journal_date
        headerData['Ref No'] = i.journal_no
        headerData['Filing'] = '{:,.2f}'.format(filling)
        headerData['Labour'] = '{:,.2f}'.format(labour)
        headerData['Memo'] = i.journal_memo
        headerData['Volume'] = '{:,.2f}'.format(float(volume))
        headerData['Total RM cost'] = '{:,.2f}'.format(-float(rmTotal))
        headerData['Total FG Cost'] = '{:,.2f}'.format(float(fgTotal))
        fees = filling / getType(volume)
        headerData['Fees P/L'] = '{:,.2f}'.format(float(fees))
        ttlFees = filling + labour
        headerData['Total Fees'] = '{:,.2f}'.format(float(ttlFees))
        
    
    for i in fgd_detail:
        item_no = i[0]
        pk_qty = round(i[1], 0)
        exp_cost = round(getType(i[2]), 2)
        item_desc = i[3]
        fg_qty = i[4]
        rm_cost = round(getType(i[5]), 4)
        direct_cost = round(getType(i[6]), 2)
        cost = round(getType(i[7]), 4)
        pk_cost = round(getType(i[8]), 2)
        mainData += [ProductionFGReport(item_no, pk_qty, exp_cost, item_desc, fg_qty, rm_cost, direct_cost, cost, pk_cost)]
    
    mainNames = [('No', 'item_no', 25, 'string'), ('PK Qty', 'pk_qty', 50, 'string'), ('Exp', 'exp_cost', 35, 'number'),
                 ('Description', 'item_desc', 225, 'string'), ('Qty', 'fg_qty', 50, 'string'), ('RM', 'rm_cost', 50, 'number', 4),
                 ('Direct', 'direct_cost', 50, 'number'), ('Cost', 'cost', 50, 'number', 4), ('PK Cost', 'pk_cost', 75, 'number')]
    pk_total = sum(float(v.pk_qty * v.pk_cost) for v in mainData)
    cost_total = sum(float(v.cost * v.fg_qty) for v in mainData)
    mainTotals = [(1,), (4,), (7, cost_total), (8, pk_total)]
        
    for i in rm_sum_detail:
        bom_no = i[0]
        bom_qty = - round(getType(i[1]) , 4)
        
        bom_desc = i[2]
        bom_cost = round(getType(i[3]), 4)
        bom_total = - round(getType(i[4]), 2)
        
        x = sum([bom_no == x.item_no for x in mainData])
#        if x == 1:
#            bom_qty += sum([x.fg_qty for x in mainData])
#            bom_total += sum([x.fg_qty * x.cost for x in mainData])
        subData += [ProductionRMReport(bom_no, bom_qty, bom_desc, bom_cost, bom_total)]
    subNames = [('No', 'bom_no', 75, 'string'), ('Qty', 'bom_qty', 50, 'string', 4), ('Description', 'bom_desc', 300, 'string'),
                ('Cost', 'bom_cost', 75, 'number', 4), ('Total', 'bom_total', 75, 'number')]
    subTotals = [(4,)]
    
    model.load('Production Report', None, mainData, mainNames, mainTotals)
    model.loadHeader(headerData, headerNames)
    model.loadSubReport(subData,  subNames, subTotals)


def invSumReport(model, fromDate=None, toDate=None):
    session = Session()
    if fromDate and toDate:
        dateFilter = JournalHeader.journal_date.between(fromDate, toDate)
        reportPeriod = 'From %s To %s' % (fromDate, toDate)
    elif toDate and not fromDate:
        dateFilter = JournalHeader.journal_date <= toDate
        reportPeriod = 'On or before %s' % toDate
    else:
        dateFilter = ""
        reportPeriod = 'All dates'
    
    
    inv_query = session.query(RMD.bom_id, BOM.bom_no, BOM.bom_desc, func.sum(invQty()).label('sumQty'), func.sum(invValue()).label('sumValue')) \
                                .join(JournalHeader).join(BOM).group_by(RMD.bom_id).filter(dateFilter)
    reportList = []
    for i in inv_query:
        bom_id = i[0]
        bom_no = i[1]
        bom_desc = i[2]
        qty = round(i[3], 2)
        total = round(i[4],2)
        cost = round(float(nonZero(total, 0)) / float(nonZero(qty, 1)))
        reportList += [InventorySumReport(bom_id, bom_no, bom_desc, qty, cost, total)]
    
    field_list = [('ID', 'bom_id', 0, 'string'), ('Item', 'bom_no', 25, 'string'), ('Description', 'bom_desc', 200, 'string'),
                  ('Qty', 'qty', 75, 'number'), ('Cost', 'cost', 50, 'number'), ('Value', 'total', 75, 'number')]
    columnsToTotal = [(3,), (5,)]
    
    model.load('Inventory Evaluation Report', reportPeriod, reportList, field_list, columnsToTotal)

    

def invDetailReport(model, bomId=None, fromDate=None, toDate=None):
    session = Session()
    if fromDate and toDate:
        dateFilter = JournalHeader.journal_date.between(fromDate, toDate)
        reportPeriod = 'From %s To %s' % (fromDate, toDate)
    elif toDate and not fromDate:
        dateFilter = JournalHeader.journal_date <= toDate
        reportPeriod = 'On or before %s' % toDate
    else:
        dateFilter = ""
        reportPeriod = 'All dates'
        
    bomFilter = RMD.bom_id==bomId if bomId else ""
                    
    rmd_query = session.query(RMD.id, RMD.bom_id, BOM.bom_no, invQty(), invValue(), BOM.bom_desc,
                              JournalHeader.journal_id, JournalHeader.journal_no, JournalHeader.journal_date, JournalHeader.journal_type) \
                              .join(JournalHeader).join(BOM).filter(bomFilter).filter(dateFilter)

    q = []
    reportList = []
    balQty = 0
    balValue = 0
    for i in rmd_query:
        q += i,
        balQty = sum(float(v[3]) for v in q if v[1] == i[1])
        balValue = sum(float(v[4]) for v in q if v[1] == i[1])
        journal_id = i[6]
        journal_no = i[7]
        journal_date = i[8]
        journal_type = i[9]
        bom_id = i[1]
        bom_no = i[2]
        bom_desc = i[5]
        qty = i[3]
        total = i[4]
        avg_cost = round(float(nonZero(balValue, 0)) / float(nonZero(balQty, 1)),2)
        reportList += [InventoryReport(journal_id, journal_no, journal_date, journal_type, bom_id, 
                                       bom_no, bom_desc, qty, total, avg_cost, balQty, balValue)]

    field_list = [('Type', 'journal_type', 50, 'string'), ('ID', 'journal_id', 25, 'string'), ('No', 'journal_no', 50, 'string'), 
                  ('Date', 'journal_date', 75, 'date'), ('Item', 'bom_no', 25, 'string'), ('Description', 'bom_desc', 200, 'string'),
                  ('Qty', 'qty', 75,'number'), ('Amount', 'total', 75, 'number'), ('Qty', 'bal_qty', 75, 'number'), 
                  ('Cost', 'avg_cost', 50, 'number'), ('Value', 'bal_value', 75, 'number')]
    
    columnsToTotal = [(6,), (7,), (9, balQty), (10, balValue)]
    
    model.load('Inventory Detail Report', reportPeriod, reportList, field_list, columnsToTotal)
                                                
    