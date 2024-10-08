

# coding: utf-8
# Author: Roy.Luo
# Version: 1.0

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QBrush, QFont, QFontMetrics
from PyQt5.QtWidgets import QFileDialog, QTableWidgetItem, QListWidgetItem, QMenu, QAction, QTableWidget, QVBoxLayout, QDialog, QHeaderView

import pandas as pd

class DataFrameDialog(QDialog):
    def __init__(self, df, time_event_name, header_config, parent=None):
        super().__init__(parent)
        self.setWindowTitle("DataFrame Preview")
        self.setGeometry(100, 100, 1000, 600)

        layout = QVBoxLayout()
        self.table_widget = QTableWidget()
        layout.addWidget(self.table_widget)
        self.setLayout(layout)

        self.load_data(df, time_event_name, header_config)

    def load_data(self, df, time_event_name, header_config):
        # 重新排序列
        columns = ["name", "opt_min", "opt_nom", "opt_max", "min", "nom", "max", "NF_presence"]
        df = df.reindex(columns=[col for col in columns if col in df.columns])
        df = df.rename(columns={"name": "File Name"})
        # 根据 header_config 筛选列
        visible_columns = ["File Name"] if "File Name" in df.columns else []
        for section, columns in header_config.items():
            visible_columns.extend([col for col, visible in columns.items() if visible and col in df.columns])

        # 只选择DataFrame中实际存在的列
        df = df[[col for col in visible_columns if col in df.columns]]

        # 设置表格大小
        self.table_widget.setColumnCount(len(df.columns))
        self.table_widget.setRowCount(len(df.index) + 3)  # +3 for the header rows
        font = QFont("Arial", 8)
        self.table_widget.setFont(font)

        # 设置三级表头
        self.table_widget.setSpan(0, 0, 3, 1)  # "File Name" 列跨三行
        item = QTableWidgetItem("File Name")
        item.setFont(font)
        self.table_widget.setItem(0, 0, item)

        col_index = 1
        for section, columns in header_config.items():
            start_col = col_index
            for col, visible in columns.items():
                if visible and col in df.columns:
                    item = QTableWidgetItem(col)
                    item.setFont(font)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.table_widget.setItem(2, col_index, item)
                    col_index += 1
            if col_index > start_col:
                self.table_widget.setSpan(1, start_col, 1, col_index - start_col)
                item = QTableWidgetItem(section)
                item.setFont(font)
                item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(1, start_col, item)

        # 只有在有足够的列时才设置跨度
        if col_index > 1:
            self.table_widget.setSpan(0, 1, 1, col_index - 1)
            item = QTableWidgetItem(time_event_name)
            item.setFont(font)
            item.setTextAlignment(Qt.AlignCenter)
            self.table_widget.setItem(0, 1, item)

        # 填充数据
        for i, row in enumerate(df.itertuples(index=False)):
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setFont(font)
                if j > 0:  # 除了第一列（File Name）之外，其他列居中对齐
                    item.setTextAlignment(Qt.AlignCenter)
                self.table_widget.setItem(i + 3, j, item)

        # 优化列宽
        self.optimize_column_widths(df)

        # 设置表头样式
        self.table_widget.horizontalHeader().setVisible(False)
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setShowGrid(True)
        self.table_widget.setStyleSheet("QTableWidget::item { border: 1px solid black; }")

        # 设置所有列居中对齐，除了第一列
        for col in range(1, self.table_widget.columnCount()):
            self.table_widget.horizontalHeader().setDefaultAlignment(Qt.AlignCenter)

    def optimize_column_widths(self, df):
        font_metrics = QFontMetrics(self.table_widget.font())
        padding = 20  # 额外的padding，可以根据需要调整

        for col in range(self.table_widget.columnCount()):
            max_width = 0
            
            # 检查表头
            for row in range(3):  # 三行表头
                item = self.table_widget.item(row, col)
                if item:
                    width = font_metrics.width(item.text()) + padding
                    max_width = max(max_width, width)
            
            # 检查数据
            column_name = df.columns[col]
            for value in df[column_name].astype(str):
                width = font_metrics.width(value) + padding
                max_width = max(max_width, width)
            
            # 设置最小和最大宽度
            max_width = max(50, min(max_width, 300))  # 最小50，最大300
            self.table_widget.setColumnWidth(col, max_width)

class PerformanceTableDialog(QtWidgets.QDialog):
    def __init__(self, global_result, parent=None):
        super().__init__(parent)
        uic.loadUi('gui/toolsUI/performancetabledialog.ui', self)
        
        # 存储 global_result 对象
        self.global_result = global_result
        
        # 存储已拖拽的项目
        self.dragged_items = set()
        
        # 初始化对话框控件
        self.initialize_dialog()
        self.setup_drag_drop()
        self.setup_context_menu()
        self.listWidget_tmEvnt_raw.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)
        self.listWidget_tmEvnt_tb.setSelectionMode(QtWidgets.QAbstractItemView.ExtendedSelection)

        # 连接双击事件
        self.listWidget_tmEvnt_tb.itemDoubleClicked.connect(self.show_dataframe_preview)

    def initialize_dialog(self):
        # 初始化 "General Info" 部分信息
        self.comboBox_ptType.addItems(("Calibration","Immuinty"))
        self.comboBox_stdType.addItems(["Front", "Side", "Rear", "Rollover",""])
        self.comboBox_stdType.currentTextChanged.connect(self.update_calFlName_style)
        self.comboBox_stdType.setCurrentText(self.global_result.get_data()["GeneralInformation"].StudyType)
        self.update_calFlName_style()
        # 初始化 "Time Event" 部分信息
        categories = self.global_result.get_data()["TimeEventInformation_df"]["category"]
        unique_categories = set()
        for category in categories:
            unique_categories.update(category.split(','))
        self.comboBox_tmEvntFilt.addItems(sorted(unique_categories))
        self.comboBox_tmEvntFilt.currentTextChanged.connect(self.update_time_event_list)
        self.update_time_event_list()

        # 初始化 comboBox_prf 和 comboBox_mrg
        self.initialize_combo_boxes()

    def initialize_combo_boxes(self):
        multi_preprocessing_items = self.global_result.get_data()["MultiPreprocessingData"]
        names = [item.information.get('Name') for item in multi_preprocessing_items]
        # 更新 comboBox_prf
        self.comboBox_prf.clear()
        self.comboBox_prf.addItems(names)
        # 更新 comboBox_mrg
        self.comboBox_mrg.clear()
        self.comboBox_mrg.addItems(names)
        
    def update_time_event_list(self):
        self.listWidget_tmEvnt_raw.clear()
        df_timeEvent = self.global_result.get_data()["TimeEventInformation_df"]
        filter_text = self.comboBox_tmEvntFilt.currentText()
        df_timeEvent_filtered = df_timeEvent[df_timeEvent["category"].str.contains(filter_text, case=False, na=False)]
        for index in df_timeEvent_filtered.index:
            item = QListWidgetItem(index)
            if index in self.dragged_items:
                item.setBackground(QBrush(QColor(200, 200, 200)))  # 使用 QBrush
            self.listWidget_tmEvnt_raw.addItem(item)

    def update_calFlName_style(self):
        text = self.global_result.get_data()["GeneralInformation"].Calibration.split("\\")[-1]
        styled_text = text

        if self.comboBox_stdType.currentText() == "Front":
            styled_text = (
                text[:13] + 
                f'<span style="color: red;">{text[13:16]}</span>' + 
                text[16:]
            )
        elif self.comboBox_stdType.currentText() == "Side":
            styled_text = (
                text[:16] + 
                f'<span style="color: blue;">{text[16:19]}</span>' + 
                text[19:]
            )
        elif self.comboBox_stdType.currentText() == "Rear":
            styled_text = (
                text[:19] + 
                f'<span style="color: green;">{text[19:22]}</span>' + 
                text[22:]
            )
        elif self.comboBox_stdType.currentText() == "Rollover":
            styled_text = (
                text[:22] + 
                f'<span style="color: brown;">{text[22:25]}</span>' + 
                text[25:]
            )
        self.textEdit_calFlName.setHtml(styled_text)

    def setup_drag_drop(self):
        # 启用 listWidget_tmEvnt_raw 的拖拽
        self.listWidget_tmEvnt_raw.setDragEnabled(True)
        self.listWidget_tmEvnt_raw.setDragDropMode(QtWidgets.QAbstractItemView.DragOnly)

        # 启用 listWidget_tmEvnt_tb 接受拖拽和内部移动
        self.listWidget_tmEvnt_tb.setAcceptDrops(True)
        self.listWidget_tmEvnt_tb.setDragEnabled(True)
        self.listWidget_tmEvnt_tb.setDragDropMode(QtWidgets.QAbstractItemView.DragDrop)

        # 连接 listWidget_tmEvnt_tb 的 dropEvent
        self.listWidget_tmEvnt_tb.dropEvent = self.handle_drop_tb

    def handle_drop_tb(self, event):
        if event.source() == self.listWidget_tmEvnt_raw:
            # 如果是从 listWidget_tmEvnt_raw 拖放过来的，使用原有的处理方法
            self.handle_drop(event)
        else:
            # 如果是内部拖放，自定义处理方法
            self.handle_internal_drop(event)

    def handle_internal_drop(self, event):
        # 获取当前鼠标位置
        drop_position = event.pos()
        
        # 获取所有选中的项目
        selected_items = self.listWidget_tmEvnt_tb.selectedItems()
        if not selected_items:
            return

        # 获取目标位置的索引
        target_item = self.listWidget_tmEvnt_tb.itemAt(drop_position)
        if target_item is None:
            target_index = self.listWidget_tmEvnt_tb.count()
        else:
            target_index = self.listWidget_tmEvnt_tb.row(target_item)

        # 按照原始顺序排序选中的项目
        selected_items.sort(key=lambda x: self.listWidget_tmEvnt_tb.row(x))

        # 移除所有选中的项目
        removed_items = []
        for item in selected_items:
            row = self.listWidget_tmEvnt_tb.row(item)
            removed_items.append(self.listWidget_tmEvnt_tb.takeItem(row))

        # 插入移除的项目到新位置
        for i, item in enumerate(removed_items):
            self.listWidget_tmEvnt_tb.insertItem(target_index + i, item)

        # 重新选中移动后的项目
        for item in removed_items:
            item.setSelected(True)

        event.accept()

    def handle_drop(self, event):
        # 获取拖拽的项目
        source_widget = event.source()
        if source_widget == self.listWidget_tmEvnt_raw:
            selected_items = source_widget.selectedItems()
            for source_item in selected_items:
                item_text = source_item.text()
                
                # 检查项目是否已经存在于目标列表中
                items = self.listWidget_tmEvnt_tb.findItems(item_text, Qt.MatchExactly)
                if not items:  # 如果项目不存在，则添加
                    # 创建新项目并添加到目标列表
                    new_item = QListWidgetItem(item_text)
                    self.listWidget_tmEvnt_tb.addItem(new_item)

                    # 将原项目底色置灰
                    source_item.setBackground(QBrush(QColor(200, 200, 200)))  # 使用 QBrush

                    # 将项目添加到已拖拽集合中
                    self.dragged_items.add(item_text)

            event.accept()
        else:
            event.ignore()

    def setup_context_menu(self):
        self.listWidget_tmEvnt_tb.setContextMenuPolicy(Qt.CustomContextMenu)
        self.listWidget_tmEvnt_tb.customContextMenuRequested.connect(self.show_context_menu)

    def show_context_menu(self, position):
        context_menu = QMenu(self)
        delete_action = QAction("Remove selected", self)
        delete_action.triggered.connect(self.remove_selected_items)
        context_menu.addAction(delete_action)

        # 添加 "Remove all" 选项
        remove_all_action = QAction("Remove all", self)
        remove_all_action.triggered.connect(self.remove_all_items)
        context_menu.addAction(remove_all_action)
        
        # 显示菜单
        context_menu.exec_(self.listWidget_tmEvnt_tb.mapToGlobal(position))

    def remove_selected_items(self):
        selected_items = self.listWidget_tmEvnt_tb.selectedItems()
        if not selected_items:
            return
        
        for item in selected_items:
            row = self.listWidget_tmEvnt_tb.row(item)
            removed_item = self.listWidget_tmEvnt_tb.takeItem(row)
            
            # 从已拖拽集合中移除
            if removed_item.text() in self.dragged_items:
                self.dragged_items.remove(removed_item.text())
            
            # 在 listWidget_tmEvnt_raw 中恢复项目的背景色
            items_in_raw = self.listWidget_tmEvnt_raw.findItems(removed_item.text(), Qt.MatchExactly)
            if items_in_raw:
                items_in_raw[0].setBackground(QBrush())  # 使用空的 QBrush 来清除背景

        # 更新 listWidget_tmEvnt_raw 的显示
        self.update_time_event_list()

    def remove_all_items(self):
        # 清空 listWidget_tmEvnt_tb
        self.listWidget_tmEvnt_tb.clear()
        
        # 恢复 listWidget_tmEvnt_raw 中所有项目的背景色
        for i in range(self.listWidget_tmEvnt_raw.count()):
            item = self.listWidget_tmEvnt_raw.item(i)
            item.setBackground(QBrush())  # 使用空的 QBrush 来清除背景
        
        # 清空已拖拽集合
        self.dragged_items.clear()
        
        # 更新 listWidget_tmEvnt_raw 的显示
        self.update_time_event_list()

    def show_dataframe_preview(self, item):
        if not isinstance(item, QtWidgets.QListWidgetItem):
            QtWidgets.QMessageBox.warning(self, "错误", "无效的项目类型")
            return

        selected_prf = self.comboBox_prf.currentText()
        time_event_name = item.text()
        multi_preprocessing_items = self.global_result.get_data()["MultiPreprocessingData"]
        
        selected_item = next((mpi for mpi in multi_preprocessing_items if mpi.information.get('Name') == selected_prf), None)
        
        if selected_item:
            if time_event_name in selected_item.performance_study.time_events_dict:
                df = selected_item.performance_study.time_events_dict[time_event_name]
                if isinstance(df, pd.DataFrame):
                    header_config = self.get_header_config()
                    dialog = DataFrameDialog(df, time_event_name, header_config, self)
                    dialog.exec_()
                else:
                    QtWidgets.QMessageBox.warning(self, "错误", f"{time_event_name} 的数据不是有效的 DataFrame")
            else:
                QtWidgets.QMessageBox.warning(self, "错误", f"未找到 {time_event_name} 的数据")
        else:
            QtWidgets.QMessageBox.warning(self, "错误", f"未找到 {selected_prf} 的数据")

    def get_header_config(self):
        return {
            "RTTF": {
                "opt_min": self.checkBox_Rmin.isChecked(),
                "opt_nom": self.checkBox_Rnom.isChecked(),
                "opt_max": self.checkBox_Rmax.isChecked()
            },
            "Calibration Performance": {
                "min": self.checkBox_prfmin.isChecked(),
                "nom": self.checkBox_prfnom.isChecked(),
                "max": self.checkBox_prfmax.isChecked(),
                "NF_presence": self.checkBox_prfnfrate.isChecked()
            },
            "Margin": {
                self.comboBox_prf.currentText(): True,
                "Gain": self.checkBox_mrggain.isChecked()
            }
        }