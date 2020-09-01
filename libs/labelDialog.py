try:
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
except ImportError:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

from libs.utils import newIcon, labelValidator
from libs.utils import *

import functools

BB = QDialogButtonBox


class LabelDialog(QDialog):

    def on_open(self):
        print('Ctrl L has been fired')
        self.listWidget.setCurrentRow(1)
        self.listItemDoubleClick(self.listWidget.currentItem())

    def on_open2(self):
        print('Ctrl L2 has been fired')
        self.listWidget.setCurrentRow(2)
        self.listItemDoubleClick(self.listWidget.currentItem())

    # def my_open()

    def myAction(self):
        print("\n\n myACTION ==== \n ")
        self.listWidget.setCurrentRow(2)

    def create_label_shortcut(self, hotkey, row):
        from functools import partial
        def callback(obj):
            def select(self):
                self.listWidget.setCurrentRow(row)
                self.listItemDoubleClick(self.listWidget.currentItem())

            obj.shortcut_open = QShortcut(QKeySequence(hotkey), obj)
            obj.shortcut_open.activated.connect(select)

        setattr(self, "hotkey_%s" % hotkey, callback)
        
    @pyqtSlot(str)  #https://stackoverflow.com/questions/23116763/pyqt-how-to-connect-qcombobox-to-function-with-arguments/23117187
    def simple_print(self):
        print("a hotk ey 2" )

    @pyqtSlot(str) #https://stackoverflow.com/questions/23116763/pyqt-how-to-connect-qcombobox-to-function-with-arguments/23117187
    def simple_print2(self, arh):
        print("a hotk ey 2" )
        print(arh)

    def on_button(self, n):
        print('Button {0} clicked'.format(n))

    def __init__(self, text="Enter object label[][]", parent=None, listItem=None):
        super(LabelDialog, self).__init__(parent)

        #self.create_label_shortcut('Ctrl+U', 3)
        # myAction = newAction(self, 'myaction', self.myAction,
        #               'x', 'eye', 'myaya')
        # self.menu = QMenu()
        # self.menu.addAction(myAction)
        if listItem is not None and len(listItem) > 0:
            for idx, l in enumerate(listItem):
                if(idx < 9):

                    qshort = QShortcut(QKeySequence("Ctrl+" + str(idx+1)), self)
                    setattr(self, "hotkey_%s" % (idx+1), qshort)

                    #myFunc = functools.partialmethod(self.simple_print, typeC=str(idx+1))
                    slotLambda = lambda: self.simple_print

                    attr = getattr(self, "hotkey_%s" % (idx+1))
                    #attr.activated.connect(self.simple_print2, "HJ")
                    attr.activated.connect(functools.partial(self.on_button, (idx+1)))

        
        self.shortcut_open = QShortcut(QKeySequence('1'), self)
        self.shortcut_open.activated.connect(self.on_open)

        self.shortcut_open2 = QShortcut(QKeySequence('s'), self)
        self.shortcut_open2.activated.connect(self.on_open2)

        self.edit = QLineEdit()
        self.edit.setText(text)
        self.edit.setValidator(labelValidator())
        self.edit.editingFinished.connect(self.postProcess)
        self.edit.textChanged.connect(self.textChanged)

        model = QStringListModel()
        model.setStringList(listItem)
        completer = QCompleter()
        completer.setModel(model)
        self.edit.setCompleter(completer)

        layout = QVBoxLayout()
        layout.addWidget(self.edit)
        self.buttonBox = bb = BB(BB.Ok | BB.Cancel, Qt.Horizontal, self)
        bb.button(BB.Ok).setIcon(newIcon('done'))
        bb.button(BB.Cancel).setIcon(newIcon('undo'))
        bb.accepted.connect(self.validate)
        bb.rejected.connect(self.reject)
        layout.addWidget(bb)

        if listItem is not None and len(listItem) > 0:
            self.listWidget = QListWidget(self)
            for item in listItem:
                self.listWidget.addItem(item)
            self.listWidget.itemClicked.connect(self.listItemClick)
            self.listWidget.itemDoubleClicked.connect(self.listItemDoubleClick)
            layout.addWidget(self.listWidget)

        self.setLayout(layout)

    ## quick hack
    def textChanged(self, text):
        print("text changed to" + str(text))

        for i in range(1,10):
            if str(i) in text:
                print("select row" + str(i-1))
                self.listWidget.setCurrentRow(i-1)
                self.listItemClick(self.listWidget.currentItem())
                self.validate()
                break
                #self.listItemDoubleClick(self.listWidget.currentItem())

    def validate(self):
        try:
            if self.edit.text().trimmed():
                self.accept()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            if self.edit.text().strip():
                self.accept()

    def postProcess(self):
        print("post process")
        try:
            self.edit.setText(self.edit.text().trimmed())
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            self.edit.setText(self.edit.text())

    def popUp(self, text='', move=True):
        print("labelDialog popup================")
        self.edit.setText(text)
        self.edit.setSelection(0, len(text))
        self.edit.setFocus(Qt.PopupFocusReason)
        if move:
            self.move(QCursor.pos())
        return self.edit.text() if self.exec_() else None

    def listItemClick(self, tQListWidgetItem):
        try:
            text = tQListWidgetItem.text().trimmed()
        except AttributeError:
            # PyQt5: AttributeError: 'str' object has no attribute 'trimmed'
            text = tQListWidgetItem.text().strip()
        self.edit.setText(text)

    def listItemDoubleClick(self, tQListWidgetItem):
        self.listItemClick(tQListWidgetItem)
        self.validate()
