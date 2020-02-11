import sys
import math
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QMessageBox, QDesktopWidget,\
    QMainWindow, QAction, QMenu, qApp, QComboBox, QCalendarWidget, QGridLayout, QHBoxLayout, QLineEdit, QFrame,\
    QTableWidget, QTableWidgetItem, QGroupBox
from PyQt5.QtGui import QIcon, QColor, QFont, QFontDatabase
from PyQt5.QtCore import QDate, QDir, Qt
from Stock import Ticker
from utils import *

# Globals #

lightGreen = QColor(178, 231, 205)

class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stellar")
        self.resize(1600, 800)

        # Frames #
        self.mainWidget = mainFrame(self)

        # Initialize UI #
        self.initUI()
        self.show()

    def initUI(self):
        self.initMenuBar()
        self.initToolBar()
        self.setCentralWidget(self.mainWidget)
        self.statusBar().showMessage('Ready')

    def initMenuBar(self):
        exitAct = QAction(QIcon('exit.png'), '&Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.setStatusTip('Exit application')
        exitAct.triggered.connect(self.close)

        fileMenu = self.menuBar().addMenu('&File')

        downloadMenu = QMenu('Download', self)
        month1Act = QAction('1 Month', self)
        month1Act.setStatusTip('Download 1 Month of Data')
        month3Act = QAction('3 Month', self)
        month3Act.setStatusTip('Download 3 Months of Data')
        downloadMenu.addAction(month1Act)
        downloadMenu.addAction(month3Act)

        fileMenu.addMenu(downloadMenu)
        fileMenu.addAction(exitAct)

    def initToolBar(self):
        exitAct = QAction('Exit', self)
        exitAct.setShortcut('Ctrl+Q')
        exitAct.triggered.connect(self.close)

        self.toolbar = self.addToolBar('Exit')
        self.toolbar.addAction(exitAct)

    def contextMenuEvent(self, event):
        cmenu = QMenu(self)

        newAct = cmenu.addAction("New")
        opnAct = cmenu.addAction("Open")
        quitAct = cmenu.addAction("Quit")
        action = cmenu.exec_(self.mapToGlobal(event.pos()))

        if action == quitAct:
            qApp.quit()

    def closeEvent(self, event):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Warning!")
        msg.setText("Are you sure you want to quit?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        reply = msg.exec_()

        if(reply == QMessageBox.Yes):
            event.accept()
        else:
            event.ignore()


class statsFrame(QFrame):
    def __init__(self):
        super().__init__()

        self.mainLayout = QVBoxLayout()

        # Frames #
        self.statsFrame = QFrame(self)
        self.dataFrame = QFrame(self)

        # Layouts #
        self.statsLayout = QGridLayout()
        self.dataLayout = QVBoxLayout()

        # Labels #
        self.strike = QLabel('Strike')
        self.lastPrice = QLabel('Last Price')
        self.bid = QLabel('Bid')
        self.ask = QLabel('Ask')
        self.strikeVal = QLabel()
        self.lastPriceVal = QLabel()
        self.bidVal = QLabel()
        self.askVal = QLabel()

        # Table #
        self.dataTable = QTableWidget()

        self.initWidget()
        self.setGrid()
        self.setTable()

    def initWidget(self):
        self.statsFrame.setLayout(self.statsLayout)
        self.dataFrame.setLayout(self.dataLayout)

        self.mainLayout.addWidget(self.dataFrame)
        self.mainLayout.addWidget(self.statsFrame)
        self.setLayout(self.mainLayout)

    def setGrid(self):
        self.statsLayout.addWidget(self.strike, 1, 1)
        self.statsLayout.addWidget(self.strikeVal, 1, 2)
        self.statsLayout.addWidget(self.lastPrice, 2, 1)
        self.statsLayout.addWidget(self.lastPriceVal, 2, 2)
        self.statsLayout.addWidget(self.bid, 3, 1)
        self.statsLayout.addWidget(self.bidVal, 3, 2)
        self.statsLayout.addWidget(self.ask, 4, 1)
        self.statsLayout.addWidget(self.askVal, 4, 2)


    def setTable(self):
        self.dataLayout.addWidget(self.dataTable)
        self.dataTable.setRowCount(10)
        self.dataTable.setColumnCount(7)
        self.dataTable.setItem(0, 0, QTableWidgetItem("Strike"))
        self.dataTable.setItem(0, 1, QTableWidgetItem("Avg Price"))
        self.dataTable.setItem(0, 2, QTableWidgetItem("Bid"))
        self.dataTable.setItem(0, 3, QTableWidgetItem("Ask"))
        self.dataTable.setItem(0, 4, QTableWidgetItem("Change"))
        self.dataTable.setItem(0, 5, QTableWidgetItem("Volume"))
        self.dataTable.setItem(0, 6, QTableWidgetItem("Open Interest"))


class mainFrame(QFrame):
    def __init__(self, mainWindow):
        super().__init__()

        self.mainWindow = mainWindow

        # Frames #
        self.leftFrame = QFrame(self)
        self.rightFrame = QFrame(self)
        self.centerFrame = statsFrame()

        # Layouts #
        self.mainLayout = QHBoxLayout(self)
        self.leftLayout = QVBoxLayout()
        self.rightLayout = QVBoxLayout()

        # Buttons #
        self.calls = QPushButton("Get Calls")
        self.puts = QPushButton("Get Puts")

        # Combo Boxes #
        self.tickerBox = QComboBox(self)
        self.dateBox = QComboBox(self)

        # Calendars #
        #self.calendar = QCalendarWidget(self)

        # Roboto #
        self.tableDataFont = QFont()
        self.initWidget()
        self.center()

    def initWidget(self):
        self.initFonts()
        self.initFrames()
        self.initButtons()
        self.initComboBoxes()
        #self.initCalendar()
        self.initLayout()

    def initFrames(self):
        self.leftFrame.setLayout(self.leftLayout)
        self.rightFrame.setLayout(self.rightLayout)

        self.mainLayout.addWidget(self.leftFrame)
        self.mainLayout.addWidget(self.centerFrame)
        self.mainLayout.addWidget(self.rightFrame)

    def initButtons(self):
        self.calls.clicked.connect(self.callsBtn_Event)

    def initComboBoxes(self):
        self.tickerBox.addItem("TSLA")
        self.tickerBox.addItem("MSFT")
        self.tickerBox.activated[str].connect(self.tickerCB_Event)
        self.tickerCB_Event(self.tickerBox.currentText())

    def initCalendar(self):
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumDate(QDate(datetime.now().year, datetime.now().month - 1, 1))

    def initFonts(self):
        roboDir = QDir("Roboto")
        QFontDatabase.addApplicationFont("Roboto/Roboto-Regular.ttf")
        robotoFont = QFont("Roboto")
        robotoFont.setBold(True)
        self.centerFrame.dataTable.setFont(robotoFont)


    def initLayout(self):
        self.leftLayout.addWidget(self.tickerBox)
        self.leftLayout.addWidget(self.dateBox)
        self.rightLayout.addWidget(self.calls)
        self.rightLayout.addWidget(self.puts)

    def center(self):
        fg = self.frameGeometry()
        c = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(c)
        self.move(fg.topLeft())

    def tickerCB_Event(self, name):
        name = self.tickerBox.currentText()
        data = Ticker(name)
        dates = data.getAvailableDates()

        self.dateBox.clear()
        for date in dates:
            self.dateBox.addItem(date)

    def callsBtn_Event(self):
        self.mainWindow.statusBar().showMessage('Getting Call...')
        date = self.dateBox.currentText()
        name = self.tickerBox.currentText()
        print("Getting call for {} on date {}".format(name, date))
        data = Ticker(name)
        res = data.getCall_Date(date)
        self.mainWindow.statusBar().showMessage('Call Retreived')
        self.centerFrame.dataTable.setRowCount(len(res))

        i = 0
        for index, row in res.iloc[1:].iterrows():
            # Strike Price Table Entry
            strike = QTableWidgetItem(currencyFormat(row["strike"]))
            strike.setFlags(Qt.ItemIsEnabled)
            self.centerFrame.dataTable.setItem(1 + i, 0, strike)

            # Avg Price Table Entry
            price = QTableWidgetItem(currencyFormat((row["bid"] + row["ask"]) / 2.0))
            price.setFlags(Qt.ItemIsEnabled)
            self.centerFrame.dataTable.setItem(1 + i, 1, price)

            # Bid Price Table Entry
            bid = QTableWidgetItem(currencyFormat(row["bid"]))
            bid.setFlags(Qt.ItemIsEnabled)
            self.centerFrame.dataTable.setItem(1 + i, 2, bid)

            # Ask Price Table Entry
            ask = QTableWidgetItem(currencyFormat(row["ask"]))
            ask.setFlags(Qt.ItemIsEnabled)
            self.centerFrame.dataTable.setItem(1 + i, 3, ask)

            # Percent Change Table Entry
            percentChangeVal = row["percentChange"]
            if(percentChangeVal == "Infinity" or percentChangeVal == "nan"):
                percentChangeVal = "-"
            else:
                percentChangeVal = percentFormat(percentChangeVal)

            percentChange = QTableWidgetItem(percentChangeVal)
            percentChange.setFlags(Qt.ItemIsEnabled)
            self.centerFrame.dataTable.setItem(1 + i, 4, percentChange)

            # Volume Table Entry
            volume = QTableWidgetItem(str(row["volume"]))
            volume.setFlags(Qt.ItemIsEnabled)
            self.centerFrame.dataTable.setItem(1 + i, 5, volume)

            # Open Interest Entry
            openInterest = QTableWidgetItem(str(row["openInterest"]))
            openInterest.setFlags(Qt.ItemIsEnabled)
            self.centerFrame.dataTable.setItem(1 + i, 6, openInterest)
            if(row["inTheMoney"]):
                for j in range(self.centerFrame.dataTable.columnCount()):
                    self.centerFrame.dataTable.item(i + 1, j).setBackground(lightGreen)
            else:
                for j in range(self.centerFrame.dataTable.columnCount()):
                    self.centerFrame.dataTable.item(i + 1, j).setBackground(QColor(194, 24, 7))
            i += 1




        #self.centerFrame.strikeVal.setText("$ " + str(res.iloc[0]['strike']))
        #self.centerFrame.lastPriceVal.setText("$ " + str(res.iloc[0]['lastPrice']))
        #self.centerFrame.bidVal.setText("$ " + str(res.iloc[0]['bid']))
        #self.centerFrame.askVal.setText("$ " + str(res.iloc[0]['ask']))
        #self.mainWindow.statusBar().showMessage('')


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())