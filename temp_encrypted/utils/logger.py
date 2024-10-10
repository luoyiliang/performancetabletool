"""
日志模块

此模块提供了日志记录功能，支持将日志输出到GUI界面和文件。

主要功能:
1. 设置日志记录器，同时输出到GUI文本浏览器和日志文件
2. 支持日志文件的自动轮转

类:
- QTextBrowserHandler: 自定义的日志处理器，用于将日志输出到QTextBrowser

函数:
- setup_logger: 设置日志记录器，返回配置好的logger对象

使用方法:
1. 在GUI初始化时调用setup_logger函数，传入QTextBrowser对象
2. 使用返回的logger对象进行日志记录

依赖:
- logging: Python标准库中的日志模块
- PyQt5.QtWidgets: PyQt5库中的QTextBrowser组件

注意:
- 日志文件名为'performancetabletool.log'
- 日志文件大小限制为1MB，最多保留3个备份文件

作者: Roy.Luo
版本: 1.0
"""

# coding: utf-8
# Author: Roy.Luo
# Version: 1.0

import logging
from logging.handlers import RotatingFileHandler
from PyQt5.QtWidgets import QTextBrowser

class QTextBrowserHandler(logging.Handler):
    def __init__(self, text_browser):
        super().__init__()
        self.text_browser = text_browser

    def emit(self, record):
        msg = self.format(record)
        self.text_browser.append(msg)

def setup_logger(text_browser: QTextBrowser):
    logger = logging.getLogger('performancetabletool')
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    gui_handler = QTextBrowserHandler(text_browser)
    gui_handler.setLevel(logging.INFO)
    gui_handler.setFormatter(formatter)
    logger.addHandler(gui_handler)

    file_handler = RotatingFileHandler(
        'performancetabletool.log', 
        maxBytes=1024 * 1024,  # 1MB
        backupCount=3,
        encoding='utf-8'
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger