import sys
import platform
import inspect, os
import ntpath
import sqlalchemy.exc as exc
import sqlalchemy
import sqlalchemy.orm as orm
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
import databaseschema
import modelsandviews
import homeform
import userform
import supplierform
import itemform
import receiveform
import prodprepform
import batchform
import productionform
import inventoryadjform
import batchadjform
import finditemform
import findform
import settingsform
import utilities
import reporting
import reports
import functions
import images_rc

__version__ = '1.0.6'

TITLE = "Production Program"

class MainWindow(QMainWindow):
    
    def createAction(self, text, slot=None, shortcut=None, icon=None, tip=None, checkable=False,
                     signal="triggered()"):
        """Just enter the relevent info for the action, and we will do the rest"""
        action = QAction(text, self)
        if slot is not None:
            self.connect(action, SIGNAL(signal), slot)
        if shortcut is not None:
            action.setShortcut(shortcut)
        if icon is not None:
            action.setIcon(QIcon(icon))
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if checkable:
            action.setCheckable(True)
        return action
    
    def addActions(self, target, actions):
        """ Add multiple action at once to a menuBar or toolBar"""
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)
    
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        
        self.mdi = QWorkspace()
        self.setCentralWidget(self.mdi)
        
        settings = QSettings()
        self.restoreGeometry(settings.value("MainWindow/geometry").toByteArray())
        self.restoreState(settings.value("MainWindow/state").toByteArray())
        filename = settings.value('MainWindow/filename').toString()
        self.filename = str(filename)
        self.userModel = None
        self.go_ahead = False
        self.ui_setup = True
        self.user_id = 0
        self.date = functions.currentDate().date()
        self.openWindowDock = QDockWidget('Open Forms', self)
        
        self.setupFileMenu()
        
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)
        self.setWindowTitle(TITLE)
        self.setWindowIcon(QIcon(':/icons/mixer'))
        
        QTimer.singleShot(0, lambda: self.showLogIn(self.filename))
        
        
    def setupFileMenu(self):
        fileNewAction = self.createAction('Create New', self.creatNewFile, None, ':/icons/filenew', 'Create new production database file')
        fileOpenAction = self.createAction('Open Database', self.openFile, None, ':/icons/fileopen', 'Open database')
        fileLogInAction = self.createAction('&LogIn', self.logIn, 'Ctrl+L', ':/icons/login', 'Log In')
        fileCloseAllAction = self.createAction('Close All', self.closeAll, None,':/icons/fileclose', 'Close All Windows')
        self.fileQuitAction = self.createAction("&Quit", self.close, "Ctrl+Q", ':/icons/exit', "Close program")
        
        self.fileMenu = self.menuBar().addMenu("&File")
        self.addActions(self.fileMenu, (fileNewAction, fileOpenAction, fileLogInAction, fileCloseAllAction, None, self.fileQuitAction))

        
    def showLogIn(self, filename):
        """ decide whether to whow the log in dialog based if there are users setup in the database."""
        # // check if there is a filename to open the database, if not we are done
        if not filename:
            return
        # // now even if there is a filename we still need to check if that file exists
        # // otherwise sqlalchemy will just create a new database, and we like control
        try:
            with open(filename) : pass
        except:
            self.filename = None
            return
        # // if we are all happy, there is a filename and it exists, lets go ahead and connect to database.
        ok = self.setupDB(filename)
        if not ok:
            return
        # // now lets check if there are any users in the database, to decide whether we should show log in
        users = orm.Session().query(databaseschema.Users).count()
        if users < 1:
            self.setGoAhead(True)
        else:
            self.logIn()
        # // the log will give the go ahead if user id and password match
        # // no we want to setup the rest of the ui for the main window, 
        # // provided we have a go ahead, and the ui has not yet been setup
        self.setWindowTitle('%s - (%s), (%s)' % (TITLE, ntpath.basename(self.filename),
                             functions.dLookup(databaseschema.Users.user_name, databaseschema.Users.user_id==self.user_id)))
        if self.go_ahead and self.ui_setup:
            self.setupUi()
            self.ui_setup = False

    def setGoAhead(self, go, user_id=0):
        self.go_ahead = go
        self.user_id = user_id
        
    def setDate(self, date):
        self.date = date
        
    def getDate(self):
        default_date = functions.defaultDate()
        if default_date == 'last':
            return self.date
        else:
            return functions.currentDate().date()
        
        
    def setupDB(self, filename):
        try:
            databaseschema.setupDatabase(filename)
            self.filename = filename
        except NotImplementedError:
            QMessageBox.information(self, 'Log In - Open production file', 'Wrong file!!!', QMessageBox.Ok)
            return False
        except exc.ArgumentError:
            QMessageBox.information(self, '%s - Open database', 'Could not successfully open new database.', QMessageBox.Ok)
            return False
        
        db_version = functions.dLookup(databaseschema.Settings.value_1, databaseschema.Settings.setting == '__version__')
        if not db_version:
            QMessageBox.information(self, 'Open Database', 'v: %s, db: %s \n Wrong Database File, ' \
                                    'please contact administrator' % (__version__, db_version),
                                     QMessageBox.Ok) 
            self.closeDB()
            return False
        
        elif db_version != __version__:
            progress = QProgressDialog('Updating File', 'Cancel', 0, 100)
            progress.setCancelButton(None)
            progress.show()
            progress.setValue(50)
            functions.updateDb(progress, __version__, db_version)
            return True
        else:
            return True
            
    def openFile(self):
        self.closeAll()
        filename = QFileDialog.getOpenFileName(None, "Log In - Select production file", "", '(*.sqlite)')
        if filename.isEmpty():
            return
        filename = str(filename)
        self.closeDB()
        self.showLogIn(filename)
    
    def resetMainWindow(self):
        # // reset main window to unopened state
        self.go_ahead = False
        self.ui_setup = True
        self.closeAll()
        self.menuBar().clear()
        self.openWindowDock.hide()
        self.setupFileMenu()
        
    def closeDB(self):
        self.supplierModel = None
        self.bomModel = None
        self.itemModel = None
        self.baseListModel = None
        self.batchListModel = None
        self.userModel = None
        self.prepListModel = None
        self.resetMainWindow()
        prodDb = QSqlDatabase.database('prod')
        prodDb.close()
        prodDb = QSqlDatabase()
        QSqlDatabase.removeDatabase('prod')
    
    def setFileName(self, filename):
        self.filename = filename
    
    def setupUi(self):
        # setup Models
        self.supplierModel = modelsandviews.SupplierModel()
        self.bomModel = modelsandviews.ItemModel('BOM')
        self.itemModel = modelsandviews.ItemModel('Items')
        self.baseListModel = modelsandviews.BaseListModel()
        self.batchListModel = modelsandviews.BatchListModel()
        self.prepListModel = modelsandviews.PrepListModel()
        
        # prepare form variables
        self.home_form = None
        self.supplier_form = None
        self.item_form = None
        self.receive_form = None
        self.batch_form = None
        self.prodprep_form = None
        self.production_form = None
        self.inventoryAdj_form = None
        self.batchAdj_form = None
        self.findItem_form = None
        self.find_form = None
        self.settings_form = None
        
        # // prepare other variables
        self.from_date = QDate().currentDate().toPyDate()
        self.to_date = QDate().currentDate().toPyDate()
        self.report_bomId = None
        accounts = functions.dLookup(databaseschema.Settings.value_1, databaseschema.Settings.setting == 'export_accounts')
        accounts = accounts.split('|')
        self.ap_account = accounts[0].strip()
        self.ap_usAccount = accounts[1].strip()
        self.inv_account = accounts[2].strip()
        self.exp_class = accounts[3].strip()

        self.openWindowDock.show()
        self.openWindowDock.setObjectName('OpenWindowDock')
        self.openWindowDock.setAllowedAreas(Qt.LeftDockWidgetArea| Qt.RightDockWidgetArea)
        self.openWindowList = QListWidget()
        self.openWindowDock.setWidget(self.openWindowList)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.openWindowDock)
        self.openWindowList.clicked.connect(self.dockWindow)
        
        importSupplierAction = self.createAction('Import Supplier List', self.importSupplier, None, ':/icons/import', 'Import supplier list from excel')
        importBOMAction = self.createAction('Import BOM List', self.importBOM, None, ':/icons/import', 'Import Bill Of Material list from excel')
        importBaseAction  = self.createAction('Import Base', self.importBase, None, ':/icons/import', 'Import Bases from excel')
        importItemAction  = self.createAction('Import Item List', self.importItem, None, ':/icons/import', 'Import item list from excel')
        importReceiveAction  = self.createAction('Import Receive', self.importReceive, None, ':/icons/import', 'Import inventory receiving from excel')
        exportReceiveAction = self.createAction('Export IIF', self.exportReceive, None, ':/icons/export', 'Export receive reports to an IIF file.')
        setupUserAction = self.createAction('Setup User', self.userSetup, None, ':/icons/settings', 'Setup new user name and password')
        settingsAction = self.createAction('Preferences', self.settingsForm, None, ':/icons/settings', 'Settings and Tools')
        utilitiesMenu = self.fileMenu.addMenu('Utilities')
        self.addActions(utilitiesMenu, (importSupplierAction, importBOMAction, importBaseAction, importItemAction, importReceiveAction,
                                         None, exportReceiveAction, None, setupUserAction, settingsAction))
        self.fileMenu.insertMenu(self.fileQuitAction, utilitiesMenu)
        self.fileMenu.insertSeparator(self.fileQuitAction)

        formHomeAction = self.createAction("Home", self.homeForm, 'Ctrl+H', ":/icons/home", "Go To Home")
        formSupplierAction = self.createAction("New Supplier", self.supplierForm, None, ":/icons/account", "Add New Supplier")
        formItemAction = self.createAction("New Item", self.itemForm, None, ":/icons/item", "Add New Item")
        formReceiveAction = self.createAction("Receive Inventory", self.receiveForm, None, ":/icons/inventory", "Receive Inventory")
        formProdprepAction = self.createAction('Prepare Production', self.prodprepForm, None, ":/icons/prep", "Prepare A Production")
        formBatchAction = self.createAction('Create Batch', self.batchForm, None, ':/icons/batch', 'Create A Batch')
        formBaseAction = self.createAction('Record Base', self.baseForm, None, ':/icons/batch', 'Record A New Base')
        formProduction = self.createAction('Production', self.productionForm, None, ':/icons/production', 'Record A Production')
        formInvAdjustment = self.createAction('Adjust Inventory', self.invAdjustment, None, ':/icons/journal', 'Adjust Inventory')
        formBatchAdjAction = self.createAction('Adjust Batch RM', self.batchAdjForm, None, ':/icons/settings',
                                                'Adjust Raw Materials on a batch before production')
        
        formMenu = self.menuBar().addMenu("Form")
        self.addActions(formMenu, (formHomeAction, formSupplierAction, formItemAction, formReceiveAction, formProdprepAction, formBatchAction,
                                   formBaseAction, formProduction, formInvAdjustment, formBatchAdjAction))
        
        findMenu = self.menuBar().addMenu('Find')
        findItemAction = self.createAction('Find Item', self.findItem, None, ':/icons/find', 'Find Item')
        findAction = self.createAction('&Find', self.findForm, 'Ctrl+F', ':/icons/search', 'Find Transaction')
        self.addActions(findMenu, (findItemAction, findAction))
        
        reportInventorySumAction = self.createAction('Inventory Evaluation', self.inventorySumReport, None, ':/icons/report', 'Invenatory Report')
        reportInventoryDetailAction = self.createAction('Inventory Detail', self.inventoryDetReport, None, 
                                                        ':/icons/report', 'Inventory Detail Report')
        reportMenu = self.menuBar().addMenu('Reports')
        self.addActions(reportMenu, (reportInventorySumAction, reportInventoryDetailAction))
        
        
        self.windowNextAction = self.createAction("&Next", self.mdi.activateNextWindow, QKeySequence.NextChild)
        self.windowPrevAction = self.createAction("&Previous", self.mdi.activatePreviousWindow, QKeySequence.PreviousChild)
        self.windowCascadeAction = self.createAction("Casca&de", self.mdi.cascade)
        self.windowTileAction = self.createAction("&Tile", self.mdi.tile)
        self.windowRestoreAction = self.createAction("&Restore All", self.windowRestoreAll)
        self.windowMinimizeAction = self.createAction("&Iconize All", self.windowMinimizeAll)
        self.windowArrangeIconsAction = self.createAction("&Arrange Icons", self.mdi.arrangeIcons)
        self.windowCloseAction = self.createAction("&Close", self.mdi.closeActiveWindow, QKeySequence.Close)
        self.showDockAction = self.createAction('Show Dock Window', self.showDockWindow)
        
        formToolBar = self.addToolBar('Forms Toolbar')
        formToolBar.setObjectName('FormToolBar')
        self.addActions(formToolBar, (formHomeAction, formSupplierAction, formItemAction, formReceiveAction, formProdprepAction, 
                                      formBatchAction, formProduction, formBatchAdjAction, formInvAdjustment))
        findToolBar = self.addToolBar('Find Toolbar')
        findToolBar.setObjectName('FindToolBar')
        self.addActions(findToolBar, (findItemAction, findAction))
        
        self.windowMapper = QSignalMapper(self)
        self.connect(self.windowMapper, SIGNAL("mapped(QWidget*)"), self.mdi, SLOT("setActiveWindow(QWidget*)"))
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.connect(self.windowMenu, SIGNAL("aboutToShow()"), self.updateWindowMenu)
        
        helpMenu = self.menuBar().addMenu('Help')
        aboutAction = self.createAction('&About Production Program', self.helpAbout)
        self.addActions(helpMenu, (aboutAction,))
        
        self.homeForm()
        
        self.updateWindowMenu()

    def windowRestoreAll(self):
        for form in self.mdi.windowList():
            form.showNormal()
   
    def windowMinimizeAll(self):
        for form in self.mdi.windowList():
            form.showMinimized()
    
    def updateWindowMenu(self):
        self.windowMenu.clear()
        self.addActions(self.windowMenu, (self.showDockAction, None, self.windowNextAction, self.windowPrevAction,
                                          self.windowCascadeAction, self.windowTileAction,
                                          self.windowRestoreAction, self.windowMinimizeAction,
                                          self.windowArrangeIconsAction, None,
                                          self.windowCloseAction))
        forms = self.mdi.windowList()
        if not forms:
            return
        self.windowMenu.addSeparator()
        i = 1
        menu = self.windowMenu
        for form in forms:
            title = form.windowTitle()
            
            if i == 10:
                self.windowMenu.addSeparator()
                menu = menu.addMenu("&More")
            accel = ""
            if i < 10:
                accel = "&%d " % i
            elif i < 36:
                accel = "&%c " % chr(i + ord("@") - 9)
            action = menu.addAction("%s%s" % (accel, title))
            self.connect(action, SIGNAL("triggered()"), self.windowMapper, SLOT("map()"))
            self.windowMapper.setMapping(action, form)
            self.openWindowList.addAction(action)
            i += 1
            
    def showDockWindow(self):
        self.openWindowDock.show()
        
    def updateDockWindow(self, add_form=None):
        self.window_dict = {}
        self.openWindowList.clear()
        
        if add_form:
            title = add_form.windowTitle()
            title_list = self.window_dict.keys()
            if title in title_list:
                title = '%s + d' % (title, title_list.count(title))
            self.window_dict[title] = add_form
            self.openWindowList.addItem(title)
           
        forms = self.mdi.windowList(QWorkspace.StackingOrder)
        for form in forms:
            if form != add_form:
                title = form.windowTitle()
                title_list = self.window_dict.keys()
                j = 1
                if title in title_list:
                    for i in title_list:
                        if title == i[:-4]:
                            j += 1
                        
                    title = title +' (' + str(j) + ')'
                self.window_dict[title] = form
                self.openWindowList.addItem(title)
    
    def dockWindow(self):
        item = self.openWindowList.currentItem().text()
        form = self.window_dict[item]
        self.mdi.setActiveWindow(form)
        
        
    def creatNewFile(self):
        filename = QFileDialog.getSaveFileName(self, 'New Database - Specify file name')
        if not filename:
            return
        if not '.sqlite' in filename:
            filename += '.sqlite'
        databaseschema.setupDatabase(str(filename))
        databaseschema.createLists()
        
    def logIn(self):
        self.resetMainWindow()
        # // show log in form
        if not self.userModel:
            self.userModel = modelsandviews.UserModel()
        userForm = userform.UserForm(self.userModel, 1, ntpath.basename(self.filename), self)
        userForm.exec_()
        if self.go_ahead and self.ui_setup:
            self.setupUi()
            self.ui_setup = False
        
    def closeAll(self):
        self.mdi.closeAllWindows()
        
    def importSupplier(self):
        utilities.importSupplierList()
    
    def importBOM(self):
        utilities.importBOM()
    
    def importBase(self):
        utilities.importBaseList()
    
    def importItem(self):
        utilities.importItemList()
    
    def importReceive(self):
        utilities.importReceive(self.user_id)
    
    def exportReceive(self):
        dialog = utilities.ExportIIFDialog(self)
        dialog.ap_lineEdit.setText(str(self.ap_account))
        dialog.ap_us_lineEdit.setText(str(self.ap_usAccount))
        dialog.inv_lineEdit.setText(str(self.inv_account))
        dialog.class_lineEdit.setText(str(self.exp_class))
        if dialog.exec_():
            self.ap_account = str(dialog.ap_lineEdit.text())
            self.ap_usAccount = str(dialog.ap_us_lineEdit.text())
            self.inv_account = str(dialog.inv_lineEdit.text())
            self.exp_class = str(dialog.class_lineEdit.text())
            utilities.exportReceiveIIF(self.ap_account, self.ap_account, self.inv_account, self.exp_class)
    
    def userSetup(self):
        if not self.userModel:
            self.userModel = modelsandviews.UserModel()
        userForm = userform.UserForm(self.userModel, 0, ntpath.basename(self.filename), self)
        userForm.exec_()
        
    def settingsForm(self):
        self.settings_form = settingsform.SettingsForm(self.bomModel, self)
        self.settings_form.exec_()
    
    def homeForm(self):
        if self.home_form in self.mdi.windowList():
            self.mdi.setActiveWindow(self.home_form)
            return
        self.home_form = homeform.HomeForm(self.batchListModel, self)
        self.mdi.addWindow(self.home_form)
        self.updateDockWindow(self.home_form)
        self.home_form.show()
        
    def supplierForm(self):
        if self.supplier_form in self.mdi.windowList():
            self.mdi.setActiveWindow(self.supplier_form)
            return
        self.supplier_form = supplierform.SupplierForm(self.supplierModel, self)
        self.mdi.addWindow(self.supplier_form)
        self.updateDockWindow(self.supplier_form)
        self.supplier_form.show()
    
    def itemForm(self, itemType=0):
        if self.item_form in self.mdi.windowList():
            self.mdi.setActiveWindow(self.item_form)
            return self.item_form
        self.item_form = itemform.ItemForm(self.supplierModel, self.bomModel, self.baseListModel, itemType, self)
        self.mdi.addWindow(self.item_form)
        self.updateDockWindow(self.item_form)
        self.item_form.show()
        return self.item_form
        
    def receiveForm(self):
        if self.receive_form in self.mdi.windowList():
            self.mdi.setActiveWindow(self.receive_form)
            return self.receive_form
        self.receive_form = receiveform.ReceiveForm(self.supplierModel, self.bomModel, self)
        self.mdi.addWindow(self.receive_form)
        self.updateDockWindow(self.receive_form)
        self.receive_form.show()
        return self.receive_form
    
    def prodprepForm(self):
        if self.prodprep_form in self.mdi.windowList():
            self.mdi.setActiveWindow(self.prodprep_form)
            return self.prodprep_form
        self.prodprep_form = prodprepform.ProductionPrep(self.itemModel, self.baseListModel, self)
        self.mdi.addWindow(self.prodprep_form)
        self.updateDockWindow(self.prodprep_form)
        self.prodprep_form.show()
        return self.prodprep_form
        
    def batchForm(self):
        if self.batch_form in self.mdi.windowList():
            self.mdi.setActiveWindow(self.batch_form)
            self.batch_form.changeLayout(False)
            return self.batch_form
        self.batch_form = batchform.BatchForm(self.baseListModel, self.bomModel, 1, self)
        self.mdi.addWindow(self.batch_form)
        self.updateDockWindow(self.batch_form)
        self.batch_form.show()
        return self.batch_form
    
    def baseForm(self):
        if self.batch_form in self.mdi.windowList():
            self.mdi.setActiveWindow(self.batch_form)
            self.batch_form.changeLayout(False)
            return self.batch_form
        self.batch_form = batchform.BatchForm(self.baseListModel, self.bomModel, 0, self)
        self.mdi.addWindow(self.batch_form)
        self.updateDockWindow(self.batch_form)
        self.batch_form.show()
        return self.batch_form
    
    def productionForm(self):
        if self.production_form in self.mdi.windowList():
            self.mdi.setActiveWindow(self.production_form)
            return self.production_form
        self.production_form = productionform.ProductionForm(self.baseListModel, self.batchListModel, 
                                                             self.itemModel, self.bomModel, self.prepListModel, self)
        self.mdi.addWindow(self.production_form)
        self.updateDockWindow(self.production_form)
        self.production_form.show()
        return self.production_form
    
    def invAdjustment(self):
        if self.inventoryAdj_form in self.mdi.windowList():
            self.mdi.setActiveWindow(self.inventoryAdj_form)
            return self.inventoryAdj_form
        self.inventoryAdj_form = inventoryadjform.InventoryAdjForm(self.bomModel, self)
        self.mdi.addWindow(self.inventoryAdj_form)
        self.updateDockWindow(self.inventoryAdj_form)
        self.inventoryAdj_form.show()
        return self.inventoryAdj_form
    
    def batchAdjForm(self):
        if self.batchAdj_form in self.mdi.windowList():
            self.mdi.setActiveWindow(self.batchAdj_form )
            return
        self.batchAdj_form  = batchadjform.BatchAdjForm(self)
        self.mdi.addWindow(self.batchAdj_form )
        self.updateDockWindow(self.batchAdj_form )
        self.batchAdj_form .show()
    
    def reportSettings(self, report, parent=None):
        dialog = reports.ReportDialog(self.bomModel)
        from_date = self.from_date if self.from_date else QDate().currentDate()
        to_date = self.to_date if self.to_date else QDate().currentDate()
        dialog.from_date.setDate(from_date)
        dialog.to_date.setDate(to_date)
        bom_no = functions.dLookup(databaseschema.BOM.bom_no, databaseschema.BOM.bom_id==self.report_bomId)
        bom_index = dialog.bom_comboBox.findText(str(bom_no), Qt.MatchExactly) \
                        if self.report_bomId else -1
        dialog.bom_comboBox.setCurrentIndex(bom_index)
        if dialog.exec_():
            self.from_date = dialog.from_date.date().toPyDate()
            self.to_date = dialog.to_date.date().toPyDate()
            if dialog.range_comboBox.currentText() == 'All':
                self.from_date = None
                self.to_date = None
            bom_no = str(dialog.bom_comboBox.currentText())
            self.report_bomId = functions.dLookup(databaseschema.BOM.bom_id, databaseschema.BOM.bom_no==bom_no)
            if parent:
                parent.refresh()
    
    def refreshReport(self, model, report=None):
        if report == 'inv_sum':
            reports.invSumReport(model, None, self.to_date)
        elif report == 'inv_detail':
            reports.invDetailReport(model, self.report_bomId, self.from_date, self.to_date)
        
   
    def inventorySumReport(self):
        report_name = 'inv_sum'
        reportModel = reporting.ReportModel('Simple List')
        self.refreshReport(reportModel, report_name)
        self.reportForm(reportModel, self, report_name, True)
        
    
    def inventoryDetReport(self, bomId=None):
        self.report_bomId = bomId if bomId else self.report_bomId
        report_name = 'inv_detail'
        reportModel = reporting.ReportModel('Simple List')
        self.refreshReport(reportModel, report_name)
        self.reportForm(reportModel, self, report_name, True)
    
    
    def findItem(self, itemType=0, ascForm=None, title=None):
        if ascForm and self.findItem_form:
            self.findItem_form.reject()
        if self.findItem_form in self.mdi.windowList():
            self.mdi.setActiveWindow(self.findItem_form)
            self.findItem_form.changeType(itemType)
            if ascForm:
                formTtl = self.findItem_form.windowTitle()
                self.findItem_form.setWindowTitle('%s - (%s)' % (formTtl, title))
            return
        self.findItem_form = finditemform.FindItemForm(self.supplierModel, itemType, self, ascForm)
        self.mdi.addWindow(self.findItem_form)
        self.updateDockWindow(self.findItem_form)
        if ascForm:
                formTtl = self.findItem_form.windowTitle()
                self.findItem_form.setWindowTitle('%s - (%s)' % (formTtl, title))
        self.findItem_form.show()
       
    
    def findForm(self):
        if self.find_form in self.mdi.windowList():
            self.mdi.setActiveWindow(self.find_form)
            return
        self.find_form = findform.FindForm(self.supplierModel, self)
        self.mdi.addWindow(self.find_form)
        self.updateDockWindow(self.find_form)
        self.find_form.show()
        
   
    def reportForm(self, model, parent, report=None, modify=False):
        self.report_form = reporting.ReportForm(model, parent, report, modify)
        self.mdi.addWindow(self.report_form)
        self.updateDockWindow(self.report_form)
        self.report_form.show()
        return self.report_form
    
    def helpAbout(self):
        db_v = functions.dLookup(databaseschema.Settings.value_1, databaseschema.Settings.setting=='__version__')
        QMessageBox.about(self, "About Production Program",
                """<b>Production Program</b> v {0}, db_v {1}
                <p>Copyright &copy; 2013 YF Consulting Inc. 
                All rights reserved.
                <p>This application should be used to calculate Costs of manufactured products and for Bill of material Inventory Control.
                <p>Python {2} - Qt {3} - PyQt {4}  - SQLAlchemy {5} on {6}""".format(
                __version__, db_v, platform.python_version(),
                QT_VERSION_STR, PYQT_VERSION_STR, sqlalchemy.__version__, 
                platform.system()))
    
    def refreshModels(self):
        self.batchListModel.select()
        self.itemModel.select()
        self.bomModel.select()
        self.prepListModel.select()
        
    def formClosed(self):
        self.updateDockWindow()
        
   
    def closeEvent(self, event):
        settings = QSettings()
        settings.setValue("MainWindow/geometry", QVariant(self.saveGeometry()))
        settings.setValue("MainWindow/state", QVariant(self.saveState()))
        settings.setValue('MainWindow/filename', QVariant(self.filename))
        self.mdi.closeAllWindows()
        

               
if __name__ == '__main__':
    
    import singleton
    me = singleton.SingleInstance()
    app = QApplication(sys.argv)
    app.setOrganizationName("YF Services")
    app.setOrganizationDomain("hatzolah.com")
    app.setApplicationName(TITLE)
    form = MainWindow()
    form.show()
    app.exec_()
  
    
        
        
        
