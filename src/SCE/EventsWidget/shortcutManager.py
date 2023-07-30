import re

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class Message():
    def __init__(self) -> None:
        self.colorHex = ""
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
    eventSignal = pyqtSignal(Message)

    def __init__(self, eventsManager, tableWidget, columnShortcut):
        super().__init__(eventsManager)
        self.eventsManager =eventsManager
        self.tableWidget = tableWidget
        self.columnShortcut = columnShortcut

    def addItemShortcut(self, row, name="") -> None :
        self.tableWidget.setItem(row, self.columnShortcut, ItemShortcut(self, name))

    def removeShortcutKey(self, row) -> None :
        itemShortcut = self.tableWidget.item(row, self.columnShortcut)
        if itemShortcut :
            itemShortcut.removeShortcutKey()

    def updateFunctor(self, row) -> None :
        itemShortcut = self.tableWidget.item(row, self.columnShortcut)
        if itemShortcut :
            [color, shortcut, category, description] = self.eventsManager.getDataRow(row)
            itemShortcut.update(color, shortcut, category, description)

    def getCurrentTime(self) -> float:
        return self.eventsManager.getCurrentTime()

    def verifyShortcutAlreadyUse(self, name, skipRow = -1) -> bool:
        if name == "" :
            return False
        for i in range(self.tableWidget.rowCount()) :
            if i == skipRow :
                continue
            if self.tableWidget.item(i, self.columnShortcut).text() == name :
                return True
        return False
    
    def verifyShortcutForm(self, name) -> bool :
        if name == "" :
            return True
        if re.fullmatch(r"(CTRL\+)?(SHIFT\+)?(ALT\+)?([A-Z]|[0-9])", name) == None and \
            re.fullmatch(r"(CTRL\+)?(ALT\+)?(SHIFT\+)?([A-Z]|[0-9])", name) == None and \
            re.fullmatch(r"(SHIFT\+)?(CTRL\+)?(ALT\+)?([A-Z]|[0-9])", name) == None and \
            re.fullmatch(r"(SHIFT\+)?(ALT\+)?(CTRL\+)?([A-Z]|[0-9])", name) == None and \
            re.fullmatch(r"(ALT\+)?(CTRL\+)?(SHIFT\+)?([A-Z]|[0-9])", name) == None and \
            re.fullmatch(r"(ALT\+)?(SHIFT\+)?(CTRL\+)?([A-Z]|[0-9])", name) == None :
            return False
        return True

class ItemShortcut(QTableWidgetItem):
    def __init__(self, shortcutManager, name = "") -> None:
        super().__init__(name.upper())
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

    def update(self, colorHex, shortcut, category, description) -> None:
        self.shortcut.setKey(shortcut)
        
        self.functor.message.colorHex = colorHex
        self.functor.message.shortcut = shortcut
        self.functor.message.category = category
        self.functor.message.description = description

    def verifyShortcutAlreadyUse(self) -> bool:
        return self.shortcutManager.verifyShortcutAlreadyUse(self.text(), self.row())
    
    def verifyShortcutForm(self) -> bool :
        return self.shortcutManager.verifyShortcutForm(self.text())