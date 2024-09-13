from PyQt5 import QtWidgets

class ErrorDialog(QtWidgets.QMessageBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setIcon(QtWidgets.QMessageBox.Critical)
        self.setWindowTitle("错误")

    def show_error(self, message):
        self.setText(message)
        self.exec_()
