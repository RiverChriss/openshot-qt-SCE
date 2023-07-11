import sys

try:
    #Path when import for project Openshot
    from SCE.EventsWidget.ui_eventswidget import Ui_EventsWidget # I use this include to test Openshot vs Qt creator
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
except ImportError:
    #Path when import for QtCreator (laungh this project)
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    from PySide6.QtCore import *

class ShortcutManager():

    def __init__(self, parent):
        self.parent = parent
        self.shortcuts = []

    def add(self, index):
        self.shortcuts.insert(index, QShortcut(self.parent))

    def remove(self, index):
        self.shortcuts[index].setKey('')
        try:
            self.shortcuts[index].activated.disconnect()
        except:
            print(end="")
        finally:
            del self.shortcuts[index]

    def update(self, row):
        if row == -1 :
            raise ValueError("value -1 can't be pass to update")
        data = self.parent.getDataTable()[row]
        self.shortcuts[row].setKey(data[3])
        try:
            self.shortcuts[row].activated.disconnect()
        except:
            print(end="")
        finally:
            self.shortcuts[row].activated.connect(lambda : self.test([data[0], data[1], data[2]], data[3], data[4], data[5]))


    def test(self, color, shortcut, category, description):
        print(f"{color}")
        print(f"{shortcut}")
        print(f"{category}")
        print(f"{description}")