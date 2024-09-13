from PyQt5.QtCore import QObject, pyqtSignal

class DataLoadedSignal(QObject):
    data_loaded = pyqtSignal(dict)

data_loaded_signal = DataLoadedSignal()
