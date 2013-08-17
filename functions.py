import sys
import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy import  *
from sqlalchemy.orm import *
from databaseschema import *
import datetime
import dateutil.parser as parser



def updateDb(progress, version, db_version):
    if version == '1.0.6':
        if db_version == '1.0.5':
            setupDatabase.engine.execute('ALTER TABLE batch_header ADD COLUMN prep_id INTEGER')
            createLists(None, version)
        
        elif db_version == '1.0.4':
            ses = Session()
            
            createLists(('settings_list',), version)
            
            item_list = ses.query(Items)
            lines_count = item_list.count()
            progress.setMaximum(lines_count)
            j = 0
            for i in item_list:
                j += 1
                progress.setValue(j)
                QApplication.processEvents()
                cat_id = dLookup(Lists.id, Lists.item==i.category)
                if cat_id:
                    update = item_list.get(i.item_id)
                    update.category = cat_id
                sesa_id = dLookup(Lists.id, Lists.item==i.season)
                if sesa_id:
                    update = item_list.get(i.item_id)
                    update.season = sesa_id
            
        ses.flush()
        ses.commit()
        ses.close()
    
    
def closingDate(date):
    """ Checks if there is a date constraint, if yes, takes date checks it against date saved in database,
    returns True if passed in date is later, if passed in date is earlier, it will only return True 
    if a good password is supplied, else it returns false """
    #// check if the closing date option is on
    where = Settings.setting=='closing_date'
    on = dLookup(Settings.bool_value, where)
    if not eval(on):
        return True
    #// if its on, get the date and password for comparison
    #// make sure that date passed id only date not datetime
    if isinstance(date, datetime.datetime):
        date = date.date()
    elif isinstance(date, str):
        date = parser.parse(date).date()
    closing_date = dLookup(Settings.date_value, where)
    if not closing_date:
        return True
    closing_date = parser.parse(closing_date).date()
    closing_pass = dLookup(Settings.value_1, where)
    #// if the date is before the closing date
    if date <= closing_date:
        ok = False
        #// do a loop, so if its a wrong password it automatically shows the input again.
        while not ok:
            password, supplied = QInputDialog.getText(None, 'Closing Date', 'Please enter the closing password')
            if not supplied:
                return False
            password = str(password)
            if password == closing_pass:
                ok = True
            else:
                QMessageBox.information(None, 'Closing Date', 'Password does not match!', QMessageBox.Ok)
                ok = False
        return ok
    else:
        return True
    return False
            
def defaultDate():
    option = dLookup(Settings.value_1, Settings.setting=='default_date')
    return option

def currentDate():
    now = datetime.datetime.now()
    return now

def dateRange(selection):
    curMonth = currentDate().month
    curYear = currentDate().year
    beginning = currentDate()
    end = beginning
    if selection == 'This Month':
        beginning = datetime.date(curYear, curMonth, 1)
        end = datetime.date(curYear, curMonth + 1, 1) - datetime.timedelta(days=1)
    elif selection == 'This Year':
        beginning = datetime.date(curYear, 1, 1)
        end = datetime.date(curYear + 1, 1, 1) - datetime.timedelta(days=1)
    elif selection == 'Last Month':
        beginning = datetime.date(curYear, curMonth - 1, 1)
        end = datetime.date(curYear, curMonth, 1) - datetime.timedelta(days=1)
    elif selection == 'Last Year':
        beginning = datetime.date(curYear - 1, 1, 1)
        end = datetime.date(curYear, 1, 1) - datetime.timedelta(days=1)
    elif selection == 'Custom':
        beginning = None
        end = None
    return (beginning, end)

def invQty():
    inv_qty = case([(JournalHeader.journal_type == 'Bill', RMD.qty), 
                        (and_(JournalHeader.journal_type == 'Production', RMD.rec_type == 'rcv'), RMD.qty),],
                        else_ = - RMD.qty).label('inv_qty')
    return inv_qty
    
def invValue():    
    inv_value = case([(JournalHeader.journal_type == 'Bill', RMD.total), 
                        (and_(JournalHeader.journal_type == 'Production', RMD.rec_type == 'rcv'), RMD.total),],
                        else_ = - RMD.total).label('inv_value')
    return inv_value
    
def lookupValue(session, bomID, date, journalID):
    
    if not session:
        session = Session()
    qty = 0
    value = 0
    
    date = parser.parse(date).date()
    dateFilter = JournalHeader.journal_date <= date
    bomIdFilter = RMD.bom_id == bomID
    journalIdFilter = RMD.journal_id != journalID
    
    invQuery = session.query(RMD.bom_id, func.sum(invQty()).label('sumQty'), func.sum(invValue()).label('sumValue')) \
                    .join(JournalHeader) \
                    .filter(dateFilter).filter(bomIdFilter).filter(journalIdFilter)
                
    for i in invQuery:
        qty = nonZero(i.sumQty, 0)
        value = nonZero(i.sumValue, 0)
        
    return (qty, value)

def avgCost(bomID, date=str(currentDate().date()), journalID=None):
    """ return avgCost of BOM. supply a bom_id and a date 'yyyy-mm-dd' to cap calculation period, 
    and a journl_id to exclude it from the query if that journal already exists in the database.
    """
    session = Session()
    qty, value = lookupValue(session, bomID, date, journalID)
    
    if not qty:
        qty = 1
    if not value:
        value = 0
    
    cost = round(value / qty, 4)
    if cost == 0:
        cost = dLookup(BOM.bom_cost, BOM.bom_id==bomID)
    if not cost:
        cost = 0
    return cost


def adjustAvgCost(session, bomID, date=str(currentDate().date()), journalID=None, cost=None):
    """ adjusts inventory value for bomID,
    takes 'bomID', the bom_id you wish to adjust inventory,
    takes 'date', to calculate value before that date
    takes 'journalID', to exclude the current journal from calculation,
    takes 'cost', if function is called from a receive pass cost from current receive.
    returns an AdjRMD object
    """

#    session = Session()
    journal_id = journalID
    qty, value = lookupValue(session, bomID, date, journalID)
    if qty >= 0:
        return

    _date_ = parser.parse(date).date()
    dateFilter = ReceiveHeader.journal_date <= _date_
    bomIdFilter = ReceiveRMD.bom_id == bomID
    journalIdFilter = ReceiveRMD.journal_id != journal_id
    typeFilter = ReceiveHeader.journal_type == 'Bill'
    if not cost:
        # // find last cost
        lastCostQuery = session.query(ReceiveRMD).join(ReceiveHeader).filter(dateFilter) \
                                        .filter(bomIdFilter).filter(journalIdFilter).filter(typeFilter) \
                                        .order_by(desc(ReceiveHeader.journal_date)).first()
        try:
            cost = lastCostQuery.cost
            journal_id = lastCostQuery.journal_id
        except AttributeError:
            cost = None
        # // if no cost, meaning that no receiving journal for item exists, just get out
        if not cost:
            return
    # // check if adjustment already exists in a later date
    jQuery = session.query(AdjRMD.bom_id).join(ReceiveHeader).filter(AdjRMD.bom_id==bomID) \
                        .filter(ReceiveHeader.journal_date>=date).subquery()
    session.query(AdjRMD).filter(AdjRMD.bom_id.in_(jQuery)).delete('fetch')
    # // check if adj already exists, delete if yes
    session.query(AdjRMD).filter(AdjRMD.bom_id==bomID).filter(AdjRMD.journal_id==journal_id).delete()
    commitToDB(session)
    # // need to recalculate value after previous line was deleted.
    qty, value = lookupValue(session, bomID, date, journalID)     
    cost = float(cost)
    rmd_desc = dLookup(BOM.bom_desc, BOM.bom_id==bomID)
    # // calculate value to adj
    adjValue = nonZero(qty, 0) * nonZero(cost, 0) - nonZero(value, 0)
    # // add line to session.
    adjRmd = [AdjRMD(bomID, 0, 0, unicode(cost), 'adj %s' % date, 0, unicode(adjValue), journal_id, rmd_desc)]
    return adjRmd
    
def commitToDB(session):    
    try:
        session.flush
        session.commit()
    except Exception, e:
        session.rollback()
        raise e
    


def getType(variable):
#    print variable, type(variable)
    """ converts QString, to float """
    if variable == 'None':
        return 0
    elif isinstance(variable, QString):
        return variable.toFloat()[0]
    elif not variable:
        return 0
    else:
        return float(variable)
    
def nonZero(variable, number=0):
    """ if the variable passed in is 0 or None, it returns the int you specify"""
#    print type(variable), 'ver':, variable, isinstance(variable, (int, float))
    if variable is None:
        variable = number
        return variable
    if isinstance(variable, (int, long, float, complex)):
        variable = variable 
    if isinstance(variable, str):
        variable = float(variable)
    elif isinstance(variable, QString):
        if variable.isEmpty():
            return number
        variable = str(variable)
        variable = float(variable)
    elif isinstance(variable, unicode):
        variable = str(variable)
        if not variable:
            variable = number
        else:
            variable = float(variable)
    if variable == float():
        variable = number
        return variable
    else:
        return variable
    
def dLookup(field, where):
    """looks up a field in the database, with a specified where clause
    Table.field, Table.field == where
    Returns corresponding value.""" 
    s = select([field], where)
    stmt = s.execute()
    myList = stmt.fetchall()
    row_count = len(myList)
    if row_count < 1:
        return None
    for record in myList:
        if isinstance(myList, list):
            return str(record[0])
        else:
            return record
    
def dMax(field):
    """ returns the max of the specified field from the database,just supply Table.field"""
    s = select([func.max(field)])
    stmt = s.execute()
    for record in stmt:
        r = str(record[0])
        if r == 'None':
            return 0
        else:
            return int(str(record[0]))
        
def addActions(self, target, actions):
        """ Add multiple action at once to a menuBar or toolBar"""
        if target is None:
            return
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
