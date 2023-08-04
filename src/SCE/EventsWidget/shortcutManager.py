import re

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class MessageTag():
    def __init__(self) -> None:
        self.colorHex = ""
        self.shortcut = ""
        self.category = ""
        self.description = ""

class MessageCloseTag():
    def __init__(self) -> None:
        self.category = ""
        self.shortcut = ""

class FunctorCloseTag():
    def __init__(self, shortcutManager) -> None:
        # Variable logic
        self.shortcutManager = shortcutManager

        # Data Store
        self.message = MessageCloseTag()

    def __call__(self) -> None:
        self.shortcutManager.closeTagSignal.emit(self.message)


class FunctorShortcut():
    def __init__(self, shortcutManager) -> None:
        # Variable logic
        self.shortcutManager = shortcutManager

        # Data Store
        self.message = MessageTag()

    def __call__(self) -> None:
        self.shortcutManager.eventSignal.emit(self.message)
        

        
class ShortcutManager(QObject):
    eventSignal = pyqtSignal(MessageTag)
    closeTagSignal = pyqtSignal(MessageCloseTag)
    secondKey = "SHIFT+"

    def __init__(self, eventsManager, tableWidget, columnShortcut):
        super().__init__(eventsManager)
        self.eventsManager =eventsManager
        self.tableWidget = tableWidget
        self.columnShortcut = columnShortcut

    def addItemShortcut(self, row, name="") -> None :
        self.tableWidget.setItem(row, self.columnShortcut, ItemShortcut(self, name))

    def remove(self, row) -> None :
        itemShortcut = self.tableWidget.item(row, self.columnShortcut)
        if itemShortcut :
            itemShortcut.removeShortcutKey()

    def removeShortcutKey(self, row) -> None:
        itemShortcut = self.tableWidget.item(row, self.columnShortcut)
        if itemShortcut :
            itemShortcut.removeShortcutKey()

    def updateFunctor(self, row) -> None :
        itemShortcut = self.tableWidget.item(row, self.columnShortcut)
        if itemShortcut :
            [color, shortcut, category, description] = self.eventsManager.getDataRow(row)
            itemShortcut.update(color, shortcut, category, description)

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
        if re.fullmatch(r"([A-Z]|[0-9])", name) == None :
            return False
        return True

class ItemShortcut(QTableWidgetItem):
    def __init__(self, shortcutManager, name = "") -> None:
        super().__init__(name.upper())
        self.shortcutManager = shortcutManager

        # Format
        self.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

        self.shortcutTag = QShortcut(self.shortcutManager.eventsManager)
        self.shortcutCloseTag = QShortcut(self.shortcutManager.eventsManager)

        self.functorTag = FunctorShortcut(shortcutManager)
        self.functorCloseTag = FunctorCloseTag(shortcutManager)

        self.shortcutTag.activated.connect(self.functorTag)
        self.shortcutCloseTag.activated.connect(self.functorCloseTag)

    
    def removeShortcutKey(self) -> None:
        self.setText("")
        self.shortcutTag.setKey('')
        try:
            self.shortcutTag.activated.disconnect()
        except:
            print(end="")

        self.shortcutCloseTag.setKey('')
        try:
            self.shortcutCloseTag.activated.disconnect()
        except:
            print(end="")

    def update(self, colorHex, shortcut, category, description) -> None:
        self.shortcutTag.setKey(shortcut)
        self.shortcutCloseTag.setKey(ShortcutManager.secondKey + shortcut)

        self.functorCloseTag.message.category = category
        self.functorTag.message.shortcut = ShortcutManager.secondKey + shortcut

        self.functorTag.message.colorHex = colorHex
        self.functorTag.message.shortcut = shortcut
        self.functorTag.message.category = category
        self.functorTag.message.description = description
   
    def verifyShortcutAlreadyUse(self) -> bool:
        return self.shortcutManager.verifyShortcutAlreadyUse(self.text(), self.row())
    
    def verifyShortcutForm(self) -> bool :
        return self.shortcutManager.verifyShortcutForm(self.text())