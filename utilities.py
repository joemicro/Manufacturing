#-*- coding: UTF-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy import  *
from sqlalchemy.orm import *
from databaseschema import *
from functions import *
import ctypes
import csv
import datetime
import dateutil.parser as parser

CODEC = 'latin-1'
session = Session()
MessageBox = ctypes.windll.user32.MessageBoxA

def lineCount(filename):
    with open(filename, 'r') as fh:
        for i, line in enumerate(fh):
            pass
    return i + 1 

def getFile(function):
    filename = QFileDialog.getOpenFileName(None, "%s - Select file to import" % function, "", '(*.csv)')
    if not filename.isEmpty():
        return filename
    else:
        return
    
    

def importSupplierList():
    """ import supplier list from csv file, file should be formatted with first line <HDR>
    and subsequent lines with <DTL>"""
    name = None
    curr = None
    funcName = 'Import Supplier'
    pValue = 0
    myList = []
    log = []
    
    # Get file name, and set up progress
    filename = getFile(funcName)
    if not filename:
        return
    lines = lineCount(filename)
    progress = QProgressDialog('Importing...', 'Abort Import', 0, lines)
    progress.setCancelButton(None)
    
    # Open file
    with open(filename, 'r') as fh:
        # check for header row
        firstLine = fh.readline()
        if not firstLine.startswith('<HDR>'):
            MessageBox(None, 'No header row found!', funcName, 0)
            return
        fh.seek(0)
        
        # construct from the file, a list i could import to my database.
        progress.setLabelText('Reading file')
        pValue = pValue + 1
        progress.setValue(pValue)
        for line in fh:
            pValue += 1
            progress.setValue(pValue)
            QApplication.processEvents()
            if line.startswith('<HDR>'):
                fields = line.strip('\n').split(',') # split the line by comma, since its csv
                try:
                    name = fields.index('Name') # get the field index
                    curr = fields.index('Currency') # get the field index
                except Exception, e:
                    MessageBox(None, str(e), funcName, 0)
                    return
                continue # when done with the header row
            
            fields = line.split(',') # go to the next row, split line into fields
            myList = myList + [(fields[name], fields[curr].rstrip('\n'))] # contruct a proper list
            
    progress.setLabelText('Importing...')
    pValue = 1
    progress.setValue(pValue)        
    # go through my list and check for duplicates and send to DB
    for rec in myList:
        pValue += 1
        progress.setValue(pValue)
        QApplication.processEvents()
        if not rec[0]: #make sure there is a supplier name, if not add to log and skip line.
            log = log + [rec, ['Not Imported', 'Missing supplier name']]
            continue
        # check if already in DB, if yes add to log errors
        supplier_id = dLookup(Suppliers.supplier_id, Suppliers.supplier_name==rec[0]) 
        if supplier_id: 
            supplier = session.query(Suppliers).filter(Suppliers.supplier_id==supplier_id)
            supplier.update({'supplier_name': rec[0], 'currency': rec[1]})
            log = log + [(rec, ['Updated', 'Already in list'])]
            continue
        # check if duplicate in list, if yes add to log errors
        if myList.count(rec) > 1:
            log = log + [(rec, ['Not Imported', 'Duplicate'])]
            continue
        # add to session
        addSupplier(rec, False)
    sendToDB()
    # if a log was constructed, send to file.
    if log:
        progress.setLabelText('Writing log')
        writeLog(log)
    progress.setLabelText('Imported successfully')
    progress.setValue(100)
        
def addSupplier(rec, send):
    """ add supplier object to session, and flush to database, based on user choice"""
    session.add(Suppliers(rec[0], rec[1]))
    if send:
        sendToDB()
        
def importBOM():
    """ import BOM list from csv file, file should be formatted with first line <HDR>
    and subsequent lines with <DTL>"""
    myList = []
    log = []
    hdrCount = 0
    dtlCount = 0
    pValue = 0
    funcName = 'Import BOM'
    # // Get file name
    filename = getFile(funcName)
    if not filename:
        return
    # // Open file, and set up progress
    lines = lineCount(filename)
    progress = QProgressDialog('Importing...', 'Abort Import', 0, lines)
    progress.setCancelButton(None)
    with open(filename, 'r') as fh:
        reader = csv.reader(fh) # // instantiate csv reader
        # // check for header row
        firstLine = reader.next()
        if not firstLine[0].startswith('<HDR>'):
            MessageBox(None, 'No header row found!', funcName, 0)
            return
        fh.seek(0)
        
        # // construct from the a file a list i could import to my database.
        lineNo = 0
        progress.setLabelText('Reading file')
        for line in reader:
            lineNo += 1
            pValue += 1
            progress.setValue(pValue)
            QApplication.processEvents()
            if line[0].startswith('<HDR>'):
                hdrCount = len(line)
                try:
                    supplier = line.index('supplier') # // get the field index
                    bom_no = line.index('bom_no') 
                    bom_desc = line.index('bom_desc')
                    bom_cost = line.index('bom_cost')
                    hachsher = line.index('hachsher')
                    bom_supplier_no = line.index('bom_supplier_no')
                    measure = line.index('measure')
                    pack = line.index('pack')
                    uom = line.index('uom')
                    i_inactive = line.index('inactive')
                    i_mix_item = line.index('mix_item')
                    qb_parent_path = line.index('qb_parent_path')
                    qb_account = line.index('qb_account')
                except Exception, e:
                    MessageBox(None, str(e), funcName, 0)
                    return
                continue
            elif line[0].startswith('<DTL>'):
                dtlCount = len(line)
                if hdrCount != dtlCount:
                    log = log + [(['line: ' + lineNo], [line], ['Not Imported', 
                                                                'To many fields in relation to headers. check if there are commas.'])]
                    continue
                supplier_id = dLookup(Suppliers.supplier_id, Suppliers.supplier_name==line[supplier])
                if not supplier_id and line[supplier].rstrip('\n'):
                    addSupplier((line[supplier], 'CAD'), True)
                    supplier_id = dLookup(Suppliers.supplier_id, Suppliers.supplier_name==line[supplier])
                inactive = '1' if (line[i_inactive] == 'TRUE' or str(line[i_inactive]) == '1') else '0'
                mix_item = '1' if (line[i_mix_item] == 'TRUE' or str(line[i_mix_item]) == '1') else '0'
                if mix_item == '1':
                    log = log + [(['line: ' + str(lineNo)], [line], ['Not imported because its a mix item, please add mix items manually'])]
                    continue
                # // construct a tuple of each line to add to list
                myList = myList + [(supplier_id, line[bom_no], line[bom_desc], line[bom_cost], 
                                    line[hachsher], line[bom_supplier_no], line[measure], line[pack], 
                                    line[uom], inactive, mix_item, unicode(line[qb_parent_path], CODEC), unicode(line[qb_account], CODEC))] 
            
    pValue = 1
    progress.setLabelText('Importing file')       
    for rec in myList:
        if not rec[1]:
            log = log + [(rec, ['Not Imported', 'Missing BOM no.'])]
            continue
        # // check if already in DB, if yes update
        bom_id = dLookup(BOM.bom_id, BOM.bom_no==rec[1]) 
        if bom_id: 
            bom = session.query(BOM).filter(BOM.bom_id==bom_id)
            bom.update({'supplier_id': rec[0], 'bom_no': rec[1], 'bom_desc': rec[2],
                        'bom_cost': unicode(rec[3]), 'hachsher': rec[4], 'bom_supplier_no': rec[5],
                        'measure': rec[6], 'pack': unicode(rec[7]), 'uom': rec[8], 'inactive': int(rec[9]), 'mix_item': int(rec[10]),
                        'qb_parent_path': rec[11], 'qb_account': rec[12]})
            log = log + [(rec, ['Updated', 'Already in list'])]
            continue
        # // check if duplicate in list, if yes add to log errors
        if myList.count(rec) > 1:
            log = log + [(rec, ['Not Imported', 'Duplicate'])]
            continue
        # // add to session
        addBOM(rec, False)
        pValue += 1
        progress.setValue(pValue)
        QApplication.processEvents()
    sendToDB()
    # // if a log was constructed, send to file.
    if log:
        progress.setLabelText('Writing log file')
        writeLog(log)

def addBOM(rec, send):
    """ add BOM object to session, and flush to database, based on user choice"""
    session.add(BOM(None, rec[0], rec[1], rec[2], unicode(rec[3]), rec[4], rec[5], rec[6], 
                        unicode(rec[7]), rec[8], int(rec[9]), int(rec[10]), rec[11], rec[12]))
    if send:
        sendToDB()
    

def importBaseList():
    """ Import Base List, file should be formated with caption header row <HDRC>, then detail header row <HDRD>,
    then caption detail <DTLC>, then detail details <DTLD>"""  
    #prepare variables
    headerDict = {}
    detailDict = {}
    log = []
    errorBase = []
    base_id = dMax(BaseHeader.base_id)
    baseNo = None
    pValue = 0
    skip = False
    funcName = 'Import Base'
    
    # Get file name
    filename = getFile(funcName)
    if not filename:
        return
    #get number of lnes will need to work, to estimate progess
    lines = lineCount(filename)
    progress = QProgressDialog('Importing...', 'Abort Import', 0, lines)
    progress.setCancelButton(None)
   
    # open file, and work with it
    with open(filename, 'r') as fh:
        reader = csv.reader(fh)
        # check for header row
        firstLine = reader.next()
        if not firstLine[0].startswith('<HDRC>'):
            MessageBox(None, 'No header row found!', funcName, 0)
            return
        fh.seek(0)
        
        # construct from the a file a list i could import to my database.
        lineNo = 0 #get lineNo, to report if there is an error
        progress.setLabelText('Reading file')
        # loop through lines evaluate each one.
        for line in reader:
            lineNo += 1
            pValue += 1
            progress.setValue(pValue)
            QApplication.processEvents()
            # if there was a problem with the header, skip all rows until next header
            # wouldn't want to attach details to wrong header.
            if skip:
                if not line.startswith('<DTLC>'):
                    continue
                else:
                    skip = False
                    
            # get the field indexes, by evaluating the header for field names.
            if line[0].startswith('<HDRC>'):
                hdrCountC = len(line)
                try:
                    base_date = line.index('base_date') # get the field index
                    base_no = line.index('base_no') 
                    base_type = line.index('base_type')
                    base_desc = line.index('base_desc')
                    base_volume = line.index('base_volume')
                    inflation_factor = line.index('inflation_factor')
                    base_memo = line.index('base_memo')
                except Exception, e:
                    MessageBox(None, str(e), funcName, 0)
                    return
                continue
            
            # Get field indexes for detail, by evaluating header for field names
            elif line[0].startswith('<HDRD>'):
                hdrCountD = len(line)
                try:
                    bom = line.index('bom')
                    bom_qty = line.index('bom_qty')
                except Exception, e:
                    MessageBox(None, str(e), funcName, 0)
                    return
                continue
            
            # once we know the field index, we know which field goes where, 
            # lets construct a dictionary we could import,
            # m using a dict, so it should be easy to pop items if there are errors.
            elif line[0].startswith('<DTLC>'):
                dtlCountC = len(line)
                # check if there are the same amount of fields in detail as in header, could change if there is a comma in desc.
                if hdrCountC != dtlCountC:
                    log += [(['line: ' + str(lineNo)], [line], ['Not Imported', 'To many fields in relation to headers. " \
                                    "check if there are commas. or fields without headers.'])]
                    skip = True
                    continue
                base_id += 1
                try:
                    baseDate = parser.parse(line[base_date]).date()
                except ValueError:
                    MessageBox(None, 'Incorrect date format on line %s' % (lineNo + 1), funcName, 0)
                    return
                baseNo = line[base_no]
                try:
                    inflation = float(line[inflation_factor].strip())
                    df_volume = line[base_volume].strip()
                    df_volume = int(float(df_volume)) if float(df_volume).is_integer() else float(df_volume) 
                except ValueError, e:
                    log += [(['line: ' + str(lineNo)], [line], [str(e)])]
                    skip = True
                    continue
                headerDict.setdefault(base_id, []).append((base_id, baseDate, baseNo, line[base_type], 
                                    line[base_desc], df_volume, inflation, 
                                    line[base_memo]))
            
            # now construct a detail dictionary
            elif line[0].startswith('<DTLD>'):
                dtlCountD = len(line)
                if hdrCountD != dtlCountD:
                    log = log + [([baseNo], [lineNo], [line], ['Not Imported',
                                                                'To many fields in relation to headers. check if there are commas.'])]
                    errorBase += [base_id]
                    continue
                bom_id = dLookup(BOM.bom_id, BOM.bom_no==line[bom])
                if not bom_id:
                    log = log + [([baseNo], [lineNo], [line], ['Not Imported', 'Missing BOM'])]
                    errorBase += [base_id]
                    continue
                try:
                    bomQty = float(line[bom_qty].strip())
                except ValueError, e:
                    log = log + [(['line: ' + str(lineNo)], [line], [str(e)])]
                    errorBase += [base_id]
                    continue
                detailDict.setdefault(base_id, []).append((base_id, bom_id, bomQty))
    
    #remove error bases from header and detail list.
    if errorBase:
        for i in errorBase:
            del headerDict[i]
            del detailDict[i]
    
    # Lets start importing,
    # reset progress
    pValue = 1
    progress.setLabelText('Importing file') 
    
    # loop through dictionary, to start importing records.      
    for key, rec in headerDict.iteritems(): # get the key, and the record (which a list of fields) for each record in the dict
        # check if there are duplicates in list, if yes add to log errors
        if rec.count(rec[0]) > 1:
            log = log + [(rec, ['Not Imported', 'Duplicate'])]
            continue
        
        rec = rec[0] # each rec has a list of tupples, need to work with each individual tupple.
        
        # check if there are details for base record, else skip to next line
        dtlKey = detailDict.get(key, None)
        if dtlKey is None:
            log = log + [(rec, ['Not Imported', 'There are no details for this base.'])]
            continue
        
        # if there is no base number
        if not rec[2]: 
            log = log + [(rec, ['Not Imported', 'Missing Base Number.'])]
            continue
        
        # check if already in DB, if yes update
        baseID = dLookup(BaseHeader.base_id, BaseHeader.base_no==rec[2]) 
        if baseID:
            session.query(BaseDetail).filter(BaseDetail.base_id==baseID).delete() #delete details, for this base
            base = session.query(BaseHeader).filter(BaseHeader.base_id==baseID) # get the query to update
            base.update({'base_date': rec[1], 'base_no': rec[2], 'base_type': rec[3],
                        'base_desc': rec[4], 'base_volume': unicode(rec[5]), 'inflation_factor': unicode(rec[6]),
                        'base_memo': rec[7]})
            detailList = detailDict[key] #get list of items for current base
            for item in detailList:
                session.add(BaseDetail(baseID, int(item[1]), unicode(item[2]))) # add to session, to send to db later.
            log = log + [(rec, ['Updated', 'Already in list'])]
            continue
        
        # add to session
        session.add(BaseHeader(key, rec[1], rec[2], rec[3], rec[4], unicode(rec[5]), unicode(rec[6]), rec[7]))
        detailList = detailDict[key] #get list of items for current base
        for item in detailList:
            session.add(BaseDetail(key, int(item[1]), unicode(item[2]))) # add to session, to send to db later.
        pValue += 1
        progress.setValue(pValue)
        QApplication.processEvents()
    sendToDB()
    
    # if a log was constructed, send to file.
    if log:
        progress.setLabelText('Writing log file')
        writeLog(log)
        

def importReceive(userId):
    """ Import Receive Report, file should be formated with caption header row <HDRC>, then detail header row <HDRD>,
    then caption detail <DTLC>, then detail details <DTLD>"""  
    # // prepare variables
    headerDict = {}
    detailDict = {}
    log = []
    errorReport = []
    journalNo = None
    journal_id = dMax(JournalHeader.journal_id)
    pValue = 0
    skip = False
    funcName = 'Import Receive Report'
    
    # // Get file name
    filename = getFile(funcName)
    if not filename:
        return
    # // get number of lines will need to work, to estimate progress
    lines = lineCount(filename)
    progress = QProgressDialog('Importing...', 'Abort Import', 0, lines)
    progress.setCancelButton(None)
   
    # // open file, and work with it
    with open(filename, 'r') as fh:
        reader = csv.reader(fh)
        # // check for header row
        firstLine = reader.next()
        if not firstLine[0].startswith('<HDRC>'):
            MessageBox(None, 'No header row found!', funcName, 0)
            return
        fh.seek(0)
        
        # // construct from the a file a list i could import to my database.
        lineNo = 0 # // get lineNo, to report if there is an error
        progress.setLabelText('Reading file')
        # // loop through lines and evaluate each one.
        for line in reader:
            lineNo += 1
            pValue += 1
            progress.setValue(pValue)
            QApplication.processEvents()
            # // if there was a problem with the header, skip all rows until next header
            # // wouldn't want to attach details to wrong header.
            if skip:
                if not line[0].startswith('<DTLC>'):
                    continue
                else:
                    skip = False
                    
            # // get the field indexes, by evaluating the header for field names.
            if line[0].startswith('<HDRC>'):
                hdrCountC = len(line)
                try:
                    journal_type = line.index('journal_type') # get the field index
                    journal_date = line.index('journal_date') 
                    journal_no = line.index('journal_no')
                    journal_memo = line.index('journal_memo')
                    supplier_name = line.index('supplier_name')
                    journal_total = line.index('journal_total')
                    currency_rate = line.index('currency_rate')
                    shipping = line.index('shipping')
                    gst = line.index('gst')
                    qst = line.index('qst')
                    export = line.index('export')
                except Exception, e:
                    MessageBox(None, str(e), funcName, 0)
                    return
                continue
            
            # // Get field indexes for detail, by evaluating header for field names
            elif line[0].startswith('<HDRD>'):
                hdrCountD = len(line)
                try:
                    bom_no = line.index('bom_no')
                    rmd_desc = line.index('rmd_desc')
                    qty = line.index('qty')
                    cost = line.index('cost')
                    cost_native = line.index('price')
                    rmd_shipping = line.index('rmd_shipping')
                    rmd_memo = line.index('rmd_memo')
                    total = line.index('total')
                    native_total = line.index('native_total')
                except Exception, e:
                    MessageBox(None, str(e) + str(line), funcName, 0)
                    return
                continue
            
            # // once we know the field index, we know which field goes where, 
            # // lets construct a dictionary we could import,
            # // i am using a dict, so it should be easy to pop items if there are errors.
            elif line[0].startswith('<DTLC>'):
                dtlCountC = len(line)
                # check if there are the same amount of fields in detail as in header, could change if there is a comma in desc.
                if hdrCountC != dtlCountC:
                    log = log + [(['line: ' + str(lineNo)], [line], ['Not Imported', 'To many fields in relation to headers. " \
                                    "check if there are commas. or fields without headers.'])]
                    skip = True
                    continue
                journal_id += 1
                journalNo = line[journal_no]
                supplier_id = dLookup(Suppliers.supplier_id, Suppliers.supplier_name==line[supplier_name])
                if not supplier_id and line[supplier_name].rstrip('\n'):
                    addSupplier((line[supplier_name], 'CAD'), True)
                    supplier_id = dLookup(Suppliers.supplier_id, Suppliers.supplier_name==line[supplier_name])
                to_export = '1' if line[export] == 'Y' else '0'
                try:
                    journalDate = parser.parse(line[journal_date]).date()
                    jTotal = float(line[journal_total].strip())
                    cRate = float(line[currency_rate].strip())
                    jShipping = line[shipping].strip()
                    jShipping = float(jShipping) if jShipping else ""
                    jGst = line[gst].strip()
                    jGst = float(jGst) if jGst else ""
                    jQst = line[qst].strip()
                    float(jQst) if jQst else ""
                except ValueError, e:
                    log = log + [(['line: ' + str(lineNo)], [line], ['Not Imported', 'Error: %s' % e])]
                    skip = True
                    continue
                headerDict.setdefault(journal_id, []).append((journal_id, line[journal_type], journalDate, journalNo,
                                                              line[journal_memo], supplier_id, jTotal, cRate,
                                                              jShipping, jGst, jQst, to_export))

            # // now construct a detail dictionary
            elif line[0].startswith('<DTLD>'):
                dtlCountD = len(line)
                if hdrCountD != dtlCountD:
                    log = log + [([journalNo], [line], ['Not Imported', 'To many fields in relation to headers. check if there are commas.'])]
                    errorReport += [journal_id]
                    continue
                bom_id = dLookup(BOM.bom_id, BOM.bom_no==line[bom_no])
                if not bom_id:
                    addBOM((supplier_id, line[bom_no], line[rmd_desc], line[cost], 
                                None, None, None, None, None, False, False, None, None), True)
                    bom_id = dLookup(BOM.bom_id, BOM.bom_no==line[bom_no])
                try:
                    d_cRate = cRate if cRate else 1
                    rQty = float(line[qty].strip())
                    rCost = float(line[cost].strip())
                    rCostNative = float(line[cost_native].strip())
                    rShipping = line[rmd_shipping].strip()
                    rShipping = float(rShipping) if rShipping else ""
                    rTotal = line[total].strip()
                    rTotal = float(rTotal) if rTotal else (getType(rShipping) + getType(rCostNative)) * getType(rQty) * d_cRate
                    rNativeTtl = line[native_total].strip()
                    rNativeTtl = float(rNativeTtl) if rNativeTtl else (getType(rShipping) + getType(rCostNative)) * getType(rQty)
                except ValueError, e:
                    log = log + [([journalNo], [line], ['Not Imported', 'Error: %s' % e])]
                    errorReport += [journal_id]
                    continue
                detailDict.setdefault(journal_id, []).append((journal_id, bom_id, line[rmd_desc], rQty, rCost, rCostNative,
                                                              rShipping, line[rmd_memo], rTotal, rNativeTtl))
            
    
    # // remove error bases from header and detail list.
    if errorReport:
        for i in errorReport:
            try:
                del headerDict[i]
                del detailDict[i]
            except KeyError:
                continue
    
    # // Lets start importing,
    # // reset progress
    pValue = 1
    progress.setLabelText('Importing file') 
    
    # // loop through dictionary, to start importing records.      
    for key, rec in headerDict.iteritems(): # // get the key, and the record (which is a list of fields) for each record in the dict
        # // check if there are duplicates in list, if yes add to log errors
        if rec.count(rec[0]) > 1:
            log = log + [(rec, ['Not Imported', 'Duplicate'])]
            continue
        
        rec = rec[0] # // each rec has a list of tuples, need to work with each individual tuple.
        
        # // check if there are details for base record, else skip to next line
        dtlKey = detailDict.get(key, None) # // if no key none is returned
        if dtlKey is None:
            log = log + [(rec, ['Not Imported', 'There are no details for this Receiving Report.'])]
            continue
        
        # // if there is no supplier
        if not rec[5]: 
            log = log + [(rec, ['Not Imported', 'Missing supplier.'])]
            continue
        
        # // add to session
        journal_date = str(rec[2])
        modified_date = QDateTime().currentDateTime().toPyDateTime()
        log_memo = 'Created - Via import'
        session.add(ReceiveHeader(key, rec[1], rec[2], rec[3], rec[4], rec[5], unicode(rec[6]), unicode(rec[7]), unicode(rec[8]),
                                   unicode(rec[9]), unicode(rec[10]), modified_date, rec[11]))
        session.add(Logs(journal_id, userId, modified_date, log_memo))
        detailList = detailDict[key] # // get list of items for current receive
        for item in detailList:
            session.add(ReceiveRMD(key, int(item[1]), item[2], unicode(item[3]), unicode(item[4]), unicode(item[5]),
                                    unicode(item[6]), item[7], unicode(item[8]), unicode(item[9]))) # // add to session, to send to db later.
        # // adjust avgCost
        adjList = adjustAvgCost(session, item[1], journal_date, key, item[4])
        if adjList:
            for adj in adjList:
                session.add(adj)
        # // update progress.        
        pValue += 1
        progress.setValue(pValue)
        QApplication.processEvents()
    sendToDB()
    
    # // if a log was constructed, send to file.
    if log:
        progress.setLabelText('Writing log file')
        writeLog(log)
        
                
def importItemList():
    """ Import Item List, file should be formated with item header row <HDRC>, then baseAssembly row <HDRB>,
    then itemAssembly row <HDRI>, then item detail <DTLC>, then baseAssembly details <DTLB>, itemAssembly details <DTLI>"""  
    # // prepare variables
    itemDict = {}
    baseDict = {}
    bomDict = {}
    log = []
    errorItems = []
    item_id = dMax(Items.item_id)
    itemNo = None
    pValue = 0
    skip = False
    funcName = 'Import Item'
    
    # // Get file name
    filename = getFile(funcName)
    if not filename:
        return
    # // get number of lines will need to work with, to estimate progress
    lines = lineCount(filename)
    progress = QProgressDialog('Importing...', 'Abort Import', 0, lines)
    progress.setCancelButton(None)
   
    # // open file, and work with it
    with open(filename, 'r') as fh:
        reader = csv.reader(fh)
        # // check for header row
        firstLine = reader.next()
        if not firstLine[0].startswith('<HDRC>'):
            MessageBox(None, 'No header row found!', funcName, 0)
            return
        fh.seek(0)
        
        # // construct from the file a list i could import to my database.
        lineNo = 0 # // get lineNo, to report if there is an error
        progress.setLabelText('Reading file')
        # // loop through lines evaluate each one.
        for line in reader:
            # // need to increase values at the beginning, because there are conditions that advance the count before it reaches the end
            lineNo += 1
            pValue += 1
            progress.setValue(pValue)
            QApplication.processEvents()
            # // if there was a problem with the item, skip all rows until next item
            # // wouldn't want to attach details to wrong item.
            if skip:
                if not line[0].startswith('<DTLC>'):
                    continue
                else:
                    skip = False
                    
            # // get the field indexes, by evaluating the header for field names.
            if line[0].startswith('<HDRC>'):
                hdrCountC = len(line)
                try:
                    item_no = line.index('item_no') # // get the field index
                    item_desc = line.index('item_desc')
                    volume = line.index('volume')
                    pack = line.index('pack')
                    item_cost = line.index('item_cost')
                    season = line.index('season')
                    category = line.index('category')
                    inactive = line.index('inactive')
                    mix_item = line.index('mix_item')
                except Exception, e:
                    MessageBox(None, str(e), funcName, 0)
                    return
                continue
            
            # // Get field indexes for itemAssembly, by evaluating header for field names
            elif line[0].startswith('<HDRI>'):
                hdrCountI = len(line)
                try:
                    bom_no = line.index('bom_no')
                    bom_qty = line.index('bom_qty')
                except Exception, e:
                    MessageBox(None, str(e), funcName, 0)
                    return
                continue
            
            # // Get field indexes for baseAssembly, by evaluating header for field names
            elif line[0].startswith('<HDRB>'):
                hdrCountB = len(line)
                try:
                    base_no = line.index('base_no')
                    percentage = line.index('percentage')
                except Exception, e:
                    MessageBox(None, str(e), funcName, 0)
                    return
                continue
            
            # // once we know the field index, we know which field goes where, 
            # // lets construct a dictionary we could import,
            # // m using a dict, so it should be easy to pop items if there are errors.
            elif line[0].startswith('<DTLC>'):
                dtlCountC = len(line)
                # // check if there are the same amount of fields in detail as in header, could change if something goes wrong.
                if hdrCountC != dtlCountC:
                    log = log + [(['line: ' + str(lineNo)], [line], ['Not Imported', 'To many fields in relation to headers. " \
                                    "check if there are commas. or fields without headers.'])]
                    skip = True
                    continue
                i_mix_item = '1' if line[mix_item] == 'TRUE' else '0'
                if i_mix_item == '1':
                    log = log + [(['line: ' + str(lineNo)], [line], ['Not imported because its a mix item, please add mix items manually'])]
                    skip = True
                    continue
                item_id += 1
                itemNo = line[item_no].strip()
                i_inactive = '1' if line[inactive] == 'TRUE' else '0'
                # // make sure that the following are numbers, convert to float or int,
                # // don't import items that don't have volume and pack 
                try:
                    itemVolume = line[volume].strip()
                    itemVolume = int(float(itemVolume)) if float(itemVolume).is_integer() else float(itemVolume)
                    itemPack = line[pack].strip()
                    itemPack = int(float(itemPack)) if float(itemPack).is_integer() else float(itemPack)
                    itemCost = line[item_cost].strip()
                    itemCost = float(itemCost) if itemCost else ""
                except ValueError, e:
                    log = log + [(['line: ' + str(lineNo)], [line], [str(e)])]
                    skip = True
                    continue
                season_id = dLookup(Lists.id, Lists.item==line[season].strip()) if line[season].strip() else None
                category_id = dLookup(Lists.id, Lists.item==line[category].strip()) if line[category].strip() else None
                itemDict.setdefault(item_id, []).append((item_id, itemNo, line[item_desc].strip(), 
                                    itemVolume, itemPack, itemCost, season_id,
                                    category_id, i_inactive, i_mix_item))
            
            # // now construct a bomAssembly dictionary
            elif line[0].startswith('<DTLI>'):
                dtlCountI = len(line)
                if hdrCountI != dtlCountI:
                    log = log + [([itemNo], [line], ['Not Imported', 'To many fields in relation to headers. check if there are commas.'])]
                    errorItems = errorItems + [item_id]
                    continue
                bom_id = dLookup(BOM.bom_id, BOM.bom_no==line[bom_no])
                if not bom_id:
                    log = log + [([itemNo], [line], ['bom item: %s was not found' % line[bom_no]])]
                    continue               
                bomDict.setdefault(item_id, []).append((item_id, bom_id, line[bom_qty]))
            
            # // now construct a baseAssembly dictionary
            elif line[0].startswith('<DTLB>'):
                dtlCountB = len(line)
                if hdrCountB != dtlCountB:
                    log = log + [([itemNo], [line], ['Not Imported', 'To many fields in relation to headers. check if there are commas.'])]
                    errorItems = errorItems + [item_id]
                    continue
                base_id = dLookup(BaseHeader.base_id, BaseHeader.base_no==line[base_no])
                if not base_id:
                    log = log + [([itemNo], [line], ['base: %s was not found' % line[base_no]])]
                    continue               
                percent = (float(getType(line[percentage])) / 100) if line[percentage] > 1 else line[percentage]
                baseDict.setdefault(item_id, []).append((item_id, base_id, percent))
    

    # // remove error items from header and detail list.
    if errorItems:
        for i in errorItems:
            del itemDict[i]
            del bomDict[i]
            del baseDict[i]
    
    # // Lets start importing,
    # // reset progress
    pValue = 1
    progress.setLabelText('Importing file') 
    
    # // loop through dictionary, to start importing records.      
    for key, rec in itemDict.iteritems(): # // get the key, and the record (which is a list of fields) for each record in the dict
        
        pValue += 1
        progress.setValue(pValue)
        QApplication.processEvents()
        
        # // check if there are duplicates in list, if yes add to log errors
        if rec.count(rec[0]) > 1:
            log = log + [(rec, ['Not Imported', 'Duplicate'])]
            continue
        
        rec = rec[0] # // each rec has a list of tuples, need to work with each individual tuple.
        
        # // if there is no item number, skip
        if not rec[1]: 
            log = log + [(rec, ['Not Imported', 'Missing Item Number.'])]
            continue
        
        # // check if already in DB, if yes update
        itemID = dLookup(Items.item_id, Items.item_no==rec[1]) 
        if itemID:
            # // delete assemblies, for this item
            session.query(ItemAssembly).filter(ItemAssembly.item_id==itemID).delete()
            session.query(BaseAssembly).filter(BaseAssembly.item_id==itemID).delete()
            item = session.query(Items).filter(Items.item_id==itemID) # // create a query to be updated
            item.update({'item_desc': rec[2], 'volume': unicode(rec[3]), 'pack': unicode(rec[4]),
                        'item_cost': unicode(rec[5]), 'season': rec[6], 'category': rec[7],
                        'inactive': rec[8], 'mix_item': rec[9]})
            if key in bomDict:
                bomList = bomDict[key] # // get list of assemblies for current item
                for bom in bomList:
                    session.add(ItemAssembly(itemID, int(bom[1]), unicode(bom[2]))) # // add to session, to send to db later.
            if key in baseDict:
                baseList = baseDict[key]
                for base in baseList:
                    session.add(BaseAssembly(itemID, int(base[1]), unicode(base[2])))
            log = log + [(rec, ['Updated', 'Already in list'])]
            continue
        
        # // finally add to session to record new items
        session.add(Items(key, rec[1], rec[2], unicode(rec[3]), unicode(rec[4]), unicode(rec[5]), rec[6], rec[7],
                          rec[8], rec[9]))
        if key in bomDict:
            bomList = bomDict[key] # // get list of boms for current item
            for bom in bomList:
                session.add(ItemAssembly(key, int(bom[1]), unicode(bom[2]))) # // add to session, to send to db later.
        if key in baseDict:
            baseList = baseDict[key]
            for base in baseList:
                session.add(BaseAssembly(key, int(base[1]), unicode(base[2])))
        
    sendToDB()
    
    # // if a log was constructed, send to file.
    if log:
        progress.setLabelText('Writing log file')
        writeLog(log)
        
        
                  
def sendToDB():
    """ Send data to database"""
    exception = None
    try:
        session.flush()
    except ValueError, e:
        exception = e
        session.rollback()
    finally:
        session.commit()
        if exception is not None:
            raise exception
        
def writeLog(l):
    """ if a log with errors was created while importing, write it to file"""
    logFile = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop\log.csv"
    try:
        with open(logFile, 'w+') as lg:
            writer = csv.writer(lg, dialect='excel')
            for i in l:
                j = [item for sublist in i for item in sublist]
                writer.writerow(j)
        MessageBox(None, 'Log file was created %s' % logFile, 'Log File', 0)
    except IOError:
        MessageBox(None, "Can't write to file: %s" % logFile, 'Log File', 0)
    
            
#def writeLog(l):
#    """ if a log with errors was created while importing, write it to file"""
#    logFile = os.getenv("HOMEDRIVE") + os.getenv("HOMEPATH") + "\\Desktop\log.csv"
#    with open(logFile, 'w+') as lg:
#        for i in l:
#            j = [item for sublist in i for item in sublist]
#            lg.write(",".join([str(u) for u in j]) + '\n')
#    MessageBox(None, 'Log file was created %s' % logFile, 'Log File', 0)


#### Export to IIF ========================================================
class ExportIIFDialog(QDialog):
    
    def __init__(self, parent=None):
        super(ExportIIFDialog, self).__init__(parent)
        note_label = QLabel('If you want to overwrite the default QuickBooks accounts to use, specify them here \n' \
                            'make sure to specify at least an account payable account')
        ap_label = QLabel('AP Account')
        self.ap_lineEdit = QLineEdit()
        ap_us_label = QLabel('AP US Account')
        self.ap_us_lineEdit = QLineEdit()
        inv_label = QLabel('Inventory Account')
        self.inv_lineEdit = QLineEdit()
        class_label = QLabel('Class')
        self.class_lineEdit = QLineEdit()
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok| QDialogButtonBox.Cancel)
        buttonBox.button(QDialogButtonBox.Ok).setDefault(True)
        
        layout = QGridLayout()
        layout.addWidget(note_label, 0, 0, 1, 2)
        layout.addWidget(ap_label, 1, 0)
        layout.addWidget(self.ap_lineEdit, 1, 1)
        layout.addWidget(ap_us_label, 2, 0)
        layout.addWidget(self.ap_us_lineEdit, 2, 1)
        layout.addWidget(inv_label, 3, 0)
        layout.addWidget(self.inv_lineEdit, 3, 1)
        layout.addWidget(class_label, 4, 0)
        layout.addWidget(self.class_lineEdit, 4, 1)
        layout.addWidget(buttonBox, 5, 0, 1, 2)
        self.setLayout(layout)
        
        self.setWindowTitle('Export Settings')
        self.setWindowIcon(QIcon(':/icons/settings'))
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        
    
def exportReceiveIIF(apAccount=None, apUsAccount=None, invAccount=None, dfltClass=None):
    
    default_apAccount = unicode(apAccount, CODEC)
    default_apUsAccount = unicode(apUsAccount, CODEC)
    default_inv_account = unicode(invAccount, CODEC)
    default_class = dfltClass
    funcName = 'Export Receive to IIF'
    
    # // get query of headers needed to be exported
    header_query = session.query(ReceiveHeader).join(Suppliers).filter(ReceiveHeader.export==True)
    
    # // get query for details to export
    detail_query = session.query(ReceiveRMD) \
                                .join(BOM).join(ReceiveHeader).filter(ReceiveHeader.export==True)
    # // Create a detail list, creating a detail list first, 
    # // so i could use the total of the details for the header totals instead of the recorded header total in case it doesn't match
    # // !SPL,SPLID,TRNSTYPE,DATE,ACCNT,NAME,CLASS,AMOUNT,DOCNUM,MEMO,CLEAR,QNTY,PRICE,INVITEM,REIMBEXP,SERVICEDATE,OTHER2,
    detail_list = []
    for i in detail_query:
        journal_id = i.journals.journal_id
        SPLID = ""
        TRNSTYPE = 'BILL' if i.journals.journal_type == 'Bill' else 'BILL REFUND'
        DATE = i.journals.journal_date
        ACCNT = i.boms.qb_account if not invAccount else default_inv_account
        NAME = ""
        CLASS = ""
        journal_total = i.total if i.journals.journal_type == 'Bill' else - i.total 
        AMOUNT = round(float(nonZero(journal_total, 0)), 2)
        DOCNUM = ""
        MEMO = i.rmd_desc
        CLEAR = 'N'
        QNTY = round(float(nonZero(i.qty, 0)), 4)
        PRICE = round(float(nonZero(i.cost, 0)), 4)
        INVITEM = i.boms.qb_parent_path + ":" + i.boms.bom_no if i.boms.qb_parent_path else i.boms.bom_no
        detail_list += [(journal_id, 'SPL', SPLID, TRNSTYPE, DATE, ACCNT, NAME, CLASS, AMOUNT, DOCNUM, MEMO, CLEAR, QNTY, PRICE, INVITEM)]
    
    # // create a header list
    # // !TRNS,TRNSID,TRNSTYPE,DATE,ACCNT,NAME,CLASS,AMOUNT,DOCNUM,MEMO,CLEAR,TOPRINT,ADDR5,DUEDATE,TERMS
    header_list = []
    for i in header_query:
        journal_id = i.journal_id
        TRNSID = ""
        TRNSTYPE = 'BILL' if i.journal_type == 'Bill' else 'BILL REFUND'
        DATE = i.journal_date
        currency = dLookup(Suppliers.currency, Suppliers.supplier_name == i.suppliers.supplier_name)
        ACCNT = default_apAccount if currency == 'CAD' else default_apUsAccount
        NAME = i.suppliers.supplier_name
        CLASS = default_class
        journal_amount = sum(float(nonZero(v[8], 0)) for v in detail_list if v[0] == journal_id)
        AMOUNT = - journal_amount
        DOCNUM = i.journal_no
        MEMO = i.journal_memo if i.journal_memo else ""
        CLEAR = 'N'
        TOPRINT = 'N'
        ADDR5 = ""
        DUEDATE = i.journal_date
        TERMS = 'Net 30'
        header_list += [(journal_id, 'TRNS', TRNSID, TRNSTYPE, DATE, ACCNT, NAME, CLASS, AMOUNT, DOCNUM, MEMO, CLEAR, 
                         TOPRINT, ADDR5, DUEDATE, TERMS)]
        
    # // no lets export thous lists to csv creating an IIF file
    # // First get file name and add extension IIF, apparently it only works with csv
    filename = QFileDialog.getSaveFileName(None, 'Export Receive Report to IIF')
    if not filename:
        return
    if not '.iif' in filename:
        filename += '.iif'
    # // create column headers
    header_col = ['!TRNS','TRNSID','TRNSTYPE','DATE','ACCNT','NAME','CLASS','AMOUNT','DOCNUM','MEMO','CLEAR','TOPRINT','ADDR5','DUEDATE','TERMS']
    detail_col = ['!SPL','SPLID','TRNSTYPE','DATE','ACCNT','NAME','CLASS','AMOUNT','DOCNUM','MEMO','CLEAR','QNTY','PRICE','INVITEM']
    # // open file and start writing to csv
    with open(filename, 'w+') as iif:
        iif.write(",".join([str(i) for i in header_col]) + '\n')
        iif.write(",".join([str(i) for i in detail_col]) + '\n')
        iif.write('!ENDTRNS\n')
        for row in header_list:
            iif.write(",".join([str(i) for i in row[1:]]) + '\n')
            for det_row in detail_list:
                if det_row[0] == row[0]:
                    iif.write(",".join([str(i) for i in det_row[1:]]) + '\n')
            iif.write('ENDTRNS\n') # // need to make sure there is no space after 'ENDTRNS' else QB wont import
    session.query(ReceiveHeader).update({'export': False})
    session.commit()
    session.flush()
    MessageBox(None, 'Exported Successfully!!', funcName, 0)
#app = QApplication(sys.argv)
#setupDatabase("Production.sqlite")


#importSupplierList()
#importBOM()
#importBaseList()
#importItemList()
#importReceive()