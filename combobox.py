import sys
try:
    from PyQt5.QtWidgets import QWidget, QHBoxLayout, QComboBox
except ImportError:
    # needed for py3+qt4
    # Ref:
    # http://pyqt.sourceforge.net/Docs/PyQt4/incompatible_apis.html
    # http://stackoverflow.com/questions/21217399/pyqt4-qtcore-qvariant-object-instead-of-a-string
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtGui import QWidget, QHBoxLayout, QComboBox


class ComboBox(QWidget):
    def __init__(self, parent=None, items=[]):
        super(ComboBox, self).__init__(parent)

        layout = QHBoxLayout()
        self.cb = QComboBox()
        self.items = items
        self.cb.addItems(self.items)

        self.cb.currentIndexChanged.connect(parent.comboSelectionChanged)

        layout.addWidget(self.cb)
        self.setLayout(layout)

        self.lockedLabel = None

        self.foundLock = False

    def update_items(self, items, locked=False):
        self.items = items
        print("[combobox] updating items...")

        if not locked:
            self.cb.clear()
        self.cb.addItems(self.items)

        self.foundLock = False
        if (self.lockedLabel != None
            and self.lockedLabel in items):
          
            print("[combobox] item matches lockedLabel:  settting...")
            self.cb.setCurrentText(self.lockedLabel)

            self.foundLock = True
        