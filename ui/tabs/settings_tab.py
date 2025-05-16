#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
设置标签页
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout,
    QLabel, QLineEdit, QPushButton, QCheckBox, QSpinBox, QMessageBox
)
from PyQt5.QtCore import Qt, pyqtSignal

from ui.dialogs.message_box import HighDPIMessageBox
from core.password_manager import PasswordManager


class SettingsTab(QWidget):
    """设置标签页"""

    unlocked_changed = pyqtSignal(bool)  # 添加信号

    def __init__(self, parent=None):
        super().__init__(parent)

        # 获取主窗口引用
        self.main_window = parent

        # 获取密码管理器
        self.password_manager = PasswordManager()

        # 初始化UI
        self._init_ui()

    def _init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)

        # 创建解锁组
        unlock_group = QGroupBox("软件解锁")
        unlock_layout = QFormLayout(unlock_group)
        unlock_layout.setContentsMargins(15, 20, 15, 15)
        unlock_layout.setSpacing(10)

        # 密码输入框
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_input.setPlaceholderText("请输入解锁密码")
        unlock_layout.addRow("解锁密码：", self.password_input)

        # 解锁按钮
        unlock_button_layout = QHBoxLayout()
        unlock_button_layout.setContentsMargins(0, 10, 0, 0)
        unlock_button_layout.setSpacing(10)

        self.unlock_button = QPushButton("解锁软件")
        self.unlock_button.clicked.connect(self._on_unlock)
        self.unlock_button.setProperty("primary", True)

        unlock_button_layout.addWidget(self.unlock_button)
        unlock_button_layout.addStretch()

        unlock_layout.addRow("", unlock_button_layout)

        # 密码提示
        # password_hint = QLabel(
        #     "密码规则：<br>"
        #     "1. 基于当天日期计算：年月日数字乘以2的后6位数<br>"
        #     "2. 如果解锁时间在当日中午12:00前（不含12:00），使用上述计算结果<br>"
        #     "3. 如果解锁时间在当日中午12:00后（含12:00），使用上述计算结果减去12"
        # )
        # password_hint.setWordWrap(True)
        # password_hint.setStyleSheet("color: #666; font-size: 9pt;")
        # unlock_layout.addRow("", password_hint)

        # 创建浏览器设置组
        self.browser_group = QGroupBox("浏览器设置")
        browser_layout = QFormLayout(self.browser_group)
        browser_layout.setContentsMargins(15, 20, 15, 15)
        browser_layout.setSpacing(10)

        # 无头模式选项
        self.headless_checkbox = QCheckBox("启用无头模式（不显示浏览器窗口）")
        browser_layout.addRow("", self.headless_checkbox)

        # 超时设置
        self.timeout_spinbox = QSpinBox()
        self.timeout_spinbox.setRange(10, 300)
        self.timeout_spinbox.setValue(60)
        self.timeout_spinbox.setSuffix(" 秒")
        browser_layout.addRow("页面加载超时：", self.timeout_spinbox)

        # 添加组件到主布局
        main_layout.addWidget(unlock_group)
        main_layout.addWidget(self.browser_group)
        main_layout.addStretch()

        # 更新UI状态
        self._update_ui_state()

    def _update_ui_state(self):
        """更新UI状态"""
        is_unlocked = self.password_manager.is_unlocked()

        if is_unlocked:
            self.unlock_button.setText("已解锁")
            self.unlock_button.setEnabled(False)
            self.password_input.setEnabled(False)
        else:
            self.unlock_button.setText("解锁软件")
            self.unlock_button.setEnabled(True)
            self.password_input.setEnabled(True)

    def _on_unlock(self):
        """解锁按钮点击事件"""
        password = self.password_input.text().strip()

        if not password:
            HighDPIMessageBox.warning(self, "输入错误", "请输入解锁密码。")
            return

        if not password.isdigit():
            HighDPIMessageBox.warning(self, "输入错误", "密码应为数字。")
            return

        print(f"解锁前状态: {self.password_manager.is_unlocked()}")
        if self.password_manager.verify_password(password):  # 修改这里，使用verify_password而不是unlock
            print(f"解锁后状态: {self.password_manager.is_unlocked()}")
            QMessageBox.information(self, "解锁成功", "软件已解锁！")
            self._update_ui_state()
            self.unlocked_changed.emit(True)  # 发送解锁信号
        else:
            QMessageBox.warning(self, "解锁失败", "密码错误！")

    def set_enabled(self, enabled):
        """设置启用状态"""
        # 仅更新浏览器设置组的标题和控件状态
        # 解锁组保持原样，因为它需要一直可用
        self.browser_group.setTitle("浏览器设置" if enabled else "")
        
        # 启用/禁用浏览器设置控件
        self.headless_checkbox.setEnabled(enabled)
        self.timeout_spinbox.setEnabled(enabled)
        self.timeout_spinbox.setPrefix("页面加载超时：" if enabled else "")