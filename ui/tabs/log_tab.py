#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志显示标签页
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPlainTextEdit, QPushButton,
    QHBoxLayout, QFileDialog
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextCursor
from datetime import datetime


class LogTab(QWidget):
    """日志显示标签页"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self._init_ui()

    def _init_ui(self):
        """初始化UI"""
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        # 日志显示区域
        self.log_text = QPlainTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setMaximumBlockCount(5000)  # 限制最大行数
        self.log_text.setLineWrapMode(QPlainTextEdit.NoWrap)  # 不自动换行
        layout.addWidget(self.log_text)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)

        # 清空按钮
        self.clear_button = QPushButton("清空日志")
        self.clear_button.clicked.connect(self.clear_log)
        
        # 导出按钮
        self.export_button = QPushButton("导出日志")
        self.export_button.clicked.connect(self.export_log)
        
        button_layout.addStretch()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.export_button)
        
        layout.addLayout(button_layout)

    def append_log(self, message):
        """添加日志"""
        # 添加时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        # 添加日志并滚动到底部
        self.log_text.appendPlainText(formatted_message)
        self.log_text.moveCursor(QTextCursor.End)

    def clear_log(self):
        """清空日志"""
        self.log_text.clear()

    def export_log(self):
        """导出日志"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "导出日志",
            f"log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "文本文件 (*.txt)"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.toPlainText())
            except Exception as e:
                from ui.dialogs.message_box import HighDPIMessageBox
                HighDPIMessageBox.critical(self, "导出失败", f"导出日志失败：{str(e)}")