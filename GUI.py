import sys
from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QPushButton, QVBoxLayout, QMessageBox, QDesktopWidget,\
    QMainWindow, QAction, QMenu
from PyQt5.QtGui import QIcon


class UI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Stellar")
        self.resize(800, 600)

        # Windows #
        self.mainWidget = MainWidget(self)

        # Initialize UI #
        self.initUI()
        self.show()

    def initUI(self):
        self.initMenuBar()
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

class MainWidget(QWidget):
    def __init__(self, mainWindow):
        super().__init__()

        # Main Window #
        self.mainWindow = mainWindow

        # Buttons #
        self.quit_btn = QPushButton('Quit')
        # Layouts #
        self.layout = QVBoxLayout()

        # Initialize #
        self.initWidget()

    def initWidget(self):
        self.initButtons()
        self.initLayouts()

    def initButtons(self):
        self.quit_btn.clicked.connect(self.mainWindow.close)
        self.quit_btn.resize(10, 2)

    def initLayouts(self):
        self.layout.addWidget(self.quit_btn)
        self.setLayout(self.layout)

    def center(self):
        fg = self.frameGeometry()
        c = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(c)
        self.move(fg.topLeft())





if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = UI()
    sys.exit(app.exec_())