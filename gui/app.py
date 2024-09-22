import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog
from utils import globalResultLoader


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        # 使用 uic 加载 .ui 文件
        uic.loadUi("main_frame.ui", self)

        # 绑定按钮点击事件
        self.pushButton_LoadXML.clicked.connect(self.load_file)

    def load_file(self):
        # 打开文件选择对话框
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Global Result XML File", "",
                                                   "XML Files (*.xml);;All Files (*)",
                                                   options=options)
        if file_name:
            # 加载GlobalResult
            target_global_result = globalResultLoader.load_global_result(file_name)
            summary = target_global_result.print_summary()
            
            # 将summary显示在textEdit_logViewer中
            self.textEdit_logViewer.setPlainText(summary)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
