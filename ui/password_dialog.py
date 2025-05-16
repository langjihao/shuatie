#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
密码对话框UI
"""

import os
from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon


class PasswordDialog(QDialog):
    """密码对话框"""
    
    def __init__(self, password_manager, parent=None):
        super().__init__(parent)
        
        self.password_manager = password_manager
        
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("软件解锁")
        self.setFixedSize(400, 220)
        self.setStyleSheet("""
            QDialog {
                background-color: white;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
            }
            QLineEdit {
                padding: 8px;
                border: 1px solid #dddddd;
                border-radius: 4px;
                font-size: 14px;
                min-height: 36px;
            }
            QLineEdit:focus {
                border: 1px solid #80bdff;
            }
            QPushButton {
                min-width: 100px;
                min-height: 36px;
                padding: 8px 16px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton#okButton {
                background-color: #007bff;
                color: white;
                border: none;
            }
            QPushButton#okButton:hover {
                background-color: #0069d9;
            }
            QPushButton#cancelButton {
                background-color: #f8f9fa;
                border: 1px solid #ddd;
                color: #333;
            }
            QPushButton#cancelButton:hover {
                background-color: #e2e6ea;
            }
            #infoLabel {
                color: #666666;
                font-size: 12px;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(15)
        
        # Logo或图标
        icon_label = QLabel()
        if os.path.exists("resources/lock.png"):
            icon_label.setPixmap(QIcon("resources/lock.png").pixmap(48, 48))
        icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # 提示标签
        info_label = QLabel("请输入解锁密码:")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        # 密码输入框
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("请输入密码")
        self.password_input.setMaxLength(6)  # 限制最大长度为6位
        layout.addWidget(self.password_input)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        button_layout.setSpacing(10)
        
        self.ok_button = QPushButton("确定")
        self.ok_button.setObjectName("okButton")
        self.ok_button.clicked.connect(self.verify_password)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.setObjectName("cancelButton")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        # 提示信息
        hint_label = QLabel("提示: 密码为6位动态数字")
        hint_label.setObjectName("infoLabel")
        hint_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint_label)
        
        # 设置回车键触发确定按钮
        self.password_input.returnPressed.connect(self.verify_password)
    
    def verify_password(self):
        """验证密码"""
        password = self.password_input.text().strip()
        
        if not password:
            QMessageBox.warning(self, "错误", "请输入密码")
            return
        
        if not password.isdigit() or len(password) != 6:
            QMessageBox.warning(self, "错误", "密码必须是6位数字")
            self.password_input.clear()
            return
        
        if self.password_manager.verify_password(password):
            self.accept()
        else:
            QMessageBox.warning(self, "错误", "密码错误，请重试")
            self.password_input.clear()
            self.password_input.setFocus()
