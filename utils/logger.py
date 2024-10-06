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

    # 创建格式器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    gui_handler = QTextBrowserHandler(text_browser)
    gui_handler.setLevel(logging.INFO)
    gui_handler.setFormatter(formatter)
    logger.addHandler(gui_handler)

    file_handler = RotatingFileHandler(
        'performancetabletool.log', 
        maxBytes=1024 * 1024,  # 1MB
        backupCount=5
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger