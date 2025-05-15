#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
密码对话框UI
"""

from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt


class PasswordDialog(QDialog):
    """密码对话框"""
    
    def __init__(self, password_manager, parent=None):
        super().__init__(parent)
        
        self.password_manager = password_manager
        
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setWindowTitle("软件解锁")
        self.setFixedSize(300, 150)
        
        layout = QVBoxLayout(self)
        
        # 提示标签
        info_label = QLabel("请输入解锁密码:")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        # 密码输入框
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("请输入密码")
        layout.addWidget(self.password_input)
        
        # 按钮布局
        button_layout = QHBoxLayout()
        
        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.verify_password)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        
        layout.addLayout(button_layout)
        
        # 提示信息
        hint_label = QLabel("提示: 密码基于当天日期计算")
        hint_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(hint_label)
    
    def verify_password(self):
        """验证密码"""
        password = self.password_input.text().strip()
        
        if not password:
            QMessageBox.warning(self, "错误", "请输入密码")
            return
        
        if self.password_manager.verify_password(password):
            self.accept()
        else:
            QMessageBox.warning(self, "错误", "密码错误，请重试")
            self.password_input.clear()
            self.password_input.setFocus()
