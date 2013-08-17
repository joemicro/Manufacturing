from PyQt4.QtCore import *
from PyQt4.QtGui import *
from math import *
import sys
import modelsandviews

class NumberLineEdit(QLineEdit):
    
    def __init__(self, parent=None):
        super(NumberLineEdit, self).__init__(parent)
        self.editingFinished.connect(self.validate)
        
    def validate(self):
        text = unicode(self.text())
        try:
            text = eval(text)
            self.setText(str(text))
        except ValueError, e:
            self.setText("")
            

class GenericDelegate(QItemDelegate):
    
    def __init__(self, parent=None):
        super(GenericDelegate, self).__init__(parent)
        self.delegates = {}
        
    def insertDelegate(self, column, delegate):
        delegate.setParent(self)
        self.delegates[column] = delegate
        
    def removeDelegate(self, column):
        if column in self.delegates:
            del self.delegates[column]
    
    def paint(self, painter, option, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.paint(painter, option, index)
        else:
            QItemDelegate.paint(self, painter, option, index)
            
    def createEditor(self, parent, option, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            return delegate.createEditor(parent, option, index)
        else:
            return QItemDelegate.createEditor(self, parent, option, index)
        
    def setEditorData(self, editor, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setEditorData(editor, index)
        else:
            QItemDelegate.setEditorData(self, editor, index)
            
    def setModelData(self, editor, model, index):
        delegate = self.delegates.get(index.column())
        if delegate is not None:
            delegate.setModelData(editor, model, index)
        else:
            QItemDelegate.setModelData(self, editor, model, index)
            
class NumberDelegate(QItemDelegate):
    
    def __init__(self, parent=None):
        super(NumberDelegate, self).__init__(parent)
    
        
    def createEditor(self, parent, option, index):
        lineedit = modelsandviews.MyLineEdit(parent)
        return lineedit
    
    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toString()
        editor.setText(value)
    
    def setModelData(self, editor, model, index):
        text = unicode(editor.text())
        if not text:
            return
        try:
            model.setData(index, QVariant(eval(text)))
        except ValueError, e:
            print ("err:", e, text, type(text), "Wrong Format")
            return False
            

class PlainTextDelegate(QItemDelegate):
    
    def __init__(self, parent=None):
        super(PlainTextDelegate, self).__init__(parent)
        
    def createEditor(self, parent, option, index):
        lineedit = modelsandviews.MyLineEdit(parent)
        return lineedit
    
    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.DisplayRole).toString()
        editor.setText(value)
        
    
    def setModelData(self, editor, model, index):
        try:
            text = editor.text()
            model.setData(index, QVariant(text))
        except:
            return False
        
        
class ComboDelegate(QItemDelegate):
    """ creates a combo delegate for tableView,
    Takes in 'model', the model from where the combo box should take data
    Takes in 'hide' default is True, a boolean variable, True if you want the first column
    in the view to be hidden, equally for the modelColumn setting, True will set column 1 as model
    instead of column 0 """
    
    def __init__(self, model, hide=True, parent=None):
        super(ComboDelegate, self).__init__(parent)
        self.__model = model
        self.__hide = hide
    
    def createEditor(self, parent, option, index):

        view = modelsandviews.ItemView(self.__model, self.__hide)
        self.combobox = modelsandviews.ItemComboBox(parent)
#        self.combobox = QComboBox(parent)
        self.combobox.setModel(self.__model)
        self.combobox.setView(view)
        self.combobox.setModelColumn(0)
        if self.__hide:
            self.combobox.setModelColumn(1)
        self.combobox.setCurrentIndex(-1)
        self.combobox.setEditable(True)
        self.combobox.setInsertPolicy(QComboBox.NoInsert)
        self.combobox.view().setFixedWidth(300)
        return self.combobox
    
    def setEditorData(self, editor, index):
#        i = index.sibling(index.row(), 0) ///////// left this for coding reference /////////
#        text = i.model().data(i, Qt.DisplayRole).toString()
        text = index.model().data(index, Qt.DisplayRole).toString()
        indexOfText = editor.findText(text, Qt.MatchRegExp)
        editor.setCurrentIndex(indexOfText)
        
    def setModelData(self, editor, model, index):
        # i only want to set text, if text is in the list, so look for the text that was typed in the comboBox
        text = editor.currentText()
        indexOfText = editor.findText(text, Qt.MatchRegExp)
        if indexOfText == -1: # if no text was find, (if no text was found result is -1
            return
        editor.setCurrentIndex(indexOfText) # else set comboBox to index of found text
        # once the editor the item in the comboBox is properly selected, lets set info to model
        row = editor.currentIndex()
        i = self.__model.index(row, 0)
        indexOfValue, ok = self.__model.data(i).toInt()
        if ok:
            model.setData(index, QVariant(indexOfValue), Qt.EditRole)
#        model.setData(index, QVariant(editor.itemText(i)), Qt.EditRole)
        

    