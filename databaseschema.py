import sys
import os
from sqlalchemy import  *
from sqlalchemy.orm import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from sqlalchemy.ext.hybrid import hybrid_property, hybrid_method
import datetime



def closeDB():
    prodDb = QSqlDatabase.database('prod')
    prodDb.close()
    QSqlDatabase.removeDatabase('prod')

def setupDatabase(filename):
    
    filename = os.path.join(os.path.dirname(__file__), filename)
    database = "sqlite:///%s" % filename
    setupDatabase.engine = create_engine(database)
    metadata = MetaData(setupDatabase.engine)
    
    
    user_table = Table("users", metadata,
                       Column("user_id", Integer, primary_key=True),
                       Column("user_name", String),
                       Column("password", String))

    supplier_table = Table("supplier_list", metadata,
                           Column("supplier_id", Integer, primary_key=True),
                           Column("supplier_name", String),
                           Column("currency", String(10)))
  
    bom_table = Table("bom", metadata,
                      Column("bom_id", Integer, primary_key=True),
                      Column("supplier_id", Integer, ForeignKey("supplier_list.supplier_id")),
                      Column("bom_no", String(10)),
                      Column("bom_desc", String),
                      Column("bom_cost", Unicode),
                      Column("hachsher", String(10)),
                      Column("bom_supplier_no", String(45)),
                      Column("measure", String(10)),
                      Column("pack", Unicode),
                      Column("uom", String(10)),
                      Column('qb_parent_path', String),
                      Column('qb_account', Unicode),
                      Column("inactive", Boolean),
                      Column("mix_item", Boolean))
    
    item_list_table = Table("item_list", metadata,
                            Column("item_id", Integer, autoincrement=False, primary_key=True),
                            Column("item_no", String),
                            Column("item_desc", String),
                            Column("volume", Unicode),
                            Column("pack", Unicode),
                            Column("item_cost", Unicode),
                            Column("season", Integer, ForeignKey('lists.id')),
                            Column("category", Integer, ForeignKey('lists.id')),
                            Column("inactive", Boolean),
                            Column("mix_item", Boolean))
    
    item_assembly_table = Table("item_assembly", metadata,
                                Column("id", Integer, primary_key=True),
                                Column("item_id", Integer, ForeignKey("item_list.item_id")),
                                Column("bom_id", Integer, ForeignKey("bom.bom_id")),
                                Column("bom_qty", Unicode))
    
    base_assembly_table = Table("base_assembly", metadata,
                                Column("id", Integer, primary_key=True),
                                Column("item_id", Integer, ForeignKey("item_list.item_id")),
                                Column("base_id", Integer, ForeignKey("base_header.base_id")),
                                Column("percentage", Unicode))

    base_header_table = Table("base_header", metadata,
                              Column("base_id", Integer, autoincrement=False, primary_key=True),
                              Column("base_date", Date),
                              Column("base_no", String(10)),
                              Column('base_type', String(10)),
                              Column("base_desc", String),
                              Column("base_volume", Unicode),
                              Column("inflation_factor", Unicode),
                              Column("base_memo", String))

    base_detail_table = Table("base_detail", metadata,
                              Column("id", Integer, primary_key=True),
                              Column("base_id", Integer, ForeignKey("base_header.base_id")),
                              Column("bom_id", Integer, ForeignKey("bom.bom_id")),
                              Column("bom_qty", Unicode))
    
    associated_base_table = Table('associated_base', metadata,
                                  Column('id', Integer, primary_key=True),
                                  Column('base_id', Integer, ForeignKey('base_header.base_id')),
                                  Column('asso_id', Integer, ForeignKey('base_header.base_id')),
                                  Column('percentage', Unicode))
    
    batch_header_table = Table("batch_header", metadata,
                               Column("batch_id", Integer, autoincrement=False, primary_key=True),
                               Column('base_id', Integer, ForeignKey('base_header.base_id')),
                               Column("journal_id", Integer, ForeignKey("journal_header.journal_id")),
                               Column('prep_id', Integer, ForeignKey('prep_header.prep_id')),
                               Column("batch_date", Date),
                               Column("base_volume", Unicode),
                               Column("multiple", Unicode),
                               Column("inflation_factor", Unicode),
                               Column("batch_memo", String))
        
    batch_detail_table = Table("batch_detail", metadata,
                               Column("id", Integer, primary_key=True),
                               Column("base_id", Integer, ForeignKey("batch_header.batch_id")),
                               Column("bom_id", Integer, ForeignKey("bom.bom_id")),
                               Column("cost", Unicode),
                               Column("bom_qty", Unicode))
   
    journal_header_table = Table("journal_header", metadata,
                                 Column("journal_id", Integer, autoincrement=False, primary_key=True),
                                 Column("journal_type", String(10)),
                                 Column("journal_date", Date),
                                 Column("journal_no", String(45)),
                                 Column("journal_memo", String),
                                 Column("supplier_id", Integer, ForeignKey("supplier_list.supplier_id")),
                                 Column('journal_total', Unicode),
                                 Column("shipping", Unicode),
                                 Column("currency_rate", Unicode),
                                 Column("gst", Unicode),
                                 Column("qst", Unicode),
                                 Column("filing_charge", Unicode),
                                 Column("labour_charge", Unicode),
                                 Column("mix", Boolean),
                                 Column('export', Boolean),
                                 Column('modified_date', Date),
                                 Column('rec_type', String(3)))

    log_table = Table("log", metadata,
                      Column("id", Integer, primary_key=True),
                      Column("journal_id", Integer, ForeignKey("journal_header.journal_id")),
                      Column("user_id", Integer, ForeignKey("users.user_id")),
                      Column("log_date", DateTime),
                      Column("log_memo", String))
    
    rmd_table = Table("rmd", metadata,
                      Column("id", Integer, primary_key=True),
                      Column("bom_id", Integer, ForeignKey("bom.bom_id")),
                      Column("journal_id", Integer, ForeignKey("journal_header.journal_id")),
                      Column('batch_id', Integer, ForeignKey('batch_header.batch_id')),
                      Column("cost", Unicode),
                      Column("rmd_desc", String),
                      Column("qty", Unicode),
                      Column("cost_native", Unicode),
                      Column("rmd_shipping", Unicode),
                      Column('native_total', Unicode),
                      Column("total", Unicode),
                      Column("rmd_memo", String),
                      Column("new_qty", Unicode),
                      Column("new_value", Unicode),
                      Column('rec_type', String(3)))
    
    fgd_table = Table("fgd", metadata,
                      Column("fgd_id", Integer, autoincrement=False, primary_key=True),
                      Column("item_id", Integer, ForeignKey("item_list.item_id")),
                      Column("journal_id", Integer, ForeignKey("journal_header.journal_id")),
                      Column("fgd_desc", String), 
                      Column("fgd_qty", Unicode),
                      Column('rm_cost', Unicode),
                      Column('direct_cost', Unicode),
                      Column("cost", Unicode))
                      
    
    fgd_batch_assembly_table = Table("fgd_batch_assembly", metadata,
                               Column("id", Integer, primary_key=True),
                               Column("item_id", Integer, ForeignKey("fgd.fgd_id")),
                               Column("base_id", Integer, ForeignKey("base_header.base_id")),
                               Column("percentage", Unicode))
    
    fgd_bom_assembly_table = Table('fgd_bom_assembly', metadata,
                                   Column('id', Integer, primary_key=True),
                                   Column('item_id', Integer, ForeignKey('fgd.fgd_id')),
                                   Column('bom_id', Integer, ForeignKey('rmd.bom_id')))
    
    lists_table = Table('lists', metadata,
                        Column('id', Integer, primary_key=True),
                        Column('type', String),
                        Column('item', String))
    
    settings_table = Table('settings', metadata,
                           Column('setting', String, primary_key=True),
                           Column('date_value', Date),
                           Column('bool_value', Boolean),
                           Column('value_1', String),
                           Column('value_2', String),
                           Column('value_3', String))
    
    prep_header_table = Table('prep_header', metadata,
                              Column('prep_id', Integer, autoincrement=False, primary_key=True),
                              Column('prod_id', Integer, ForeignKey('journal_header.journal_id')),
                              Column('prep_date', Date),
                              Column('prep_memo', String))
    
    prep_detail_table = Table('prep_detail', metadata,
                              Column('pd_id', Integer, autoincrement=False, primary_key=True),
                              Column('header_id', Integer, ForeignKey('prep_header.prep_id')),
                              Column('item_id', Integer, ForeignKey('item_list.item_id')),
                              Column('qty', Unicode),
                              Column('pack', Unicode),
                              Column('volume', Unicode))
                              
    prep_assembly_table = Table('prep_assembly', metadata,
                                Column('id', Integer, primary_key=True),
                                Column('pd_id', Integer, ForeignKey('prep_detail.pd_id')),
                                Column('batch_id', Integer, ForeignKey('batch_header.batch_id')),
                                Column('percentage', Unicode),
                                Column('inflation', Unicode))
    
    metadata.create_all()
    
    clear_mappers()
    mapper(Lists, lists_table)
    mapper(Settings, settings_table)
    mapper(RMD, rmd_table, properties={'boms': relationship(BOM, backref='rmds'),
                                       'bomAssemblies': relationship(FGDBOMAssembly, backref='rmds'),
                                       'batches': relationship(BatchHeader, backref='rmds')},
           polymorphic_on=rmd_table.c.rec_type, polymorphic_identity="rmd")
    mapper(ReceiveRMD, inherits=RMD, polymorphic_identity='rcv')
    mapper(BatchRMD, inherits=RMD, polymorphic_identity='btc')
    mapper(AssemblyRMD, inherits=RMD, polymorphic_identity='asb')
    mapper(AdjRMD, inherits=RMD, polymorphic_identity="adj")
    mapper(FGDBatchAssembly, fgd_batch_assembly_table)
    mapper(FGDBOMAssembly, fgd_bom_assembly_table)
    mapper(FGD, fgd_table, properties={'assemblies': relationship(FGDBatchAssembly, backref='fgds'),
                                       'bomAssemblies': relationship(FGDBOMAssembly, backref='fgds')})
    
    mapper(Users, user_table, properties={'logs': relationship(Logs)})
    mapper(Suppliers, supplier_table, properties={'journals': relationship(JournalHeader)})
    mapper(BOM, bom_table, properties={'suppliers': relationship(Suppliers),
                                       'items': relationship(ItemAssembly, backref='boms')})
    mapper(Items, item_list_table, properties={'fgds': relationship(FGD, backref='items'), 
                                               'items': relationship(ItemAssembly),
                                               'bases': relationship(BaseAssembly),
                                               'lists': relationship(Lists, primaryjoin=item_list_table.c.category==lists_table.c.id,
                                                                      backref='items')})
    mapper(ItemAssembly, item_assembly_table)
    mapper(BaseAssembly, base_assembly_table)
    mapper(BaseHeader, base_header_table, properties={'details': relationship(BaseDetail),
                                                      'batches': relationship(BatchHeader, backref='bases'),
                                                      'assemblies': relationship(BaseAssembly, backref='bases'),
                                                      'fgdAssemblies': relationship(FGDBatchAssembly),
                                                      'associated': relationship(AssociatedBase, 
                                                                                 primaryjoin=base_header_table.c.base_id==associated_base_table.c.base_id)})
    mapper(BaseDetail, base_detail_table)
    mapper(AssociatedBase, associated_base_table)
    mapper(BatchHeader, batch_header_table, properties={'details': relationship(BatchDetail)})
    mapper(BatchDetail, batch_detail_table, properties={'boms': relationship(BOM)})
                                                        
    mapper(Logs, log_table)
    
    mapper(JournalHeader, journal_header_table, properties={'suppliers': relationship(Suppliers),
                                                            'rmds': relationship(RMD, backref='journals'), 'fgds': relationship(FGD)},
           polymorphic_on=journal_header_table.c.rec_type, polymorphic_identity="Jrn")
    mapper(ReceiveHeader, inherits=JournalHeader, polymorphic_identity="Rcv")
    mapper(ProductionHeader, inherits=JournalHeader, polymorphic_identity="Prd")
    mapper(AdjustmentHeader,inherits=JournalHeader, polymorphic_identity='Adj')
    mapper(PrepHeader, prep_header_table, properties={'journals': relationship(JournalHeader, backref='preps'),
                                                      'batches': relationship(BatchHeader, backref='preps')})
    mapper(PrepDetail, prep_detail_table, properties={'headers': relationship(PrepHeader, backref='details')})
    mapper(PrepAssembly, prep_assembly_table, properties={'prep_details': relationship(PrepDetail, backref='assemblies'),
                                                          'batches': relationship(BatchHeader)})
    
    db = QSqlDatabase.addDatabase('QSQLITE', 'prod')
    db.setDatabaseName(filename)
    db.open()

  
def createLists(listType='All', version=None):
    ses = Session()
    if listType:
        itemCat_list = [Lists('itemCategory', 'Cream'), Lists('itemCategory', 'Parvine'), Lists('itemCategory', 'No Sugar'),
                         Lists('itemCategory', 'Sorbeto'), Lists('itemCategory', 'Flavour')]
        season_list = [Lists('season', 'All Year'), Lists('season', 'Passover')]
        
        settings_list = [Settings('__version__', None, None, '1.0.4'), Settings('update_price', None, False), 
                         Settings('check_price', None, True, '5.0'), Settings('default_date', None, None, 'current'),
                         Settings('closing_date', datetime.datetime.now().date(), False), 
                         Settings('export_accounts', None, None, 'account1|account2|account3|account4')]
        
        
        
        lists = (itemCat_list, season_list, settings_list) if listType == 'All' else [eval(i) for i in listType]
        
        for my_list in lists:
            ses.add_all(my_list)
        
    ses.query(Settings).filter(Settings.setting=='__version__').update({'value_1': version})
    
    ses.flush()
    ses.commit()
    ses.close()
    
class Lists(object):
    def __init__(self, type, item):
        self.type = type
        self.item = item

class Settings(object):
    def __init__(self, setting, date_value=None, bool_value=None, value_1=None, value_2=None, value_3=None):
        self.setting = setting
        self.date_value = date_value
        self.bool_value = bool_value
        self.value_1 = value_1
        self.value_2 = value_2
        self.value_3 = value_3
        
        
class Users(object):
    def __init__(self, user_name, password, user_id=None):
        self.user_id = user_id
        self.user_name = user_name
        self.password = password
        
class Suppliers(object):
    def __init__(self, supplier_name, currency, supplier_id=None, selected=None):
        self.supplier_id = supplier_id
        self.supplier_name = supplier_name
        self.currency = currency
        self.selected = selected
    
    def __repr__(self):
        return "<suppliers: (%s, %s)>" % (self.supplier_name, self.currency)
        
                
class BOM(object):
    def __init__(self, bom_id=None, supplier_id=None, bom_no=None, bom_desc=None, bom_cost=0, hachsher=None, bom_supplier_no=None, 
                  measure="KG", pack=None, uom="KG", inactive=False, mix_item=False, qb_parent_path=None, qb_account=None):
        self.bom_id = bom_id
        self.supplier_id = supplier_id
        self.bom_no = bom_no
        self.bom_desc = bom_desc
        self.bom_cost = bom_cost
        self.hachsher = hachsher
        self.bom_supplier_no = bom_supplier_no
        self.measure = measure
        self.pack = pack
        self.uom = uom
        self.inactive = inactive
        self.mix_item = mix_item
        self.qb_parent_path = qb_parent_path
        self.qb_account = qb_account
    
    @hybrid_property
    def supplier_name(self):
        if not self.supplier_id:
            return ""
        return self.suppliers.supplier_name
    
class Items(object):
    def __init__(self, item_id=None, item_no=None, item_desc=None, volume=None, pack=None, item_cost=None,
                  season=None, category=None, inactive=False, mix_item=False):
        
        self.item_id = item_id
        self.item_no = item_no
        self.item_desc = item_desc
        self.volume = volume
        self.pack = pack
        self.item_cost = item_cost
        self.season = season
        self.category = category
        self.inactive = inactive
        self.mix_item = mix_item
    
    @hybrid_property
    def category_txt(self):
        if self.category:
            return self.lists.item
        else:
            return ""
        
class ItemAssembly(object):
    
    def __init__(self, item_id=None, bom_id=None, bom_qty=1, cost=None):
        self.item_id = item_id
        self.bom_id = bom_id
        self.bom_qty = bom_qty
        self.cost = cost
        
        
class BaseAssembly(object):
    def __init__(self, item_id=None, base_id=None, percentage=1, value=None):
            self.item_id = item_id
            self.base_id = base_id
            self.percentage = percentage
            self.value = value
    

class BaseHeader(object):
    def __init__(self, base_id, base_date, base_no, base_type, base_desc, base_volume, inflation_factor, base_memo):
        self.base_id = base_id
        self.base_date = base_date
        self.base_no = base_no
        self.base_type = base_type
        self.base_desc = base_desc
        self.base_volume = base_volume
        self.inflation_factor = inflation_factor
        self.base_memo = base_memo

class BaseDetail(object):
    def __init__(self, base_id=None, bom_id=None, bom_qty=None, cost=None):
        self.base_id = base_id
        self.bom_id = bom_id
        self.bom_qty = bom_qty
        self.cost = cost
        
class AssociatedBase(object):
    def __init__(self, base_id=None, asso_id=None, percentage=1):
        self.base_id = base_id
        self.asso_id = asso_id
        self.percentage = percentage

class BatchHeader(object):
    def __init__(self, batch_id, base_id, batch_date, base_volume, multiple, inflation_factor, batch_memo, journal_id=None, prep_id=None):
        self.batch_id = batch_id
        self.base_id = base_id
        self.journal_id = journal_id
        self.batch_date = batch_date
        self.base_volume = base_volume
        self.multiple = multiple
        self.inflation_factor = inflation_factor
        self.batch_memo = batch_memo
        self.prep_id = prep_id
    
    @hybrid_property
    def base_no(self):
        return self.bases.base_no
    @hybrid_property
    def base_desc(self):
        return self.bases.base_desc

class BatchDetail(object):
    def __init__(self, base_id=None, bom_id=None, cost=None, bom_qty=None, total=None):
        self.base_id = base_id
        self.bom_id = bom_id
        self.cost = cost
        self.bom_qty = bom_qty 
        self.total = total
    
        
class Logs(object):
    def __init__(self, journal_id, user_id, log_date, log_memo):
        self.journal_id = journal_id
        self.user_id = user_id
        self.log_date = log_date
        self.log_memo = log_memo  
                                                                  
class JournalHeader(object):
    def __init__(self, journal_id, journal_type, journal_date, journal_no, journal_memo, modified_date):
        
        self.journal_id = journal_id
        self.journal_type = journal_type
        self.journal_date = journal_date
        self.journal_no = journal_no
        self.journal_memo = journal_memo
        self.modified_date = modified_date
    
    def __repr__(self):
        return "<%s: (%s, %s, %s)>" % (self.__class__.__name__, self.journal_id, self.journal_no, self.journal_date)    

class ReceiveHeader(JournalHeader):
    def __init__(self, journal_id, journal_type, journal_date, journal_no, journal_memo,
                  supplier_id, journal_total, currency_rate, shipping, gst, qst, modified_date, export=False):        
        JournalHeader.__init__(self, journal_id, journal_type, journal_date, journal_no, journal_memo, modified_date)
        
        self.supplier_id = supplier_id
        self.journal_total = journal_total
        self.currency_rate = currency_rate
        self.shipping = shipping
        self.gst = gst
        self.qst = qst
        self.export = export
    
    @hybrid_property
    def supplier_name(self):
        if not self.supplier_id:
            return ""
        return self.suppliers.supplier_name

class ProductionHeader(JournalHeader):
    def __init__(self, journal_id, journal_type, journal_date, journal_no, journal_memo,
                  filing_charge, labour_charge, mix, modified_date):
        JournalHeader.__init__(self, journal_id, journal_type, journal_date, journal_no, journal_memo, modified_date)
        self.filing_charge = filing_charge
        self.labour_charge = labour_charge   
        self.mix = mix
        
class AdjustmentHeader(JournalHeader):
    def __init__(self, journal_id, journal_type, journal_date, journal_memo, modified_date, journal_no=None):
        JournalHeader.__init__(self, journal_id, journal_type, journal_date, journal_no, journal_memo, modified_date)
        self.journal_id = journal_id
        self.journal_type = journal_type
        self.journal_date = journal_date
        self.journal_memo = journal_memo


class RMD(object):
    def __init__(self, journal_id, bom_id, qty, total):
        
        self.journal_id = journal_id
        self.bom_id = bom_id
        self.qty = qty
        self.total = total  
    

class ReceiveRMD(RMD):
    def __init__(self, journal_id=None, bom_id=None, rmd_desc=None, qty=None, cost=None, 
                 cost_native=None, rmd_shipping=None, rmd_memo=None, total=None, native_total=None):
        
        RMD.__init__(self, journal_id, bom_id, qty, total)
        self.rmd_desc = rmd_desc
        self.cost = cost
        self.cost_native = cost_native
        self.rmd_shipping = rmd_shipping
        self.rmd_memo = rmd_memo
        self.native_total = native_total


class BatchRMD(RMD):
    def __init__(self, journal_id=None, bom_id=None, qty=None, cost=None, total=None, batch_id=None):
        
        RMD.__init__(self, journal_id, bom_id, qty, total)
        self.cost = cost
        self.batch_id = batch_id
        
class AssemblyRMD(RMD):
    def __init__(self, journal_id=None, bom_id=None, qty=None, cost=None, total=None):
        
        RMD.__init__(self, journal_id, bom_id, qty, total)
        self.cost = cost
   
class AdjRMD(RMD):
    def __init__(self, bom_id=None, new_qty=None, new_value=None, cost=None, rmd_memo=None, 
                 qty=None, total=None, journal_id=None, rmd_desc=None):
        
        RMD.__init__(self, journal_id, bom_id, qty, total)
        self.cost = cost
        self.rmd_memo = rmd_memo
        self.new_qty = new_qty
        self.new_value = new_value
        

class FGD(object):
    def __init__(self, fgd_id=None, item_id=None, fgd_desc=None, fgd_qty=None, 
                 cost=None, journal_id=None, rm_cost=None, direct_cost=None):
        
        self.fgd_id = fgd_id
        self.item_id = item_id
        self.fgd_desc = fgd_desc
        self.fgd_qty = fgd_qty
        self.cost = cost
        self.journal_id = journal_id
        self.rm_cost = rm_cost
        self.direct_cost = direct_cost
        
        
class FGDBatchAssembly(object):
    def __init__(self, item_id, base_id, percentage):
        self.item_id = item_id
        self.base_id = base_id
        self.percentage = percentage
        
    def __repr__(self):
        return '<FGDBatchAssembly: item %s,  base %s,  percent %s> ' % (self.item_id, self.base_id, self.percentage)
        
class FGDBOMAssembly(object):
    def __init__(self, item_id, bom_id):
        self.item_id = item_id
        self.bom_id = bom_id

class PrepHeader(object):        
    def __init__(self, prep_id, prep_date, prep_memo, prod_id=None):
        self.prep_id = prep_id
        self.prod_id = prod_id
        self.prep_date = prep_date
        self.prep_memo = prep_memo

class PrepDetail(object):
    def __init__(self, pd_id=None, item_id=None, qty=1, pack=None, volume=None, header_id=None, total=None):
        self.header_id = header_id
        self.pd_id = pd_id
        self.item_id = item_id
        self.qty = qty
        self.pack = pack
        self.volume = volume
        self.total = total
        
class PrepAssembly(object):
    def __init__(self, pd_id=None, batch_id=None, percentage=None, inflation=None, base_id=None, weight=None):
        self.pd_id = pd_id
        self.batch_id = batch_id
        self.percentage = percentage
        self.inflation = inflation
        self.base_id = base_id
        self.weight = weight
   
        
class ProductionFGReport(object):
    def __init__(self, item_no, pk_qty, exp_cost, item_desc, fg_qty, rm_cost, direct_cost, cost, pk_cost):
        self.item_no = item_no
        self.pk_qty = pk_qty
        self.exp_cost = exp_cost
        self.item_desc = item_desc
        self.fg_qty = fg_qty
        self.rm_cost = rm_cost
        self.direct_cost = direct_cost
        self.cost = cost
        self.pk_cost = pk_cost
        
class ProductionRMReport(object):
    def __init__(self, bom_no, bom_qty, bom_desc, bom_cost, bom_total):
        self.bom_no = bom_no
        self.bom_qty = bom_qty
        self.bom_desc = bom_desc
        self.bom_cost = bom_cost
        self.bom_total = bom_total
        
class DetailFind(object):
    def __init__(self, journal_id, item_no, item_desc, item_cost, journal_no, journal_date, journal_type):
        self.journal_id = journal_id
        self.item_no = item_no
        self.item_desc = item_desc
        self.item_cost = item_cost
        self.journal_no = journal_no
        self.journal_date = journal_date
        self.journal_type = journal_type

class InventorySumReport(object):
    def __init__(self, bom_id, bom_no, bom_desc, qty, cost, total):
        self.bom_id = bom_id
        self.bom_no = bom_no
        self.bom_desc = bom_desc
        self.qty = qty
        self.cost = cost
        self.total = total
        
class InventoryReport(object):
    def __init__(self, journal_id, journal_no, journal_date, journal_type, bom_id, bom_no, bom_desc,
                 qty, total, avg_cost, bal_qty=None, bal_value=None):
        self.journal_id = journal_id
        self.journal_no = journal_no
        self.journal_date = journal_date
        self.journal_type = journal_type
        self.bom_id = bom_id
        self.bom_no = bom_no
        self.bom_desc = bom_desc
        self.qty = qty
        self.total = total
        self.bal_qty = bal_qty
        self.bal_value = bal_value
        self.avg_cost = avg_cost