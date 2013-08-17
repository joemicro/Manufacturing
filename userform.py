import os
import sys
import ntpath
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from sqlalchemy import  *
import sqlalchemy.exc as exc
from sqlalchemy.orm import *
from databaseschema import *
from functions import *
import modelsandviews


localTITLE = "User Login"


class UserForm(QDialog):
    
    
    
    def __init__(self, model, formType=0, filename=None, parent=None):
        super(UserForm, self).__init__(parent)
        
        self.setWindowTitle(localTITLE)
        self.formType = formType
        self.myParent = parent
        self.dirty = False
        self.editing = False
        self.session = Session()
        self.current_record = None
        self.record_id = None
        self.filename = filename
        
        self.model = model
        self.label_3 = QLabel("Recall User")
        self.view = modelsandviews.UserView(self.model)
        self.recall_user = modelsandviews.UserComboBox(self.model)
        self.label_3.setBuddy(self.recall_user)
        label_1 = QLabel("Name")
        self.user_lineEdit = QLineEdit()
        label_1.setBuddy(self.user_lineEdit)
        label_2 = QLabel("Password")
        self.password = QLineEdit()
        self.password.setEchoMode(QLineEdit.Password)
        label_2.setBuddy(self.password)
        frame = QFrame()
        self.fileName_label = QLabel(frame)
        hLine = QFrame()
        hLine.setFrameShape(QFrame.HLine)
        hLine.setFrameShadow(QFrame.Sunken)
        
        self.save_button = QPushButton("&Save New")
        self.delete_button = QPushButton("&Delete")
        self.close_button = QPushButton("C&lose")
        
        
        self.delete_button.setIcon(QIcon(':/icons/delete'))
        self.close_button.setIcon(QIcon(':/icons/exit'))
        self.setWindowIcon(QIcon(':/icons/login'))
        
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.save_button)
        buttonLayout.addWidget(self.delete_button)
        buttonLayout.addWidget(self.close_button)
        buttonLayout.setContentsMargins(11, 25, 11, 11)
        fieldlayout = QGridLayout()
        fieldlayout.addWidget(self.label_3, 0, 0, 1, 1)
        fieldlayout.addWidget(self.recall_user, 0, 1 ,1 ,3)
        fieldlayout.addWidget(self.fileName_label, 0, 1 ,1 ,3)
        fieldlayout.addWidget(frame, 1, 1, 1, 3)
        fieldlayout.addWidget(label_1, 2, 0,1 ,1)
        fieldlayout.addWidget(self.user_lineEdit, 2, 1, 1, 3)
        fieldlayout.addWidget(label_2, 3, 0, 1, 1)
        fieldlayout.addWidget(self.password, 3, 1, 1, 3)
        layout = QVBoxLayout()
        layout.addLayout(fieldlayout)
        layout.addWidget(hLine)
        layout.addLayout(buttonLayout)
        self.setLayout(layout)
        
        if formType == 0:
            self.fileName_label.setVisible(False)
            self.label_3.setVisible(True)
            self.recall_user.setVisible(True)
            self.save_button.setText('&Save New')
            self.save_button.setIcon(QIcon(':/icons/save'))
            self.delete_button.setVisible(True)
            self.localTITLE = 'User Setup'
        elif formType == 1:
            self.fileName_label.setVisible(True)
            self.fileName_label.setText('File: %s' % self.filename)
            self.label_3.setVisible(False)
            self.recall_user.setVisible(False)
            self.save_button.setText('Log In')
            self.save_button.setIcon(QIcon(':/icons/login'))
            self.delete_button.setVisible(False)
            self.localTITLE = 'User LogIn'
        
        self.connect(self.save_button, SIGNAL("clicked()"), self.save)
        self.connect(self.close_button, SIGNAL("clicked()"),lambda: self.accept(False))
        self.connect(self.delete_button, SIGNAL("clicked()"), self.delete)
        self.connect(self.recall_user, SIGNAL("activated(int)"), self.recall)
        self.connect(self.password, SIGNAL("textEdited(QString)"), self.dataChanged)
        self.connect(self.user_lineEdit, SIGNAL("textEdited(QString)"), self.dataChanged)
        self.connect(self.recall_user, SIGNAL("keyPressEvent(QKeyEvent*)"), self.verify)
    
        
    def verify(self):
        text = self.recall_user.currentText()
        index = self.recall_user.findText(text)
        if index == -1:
            print "index not valid"
    
    
    def dataChanged(self):
        """ set form to dirty, as soon as some data is changed"""
        if self.formType == 0:
            self.dirty = True
            self.setWindowTitle("%s - Editing..." % self.localTITLE)
        
    
    def login(self):
        if not self.filename:
            QMessageBox.information(self, 'Log In', 'Please open a production file first.', QMessageBox.Ok)
            return
        user_name = str(self.user_lineEdit.text())
        user = dLookup(Users.user_id, Users.user_name.ilike(user_name))
        if not user:
            QMessageBox.information(self, 'Log In', 'User not found', QMessageBox.Ok)
            return
        password = dLookup(Users.password, Users.user_id==user)
        supplied_pass = str(self.password.text())
        if not password == supplied_pass:
            QMessageBox.information(self, 'Log In', 'Incorrect password', QMessageBox.Ok)
            return
        self.accept(True, user)
    
    
    def reject(self):
        self.accept(False)
    
    
    def accept(self, go, user=0):
        """ close form, and save changes"""
        if self.dirty:
            answer = QMessageBox.question(self, "Editing - %s" % self.localTITLE, "Would you like to save your data?",
                                 QMessageBox.Yes| QMessageBox.No| QMessageBox.Cancel)
            if answer == QMessageBox.Cancel:
                return
            elif answer == QMessageBox.No:
                QDialog.accept(self)
            elif answer == QMessageBox.Yes:
                self.save()
        self.myParent.setGoAhead(go, user)
        QDialog.accept(self)
        

    def save(self):
        """ save record, or clear form if no data has been modified"""
        if self.save_button.text() == 'Log In':
            self.login()
            return
        if not self.dirty:
            self.clear()
            return
        # if data was edited, save information
        user_name = str(self.user_lineEdit.text())
        password = str(self.password.text())
        if not user_name:
            QMessageBox.information(self, "Save - %s" % self.localTITLE, "Please sepcify a user name before saving",
                                    QMessageBox.Ok)
            return
        if self.editing:
            self.current_record.update({'user_name': user_name, 'password': password})
        else:
            # check if supplier already exists.
            user = dLookup(Users.user_name, Users.user_name==user_name)
            if user:
                QMessageBox.information(self, 'Save - %s' % self.localTITLE, 'User already exists in list', QMessageBox.Ok)
                return
            self.session.add(Users(user_name, password))
        exception = None
        try:
            self.session.flush()
        except ValueError, e:
            exception = e
            self.session.rollback()
        finally:
            self.session.commit()
            if exception is not None:
                raise exception
        self.clear()
        
        
    def recall(self, row):
        """ recall record """
        # // first find out if the user is in middle of entering data.
        if self.dirty:
            answer = QMessageBox.question(self, "Editing - %s" % localTITLE, "Would you like to save your data?",
                                 QMessageBox.Yes| QMessageBox.Discard| QMessageBox.Cancel)
            if answer == QMessageBox.Cancel:
                return
            elif answer == QMessageBox.Yes:
                self.save()
                
        i_index = self.model.index(row, 0)
        record = self.model.data(i_index).toString()
        if not record:
            self.clear()
            return
        record = str(record)
        self.current_record = self.session.query(Users).filter_by(user_id=record)
        for user in self.current_record :
            self.user_lineEdit.setText(user.user_name)
            self.password.setText(user.password)
            self.record_id = user.user_id
        self.editing = True
    
    
    def delete(self):
        if self.record_id:
            used = dLookup(Logs.user_id, Logs.user_id==self.record_id)
            if used:
                QMessageBox.information(self, "Delete - %s" % self.localTITLE, "Can't delete user," \
                                            "because it was already used elsewhere", QMessageBox.Ok)
                return
            answer = QMessageBox.question(self, "Delete - %s" % localTITLE, "Are you sure you " \
                                          "want to delete user: %s" % self.user_lineEdit.text(), 
                                          QMessageBox.Yes| QMessageBox.No, QMessageBox.NoButton)
            if answer == QMessageBox.No:
                return
            self.current_record.delete()
            exception = None
            try:
                self.session.flush()
            except ValueError, e:
                exception = e
                self.session.rollback()
            finally:
                self.session.commit()
                if exception is not None:
                    raise exception
            self.clear()
            
    
    def clear(self):
        self.view.resize()
        self.model.select()
        for widget in self.children():
            if isinstance(widget, (QLineEdit, QTextEdit)):
                widget.clear()
            elif isinstance(widget, QComboBox):
                widget.setCurrentIndex(-1)
            elif isinstance(widget, QCheckBox):
                widget.setChecked(False)
        self.user_lineEdit.setFocus()
        self.dirty = False
        self.editing = False   
        
        self.setWindowTitle(self.localTITLE)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    setupDatabase("Production.sqlite")
    model = modelsandviews.SupplierModel()
    form = UserForm()
    form.resize(200, 200)
    form.show()
    app.exec_()