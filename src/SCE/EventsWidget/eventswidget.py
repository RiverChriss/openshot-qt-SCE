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
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
except ImportError:
    #Path when import for QtCreator (laungh this project)
    from ui_eventswidget import Ui_EventsWidget
    from PySide6.QtWidgets import *
    from PySide6.QtGui import *
    from PySide6.QtCore import *



INDEX_COLUMN_COLOR = 0
INDEX_COLUMN_SHORTCUT = 1
INDEX_COLUMN_CATEGORY = 2
INDEX_COLUMN_DESCRIPTION = 3
HEADER_REF = ["ColorR", "ColorG", "ColorB", "Shortcut", "Category", "Description"]


class ComboCategories(QComboBox):
    map = {"":0, "Task":1, "Cycle":2, "Operation":3}
    def __init__(self, parent=None, index=-1):
        super().__init__(parent)
        self.addItems(["", "Task", "Cycle", "Operation"])
        self.setCurrentIndex(index)



class ColorWidget(QPushButton):
    DEFAULT_COLOR = [50, 50, 50]
    def __init__(self, parent=None, rgb=DEFAULT_COLOR):
        super().__init__(parent)
        self.color = rgb
        self.SetBackgroundColor(self.color[0], self.color[1], self.color[2])

        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid() :
            self.color = [color.red(), color.green(), color.blue()]
            self.SetBackgroundColor(color.red(), color.green(), color.blue())


    def SetBackgroundColor(self, red, green, blue):
        self.setStyleSheet(f"background-color: rgb({red}, {green}, {blue});"
                            "margin-left: 10px;"
                            "margin-right: 10px;")
        
    def getColor(self):
        return self.color



class EventsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_EventsWidget()
        self.ui.setupUi(self)

        # init
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(INDEX_COLUMN_COLOR, QHeaderView.ResizeMode.Fixed)
        self.ui.tableWidget.setColumnWidth(INDEX_COLUMN_COLOR, 65)
        self.insertRow()
        self.insertRow()
        self.insertRow()
        self.insertRow()
        self.insertRow()


        # Add Connection
        self.ui.btn_Insert.clicked.connect(self.on_btn_Insert)
        self.ui.btn_Remove.clicked.connect(self.on_btn_Remove)
        self.ui.btn_Load.clicked.connect(self.on_btn_Load)
        self.ui.btn_Save.clicked.connect(self.on_btn_Save)

    def insertRow(self, index=0, rgb=ColorWidget.DEFAULT_COLOR, shotcut="", category="", description=""):
        self.ui.tableWidget.insertRow(index)
        self.ui.tableWidget.setCellWidget(index,INDEX_COLUMN_CATEGORY, ComboCategories(self, ComboCategories.map[category]))
        self.ui.tableWidget.setCellWidget(index,INDEX_COLUMN_COLOR, ColorWidget(self, rgb))
        itemShortcut = QTableWidgetItem()
        itemShortcut.setText(shotcut)
        itemShortcut.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
        self.ui.tableWidget.setItem(index, INDEX_COLUMN_SHORTCUT, itemShortcut)
        itemDescription = QTableWidgetItem()
        itemDescription.setText(description)
        self.ui.tableWidget.setItem(index, INDEX_COLUMN_DESCRIPTION, itemDescription)


    def on_btn_Insert(self):
        rowIndex = self.ui.tableWidget.currentRow() + 1
        self.insertRow(rowIndex)

    def on_btn_Remove(self):
        rowIndex = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.removeRow(rowIndex)
        # TODO_SCE:: Probablement retirer le link shortcut

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
                    self.ui.tableWidget.removeRow(0)
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

    def getDataTable(self):
        data = []
        for i in range(self.ui.tableWidget.rowCount()):
            color = self.ui.tableWidget.cellWidget(i,INDEX_COLUMN_COLOR).getColor()
            shotcut = self.ui.tableWidget.item(i, INDEX_COLUMN_SHORTCUT)
            if (shotcut == None):
                shotcut = ""
            else:
                shotcut = shotcut.text()
            category = self.ui.tableWidget.cellWidget(i, INDEX_COLUMN_CATEGORY).currentText()
            description = self.ui.tableWidget.item(i, INDEX_COLUMN_DESCRIPTION)
            if (description == None):
                description = ""
            else:
                description = description.text()
            data.append([color[0], color[1], color[2], shotcut, category, description])
        return data

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = EventsWidget()
    widget.show()
    sys.exit(app.exec())
