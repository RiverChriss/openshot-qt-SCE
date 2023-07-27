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


class ComboCategory(QComboBox):
    def __init__(self, categoryManager, name=""):
        super().__init__(categoryManager.eventsManager)
        self.itemQtTable = QTableWidgetItem(name, QTableWidgetItem.ItemType.UserType)
        self.categoryManager = categoryManager

        for category in self.categoryManager.listCategory:
            self.addItem(category)

        self.setCurrentIndex(self.getIndex(name))
        self.currentIndexChanged.connect(self.on_currentIndexChanged)

    def on_currentIndexChanged(self, indexComboBox):
        table = self.categoryManager.tableWidget
        previous = table.blockSignals(True) # Need to block the signal itemChanged

        self.itemQtTable.setText(self.itemText(indexComboBox))
        self.categoryManager.eventsManager.shortcutManager.updateFunctor(self.itemQtTable.row())

        self.categoryManager.eventsManager.detectSaveNeeded()
        table.blockSignals(previous)
        table.setCurrentCell(-1, -1)

    def getIndex(self, name) -> int:
        return self.findText(name)

    def addSelfToTable(self, row):
        # QTableWidgetItem know is position in a Table
        # Need to mute signal setItem emit a change in the Table
        table = self.categoryManager.tableWidget
        previous = table.blockSignals(True)
        table.setCellWidget(row, self.categoryManager.indexColumn, self)
        table.setItem(row, self.categoryManager.indexColumn, self.itemQtTable)
        table.blockSignals(previous)

class CategoryManager(QObject) :
    def __init__(self, eventsManager, tableWidget,indexColumn) :
        super().__init__(eventsManager)
        self.eventsManager = eventsManager
        self.tableWidget = tableWidget
        self.indexColumn = indexColumn
        self.listCategory = []

    def addComboBox(self, row, name="") -> None:
        comboBox = ComboCategory(self, name)
        comboBox.addSelfToTable(row)

    def addCategory(self, name) -> None :
        self.listCategory.append(name)
        for i in range(self.tableWidget.rowCount()):
            self.tableWidget.cellWidget(i, self.indexColumn).addItem(name)

    def removeCategory(self, name) -> None :
        self.listCategory.remove(name)
        for i in range(self.tableWidget.rowCount()):
            comboBox = self.tableWidget.cellWidget(i, self.indexColumn)
            comboBox.removeItem(comboBox.getIndex(name))