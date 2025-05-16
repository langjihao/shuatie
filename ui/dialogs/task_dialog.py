#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
任务编辑对话框
"""

from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout,
    QLabel, QLineEdit, QDoubleSpinBox, QComboBox,
    QPushButton, QGroupBox, QRadioButton, QButtonGroup,
    QSpinBox
)
from PyQt5.QtCore import Qt


class TaskDialog(QDialog):
    """任务编辑对话框"""

    def __init__(self, parent=None, task_data=None):
        super().__init__(parent)

        self.task_data = task_data or {}
        self._init_ui()

    def _init_ui(self):
        """初始化UI"""
        self.setWindowTitle("编辑任务")
        self.setMinimumWidth(400)

        main_layout = QVBoxLayout(self)

        # 基本信息组
        basic_group = QGroupBox("基本信息")
        basic_layout = QFormLayout(basic_group)

        # 网址输入
        self.url_input = QLineEdit()
        self.url_input.setText(self.task_data.get('url', ''))
        basic_layout.addRow("网址:", self.url_input)

        # 等待时间
        self.wait_time = QDoubleSpinBox()
        self.wait_time.setRange(0, 20)
        self.wait_time.setSingleStep(0.5)
        self.wait_time.setDecimals(1)
        self.wait_time.setValue(self.task_data.get('wait_time', 2.0))
        self.wait_time.setSuffix(" 秒")
        basic_layout.addRow("等待时间:", self.wait_time)

        # 浏览时间
        self.browse_time = QDoubleSpinBox()
        self.browse_time.setRange(0, 30)
        self.browse_time.setSingleStep(0.5)
        self.browse_time.setDecimals(1)
        self.browse_time.setValue(self.task_data.get('browse_time', 5.0))
        self.browse_time.setSuffix(" 秒")
        basic_layout.addRow("浏览时间:", self.browse_time)

        # 滑动浏览
        self.scroll_enabled = QComboBox()
        self.scroll_enabled.addItems(["开启", "关闭"])
        self.scroll_enabled.setCurrentText("开启" if self.task_data.get('scroll_enabled', True) else "关闭")
        basic_layout.addRow("滑动浏览:", self.scroll_enabled)

        # 关闭等待时间
        self.close_wait_time = QDoubleSpinBox()
        self.close_wait_time.setRange(0, 120)
        self.close_wait_time.setSingleStep(0.5)
        self.close_wait_time.setDecimals(1)
        self.close_wait_time.setValue(self.task_data.get('close_wait_time', 1.0))
        self.close_wait_time.setSuffix(" 秒")
        basic_layout.addRow("关闭等待:", self.close_wait_time)

        main_layout.addWidget(basic_group)

        # 循环设置组
        loop_group = QGroupBox("循环设置")
        loop_layout = QVBoxLayout(loop_group)

        # 循环类型选择
        self.loop_type_group = QButtonGroup(self)
        
        type_layout = QHBoxLayout()
        
        self.time_radio = QRadioButton("按时间循环")
        self.time_radio.setChecked(self.task_data.get('loop_type', 'time') == 'time')
        self.loop_type_group.addButton(self.time_radio)
        type_layout.addWidget(self.time_radio)
        
        self.count_radio = QRadioButton("按次数循环")
        self.count_radio.setChecked(self.task_data.get('loop_type', 'time') == 'count')
        self.loop_type_group.addButton(self.count_radio)
        type_layout.addWidget(self.count_radio)
        
        loop_layout.addLayout(type_layout)

        # 循环参数
        params_layout = QFormLayout()
        
        # 循环时间
        self.loop_time = QSpinBox()
        self.loop_time.setRange(1, 1440)  # 最多24小时
        self.loop_time.setValue(self.task_data.get('loop_time', 60))
        self.loop_time.setSuffix(" 分钟")
        params_layout.addRow("循环时间:", self.loop_time)
        
        # 循环次数
        self.loop_count = QSpinBox()
        self.loop_count.setRange(1, 10000)
        self.loop_count.setValue(self.task_data.get('loop_count', 1))
        self.loop_count.setSuffix(" 次")
        params_layout.addRow("循环次数:", self.loop_count)
        
        loop_layout.addLayout(params_layout)
        
        main_layout.addWidget(loop_group)

        # 按钮
        button_layout = QHBoxLayout()
        button_layout.addStretch()

        self.ok_button = QPushButton("确定")
        self.ok_button.clicked.connect(self.accept)
        
        self.cancel_button = QPushButton("取消")
        self.cancel_button.clicked.connect(self.reject)

        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)

        main_layout.addLayout(button_layout)

        # 连接信号
        self.time_radio.toggled.connect(self._on_loop_type_changed)
        self.count_radio.toggled.connect(self._on_loop_type_changed)
        
        # 初始化控件状态
        self._on_loop_type_changed()

    def _on_loop_type_changed(self):
        """循环类型改变事件"""
        self.loop_time.setEnabled(self.time_radio.isChecked())
        self.loop_count.setEnabled(self.count_radio.isChecked())

    def get_task_data(self):
        """获取任务数据"""
        return {
            'url': self.url_input.text().strip(),
            'wait_time': self.wait_time.value(),
            'browse_time': self.browse_time.value(),
            'scroll_enabled': self.scroll_enabled.currentText() == "开启",
            'close_wait_time': self.close_wait_time.value(),
            'loop_type': 'time' if self.time_radio.isChecked() else 'count',
            'loop_time': self.loop_time.value(),
            'loop_count': self.loop_count.value()
        }