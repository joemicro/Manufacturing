from __future__ import division
import gzip
import os
import platform
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from databaseschema import *
from functions import *
from xlwt import Workbook, easyxf
import modelsandviews



class ReportModel(QAbstractTableModel):
    
    def __init__(self, reportType, parent=None):
        super(ReportModel, self).__init__(parent)
        
        self.reportHeaderData = {} # // to store header data, like for production report.
        self.headerFieldNames = []
        
        self.mainData = []         # // used for list data, like a list report, or the first report on production report
        self.mainFieldNames = []   # // used to specify header information, like field names for data function, and field length
                                   # // for painting and field formatting format = ('ID', 'bom_id', 25, 'string')
        self.columnsToTotal = []   # // a list specifying which columns to total, 
                                   # // format = [(i, total)] specify the column index optional supply a total 
        self.subData = []          # // same as main data, but for secondary report
        self.subFieldNames = []
        self.subTotals = []        # // same as above but sub report totals
        
        self.reportName = QString()
        self.reportPeriod = QString()
        
        self.columnToCalc = None # // reserved for later used, in mainTotal func
        
        self.reportType = reportType
        
    def mainColumnNames(self):
        names = []
        for i in self.mainFieldNames:
            names += [(i[0])]
        return names
        
    def sortMain(self, field, order):
        """ sort main data list, by specified field and specified order. """
        # // since user specified a readable field name, loop through fieldName list where program field name is stored,
        # // and find corresponding field name
        fieldInfo = next((x for x in self.mainFieldNames if x[0] == field), None) 
        fieldKey = fieldInfo[1]
        # // setup a sort key to filter on
        sortKey = 'item.' + fieldKey
        # // filter list.
        self.mainData.sort(key=lambda item: eval(sortKey), reverse=order)
        
    def sortSub(self, field, order):
        """ sort secondary data list, by specified field and specified order. """
        fieldInfo = next((x for x in self.subFieldNames if x[0] == field), None)
        fieldKey = fieldInfo[1]
        sortKey = 'item.' + fieldKey
        self.subData.sort(key=lambda item: eval(sortKey), reverse=order)
        
        
    def mainRowCount(self):
        count = len(self.mainData)
        return count
    
    def subRowCount(self):
        count = len(self.subData)
        return count
    
    def rowCount(self, index=QModelIndex()):
        """ base implementation, return the number of rows in the model, if this is not spacified, the model has no dimensins.
        take the total of rows from all data lists, and calculate total rows. """
        hdrCount = 1 if self.reportHeaderData else 0
        count = len(self.mainData) + len(self.subData) + hdrCount
        return count
    
    def columnCount(self, index=QModelIndex()):
        """ base implemantation, need to know how many columns, take the max from the data lists """
        mainCount = len(self.mainFieldNames)
        detailCount = 0
        if self.subFieldNames:
            detailCount = len(self.subFieldNames)
        headerCount = 0
        if self.reportHeaderData:
            headerCount = len(self.reportHeaderData)
        count = max(headerCount, detailCount, mainCount)
        return count
    
    def data(self, index, listType='main', role=Qt.DisplayRole):
        """ base implemantation, returns requested data stored in the model"""
        # // select from which list to return data from, and which list has the appropriate field names to access the data
        if listType == 'main':
            dataList = self.mainData
            fieldList = self.mainFieldNames
        elif listType == 'header':
            dataList = self.reportHeaderData
            fieldList = self.headerFieldNames
        elif listType == 'sub':
            dataList = self.subData
            fieldList = self.subFieldNames
        # // check if the index user is looking for is valid
        if not index.isValid() or not (0 <= index.row() < len(dataList)):
#            print 'index not valid', listType, index.row()
            return QVariant()
        # // loop through fieldName list to find the field namehat corresponds to the requested info, and display its data.
        result = dataList[index.row()]
        column = index.column()
        if role == Qt.DisplayRole:
            i = 0
            while i <= len(fieldList):
                field = fieldList[i][1]
                field = 'result.' + field
                if column == i:
                    return QVariant(unicode(eval(field)))
                i += 1
        return QVariant()
    
    def load(self, reportName, period, mainData, mainFieldNames, mainTotals):
        """ load main report data into model. need to supply 
          - Report Name
          - Reporting period for sub header
          - the actual report data
          - the field names, header, width, format
          - a list of columns you want me to total """
        self.beginResetModel()
        self.mainData = []
        self.mainFieldNames = []                    
        self.columnsToTotal = []                      
        self.endResetModel()
        
        for row in mainData:
            self.mainData.append(row)
            
        for row in mainFieldNames:
            self.mainFieldNames.append(row)   
        
        for row in mainTotals:
            self.columnsToTotal.append(row)
            
        self.reportName = reportName
        self.reportPeriod = period
    
    
    def loadHeader(self, headerData, headerNames):
        
        self.beginResetModel()
        self.reportHeaderData = {}
        self.headerFieldNames = []
        self.endResetModel()
        
        self.reportHeaderData = headerData
            
        for row in headerNames:
            self.headerFieldNames.append(row)
                 
    
    def loadSubReport(self, subData,  subFieldNames, subTotals):
       
        self.beginResetModel()             
        self.subData = []     
        self.subFieldNames = []
        self.subTotals = []    
        self.endResetModel()
        
        for row in subData:
            self.subData.append(row)
        
        for row in subFieldNames:
            self.subFieldNames.append(row)
        
        for row in subTotals:
            self.subTotals.append(row)
    
   
    def columnToCalculate(self, record):
        """ returns the column in list to total""" 
        try:
            col = self.mainFieldNames[self.columnToCalc][1]
            field = getType(eval('record.' + col))
        except AttributeError:
            col = self.subFieldNames[self.columnToCalc][1]
            field = getType(eval('record.' + col))
        return field
    
    def mainTotalList(self):
        """ returns a constructed list of: an x-Position for painting, a column number, and a total to paint """
        totalList = []
        # // if no columns have been specified return
        if not self.columnsToTotal:
            return
        # // loop through the list of columns user submitted
        for col in self.columnsToTotal:
            
            # // set variable to be used for the columnToCalculate function, so it knows which index to return
            self.columnToCalc = col[0]
            x = 0
            xPosition = 0
            # // calculate an x-position you the total should be painted at
            for width in self.mainFieldNames:
                if x != col[0]:
                    xPosition += width[2]
                else:
                    break
                x += 1
            # // calculate the actual total
            if len(col) <= 1:
                total = sum(map(self.columnToCalculate, self.mainData))
            else:
                total = col[1]
            # add variable to list
            totalList += [(xPosition, col[0], total)]
        return totalList
        
    def subTotalList(self):
        """ returns a constructed list of an xPosition for painting, a column number, and a total to paint """
        totalList = []
        # if no columns have been specified return
        if not self.subTotals:
            return totalList
        # loop through the list of columns user decided wans to total
        for col in self.subTotals:
            
            # set variable to be used for the columnToCalculate function, so it know which index to return
            self.columnToCalc = col[0]
            x = 0
            xPosition = 0
            # now build an xposition the total should be painted on.
            for width in self.subFieldNames:
                if x != col[0]:
                    xPosition += width[2]
                else:
                    break
                x += 1
            # calculate the actual total
            if len(col) <= 1:
                total = sum(map(self.columnToCalculate, self.subData))
            else:
                total = col[1]
            # add variable to list
            totalList += [(xPosition, col[0], total)]
        return totalList
    
    def clear(self):
        self.beginResetModel()
        self.reportHeaderData = {}
        self.headerFieldNames = []
        self.mainData = []
        self.mainFieldNames = []                    
        self.columnsToTotal = []                      
        self.subData = []     
        self.subFieldNames = []
        self.subTotals = []    
        self.columnToCalc = None
        self.columnsToTotal = []
        self.endResetModel()
        
    
    def export(self, filename=None):
        # ask user to save file, so he should know where to find it
        filename = QFileDialog.getSaveFileName(None, 'Save report: %s to excel' % self.reportName)
        if not filename:
            return
        if not '.xls' in filename:
            filename += '.xls'
        # setup formatting
        headerStyle = easyxf('font: name Arial, height 160, bold True; borders: bottom thick')
        detailStyle = easyxf('font: name Arial, height 160')
        totalStyle = easyxf('font: name Arial, height 160, bold True; borders: top thin, bottom thick')
        book = Workbook()
        sheet = book.add_sheet(self.reportName)
        sheet.panes_frozen = True
        # write column headers
        for col in range(len(self.mainFieldNames)):
            text = self.mainFieldNames[col][0]
            sheet.write(0, col, text, headerStyle)
        y = 1
        # write row data
        for row in range(len(self.mainData)):
            for col in range(len(self.mainFieldNames)):
                text = str(self.data(self.index(row, col)).toString())  
                if self.mainFieldNames[col][3] == 'number':
                    text = float(text)
                sheet.write(y, col, text, detailStyle)
            y += 1
        # get and write totals
        totals = self.mainTotalList()
        if totals:
            for row in range(len(totals)):
                col = totals[row][1]
                total = float(totals[row][2])
                sheet.write(y, col, total, totalStyle)
        
        # if there is secondary report lets export that too.  
        if self.subData:
            y += 2
            for col in range(len(self.subFieldNames)):
                text = self.subFieldNames[col][0]
                sheet.write(y, col, text, headerStyle)
            y += 1
            for row in range(len(self.subData)):
                for col in range(len(self.subFieldNames)):
                    text = str(self.data(self.index(row, col), 'sub').toString())  
                    if self.subFieldNames[col][3] == 'number':
                        text = float(text)
                    sheet.write(y, col, text, detailStyle)
                y += 1
            totals = self.subTotalList()
            if totals:
                for row in range(len(totals)):
                    col = totals[row][1]
                    total = float(totals[row][2])
                    sheet.write(y, col, total, totalStyle)
        book.save(filename)

#==========================================================================
### Setup report view, this where the paint job is getting done ===========
class ReportView(QWidget):
    
    def __init__(self, parent=None):
        super(ReportView, self).__init__(parent)
        self.scrollarea = None
        self.model = None
        self.double_clicked = False
        self.setFocusPolicy(Qt.StrongFocus)
        
        self.reportName = QString()
        self.reportPeriod = QString()
        
        self.headerFieldNames = []
        self.mainFieldNames = []
        self.subFieldNames = []
        self.mainTotals = []
        self.subTotals = []
        
        # painting variables
        fontMetrics = QFontMetrics(self.font())
        self.fontSize = fontMetrics.height() * 1.5
        self.selectedRow = -1
        
        self.fields = 0
        self.headerY = 4 * self.fontSize
        
        self.indicatorSize = int(self.fontSize* .8)
        self.offset = int(1.5 * (self.fontSize - self.indicatorSize))
        self.Y = 0
        self.reportFont  = QFont('Arial')

        
    def setModel(self, model):
        self.model = model
        self.reportType = self.model.reportType
        self.reportHeaderData = self.model.reportHeaderData
        self.headerFieldNames = self.model.headerFieldNames
        self.mainFieldNames = self.model.mainFieldNames
        self.subFieldNames = self.model.subFieldNames
        self.mainTotals = self.model.mainTotalList()
        self.subTotals = self.model.subTotalList()
        self.reportName = self.model.reportName
        self.reportPeriod = self.model.reportPeriod
        self.fields = len(self.model.mainFieldNames)
        self.subFields = len(self.model.subFieldNames)
        
        self.model.dataChanged.connect(self.setNewSize)
        self.model.modelReset.connect(self.setNewSize)
        
        self.setNewSize()
        
    def getFieldWidth(self, record):
        hdr = record[2]
        return hdr
    
    def sizeHeight(self):
        if not self.model:
            return 0
        footer = 6 * self.fontSize
        sizeHeight = self.fontSize * self.model.rowCount()
        sizeHeight += self.headerY + footer
        return sizeHeight
    
    def sizeWidth(self):
        fields = max(len(self.mainFieldNames), len(self.subFieldNames), len(self.headerFieldNames))
        if len(self.mainFieldNames) == fields:
            width = sum(map(self.getFieldWidth, self.mainFieldNames))
        elif len(self.subFieldNames) == fields:
            width = sum(map(self.getFieldWidth, self.subFieldNames))
        elif len(self.headerFieldNames) == fields:
            width = sum(map(self.getFieldWidth, self.headerFieldNames ))   
        return (fields, width)   
    
    def setNewSize(self):
        self.resize(self.sizeHint())
        self.update()
        self.updateGeometry()
        
    def minimumSizeHint(self):
        size = self.sizeHint()
        size.setHeight(self.fontSize * 3)
        return size
   
    def sizeHint(self):
        size = self.fontSize
        fields, width = self.sizeWidth()
        qSize = QSize(width + (size * fields), 
                      (size / nonZero(fields, 1)) + (self.sizeHeight()))
        return qSize
    
    def printReport(self):
        if not self.model:
            return
        printer = QPrinter()
        dialog = QPrintDialog(printer, self)
        if not dialog.exec_():
            return
        printer.setPaperSize(QPrinter.Letter)
        painter = QPainter(printer)
        rect = printer.pageRect()
        self.paintMe(painter, rect, printer)
        painter.end()
           
    def paintEvent(self, event):
        if not self.model:
            return
        painter = QPainter(self)
        self.paintMe(painter, event.rect())
        
    def paintMe(self, painter, rect, printer=None):
        if self.reportType == 'Simple List':
            self.paintReportHeader(painter, rect)
            self.paintRows(painter, rect, self.model.mainRowCount(), self.fields, self.mainFieldNames, self.mainTotals, 'main', printer)
        elif self.reportType == 'Production':
            self.paintJournalHeader(painter, rect)
            self.paintRows(painter, rect, self.model.mainRowCount(), self.fields, self.mainFieldNames, self.mainTotals, 'main', printer)
            self.paintColumnHeader(painter, rect, self.subFieldNames)
            self.paintRows(painter, rect, self.model.subRowCount(), self.subFields, self.subFieldNames, self.subTotals, 'sub', printer)
        
    ### Painting jobs =============================   
    def paintJournalHeader(self, painter, rect):
        painter.save()
        self.reportFont.setPointSize(10)
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        painter.setPen(pen)
        
        self.Y = x = self.fontSize
        width = self.sizeHint().width() - self.fontSize
        painter.drawRect(x, self.Y, width, self.fontSize * 8)
        
        self.Y += self.fontSize * 1.5
        x += self.fontSize
        text = self.reportHeaderData['Production ID']
        painter.drawText(x, self.Y, 'Production ID:')
        painter.drawText(x + 5 * self.fontSize, self.Y, str(text))
        painter.drawLine(x, self.Y + (self.offset * 0.8), 10 * self.fontSize, self.Y + (self.offset * 0.8))
        
        self.Y += self.fontSize * 1.5
        text = self.reportHeaderData['Date']
        painter.drawText(x, self.Y, 'Date:')
        painter.drawText(x + 5 * self.fontSize, self.Y, str(text))
        painter.drawLine(x, self.Y + (self.offset * 0.8), 10 * self.fontSize, self.Y + (self.offset * 0.8))
        
        self.Y += self.fontSize * 1.5
        text = self.reportHeaderData['Ref No']
        painter.drawText(x, self.Y, 'Ref No:')
        painter.drawText(x + 5 * self.fontSize, self.Y, str(text))
        painter.drawLine(x, self.Y + (self.offset * 0.8), 10 * self.fontSize, self.Y + (self.offset * 0.8))
        
        self.Y = self.fontSize * 2.5
        x += 10 * self.fontSize
        text = self.reportHeaderData['Volume']
        painter.drawText(x, self.Y, 'Volume:')
        painter.drawText(x + 5 * self.fontSize, self.Y, str(text))
        painter.drawLine(x, self.Y + (self.offset * 0.8), x + 8 * self.fontSize, self.Y + (self.offset * 0.8))
        
        self.Y += self.fontSize * 1.5
        text = self.reportHeaderData['Total RM cost']
        painter.drawText(x, self.Y, 'Total RM cost:')
        painter.drawText(x + 5 * self.fontSize, self.Y, str(text))
        painter.drawLine(x, self.Y + (self.offset * 0.8), x + 8 * self.fontSize, self.Y + (self.offset * 0.8))
        
        self.Y += self.fontSize * 1.5
        text = self.reportHeaderData['Total FG Cost']
        painter.drawText(x, self.Y, 'Total FG Cost:')
        painter.drawText(x + 5 * self.fontSize, self.Y, str(text))
        painter.drawLine(x, self.Y + (self.offset * 0.8), x + 8 * self.fontSize, self.Y + (self.offset * 0.8))
        
        self.Y = self.fontSize * 2.5
        x += 10 * self.fontSize
        text = self.reportHeaderData['Filing']
        painter.drawText(x, self.Y, 'Filing:')
        painter.drawText(x + 5 * self.fontSize, self.Y, str(text))
        painter.drawLine(x, self.Y + (self.offset * 0.8), x + 8 * self.fontSize, self.Y + (self.offset * 0.8))
        
        self.Y += self.fontSize * 1.5
        text = self.reportHeaderData['Labour']
        painter.drawText(x, self.Y, 'Labour:')
        painter.drawText(x + 5 * self.fontSize, self.Y, str(text))
        painter.drawLine(x, self.Y + (self.offset * 0.8), x + 8 * self.fontSize, self.Y + (self.offset * 0.8))
        
        self.Y += self.fontSize * 1.5
        text = self.reportHeaderData['Fees P/L']
        painter.drawText(x, self.Y, 'Fees P/L:')
        painter.drawText(x + 5 * self.fontSize, self.Y, str(text))
        painter.drawLine(x, self.Y + (self.offset * 0.8), x + 8 * self.fontSize, self.Y + (self.offset * 0.8))
        
        self.Y += self.fontSize * 1.5
        text = self.reportHeaderData['Total Fees']
        painter.drawText(x, self.Y, 'Total Fees:')
        painter.drawText(x + 5 * self.fontSize, self.Y, str(text))
        painter.drawLine(x, self.Y + (self.offset * 0.8), x + 8 * self.fontSize, self.Y + (self.offset * 0.8))
        
        self.Y += self.fontSize * 2
        painter.restore()
        self.paintColumnHeader(painter, rect, self.mainFieldNames)
         
    def paintReportHeader(self, painter, rect):
        painter.save()
        # setup pen and paint report name
        self.reportFont.setPointSize(15)
        self.reportFont.setBold(True)
        painter.setFont(self.reportFont)
        a = QFontMetrics(painter.font())
        self.Y = a.height()
        x = self.fontSize
        painter.drawText(x, self.Y, self.reportName)
        # paint report period
        self.Y += self.Y
        self.reportFont.setPointSize(10)
        self.reportFont.setBold(False)
        painter.setFont(self.reportFont)
        painter.drawText(x, self.Y, self.reportPeriod)
        # set pen to draw underline under report header
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        painter.drawLine(x, self.Y + (self.offset * 0.8), rect.width(), self.Y + (self.offset * 0.8))
        painter.restore()
        self.paintColumnHeader(painter, rect, self.mainFieldNames)
        
    def paintColumnHeader(self, painter, rect, fieldNames):
        painter.save()
        x = self.fontSize
        # move on to write column headers
        self.reportFont.setBold(True)
        painter.setFont(self.reportFont)
        painter.fillRect(x, self.Y + (self.offset * 0.8), self.width() - self.fontSize, self.fontSize, self.palette().text())
        painter.setPen(self.palette().color(QPalette.HighlightedText))
        for hdr in fieldNames:
            if hdr[2] <= 0:
                x += self.fontSize
                continue
            header = hdr[0]                                              # header name
            painter.drawText(x, self.Y + self.fontSize, QString(header))
            x += hdr[2] + self.fontSize                                  # field width
        self.headerY = self.Y + self.fontSize
        self.setNewSize()
        painter.restore()
        
                  
    def paintRows(self, painter, rect, rowCount, fields, fieldNames, totals, listType, printer=None):
        # setup some sizes and variable to write row data
        palette = self.palette()
        size = self.fontSize
        indicatorSize = int(size * .8)
        offset = int(1.5 * (size - indicatorSize))
        minY = rect.y()
        maxY = minY + rect.height() + size
        if printer:
            minY = rect.y() + (size * 2)
            maxY = minY + rect.height() - (size * 4)
        minY -= size
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setRenderHint(QPainter.TextAntialiasing)
        
        # paint detail rows
        y = self.headerY
        color = palette.midlight()
        for row in range(rowCount):
            x = size
            #if minY <= y <= maxY: ### need to paint all rows else, can't have alternate row coloring
            painter.save()
            painter.setPen(palette.color(QPalette.Text))
            color = palette.midlight() if color == palette.light() else palette.light()
            painter.fillRect(x, y + (offset * 0.8), self.width() - size, size, color)
            
            if row == self.selectedRow:
                painter.fillRect(x, y + (offset * 0.8), self.width() - size, size, palette.highlight())
                painter.setPen(palette.color(QPalette.HighlightedText))
            
            for field in range(fields): 
                column = self.model.data(self.model.index(row, field), listType).toString()
                option = QTextOption(Qt.AlignLeft)
                width =  fieldNames[field][2]
                if fieldNames[field][3] == 'number':
                    try:
                        decimal = fieldNames[field][4]
                        formatting = '{:,.%sf}' % decimal
                        column = formatting.format(float(column)) 
                    except IndexError:
                        column = '{:,.2f}'.format(float(column))
                    option = QTextOption(Qt.AlignRight)
                option.setWrapMode(QTextOption.NoWrap)
                rect = QRectF(x, y + (offset * 0.8), width, size)
                painter.drawText(rect, column, option)
                x += (width + size)
            
            painter.restore()
            y += size
            
            # if the bottom of list is reached, stop, except if painting on printer, then just start new page
            if y > maxY:
                if printer:
                    printer.newPage()
                    self.paintColumnHeader(self, painter, rect, fieldNames)
                    y = self.headerY
                else:
                    break
                
        #Print totals
        if not totals:
            return
        painter.save()
        font = painter.font()
        font.setPointSize(10)
        font.setBold(True)
        painter.setFont(font)
        # paint totals
        for col in totals:
            x = col[0] + (size * col[1]) + size
            amount = '{:,.2f}'.format(col[2])
            painter.drawText(x, y + size, amount)
        # paint a line above
        pen = QPen(Qt.black, 1, Qt.SolidLine)
        painter.setPen(pen)
        y += (size *.25)
        painter.drawLine(size, y, self.width(), y)
        
        # and a double line beneath
        y += size + (size *.4)
        painter.drawLine(size, y, self.width(), y)
        
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        painter.setPen(pen)
        y += (size * .1)
        painter.drawLine(size, y, self.width(), y)
        painter.restore()
        
        self.Y = y
        
   
    def mouseDoubleClickEvent(self, event):
        self.double_clicked = True
        self.selectedRow = (event.y() - (self.headerY)) // self.fontSize
        self.update()
        self.emit(SIGNAL('doubleClicked(QModelIndex)'), self.model.index(self.selectedRow, 0))             
    
    def mousePressEvent(self, event):
        size = self.fontSize
        self.selectedRow = (event.y() - (self.headerY)) // size
        self.update()
        self.emit(SIGNAL("clicked(QModelIndex)"), self.model.index(self.selectedRow, 0))
        
        
    def keyPressEvent(self, event):
        if not self.model:
            return
        row = - 1
        if event.key() == Qt.Key_Up:
            row = max(0, self.selectedRow - 1)
        elif event.key() == Qt.Key_Down:
            row = min(self.selectedRow + 1, self.model.rowCount() - 1)
        if row != -1 and row != self.selectedRow:
            self.selectedRow = row
            if self.scrollarea:
                fm = QFontMetrics(self.font())
                y = fm.height() * self.selectedRow
                self.scrollarea.ensureVisible(0, y)
            self.update()
            self.emit(SIGNAL('clicked(QModelIndex)'), self.model.index(self.selectedRow, 0))
        else:
            QWidget.keyPressEvent(self, event)
            
           
#======================================================================
### setup the dialog to show the user how well i could paint.    
class ReportForm(QDialog):
    
    def __init__(self, model, parent=None, report=None, modify=False):
        super(ReportForm, self).__init__(parent)
        
        self.my_parent = parent
        self.report_name = report
        self.model = model
        self.view = ReportView()
        self.view.setModel(self.model)
        
        scrollArea = QScrollArea()
        scrollArea.setBackgroundRole(QPalette.Light)
        scrollArea.setWidget(self.view)
        self.view.scrollarea = scrollArea
        
        refreshButton = QPushButton('Refresh')
        modifyButton = QPushButton('Modify')
        if modify == False:
            modifyButton.setVisible(False)
        printButton = QPushButton('Print')
        exportButton = QPushButton('Export')
        self.sortCombobox = QComboBox()
        self.sortCombobox.addItems(self.model.mainColumnNames())
        self.sortButton = QPushButton('ASC')
        
        spacer = QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(modifyButton)
        buttonLayout.addWidget(refreshButton)
        buttonLayout.addItem(spacer)
        buttonLayout.addWidget(printButton)
        buttonLayout.addWidget(exportButton)
        buttonLayout.addWidget(self.sortCombobox)
        buttonLayout.addWidget(self.sortButton)
        
        
        layout = QVBoxLayout()
        layout.addLayout(buttonLayout)
        layout.addWidget(scrollArea)
        self.setLayout(layout)
        self.setWindowTitle(model.reportName)
        self.setWindowIcon(QIcon(':/icons/report'))
        
        modifyButton.clicked.connect(self.modify)
        refreshButton.clicked.connect(self.refresh)
        printButton.clicked.connect(self.printForm)
        exportButton.clicked.connect(self.export)
        self.sortCombobox.currentIndexChanged.connect(self.sort)
        self.sortButton.clicked.connect(self.sortOrder)
        self.connect(self.view, SIGNAL('doubleClicked(QModelIndex)'), self.editTransaction)
    
    
    def reject(self):
        QDialog.reject(self)
        self.my_parent.formClosed()
        
    def printForm(self):
        self.view.printReport()
    
    def export(self):
        self.model.export()
    
    def modify(self):
        self.my_parent.reportSettings(self.report_name, self)
        
    def refresh(self):
        self.my_parent.refreshReport(self.model, self.report_name)
        self.view.setModel(self.model)
    
    def editTransaction(self, index):
        row = index.row()
        bomId = self.model.data(index).toInt()[0]
        if self.report_name == 'inv_sum':
            self.my_parent.inventoryDetReport(bomId)
        elif self.report_name in ('trans_header_report', 'trans_detail_report'):
            jt_index = self.model.index(row, 1)
            journal_type = self.model.data(jt_index).toString()
            journal_id = self.model.data(index).toInt()[0]
    
            if journal_type in ('Bill', 'Credit'):
                jType = 0
            elif journal_type == 'Production':
                jType = 2
            elif journal_type == 'Adjustment':
                jType = 3
            
            if jType in (0, 2, 3):
                self.my_parent.editTransaction(jType, journal_id)
        
        elif self.report_name in ('raw_material', 'finished_good'):
            
            if self.report_name == 'raw_material':
                itemType = 0
            elif self.report_name == 'finished_good':
                itemType = 1

            if itemType in (0, 1):
                self.my_parent.editTransaction(itemType, bomId)
            
        
    
    def sortOrder(self):
        if self.sortButton.text() == 'ASC':
            text = 'DSC' 
            descending = True
        elif self.sortButton.text() == 'DSC':
            text = 'ASC'
            descending = False
        self.sortButton.setText(text)
        self.sort(descending)
        
    def sort(self, descending = False):
        keyText = str(self.sortCombobox.currentText())
        self.model.sortMain(keyText, descending)
        self.view.update()
        

        

if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    setupDatabase("Production.sqlite")
    
    model = ReportModel()   
    form = ReportForm(model)
    form.show()
    
    app.exec_()

 


        
        
        