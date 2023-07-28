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
    def __init__(self, shortcutManager) -> None:
        # Variable logic
        self.shortcutManager = shortcutManager
        self.compteurClick = 0

        # Data Store
        self.message = Message()

    def __call__(self) -> None:
        if (self.compteurClick % 2) == 0 :
            # Fist click
            self.message.timeBegin = self.shortcutManager.getCurrentTime()
            self.compteurClick += 1
            print(f"La touche {self.message.shortcut} a été cliquer 1 seule fois à {self.message.timeBegin}")
            return
        
        # Second click
        self.message.timeEnd = self.shortcutManager.getCurrentTime()
        self.compteurClick = 0

        if self.message.timeBegin > self.message.timeEnd :
            self.message.timeBegin, self.message.timeEnd = self.message.timeEnd, self.message.timeBegin

        self.shortcutManager.eventSignal.emit(self.message)
        

        
class ShortcutManager(QObject):
    try:
        eventSignal = pyqtSignal(Message) # if PyQt5 (Openshot use case)
    except:
        eventSignal = Signal(Message) # if PySide6 (Qtcreator use case)

    def __init__(self, eventsManager, tableWidget, columnItemUserShortcut):
        super().__init__(eventsManager)
        self.eventsManager =eventsManager
        self.tableWidget = tableWidget
        self.columnItemUserShortcut = columnItemUserShortcut

    def addItemShortcut(self, row, name="") -> None :
        self.tableWidget.setItem(row, self.columnItemUserShortcut, ItemShortcut(self, name))

    def removeShortcutKey(self, row) -> None :
        itemUserShortcut = self.tableWidget.item(row, self.columnItemUserShortcut)
        if itemUserShortcut :
            itemUserShortcut.removeShortcutKey()

    def updateFunctor(self, row) -> None :
        itemUserShortcut = self.tableWidget.item(row, self.columnItemUserShortcut)
        if itemUserShortcut :
            [red, green, blue, shortcut, category, description] = self.eventsManager.getDataRow(row)
            itemUserShortcut.update([red, green, blue], shortcut, category, description)

    def getCurrentTime(self) -> float:
        return self.eventsManager.getCurrentTime()



class ItemShortcut(QTableWidgetItem):
    def __init__(self, shortcutManager, name="") -> None:
        super().__init__(name)
        self.shortcutManager = shortcutManager

        # Format
        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.shortcut = QShortcut(self.shortcutManager.eventsManager)
        self.functor = FunctorShortcut(shortcutManager)
        self.shortcut.activated.connect(self.functor)
    
    def removeShortcutKey(self) -> None:
        self.shortcut.setKey('')
        try:
            self.shortcut.activated.disconnect()
        except:
            print(end="")

    def update(self, rgb, shortcut, category, description) -> None:
        self.shortcut.setKey(shortcut)
        
        self.functor.message.rgb[0] = rgb[0]
        self.functor.message.rgb[1] = rgb[1]
        self.functor.message.rgb[2] = rgb[2]
        self.functor.message.shortcut = shortcut
        self.functor.message.category = category
        self.functor.message.description = description