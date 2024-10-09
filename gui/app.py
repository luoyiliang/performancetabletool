# coding: utf-8
# Author: Roy.Luo
# Version: 1.0

import sys
import os
import getpass
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


from dialogs import PerformanceTableDialog

from PyQt5 import QtWidgets, uic
from utils.globalResultLoader import load_global_result
from utils.logger import setup_logger
from utils.license_validator import setup_license_validator

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        
        # 加载主界面
        uic.loadUi('gui/toolsUI/main_entry.ui', self)
        
        # 初始化日志系统
        self.logger = setup_logger(self.textBrowser_log)
        
        # 初始化许可证验证系统
        self.license_validator = setup_license_validator()
        
        # 初始化时禁用所有按钮
        self.pushButton_LdXML.setEnabled(False)
        self.pushButton_CaVl.setEnabled(False)
        self.pushButton_pt.setEnabled(False)
        
        # 连接按钮点击事件
        self.pushButton_LdXML.clicked.connect(self.load_xml)
        self.pushButton_pt.clicked.connect(self.open_performance_table)
        
        # 初始化 global_result 对象
        self.global_result = None
        
        self.logger.info("应用程序已启动")
        
        # 验证许可证
        self.validate_license()
        
    def validate_license(self):
        try:
            username = getpass.getuser()  # 获取当前系统用户名
            print(username)
        except Exception:
            username = os.getlogin()  # 如果 getpass.getuser() 失败，尝试使用 os.getlogin()
        
        self.logger.info(f"正在验证用户 {username} 的许可证")
        if self.license_validator.validate_license(username):
            self.logger.info(f"用户 {username} 许可证验证成功")
            self.pushButton_LdXML.setEnabled(True)
        else:
            self.logger.error(f"用户 {username} 许可证验证失败")
            self.pushButton_LdXML.setEnabled(False)
            QtWidgets.QMessageBox.warning(self, "许可证验证", "许可证验证失败，请联系管理员。")
        
    def load_xml(self):
        self.logger.info("开始加载XML文件")
        # 运行选择文件选项框，将用户选择的文件路径保存至变量global_result_path
        global_result_path, _ = QtWidgets.QFileDialog.getOpenFileName(self, "Please select the global result file", "", "XML Files (*.xml)")
        self.global_result = load_global_result(global_result_path)
        if self.global_result:
            # 如果XML加载成功,启用其他两个按钮
            self.pushButton_CaVl.setEnabled(True)
            self.pushButton_pt.setEnabled(True)
            self.logger.info(f"XML文件 {global_result_path} 加载成功")
        else:
            QtWidgets.QMessageBox.warning(self, "错误", "XML加载失败!")
            self.logger.error(f"XML文件 {global_result_path} 加载失败")
    
    def open_performance_table(self):
        if self.global_result:
            self.logger.info("打开性能表对话框")
            dialog = PerformanceTableDialog(self.global_result, self)
            dialog.exec_()
        else:
            QtWidgets.QMessageBox.warning(self, "错误", "请先加载XML文件!")
            self.logger.warning("尝试打开性能表对话框失败：未加载XML文件")

        
if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
