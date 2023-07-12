import sys

try:
    #Path when import for project Openshot
    from SCE.EventsWidget.ui_eventswidget import Ui_EventsWidget # I use this include to test Openshot vs Qtcreator
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
except ImportError:
    #Path when import for QtCreator (laungh this project)
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    from PySide6.QtCore import *

class Message():
    def __init__(self) -> None:
        self.rgb = ['', '', '']     # [R, G, B]
        self.shortcut = ""
        self.category = ""
        self.description = ""
        self.timeBegin = 0.0
        self.timeEnd = 0.0


class FunctorShortcut():
    def __init__(self, parent) -> None:
        # Variable logic
        self.parent = parent
        self.compteurClick = 0

        # Data Store
        self.message = Message()

    def __call__(self) -> None:
        if (self.compteurClick % 2) == 0 :
            # Fist click
            self.message.timeBegin = self.parent.getCurrentTime()
            self.compteurClick += 1
            print(f"La touche {self.message.shortcut} a été cliquer 1 seule fois à {self.message.timeBegin}")
            return
        
        # Second click
        self.message.timeEnd = self.parent.getCurrentTime()
        self.compteurClick = 0

        if self.message.timeBegin > self.message.timeEnd :
            self.message.timeBegin, self.message.timeEnd = self.message.timeEnd, self.message.timeBegin

        self.parent.eventSignal.emit(self.message)
        
    

class ShortcutManager(QObject):
    try:
        eventSignal = pyqtSignal(Message) # if PyQt5 (Openshot use case)
    except:
        eventSignal = Signal(Message) # if PySide6 (Qtcreator use case)

    def __init__(self, parent) -> None:
        super().__init__(parent)

        self.parent = parent
        self.shortcuts = []
        self.functors = []

    def add(self, row) -> None:
        self.shortcuts.insert(row, QShortcut(self.parent))
        self.functors.insert(row, FunctorShortcut(self))
        self.shortcuts[row].activated.connect(self.functors[row])

    def remove(self, row) -> None:
        self.shortcuts[row].setKey('')
        try:
            self.shortcuts[row].activated.disconnect()
        except:
            print(end="")
        finally:
            del self.shortcuts[row]
        del self.functors[row]

    def update(self, row) -> None:
        data = self.parent.getDataRow(row)
        self.shortcuts[row].setKey(data[3])
        
        self.functors[row].message.rgb[0] = data[0]
        self.functors[row].message.rgb[1] = data[1]
        self.functors[row].message.rgb[2] = data[2]
        self.functors[row].message.shortcut = data[3]
        self.functors[row].message.category = data[4]
        self.functors[row].message.description = data[5]

    def getCurrentTime(self) -> float:
        return self.parent.getCurrentTime()