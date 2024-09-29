import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from dialogs import PerformanceTableDialog

from PyQt5 import QtWidgets, uic
from utils.globalResultLoader import load_global_result
class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 加载主界面
        uic.loadUi('gui/toolsUI/main_entry.ui', self)
        
        # 初始化时禁用两个按钮
        self.pushButton_CaVl.setEnabled(False)
        self.pushButton_pt.setEnabled(False)
        
        # 连接按钮点击事件
        self.pushButton_LdXML.clicked.connect(self.load_xml)
        self.pushButton_pt.clicked.connect(self.open_performance_table)
        
        # 初始化 global_result 对象
        self.global_result = None
        
    def load_xml(self):
        # 运行选择文件选项框，将用户选择的文件路径保存至变量global_result_path
        global_result_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Please select the global result file", "", "XML Files (*.xml)")
        self.global_result = load_global_result(global_result_path)
        if self.global_result:
            # 如果XML加载成功,启用其他两个按钮
            self.pushButton_CaVl.setEnabled(True)
            self.pushButton_pt.setEnabled(True)
        else:
            QtWidgets.QMessageBox.warning(self, "错误", "XML加载失败!")
    
    def open_performance_table(self):
        if self.global_result:
            # 创建并显示性能表对话框，传入 global_result 对象
            dialog = PerformanceTableDialog(self.global_result, self)
            dialog.exec_()
        else:
            QtWidgets.QMessageBox.warning(self, "错误", "请先加载XML文件!")

        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
