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

class FunctorShortcut():
    def __init__(self) -> None:
        self.rgb = ['', '', '']
        self.shortcut = ""
        self.category = ""
        self.description = ""

    def __call__(self) -> None:
        print(f"{self.rgb}")
        print(f"{self.shortcut}")
        print(f"{self.category}")
        print(f"{self.description}")
    

class ShortcutManager():

    def __init__(self, parent):
        self.parent = parent
        self.shortcuts = []
        self.functors = []

    def add(self, row):
        self.shortcuts.insert(row, QShortcut(self.parent))
        self.functors.insert(row, FunctorShortcut())
        self.shortcuts[row].activated.connect(self.functors[row])

    def remove(self, row):
        self.shortcuts[row].setKey('')
        try:
            self.shortcuts[row].activated.disconnect()
        except:
            print(end="")
        finally:
            del self.shortcuts[row]
        del self.functors[row]

    def update(self, row):
        data = self.parent.getDataRow(row)
        self.shortcuts[row].setKey(data[3])
        
        self.functors[row].rgb[0] = data[0]
        self.functors[row].rgb[1] = data[1]
        self.functors[row].rgb[2] = data[2]
        self.functors[row].shortcut = data[3]
        self.functors[row].category = data[4]
        self.functors[row].description = data[5]