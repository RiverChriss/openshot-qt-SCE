# This Python file uses the following encoding: utf-8
import sys
import csv
import re


# Important:
# You need to run the following command to generate the ui_eventswidget.py file
#     pyside6-uic eventswidget.ui -o ui_eventswidget.py, or
#     pyside2-uic eventswidget.ui -o ui_eventswidget.py
try:
    #Path when import for project Openshot
    from SCE.EventsWidget.ui_eventswidget import Ui_EventsWidget
    from SCE.EventsWidget.shortcutManager import ShortcutManager
    from SCE.EventsWidget.categoryManager import CategoryManager
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
except ImportError:
    #Path when import for QtCreator (laungh this project)
    from ui_eventswidget import Ui_EventsWidget
    from shortcutManager import ShortcutManager
    from categoryManager import CategoryManager
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    from PySide6.QtCore import *


INDEX_COLUMN_COLOR = 0
INDEX_COLUMN_SHORTCUT = 1
INDEX_COLUMN_CATEGORY = 2
INDEX_COLUMN_DESCRIPTION = 3

HEADER_REF = ["ColorR", "ColorG", "ColorB", "Shortcut", "Category", "Description"]

class ColorWidget(QPushButton):
    DEFAULT_COLOR = [50, 50, 50]

    def __init__(self, eventsWidget, rgb=DEFAULT_COLOR):
        super().__init__(eventsWidget)
        self.itemQtTable = QTableWidgetItem(QTableWidgetItem.ItemType.UserType)
        self.eventsWidget = eventsWidget
        self.color = rgb
        self.SetBackgroundColor(self.color[0], self.color[1], self.color[2])

        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid() :
            if self.color !=  [color.red(), color.green(), color.blue()] :
                self.color = [color.red(), color.green(), color.blue()]
                self.SetBackgroundColor(color.red(), color.green(), color.blue())
                self.eventsWidget.shortcutManager.updateFunctor(self.itemQtTable.row())
                self.eventsWidget.detectSaveNeeded()
        self.itemQtTable.tableWidget().setCurrentCell(-1, -1)

    def SetBackgroundColor(self, red, green, blue):
        color = f"rgb({red}, {green}, {blue})"
        self.setStyleSheet("background-color: "
                            f"qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1, stop: 0 {color}, stop: 1 {color});"
                            "margin-left: 10px;"
                            "margin-right: 10px;")
        
    def getColor(self):
        return self.color
    
    def addSelfToTable(self, table, row):
        # QTableWidgetItem know is position in a Table
        # Need to mute signal setItem emit a change in the Table
        previous = table.blockSignals(True)
        table.setCellWidget(row, INDEX_COLUMN_COLOR, self)
        table.setItem(row, INDEX_COLUMN_COLOR, self.itemQtTable)
        table.blockSignals(previous)



class EventsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_EventsWidget()
        self.ui.setupUi(self)
        self.playerWorker = None # Need the ref to object with current Frame
        self.mainApplication = None # Need to get default application settings
        self.mainWindow = None # Need to be able call function in main_window
        self.shortcutManager = ShortcutManager(self, self.ui.tableWidget, INDEX_COLUMN_SHORTCUT)
        self.categoryManager = CategoryManager(self, self.ui.tableWidget, INDEX_COLUMN_CATEGORY)

        # init
        header = self.ui.tableWidget.horizontalHeader()
        header.setSectionResizeMode(INDEX_COLUMN_COLOR, QHeaderView.ResizeMode.Fixed)
        self.ui.tableWidget.setColumnWidth(INDEX_COLUMN_COLOR, 65)
        header.setSectionResizeMode(INDEX_COLUMN_SHORTCUT, QHeaderView.ResizeMode.ResizeToContents)
        self.ui.tableWidget.setColumnWidth(INDEX_COLUMN_CATEGORY, 110)
        header.setMaximumSectionSize(header.minimumSectionSize()*3)
        header.setSectionResizeMode(INDEX_COLUMN_DESCRIPTION, QHeaderView.ResizeMode.Stretch)
        self.ui.tableWidget.setSortingEnabled(True)
        self.ui.tableWidget.sortByColumn(INDEX_COLUMN_CATEGORY, Qt.SortOrder.AscendingOrder)
        self.ui.btn_RemoveCategory.setEnabled(False)

        # Add Connection
        self.ui.btn_Insert.clicked.connect(self.on_btn_Insert)
        self.ui.btn_Remove.clicked.connect(self.on_btn_Remove)
        self.ui.btn_ClearShortcut.clicked.connect(self.on_btn_ClearShortcut)
        self.ui.tableWidget.itemChanged.connect(self.on_itemChanged)
        self.ui.btn_AddCategory.clicked.connect(self.on_AddCategory)
        self.ui.btn_RemoveCategory.clicked.connect(self.on_RemoveCategory)
        self.categoryManager.listCountSignal.connect(lambda nbCategoryNotDefault : self.ui.btn_RemoveCategory.setEnabled(nbCategoryNotDefault))


    def setRefFromMainWindow(self, mainWindow, mainApplication, playerWorker) -> None :
        self.mainWindow = mainWindow
        self.mainApplication = mainApplication
        self.playerWorker = playerWorker

    def insertRow(self, rgb=ColorWidget.DEFAULT_COLOR, shortcut="", category="", description="") -> None:
        row = 0
        previous = self.ui.tableWidget.blockSignals(True)
        previousSort = self.ui.tableWidget.isSortingEnabled()
        self.ui.tableWidget.setSortingEnabled(False)

        self.ui.tableWidget.insertRow(row)

        self.shortcutManager.addItemShortcut(row, shortcut)

        self.categoryManager.addComboBox(row, category)

        colorItem = ColorWidget(self,rgb)
        colorItem.addSelfToTable(self.ui.tableWidget, row)

        itemDescription = QTableWidgetItem()
        itemDescription.setText(description)
        self.ui.tableWidget.setItem(row, INDEX_COLUMN_DESCRIPTION, itemDescription)

        # Need to manually update the ShortcutManager
        self.shortcutManager.updateFunctor(row)

        self.ui.tableWidget.setSortingEnabled(previousSort)
        self.ui.tableWidget.blockSignals(previous)

    def removeRow(self, row) -> None :
        previous = self.ui.tableWidget.blockSignals(True)
        self.shortcutManager.removeShortcutKey(row)
        self.ui.tableWidget.removeRow(row)
        self.ui.tableWidget.blockSignals(previous)

    def on_itemChanged(self, item):
        previous = self.ui.tableWidget.blockSignals(True)
        if item.column() == INDEX_COLUMN_SHORTCUT :
            if item.text() != "" :
                item.setText(item.text().upper())
                if not self.verifyShortcutForm(item.text()) :
                    QMessageBox.critical(self, "Shortcut Error", "Not a valid shortcut")
                    item.setText("")
                elif self.verifyShortcutAlreadyUse(item) :
                    QMessageBox.critical(self, "Shortcut Error", f"This shortcut \"{item.text()}\" is already use in the table")
                    item.setText("")
                elif item.text() in self.getAllKeyboardShortcutsValue() :
                    QMessageBox.critical(self, "Shortcut Error", f"This shortcut \"{item.text()}\" is already use in Openshot")
                    item.setText("")
        
        self.shortcutManager.updateFunctor(item.row())

        self.ui.tableWidget.blockSignals(previous)
        self.ui.tableWidget.setCurrentCell(-1, -1)
        self.detectSaveNeeded()

    def on_AddCategory(self) :
        text, ok = QInputDialog().getText(self, "Add a category", "Please enter the name of the new category")
        if ok :
            if not self.categoryManager.addCategory(text) :
                QMessageBox.warning(self, "Duplicated category", f"The category : {text} already exists")

    def on_RemoveCategory(self):
        text, ok = QInputDialog().getItem(self, "Remove a category", "Please select the category to be removed", \
                                           self.categoryManager.listCategory, editable=False)
        if ok :
            if not self.categoryManager.removeCategory(text) :
                QMessageBox.critical(self, "Invalid category", f"The category : {text} does not exists")

    def on_btn_ClearShortcut(self):
        pass
        
    def on_btn_Insert(self):
        self.insertRow()

    def on_btn_Remove(self):
        rowIndex = self.ui.tableWidget.currentRow()
        if rowIndex == -1:
            return
        self.removeRow(rowIndex)
        self.detectSaveNeeded()

    def importEventsManager(self, file_path) -> None:
        try :
            file = open(file_path)
            csvReader = csv.reader(file)
            header = []
            data = []
            header = next(csvReader)
            if header == HEADER_REF:
                # Get All the data from the file
                for row in csvReader:
                    data.append(row)
                file.close()

                # Remove old row before Load
                for i in range(self.ui.tableWidget.rowCount()):
                    self.removeRow(0)
                
                # Remove previous category before Load
                self.categoryManager.clearCategory()

                # Add row in table
                needToDialogWarning = False
                for i, [red, green, blue, shortcut, category, description] in enumerate(data):
                    if shortcut != "" :
                        shortcut = shortcut.upper()
                        # Need to verify validity of shortcut
                        if not self.verifyShortcutForm(shortcut) or \
                            shortcut in self.getAllKeyboardShortcutsValue() :
                            shortcut = ""
                            needToDialogWarning = True
                    self.insertRow([red, green, blue], shortcut, category, description)
                
                # Show DialogBoxWarning (if need)
                if needToDialogWarning :
                    QMessageBox.warning(self, "Duplicate shortcut warning!", "Some shortcuts have been deleted because they were in conflict with existing Openshot shortcuts")
            else :
                file.close()
                QMessageBox.critical(self, "Events Import Error!", "There was an issue importing the event list and the shortcuts.  Please try again or enter them manually.")
        except :
            print("ERROR : Unable to import the event list")

    def exportEventsManager(self, file_path) -> None:
        try :
            data = self.getDataTable()
            with open(file_path, 'w', newline="") as file:
                csvWriter = csv.writer(file)
                csvWriter.writerow(HEADER_REF)
                csvWriter.writerows(data)
                file.close()
        except :
            print("ERROR : Unable to export the event list")

    def getCurrentTime(self) -> float :
        if not self.playerWorker :
            return 0
        fps = QApplication.instance().project.get("fps")
        fps_float = float(fps["num"]) / float(fps["den"])
        requested_time = float(self.playerWorker.current_frame - 1) / fps_float
        return requested_time

    def getDataRow(self, row):
        color = self.ui.tableWidget.cellWidget(row, INDEX_COLUMN_COLOR).getColor()
        shortcut = self.ui.tableWidget.item(row, INDEX_COLUMN_SHORTCUT).text()
        category = self.ui.tableWidget.cellWidget(row, INDEX_COLUMN_CATEGORY).currentText()
        description = self.ui.tableWidget.item(row, INDEX_COLUMN_DESCRIPTION).text()
        return [color[0], color[1], color[2], shortcut, category, description]

    def getDataTable(self):
        data = []
        for i in range(self.ui.tableWidget.rowCount()):
            data.append(self.getDataRow(i))
        return data
    
    def getAllKeyboardShortcutsValue(self):
        """ Get a key sequence back from the setting name """
        keyboard_shortcuts = []
        if self.mainApplication :
            all_settings = self.mainApplication.get_settings()._data
            for setting in all_settings:
                if setting.get('category') == 'Keyboard':
                    keyboard_shortcuts.append(setting.get('value').upper())
        return keyboard_shortcuts

    def verifyShortcutAlreadyUse(self, item) -> bool:
        for i in range(self.ui.tableWidget.rowCount()) :
            if i != item.row() :
                if self.ui.tableWidget.item(i, INDEX_COLUMN_SHORTCUT).text() == item.text() :
                    return True
        return False
    
    def verifyShortcutForm(self, shortcut) -> bool :
        if re.fullmatch(r"(CTRL\+)?(SHIFT\+)?(ALT\+)?([A-Z]|[0-9])", shortcut) == None and \
            re.fullmatch(r"(CTRL\+)?(ALT\+)?(SHIFT\+)?([A-Z]|[0-9])", shortcut) == None and \
            re.fullmatch(r"(SHIFT\+)?(CTRL\+)?(ALT\+)?([A-Z]|[0-9])", shortcut) == None and \
            re.fullmatch(r"(SHIFT\+)?(ALT\+)?(CTRL\+)?([A-Z]|[0-9])", shortcut) == None and \
            re.fullmatch(r"(ALT\+)?(CTRL\+)?(SHIFT\+)?([A-Z]|[0-9])", shortcut) == None and \
            re.fullmatch(r"(ALT\+)?(SHIFT\+)?(CTRL\+)?([A-Z]|[0-9])", shortcut) == None :
            return False
        return True

    def detectSaveNeeded(self) :
        if self.mainApplication :
            self.mainApplication.project.has_unsaved_changes = True
        if self.mainWindow :
            self.mainWindow.setActionSaveEnabled()
    
    def addDefaultCategories(self, listName) -> None :
        for name in listName :
                self.categoryManager.addCategory(name, True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = EventsWidget()
    widget.show()
    sys.exit(app.exec())
