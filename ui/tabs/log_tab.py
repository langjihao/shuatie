#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志显示标签页
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPlainTextEdit, QPushButton,
    QHBoxLayout, QFileDialog
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QTextCursor, QTextOption
from datetime import datetime


class LogTab(QWidget):
    """日志显示标签页"""
    
    MAX_BUFFER_SIZE = 100  # 缓冲区大小
    UPDATE_INTERVAL = 500  # 更新间隔(毫秒)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.log_buffer = []  # 日志缓冲区
        self.auto_scroll = True  # 是否自动滚动
        
        # 创建定时器
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._flush_buffer)
        self.update_timer.start(self.UPDATE_INTERVAL)
        
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
        
        # 优化性能
        self.log_text.setUndoRedoEnabled(False)  # 禁用撤销重做
        self.log_text.document().setDefaultTextOption(QTextOption(Qt.AlignLeft))  # 设置左对齐
        self.log_text.setCenterOnScroll(False)  # 禁用滚动居中
        
        # 监听滚动条变化
        self.log_text.verticalScrollBar().valueChanged.connect(self._on_scroll)
        
        layout.addWidget(self.log_text)

        # 按钮区域
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)

        # 自动滚动复选框
        self.auto_scroll_checkbox = QPushButton("自动滚动")
        self.auto_scroll_checkbox.setCheckable(True)
        self.auto_scroll_checkbox.setChecked(True)
        self.auto_scroll_checkbox.clicked.connect(self._toggle_auto_scroll)

        # 清空按钮
        self.clear_button = QPushButton("清空日志")
        self.clear_button.clicked.connect(self.clear_log)
        
        # 导出按钮
        self.export_button = QPushButton("导出日志")
        self.export_button.clicked.connect(self.export_log)
        
        button_layout.addWidget(self.auto_scroll_checkbox)
        button_layout.addStretch()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.export_button)
        
        layout.addLayout(button_layout)

    def append_log(self, message):
        """添加日志"""
        # 添加时间戳
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        
        # 添加到缓冲区
        self.log_buffer.append(formatted_message)
        
        # 如果缓冲区满了，立即刷新
        if len(self.log_buffer) >= self.MAX_BUFFER_SIZE:
            self._flush_buffer()
    
    def _flush_buffer(self):
        """刷新缓冲区"""
        if not self.log_buffer:
            return
            
        # 开始一个文本块
        cursor = self.log_text.textCursor()
        cursor.beginEditBlock()
        
        try:
            # 一次性添加所有日志
            self.log_text.appendPlainText('\n'.join(self.log_buffer))
            
            # 如果开启了自动滚动，移动到底部
            if self.auto_scroll:
                scrollbar = self.log_text.verticalScrollBar()
                scrollbar.setValue(scrollbar.maximum())
        finally:
            # 结束文本块
            cursor.endEditBlock()
            
        # 清空缓冲区
        self.log_buffer.clear()
    
    def _toggle_auto_scroll(self, checked):
        """切换自动滚动"""
        self.auto_scroll = checked
        if checked:
            # 立即滚动到底部
            scrollbar = self.log_text.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
    
    def _on_scroll(self, value):
        """滚动条值改变时的处理"""
        scrollbar = self.log_text.verticalScrollBar()
        # 如果用户手动滚动到底部，自动开启自动滚动
        if value == scrollbar.maximum():
            self.auto_scroll = True
            self.auto_scroll_checkbox.setChecked(True)
        # 如果用户向上滚动，关闭自动滚动
        elif self.auto_scroll and value < scrollbar.maximum():
            self.auto_scroll = False
            self.auto_scroll_checkbox.setChecked(False)

    def clear_log(self):
        """清空日志"""
        self.log_buffer.clear()
        self.log_text.clear()

    def export_log(self):
        """导出日志"""
        # 先刷新缓冲区
        self._flush_buffer()
        
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
                
    def hideEvent(self, event):
        """隐藏事件"""
        # 停止定时器
        self.update_timer.stop()
        super().hideEvent(event)
        
    def showEvent(self, event):
        """显示事件"""
        # 启动定时器
        self.update_timer.start(self.UPDATE_INTERVAL)
        super().showEvent(event)