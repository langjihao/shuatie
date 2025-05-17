#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志显示标签页
"""

import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPlainTextEdit, QPushButton,
    QHBoxLayout, QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QTextCursor, QColor, QFont
from datetime import datetime


class LogTab(QWidget):
    """日志显示标签页"""
    
    # 定义用于更新UI的信号
    update_log_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        
        # 创建日志目录
        self.log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        os.makedirs(self.log_dir, exist_ok=True)
        
        # 初始化UI
        self._init_ui()
        
        # 连接信号到槽
        self.update_log_signal.connect(self._append_log_to_ui)

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
        
        # 设置字体
        font = QFont("Consolas", 10)  # 使用等宽字体
        self.log_text.setFont(font)
        
        # 设置样式
        self.log_text.setStyleSheet("""
            QPlainTextEdit {
                background-color: #1e1e1e;
                color: #d4d4d4;
                border: 1px solid #3c3c3c;
                selection-background-color: #264f78;
                selection-color: #ffffff;
            }
        """)
        
        # 优化性能
        self.log_text.setUndoRedoEnabled(False)  # 禁用撤销重做
        self.log_text.setCenterOnScroll(False)  # 禁用滚动居中
        
        layout.addWidget(self.log_text)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)

        # 清空按钮
        self.clear_button = QPushButton("清空日志")
        self.clear_button.clicked.connect(self.clear_log)
        self.clear_button.setStyleSheet("""
            QPushButton {
                padding: 5px 10px;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                background-color: #2d2d2d;
                color: #d4d4d4;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
        """)
        
        # 导出按钮
        self.export_button = QPushButton("导出日志")
        self.export_button.clicked.connect(self.export_log)
        self.export_button.setStyleSheet("""
            QPushButton {
                padding: 5px 10px;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                background-color: #2d2d2d;
                color: #d4d4d4;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
        """)
        
        button_layout.addStretch()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.export_button)
        
        layout.addLayout(button_layout)

    def append_log(self, message):
        """添加日志（从其他线程调用）"""
        try:
            # 添加时间戳
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_message = f"[{timestamp}] {message}"
            
            # 写入文件
            log_file = os.path.join(self.log_dir, f"log_{datetime.now().strftime('%Y%m%d')}.txt")
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(formatted_message + '\n')
            
            # 发送信号到主线程更新UI
            self.update_log_signal.emit(formatted_message)
            
        except Exception as e:
            print(f"写入日志失败: {str(e)}")
    
    def _append_log_to_ui(self, message):
        """在UI中添加日志（在主线程中执行）"""
        cursor = self.log_text.textCursor()
        cursor.movePosition(QTextCursor.End)
        cursor.insertText(message + '\n')
        
        # 滚动到底部
        self.log_text.setTextCursor(cursor)
        self.log_text.ensureCursorVisible()

    def clear_log(self):
        """清空日志"""
        self.log_text.clear()

    def export_log(self):
        """导出日志"""
        try:
            # 默认使用日期作为文件名
            default_filename = os.path.join(
                self.log_dir,
                f"log_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            )
            
            filename, _ = QFileDialog.getSaveFileName(
                self,
                "导出日志",
                default_filename,
                "文本文件 (*.txt)"
            )
            
            if filename:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.log_text.toPlainText())
        except Exception as e:
            from ui.dialogs.message_box import HighDPIMessageBox
            HighDPIMessageBox.critical(self, "导出失败", f"导出日志失败：{str(e)}")
                
    def showEvent(self, event):
        """显示事件"""
        super().showEvent(event)