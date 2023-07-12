# This Python file uses the following encoding: utf-8
import sys
import csv


# Important:
# You need to run the following command to generate the ui_eventswidget.py file
#     pyside6-uic eventswidget.ui -o ui_eventswidget.py, or
#     pyside2-uic eventswidget.ui -o ui_eventswidget.py
try:
    #Path when import for project Openshot
    from SCE.EventsWidget.ui_eventswidget import Ui_EventsWidget
    from SCE.EventsWidget.shortcutManager import ShortcutManager
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
except ImportError:
    #Path when import for QtCreator (laungh this project)
    from ui_eventswidget import Ui_EventsWidget
    from shortcutManager import ShortcutManager
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    from PySide6.QtCore import *



INDEX_COLUMN_SHORTCUT = 1
INDEX_COLUMN_DESCRIPTION = 3
HEADER_REF = ["ColorR", "ColorG", "ColorB", "Shortcut", "Category", "Description"]


class ComboCategories(QComboBox):
    MAP = {"":0, "Task":1, "Cycle":2, "Operation Left":3, "Operation Right":4, "Analyse":5}
    INDEX_COLUMN_CATEGORY = 2 # determine in UI_EventsManager

    def __init__(self, parent=None, name=""):
        super().__init__(parent)
        self.itemQtTable = QTableWidgetItem(QTableWidgetItem.ItemType.UserType)

        for key in ComboCategories.MAP.keys():
            self.addItem(key)
        self.setCurrentIndex(ComboCategories.getIndex(name))
        self.currentIndexChanged.connect(lambda index : parent.shortcutManager.update(self.itemQtTable.row()))

    def getIndex(name):
        try:
            return ComboCategories.MAP[name]
        except KeyError:
            return -1

    def addSelfToTable(self, table, row):
        # QTableWidgetItem know is position in a Table
        # Need to mute signal setItem emit a change in the Table
        previous = table.blockSignals(True)
        table.setCellWidget(row, ComboCategories.INDEX_COLUMN_CATEGORY, self)
        table.setItem(row, ComboCategories.INDEX_COLUMN_CATEGORY, self.itemQtTable)
        table.blockSignals(previous)


class ColorWidget(QPushButton):
    DEFAULT_COLOR = [50, 50, 50]
    INDEX_COLUMN_COLOR = 0  # determine in UI_EventsManager

    def __init__(self, parent=None, rgb=DEFAULT_COLOR):
        super().__init__(parent)
        self.itemQtTable = QTableWidgetItem(QTableWidgetItem.ItemType.UserType)
        self.parent = parent
        self.color = rgb
        self.SetBackgroundColor(self.color[0], self.color[1], self.color[2])

        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid() :
            if self.color !=  [color.red(), color.green(), color.blue()] :
                self.color = [color.red(), color.green(), color.blue()]
                self.SetBackgroundColor(color.red(), color.green(), color.blue())
                self.parent.shortcutManager.update(self.itemQtTable.row())


    def SetBackgroundColor(self, red, green, blue):
        self.setStyleSheet(f"background-color: rgb({red}, {green}, {blue});"
                            "margin-left: 10px;"
                            "margin-right: 10px;")
        
    def getColor(self):
        return self.color
    
    def addSelfToTable(self, table, row):
        # QTableWidgetItem know is position in a Table
        # Need to mute signal setItem emit a change in the Table
        previous = table.blockSignals(True)
        table.setCellWidget(row, ColorWidget.INDEX_COLUMN_COLOR, self)
        table.setItem(row, ColorWidget.INDEX_COLUMN_COLOR, self.itemQtTable)
        table.blockSignals(previous)



class EventsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_EventsWidget()
        self.ui.setupUi(self)
        self.playerWorker = None # Need the ref to object with current Frame
        self.shortcutManager = ShortcutManager(self)

        # init
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(ColorWidget.INDEX_COLUMN_COLOR, QHeaderView.ResizeMode.Fixed)
        self.ui.tableWidget.setColumnWidth(ColorWidget.INDEX_COLUMN_COLOR, 65)
        # self.insertRow()
        # self.insertRow()
        # self.insertRow()
        # self.insertRow()
        # self.insertRow()


        # Add Connection
        self.ui.btn_Insert.clicked.connect(self.on_btn_Insert)
        self.ui.btn_Remove.clicked.connect(self.on_btn_Remove)
        self.ui.btn_Load.clicked.connect(self.on_btn_Load)
        self.ui.btn_Save.clicked.connect(self.on_btn_Save)
        self.ui.btn_CSV.clicked.connect(self.on_btn_CSV)
        self.ui.btn_ClearShortcut.clicked.connect(self.on_btn_ClearShortcut)
        self.ui.tableWidget.cellChanged.connect(lambda row, column : self.shortcutManager.update(row))

    def setPlayerWorker(self, playerWorker):
        self.playerWorker = playerWorker

    def insertRow(self, row=0, rgb=ColorWidget.DEFAULT_COLOR, shortcut="", category="", description=""):
        previous = self.ui.tableWidget.blockSignals(True)

        self.shortcutManager.add(row)
        self.ui.tableWidget.insertRow(row)

        comboItem = ComboCategories(self, category)
        comboItem.addSelfToTable(self.ui.tableWidget, row)

        colorItem = ColorWidget(self,rgb)
        colorItem.addSelfToTable(self.ui.tableWidget, row)

        itemShortcut = QTableWidgetItem()
        itemShortcut.setText(shortcut)
        itemShortcut.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.tableWidget.setItem(row, INDEX_COLUMN_SHORTCUT, itemShortcut)

        itemDescription = QTableWidgetItem()
        itemDescription.setText(description)
        self.ui.tableWidget.setItem(row, INDEX_COLUMN_DESCRIPTION, itemDescription)

        # Need to manually update the ShortcutManager
        self.shortcutManager.update(row)

        self.ui.tableWidget.blockSignals(previous)

    def removeRow(self, row):
        previous = self.ui.tableWidget.blockSignals(True)
        self.shortcutManager.remove(row)
        self.ui.tableWidget.removeRow(row)
        self.ui.tableWidget.blockSignals(previous)

    def on_btn_ClearShortcut(self):
        print(self.getDataTable())

    def on_btn_Insert(self):
        rowIndex = self.ui.tableWidget.currentRow() + 1
        self.insertRow(rowIndex)

    def on_btn_Remove(self):
        rowIndex = self.ui.tableWidget.currentRow()
        if rowIndex == -1:
            return
        self.removeRow(rowIndex)

    def on_btn_Load(self):
        filename, _ = QFileDialog.getOpenFileName(self, "Open file", "", "*.csv")
        if filename:
            file = open(filename)
            csvreader = csv.reader(file)
            header = []
            data = []
            header = next(csvreader)
            for row in csvreader:
                data.append(row)
            file.close()
            if header == HEADER_REF:
                for i in range(self.ui.tableWidget.rowCount()):
                    self.removeRow(0)
                for i, dataRow in enumerate(data):
                    self.insertRow(i, [dataRow[0], dataRow[1], dataRow[2]], dataRow[3], dataRow[4], dataRow[5])
                print(header)
                print(data)

    def on_btn_Save(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.Option.DontUseNativeDialog
        filename, _ = QFileDialog.getSaveFileName(self, "Save File", "", "*.csv", options= options)
        if filename:
            data = self.getDataTable()
            with open(filename, 'w', newline="") as file:
                csvWriter = csv.writer(file)
                csvWriter.writerow(HEADER_REF)
                csvWriter.writerows(data)
                file.close()

    def on_btn_CSV(self):
        if self.playerWorker:
            self.logic(self.playerWorker.current_frame)
        else:
            print("PlayerWork is None")

    def logic(self, noFrame):
        fps = QApplication.instance().project.get("fps")
        fps_float = float(fps["num"]) / float(fps["den"])
        print(fps_float)
        requested_time = float(noFrame - 1) / fps_float
        print(requested_time)

    def getDataRow(self, row):
        color = self.ui.tableWidget.cellWidget(row, ColorWidget.INDEX_COLUMN_COLOR).getColor()
        shortcut = self.ui.tableWidget.item(row, INDEX_COLUMN_SHORTCUT).text()
        category = self.ui.tableWidget.cellWidget(row, ComboCategories.INDEX_COLUMN_CATEGORY).currentText()
        description = self.ui.tableWidget.item(row, INDEX_COLUMN_DESCRIPTION).text()
        return [color[0], color[1], color[2], shortcut, category, description]

    def getDataTable(self):
        data = []
        for i in range(self.ui.tableWidget.rowCount()):
            data.append(self.getDataRow(i))
        return data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = EventsWidget()
    widget.show()
    sys.exit(app.exec())
