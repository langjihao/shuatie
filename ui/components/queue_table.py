#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
队列表格组件
"""

from PySide6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView, 
    QPushButton, QHBoxLayout, QWidget, QAbstractItemView
)
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QIcon


class QueueTable(QTableWidget):
    """队列表格组件"""
    
    # 定义信号
    item_moved = Signal(int, int)  # 项目移动信号
    item_deleted = Signal(int)     # 项目删除信号
    item_edited = Signal(int)      # 项目编辑信号
    
    def __init__(self, parent=None, max_rows=10):
        super().__init__(parent)
        
        self.max_rows = max_rows
        
        # 设置表格属性
        self.setColumnCount(5)
        self.setRowCount(max_rows)
        self.setHorizontalHeaderLabels(["链接", "循环次数", "循环时间(秒)", "操作", "状态"])
        
        # 设置表格样式
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # 设置列宽
        # 链接列设置为自适应，但最小宽度为400像素
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)
        self.setColumnWidth(0, 600)  # 链接列宽度
        self.horizontalHeader().setMinimumSectionSize(400)  # 设置最小列宽
        
        # 其他列设置固定宽度
        self.horizontalHeader().setSectionResizeMode(1, QHeaderView.Fixed)    # 循环次数列固定宽度
        self.horizontalHeader().setSectionResizeMode(2, QHeaderView.Fixed)    # 循环时间列固定宽度
        self.horizontalHeader().setSectionResizeMode(3, QHeaderView.Fixed)    # 操作列固定宽度
        self.horizontalHeader().setSectionResizeMode(4, QHeaderView.Fixed)    # 状态列固定宽度
        
        # 优化各列宽度
        self.setColumnWidth(1, 120)  # 循环次数列宽
        self.setColumnWidth(2, 140)  # 循环时间列宽
        self.setColumnWidth(3, 160)  # 操作列宽
        self.setColumnWidth(4, 100)  # 状态列宽
        
        # 初始化表格
        self._init_table()
    
    def _init_table(self):
        """初始化表格"""
        # 为每一行添加操作按钮
        for row in range(self.max_rows):
            # 创建操作按钮容器
            button_widget = QWidget()
            button_layout = QHBoxLayout(button_widget)
            button_layout.setContentsMargins(2, 2, 2, 2)
            button_layout.setSpacing(5)
            
            # 上移按钮
            up_button = QPushButton()
            up_button.setIcon(QIcon("resources/up.png"))
            up_button.setToolTip("上移")
            up_button.setFixedSize(30, 30)
            up_button.clicked.connect(lambda _, r=row: self._on_move_up(r))
            
            # 下移按钮
            down_button = QPushButton()
            down_button.setIcon(QIcon("resources/down.png"))
            down_button.setToolTip("下移")
            down_button.setFixedSize(30, 30)
            down_button.clicked.connect(lambda _, r=row: self._on_move_down(r))
            
            # 编辑按钮
            edit_button = QPushButton()
            edit_button.setIcon(QIcon("resources/edit.png"))
            edit_button.setToolTip("编辑")
            edit_button.setFixedSize(30, 30)
            edit_button.clicked.connect(lambda _, r=row: self._on_edit(r))
            
            # 删除按钮
            delete_button = QPushButton()
            delete_button.setIcon(QIcon("resources/delete.png"))
            delete_button.setToolTip("删除")
            delete_button.setFixedSize(30, 30)
            delete_button.clicked.connect(lambda _, r=row: self._on_delete(r))
            
            # 添加按钮到布局
            button_layout.addWidget(up_button)
            button_layout.addWidget(down_button)
            button_layout.addWidget(edit_button)
            button_layout.addWidget(delete_button)
            
            # 设置布局对齐方式
            button_layout.setAlignment(Qt.AlignCenter)
            
            # 将按钮容器添加到表格
            self.setCellWidget(row, 3, button_widget)
            
            # 添加状态单元格
            status_item = QTableWidgetItem("未开始")
            status_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row, 4, status_item)
    
    def set_item(self, row, url, loop_count, loop_time):
        """设置表格项"""
        if row < 0 or row >= self.max_rows:
            return False
        
        # 设置链接
        url_item = QTableWidgetItem(url)
        url_item.setToolTip(url)
        self.setItem(row, 0, url_item)
        
        # 设置循环次数
        count_item = QTableWidgetItem(str(loop_count))
        count_item.setTextAlignment(Qt.AlignCenter)
        self.setItem(row, 1, count_item)
        
        # 设置循环时间
        time_item = QTableWidgetItem(str(loop_time))
        time_item.setTextAlignment(Qt.AlignCenter)
        self.setItem(row, 2, time_item)
        
        return True
    
    def get_item(self, row):
        """获取表格项"""
        if row < 0 or row >= self.max_rows:
            return None
        
        # 获取链接
        url_item = self.item(row, 0)
        url = url_item.text() if url_item else ""
        
        # 获取循环次数
        count_item = self.item(row, 1)
        loop_count = int(count_item.text()) if count_item and count_item.text().isdigit() else 0
        
        # 获取循环时间
        time_item = self.item(row, 2)
        loop_time = int(time_item.text()) if time_item and time_item.text().isdigit() else 0
        
        return {
            "url": url,
            "loop_count": loop_count,
            "loop_time": loop_time
        }
    
    def get_all_items(self):
        """获取所有表格项"""
        items = []
        for row in range(self.max_rows):
            item = self.get_item(row)
            if item and item["url"]:
                items.append(item)
        return items
    
    def clear_all(self):
        """清空所有表格项"""
        for row in range(self.max_rows):
            # 清空链接
            self.setItem(row, 0, QTableWidgetItem(""))
            
            # 清空循环次数
            count_item = QTableWidgetItem("0")
            count_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row, 1, count_item)
            
            # 清空循环时间
            time_item = QTableWidgetItem("0")
            time_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row, 2, time_item)
            
            # 重置状态
            status_item = QTableWidgetItem("未开始")
            status_item.setTextAlignment(Qt.AlignCenter)
            self.setItem(row, 4, status_item)
    
    def update_status(self, row, status):
        """更新状态"""
        if row < 0 or row >= self.max_rows:
            return
        
        status_item = QTableWidgetItem(status)
        status_item.setTextAlignment(Qt.AlignCenter)
        
        # 根据状态设置颜色
        if status == "运行中":
            status_item.setForeground(Qt.green)
        elif status == "已完成":
            status_item.setForeground(Qt.blue)
        elif status == "已跳过":
            status_item.setForeground(Qt.gray)
        elif status == "错误":
            status_item.setForeground(Qt.red)
        
        self.setItem(row, 4, status_item)
    
    def _on_move_up(self, row):
        """上移按钮点击事件"""
        if row <= 0:
            return
        
        # 交换数据
        current_item = self.get_item(row)
        above_item = self.get_item(row - 1)
        
        if current_item and current_item["url"]:
            self.set_item(row - 1, current_item["url"], current_item["loop_count"], current_item["loop_time"])
            
            if above_item and above_item["url"]:
                self.set_item(row, above_item["url"], above_item["loop_count"], above_item["loop_time"])
            else:
                self.set_item(row, "", 0, 0)
            
            # 发送信号
            self.item_moved.emit(row, row - 1)
    
    def _on_move_down(self, row):
        """下移按钮点击事件"""
        if row >= self.max_rows - 1:
            return
        
        # 交换数据
        current_item = self.get_item(row)
        below_item = self.get_item(row + 1)
        
        if current_item and current_item["url"]:
            self.set_item(row + 1, current_item["url"], current_item["loop_count"], current_item["loop_time"])
            
            if below_item and below_item["url"]:
                self.set_item(row, below_item["url"], below_item["loop_count"], below_item["loop_time"])
            else:
                self.set_item(row, "", 0, 0)
            
            # 发送信号
            self.item_moved.emit(row, row + 1)
    
    def _on_edit(self, row):
        """编辑按钮点击事件"""
        # 发送信号
        self.item_edited.emit(row)
    
    def _on_delete(self, row):
        """删除按钮点击事件"""
        # 清空当前行
        self.set_item(row, "", 0, 0)
        
        # 发送信号
        self.item_deleted.emit(row)