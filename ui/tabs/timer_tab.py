#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
定时设置标签页
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox, QRadioButton,
    QLabel, QSpinBox, QDoubleSpinBox, QTimeEdit, QCheckBox,
    QFormLayout, QPushButton
)
from PyQt5.QtCore import Qt, QTime


class TimerTab(QWidget):
    """定时设置标签页"""

    def __init__(self, parent=None):
        super().__init__(parent)

        # 获取主窗口引用
        self.main_window = parent

        # 初始化UI
        self._init_ui()

    def _init_ui(self):
        """初始化UI"""
        # 创建主布局
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(15)

        # 创建启动方式组
        self.start_group = QGroupBox("启动方式")
        start_layout = QVBoxLayout(self.start_group)
        start_layout.setContentsMargins(15, 20, 15, 15)
        start_layout.setSpacing(10)

        # 直接启动选项
        self.direct_radio = QRadioButton("直接启动")
        self.direct_radio.setChecked(True)
        self.direct_radio.toggled.connect(self._on_start_mode_changed)
        start_layout.addWidget(self.direct_radio)

        # 倒计时启动选项
        countdown_layout = QHBoxLayout()
        countdown_layout.setContentsMargins(0, 0, 0, 0)
        countdown_layout.setSpacing(5)

        self.countdown_radio = QRadioButton("倒计时启动：")
        self.countdown_radio.toggled.connect(self._on_start_mode_changed)

        self.countdown_hours = QSpinBox()
        self.countdown_hours.setRange(0, 24)
        self.countdown_hours.setValue(1)
        self.countdown_hours.setSingleStep(1)

        self.countdown_minutes = QSpinBox()
        self.countdown_minutes.setRange(0, 59)
        self.countdown_minutes.setValue(0)
        self.countdown_minutes.setSingleStep(1)

        countdown_layout.addWidget(self.countdown_radio)
        countdown_layout.addWidget(self.countdown_hours)
        countdown_layout.addWidget(QLabel("小时"))
        countdown_layout.addWidget(self.countdown_minutes)
        countdown_layout.addWidget(QLabel("分钟"))
        countdown_layout.addStretch()

        start_layout.addLayout(countdown_layout)

        # 定时启动选项
        timer_layout = QHBoxLayout()
        timer_layout.setContentsMargins(0, 0, 0, 0)
        timer_layout.setSpacing(5)

        self.timer_radio = QRadioButton("定时启动：")
        self.timer_radio.toggled.connect(self._on_start_mode_changed)

        self.timer_time = QTimeEdit()
        self.timer_time.setDisplayFormat("HH:mm")
        self.timer_time.setTime(QTime.currentTime().addSecs(3600))  # 默认设置为当前时间后1小时

        timer_layout.addWidget(self.timer_radio)
        timer_layout.addWidget(self.timer_time)
        timer_layout.addStretch()

        start_layout.addLayout(timer_layout)

        # 创建浏览器参数组
        self.browser_group = QGroupBox("浏览器参数")
        browser_layout = QFormLayout(self.browser_group)
        browser_layout.setContentsMargins(15, 20, 15, 15)
        browser_layout.setSpacing(10)

        # 打开链接后等待时间
        # self.open_wait_time = QDoubleSpinBox()
        # self.open_wait_time.setRange(0, 20)
        # self.open_wait_time.setValue(2)
        # self.open_wait_time.setSingleStep(0.5)
        # self.open_wait_time.setSuffix(" 秒")
        # browser_layout.addRow("打开链接后等待：", self.open_wait_time)

        # 页面滚动速度
        self.scroll_speed = QDoubleSpinBox()
        self.scroll_speed.setRange(0.1, 5)
        self.scroll_speed.setValue(1)
        self.scroll_speed.setSingleStep(0.1)
        self.scroll_speed.setSuffix(" 倍速")
        browser_layout.addRow("页面滚动速度：", self.scroll_speed)

        # 随机点击选项
        self.random_click_checkbox = QCheckBox("启用随机点击（模拟真实浏览）")
        browser_layout.addRow("", self.random_click_checkbox)

        # 添加组件到主布局
        main_layout.addWidget(self.start_group)
        main_layout.addWidget(self.browser_group)
        main_layout.addStretch()

    def _on_start_mode_changed(self):
        """启动方式改变事件"""
        # 更新控件状态
        self.countdown_hours.setEnabled(self.countdown_radio.isChecked())
        self.countdown_minutes.setEnabled(self.countdown_radio.isChecked())
        self.timer_time.setEnabled(self.timer_radio.isChecked())

    def set_enabled(self, enabled):
        """设置启用状态"""
        # 更新组标题
        self.start_group.setTitle("启动方式" if enabled else "")
        self.browser_group.setTitle("浏览器参数" if enabled else "")

        # 更新单选按钮文本
        self.direct_radio.setText("直接启动" if enabled else "")
        self.countdown_radio.setText("倒计时启动：" if enabled else "")
        self.timer_radio.setText("定时启动：" if enabled else "")
