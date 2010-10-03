#! /usr/bin/python
# coding=utf-8
'''
    PyPassword Generator - a programm that can help you to generate a secure passwords
    Copyright (C) 2010  Igor Melnikov

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from random import randint
from PyQt4.QtCore import SIGNAL, Qt
from PyQt4.QtGui import QDialog, QApplication, QCheckBox
from main_dialog import Ui_Dialog as Ui_MainDialog
from about_dialog import Ui_Dialog as Ui_AboutDialog
 
class PwdGenerator(QDialog):
    ''' Main class '''    
    def __init__(self, parent=None):
        super(PwdGenerator, self).__init__(parent)
        self.dialog = Ui_MainDialog()
        self.dialog.setupUi(self)
        self.connectSlots()
    
    def connectSlots(self):
        self.connect(self.dialog.btn_GenNewPwd, SIGNAL("clicked()"), self.btn_GenNewPwd_cb)
        self.connect(self.dialog.btn_About, SIGNAL("clicked()"), self.btn_About_cb)
        
    def generate_abc(self):
        '''Returns a list of available characters selected by user'''
        abc = []
        
        if self.dialog.chbox_use_digits.checkState() == Qt.Checked:
            abc.extend(map(str, range(0,10)))

        if self.dialog.chbox_use_letters.checkState() == Qt.Checked:
            abc.extend(map(chr, range(97, 123)))
            abc.extend(map(chr, range(65, 91)))
        
        qcheckbox_class_name = type(QCheckBox()).__name__
        
        if (self.dialog.chbox_use_symbols.checkState() == Qt.Checked):
            
            for check_box in self.dialog.groupBox_Symbols.children():
            
                if type(check_box).__name__ == qcheckbox_class_name:
                
                    if check_box.checkState() == Qt.Checked:
                    
                        if check_box.text() == 'space':
                            abc.append(' ')
                        elif check_box.text() == "\\":
                            abc.append('\\')
                        elif check_box.text() == "&&":
                            abc.append("&")
                        else:
                            abc.append(str(check_box.text()))
        return abc
    
    def btn_About_cb(self):
        dialog = AboutDialog()
        dialog.exec_()
        
    def btn_GenNewPwd_cb(self):
        '''Generate random password'''
        abc = self.generate_abc()
        abc_len = len(abc)
        pwd = ""
        pwd_len = int(self.dialog.spinbox_char_num.text())
        
        if abc_len < 1:
            return
        
        for i in xrange(pwd_len):
            pwd += str(abc[randint(0, abc_len-1)])
        
        self.dialog.inp_Pwd.setText(pwd)

class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)
        self.ui = Ui_AboutDialog()
        self.ui.setupUi(self)
    
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    pwgen = PwdGenerator()
    pwgen.show()
    app.exec_()