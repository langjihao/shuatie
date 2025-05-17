#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志显示标签页
"""

import os
from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QPlainTextEdit, QPushButton,
    QHBoxLayout, QFileDialog, QScrollBar
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QTextCursor, QTextOption, QColor, QFont
from datetime import datetime


class LogTab(QWidget):
    """日志显示标签页"""
    
    MAX_BUFFER_SIZE = 50  # 减小缓冲区大小以提高响应速度
    UPDATE_INTERVAL = 100  # 提高更新频率到100ms
    MAX_LOG_SIZE = 1000000  # 最大日志大小（字符数）

    def __init__(self, parent=None):
        super().__init__(parent)
        self.main_window = parent
        self.log_buffer = []  # 日志缓冲区
        self.auto_scroll = True  # 是否自动滚动
        self.last_scroll_position = 0  # 记录上次滚动位置
        
        # 创建日志文件目录
        self.log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'logs')
        os.makedirs(self.log_dir, exist_ok=True)
        
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
        self.log_text.document().setDefaultTextOption(QTextOption(Qt.AlignLeft))  # 设置左对齐
        self.log_text.setCenterOnScroll(False)  # 禁用滚动居中
        self.log_text.setMaximumBlockCount(5000)  # 限制最大行数
        
        # 优化滚动条
        scrollbar = self.log_text.verticalScrollBar()
        scrollbar.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: #2c2c2c;
                width: 14px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #4c4c4c;
                min-height: 20px;
                border-radius: 7px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        scrollbar.valueChanged.connect(self._on_scroll)
        
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
        self.auto_scroll_checkbox.setStyleSheet("""
            QPushButton {
                padding: 5px 10px;
                border: 1px solid #3c3c3c;
                border-radius: 4px;
                background-color: #2d2d2d;
                color: #d4d4d4;
            }
            QPushButton:checked {
                background-color: #0e639c;
                border-color: #1177bb;
            }
            QPushButton:hover {
                background-color: #3c3c3c;
            }
        """)

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
        
        button_layout.addWidget(self.auto_scroll_checkbox)
        button_layout.addStretch()
        button_layout.addWidget(self.clear_button)
        button_layout.addWidget(self.export_button)
        
        layout.addLayout(button_layout)

    def append_log(self, message):
        """添加日志"""
        try:
            # 添加时间戳
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_message = f"[{timestamp}] {message}"
            
            # 添加到缓冲区
            self.log_buffer.append(formatted_message)
            
            # 同时写入文件
            log_file = os.path.join(self.log_dir, f"log_{datetime.now().strftime('%Y%m%d')}.txt")
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(formatted_message + '\n')
            
            # 如果缓冲区满了，立即刷新
            if len(self.log_buffer) >= self.MAX_BUFFER_SIZE:
                self._flush_buffer()
                
        except Exception as e:
            print(f"写入日志失败: {str(e)}")
    
    def _flush_buffer(self):
        """刷新缓冲区"""
        if not self.log_buffer:
            return
            
        try:
            # 开始一个文本块
            cursor = self.log_text.textCursor()
            cursor.beginEditBlock()
            
            # 检查是否需要清理旧日志
            if len(self.log_text.toPlainText()) > self.MAX_LOG_SIZE:
                # 保留后半部分的日志
                text = self.log_text.toPlainText()
                self.log_text.setPlainText(text[len(text)//2:])
            
            # 记录当前滚动条位置
            scrollbar = self.log_text.verticalScrollBar()
            current_value = scrollbar.value()
            max_value = scrollbar.maximum()
            
            # 一次性添加所有日志
            self.log_text.appendPlainText('\n'.join(self.log_buffer))
            
            # 根据自动滚动状态决定是否滚动到底部
            if self.auto_scroll:
                scrollbar.setValue(scrollbar.maximum())
            else:
                # 如果用户正在查看历史记录，保持相对位置
                if current_value < max_value:
                    new_value = int(current_value * scrollbar.maximum() / max_value)
                    scrollbar.setValue(new_value)
            
            # 结束文本块
            cursor.endEditBlock()
            
            # 清空缓冲区
            self.log_buffer.clear()
            
        except Exception as e:
            print(f"刷新日志缓冲区失败: {str(e)}")
    
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
        
        # 检测滚动方向
        scrolling_down = value > self.last_scroll_position
        self.last_scroll_position = value
        
        # 如果滚动到底部或接近底部，启用自动滚动
        if scrolling_down and value >= scrollbar.maximum() - 10:
            self.auto_scroll = True
            self.auto_scroll_checkbox.setChecked(True)
        # 如果向上滚动且启用了自动滚动，则禁用它
        elif not scrolling_down and self.auto_scroll:
            self.auto_scroll = False
            self.auto_scroll_checkbox.setChecked(False)

    def clear_log(self):
        """清空日志"""
        self.log_buffer.clear()
        self.log_text.clear()

    def export_log(self):
        """导出日志"""
        try:
            # 先刷新缓冲区
            self._flush_buffer()
            
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
                
    def hideEvent(self, event):
        """隐藏事件"""
        # 停止定时器
        self.update_timer.stop()
        # 确保缓冲区中的日志被保存
        self._flush_buffer()
        super().hideEvent(event)
        
    def showEvent(self, event):
        """显示事件"""
        # 启动定时器
        self.update_timer.start(self.UPDATE_INTERVAL)
        super().showEvent(event)