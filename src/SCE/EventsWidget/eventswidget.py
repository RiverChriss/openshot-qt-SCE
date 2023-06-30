# This Python file uses the following encoding: utf-8
import sys


# Important:
# You need to run the following command to generate the ui_eventswidget.py file
#     pyside6-uic eventswidget.ui -o ui_eventswidget.py, or
#     pyside2-uic eventswidget.ui -o ui_eventswidget.py
try:
    #Path when import for project Openshot
    from src.SCE.EventsWidget.ui_eventswidget import Ui_EventsWidget
    from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QComboBox, QPushButton, QHeaderView, QColorDialog, QMessageBox, QShortcut
    from PyQt5.QtGui import QKeySequence
except ImportError:
    #Path when import for QtCreator (laungh this project)
    from ui_eventswidget import Ui_EventsWidget
    from PySide6.QtWidgets import QApplication, QWidget, QTableWidget, QComboBox, QPushButton, QHeaderView, QColorDialog, QMessageBox
    from PySide6.QtGui import QKeySequence, QShortcut



INDEX_COLUMN_COLOR = 0
INDEX_COLUMN_CATEGORIES = 2



class comboCategories(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.addItems(["", "Task", "Cycle", "Operation"])
        self.setCurrentIndex(-1)



class ColorWidget(QPushButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.SetBackgroundColor(50, 50, 50)

        self.clicked.connect(self.on_clicked)

    def on_clicked(self):
        color = QColorDialog.getColor()
        if color.isValid() :
            self.SetBackgroundColor(color.red(), color.green(), color.blue())


    def SetBackgroundColor(self, red, green, blue):
        self.setStyleSheet(f"background-color: rgb({red}, {green}, {blue});"
                            "margin-left: 10px;"
                            "margin-right: 10px;")



class EventsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_EventsWidget()
        self.ui.setupUi(self)

        # init
        self.ui.tableWidget.horizontalHeader().setSectionResizeMode(INDEX_COLUMN_COLOR, QHeaderView.ResizeMode.Fixed)
        self.ui.tableWidget.setColumnWidth(INDEX_COLUMN_COLOR, 65)

        # init the combobox in the table
        self.ui.tableWidget.setCellWidget(0,INDEX_COLUMN_CATEGORIES, comboCategories(self))
        self.ui.tableWidget.setCellWidget(1,INDEX_COLUMN_CATEGORIES, comboCategories(self))
        self.ui.tableWidget.setCellWidget(2,INDEX_COLUMN_CATEGORIES, comboCategories(self))
        self.ui.tableWidget.setCellWidget(3,INDEX_COLUMN_CATEGORIES, comboCategories(self))
        self.ui.tableWidget.setCellWidget(4,INDEX_COLUMN_CATEGORIES, comboCategories(self))

        # init the colorbox in the table
        self.ui.tableWidget.setCellWidget(0,INDEX_COLUMN_COLOR, ColorWidget(self))
        self.ui.tableWidget.setCellWidget(1,INDEX_COLUMN_COLOR, ColorWidget(self))
        self.ui.tableWidget.setCellWidget(2,INDEX_COLUMN_COLOR, ColorWidget(self))
        self.ui.tableWidget.setCellWidget(3,INDEX_COLUMN_COLOR, ColorWidget(self))
        self.ui.tableWidget.setCellWidget(4,INDEX_COLUMN_COLOR, ColorWidget(self))

        # Add Connection
        self.ui.btn_Insert.clicked.connect(self.on_btn_Insert)
        self.ui.btn_Remove.clicked.connect(self.on_btn_Remove)

    def on_btn_Insert(self):
        rowIndex = self.ui.tableWidget.currentRow() + 1
        self.ui.tableWidget.insertRow(rowIndex)
        self.ui.tableWidget.setCellWidget(rowIndex,INDEX_COLUMN_CATEGORIES, comboCategories(self))
        self.ui.tableWidget.setCellWidget(rowIndex,INDEX_COLUMN_COLOR, ColorWidget(self))

    def on_btn_Remove(self):
        rowIndex = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.removeRow(rowIndex)
        # TODO_SCE:: Probablement retirer le link shortcut



if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = EventsWidget()
    widget.show()
    sys.exit(app.exec())
