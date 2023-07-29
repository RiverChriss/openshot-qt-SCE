# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'eventswidget.ui'
##
## Created by: Qt User Interface Compiler version 6.5.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PyQt5.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QPushButton, QSizePolicy,
    QTableWidget, QTableWidgetItem, QWidget)

class Ui_EventsWidget(object):
    def setupUi(self, EventsWidget):
        if not EventsWidget.objectName():
            EventsWidget.setObjectName(u"EventsWidget")
        EventsWidget.resize(800, 600)
        EventsWidget.setStyleSheet(u"")
        self.gridLayout = QGridLayout(EventsWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.tableWidget = QTableWidget(EventsWidget)
        if (self.tableWidget.columnCount() < 5):
            self.tableWidget.setColumnCount(5)
        __qtablewidgetitem = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __qtablewidgetitem4)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setMinimumSize(QSize(400, 0))
        self.tableWidget.setEditTriggers(QAbstractItemView.AnyKeyPressed|QAbstractItemView.DoubleClicked|QAbstractItemView.EditKeyPressed)
        self.tableWidget.setTabKeyNavigation(False)
        self.tableWidget.setDragEnabled(False)
        self.tableWidget.setAlternatingRowColors(True)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tableWidget.setRowCount(0)
        self.tableWidget.horizontalHeader().setVisible(True)
        self.tableWidget.horizontalHeader().setMinimumSectionSize(65)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.verticalHeader().setVisible(False)

        self.gridLayout.addWidget(self.tableWidget, 1, 0, 1, 1)

        self.frame_Footer = QFrame(EventsWidget)
        self.frame_Footer.setObjectName(u"frame_Footer")
        self.frame_Footer.setFrameShape(QFrame.NoFrame)
        self.frame_Footer.setFrameShadow(QFrame.Raised)
        self.horizontalLayout = QHBoxLayout(self.frame_Footer)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.btn_Insert = QPushButton(self.frame_Footer)
        self.btn_Insert.setObjectName(u"btn_Insert")

        self.horizontalLayout.addWidget(self.btn_Insert)

        self.btn_ClearShortcut = QPushButton(self.frame_Footer)
        self.btn_ClearShortcut.setObjectName(u"btn_ClearShortcut")

        self.horizontalLayout.addWidget(self.btn_ClearShortcut)

        self.btn_Remove = QPushButton(self.frame_Footer)
        self.btn_Remove.setObjectName(u"btn_Remove")

        self.horizontalLayout.addWidget(self.btn_Remove)


        self.gridLayout.addWidget(self.frame_Footer, 2, 0, 1, 1)

        self.frame_Header = QFrame(EventsWidget)
        self.frame_Header.setObjectName(u"frame_Header")
        self.frame_Header.setFrameShape(QFrame.NoFrame)
        self.frame_Header.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.frame_Header)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.btn_AddCategory = QPushButton(self.frame_Header)
        self.btn_AddCategory.setObjectName(u"btn_AddCategory")

        self.horizontalLayout_2.addWidget(self.btn_AddCategory)

        self.btn_RemoveCategory = QPushButton(self.frame_Header)
        self.btn_RemoveCategory.setObjectName(u"btn_RemoveCategory")

        self.horizontalLayout_2.addWidget(self.btn_RemoveCategory)


        self.gridLayout.addWidget(self.frame_Header, 0, 0, 1, 1)


        self.retranslateUi(EventsWidget)

        QMetaObject.connectSlotsByName(EventsWidget)
    # setupUi

    def retranslateUi(self, EventsWidget):
        EventsWidget.setWindowTitle(QCoreApplication.translate("EventsWidget", u"EventsWidget", None))
        ___qtablewidgetitem = self.tableWidget.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("EventsWidget", u"Color", None));
        ___qtablewidgetitem1 = self.tableWidget.horizontalHeaderItem(1)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("EventsWidget", u"Shortcut", None));
        ___qtablewidgetitem2 = self.tableWidget.horizontalHeaderItem(2)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("EventsWidget", u"Category", None));
        ___qtablewidgetitem3 = self.tableWidget.horizontalHeaderItem(3)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("EventsWidget", u"Description", None));
        ___qtablewidgetitem4 = self.tableWidget.horizontalHeaderItem(4)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("EventsWidget", u"ItemUserShortcut", None));
        self.btn_Insert.setText(QCoreApplication.translate("EventsWidget", u"Insert", None))
        self.btn_ClearShortcut.setText(QCoreApplication.translate("EventsWidget", u"Clear Shortcut", None))
        self.btn_Remove.setText(QCoreApplication.translate("EventsWidget", u"Remove", None))
        self.btn_AddCategory.setText(QCoreApplication.translate("EventsWidget", u"Add Category", None))
        self.btn_RemoveCategory.setText(QCoreApplication.translate("EventsWidget", u"Remove Category", None))
    # retranslateUi

