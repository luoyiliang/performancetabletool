import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.globalResultLoader import GlobalResultLoader, main as load_xml
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QFileDialog

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        uic.loadUi('gui/main_frame.ui', self)
        
        # 连接菜单项到相应的方法
        self.actionOpen.triggered.connect(self.open_file)
        
        # 初始化数据
        self.data = None

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "打开XML文件", "", "XML Files (*.xml)")
        if file_name:
            self.data = load_xml(file_name)
            self.update_ui()

    def update_ui(self):
        if self.data:
            # 更新General Information
            general_info = self.data["GeneralInformation"]
            self.label_calibrationTool_value.setText(general_info.Calibration)
            self.label_projectFile_value.setText(general_info.Project)
            self.label_dateCreated_value.setText(general_info.Date)
            self.label_createdBy_value.setText(general_info.Customer)

            # 更新其他UI元素...

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
