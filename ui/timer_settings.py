#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
定时设置UI
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QLabel, QSpinBox, QDoubleSpinBox, QTimeEdit,
                            QRadioButton, QButtonGroup, QGroupBox, QCheckBox)
from PyQt5.QtCore import Qt, QTime


class TimerSettingsWidget(QWidget):
    """定时设置组件"""
    
    def __init__(self, is_unlocked=False, parent=None):
        super().__init__(parent)
        
        self.is_unlocked = is_unlocked
        
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout(self)
        
        # 启动方式组
        start_group = QGroupBox("启动方式" if self.is_unlocked else "")
        start_layout = QVBoxLayout(start_group)
        
        # 启动方式选择
        self.start_type_group = QButtonGroup(self)
        
        self.direct_radio = QRadioButton("直接启动" if self.is_unlocked else "")
        self.direct_radio.setChecked(True)
        self.start_type_group.addButton(self.direct_radio)
        start_layout.addWidget(self.direct_radio)
        
        # 倒计时启动
        countdown_layout = QHBoxLayout()
        
        self.countdown_radio = QRadioButton("倒计时启动" if self.is_unlocked else "")
        self.start_type_group.addButton(self.countdown_radio)
        countdown_layout.addWidget(self.countdown_radio)
        
        self.countdown_hours_spinbox = QSpinBox()
        self.countdown_hours_spinbox.setRange(0, 24)
        self.countdown_hours_spinbox.setSuffix(" 小时")
        self.countdown_hours_spinbox.setEnabled(False)
        countdown_layout.addWidget(self.countdown_hours_spinbox)
        
        self.countdown_minutes_spinbox = QSpinBox()
        self.countdown_minutes_spinbox.setRange(0, 59)
        self.countdown_minutes_spinbox.setSuffix(" 分钟")
        self.countdown_minutes_spinbox.setEnabled(False)
        countdown_layout.addWidget(self.countdown_minutes_spinbox)
        
        start_layout.addLayout(countdown_layout)
        
        # 时间点启动
        time_point_layout = QHBoxLayout()
        
        self.time_point_radio = QRadioButton("时间点启动" if self.is_unlocked else "")
        self.start_type_group.addButton(self.time_point_radio)
        time_point_layout.addWidget(self.time_point_radio)
        
        self.time_point_edit = QTimeEdit()
        self.time_point_edit.setDisplayFormat("HH:mm")
        self.time_point_edit.setEnabled(False)
        time_point_layout.addWidget(self.time_point_edit)
        
        start_layout.addLayout(time_point_layout)
        
        main_layout.addWidget(start_group)
        
        # 自动关机设置
        shutdown_group = QGroupBox("自动关机设置" if self.is_unlocked else "")
        shutdown_layout = QHBoxLayout(shutdown_group)
        
        self.shutdown_checkbox = QCheckBox("队列执行完毕后自动关机" if self.is_unlocked else "")
        shutdown_layout.addWidget(self.shutdown_checkbox)
        
        shutdown_time_label = QLabel("关机倒计时:" if self.is_unlocked else "")
        shutdown_layout.addWidget(shutdown_time_label)
        
        self.shutdown_time_spinbox = QSpinBox()
        self.shutdown_time_spinbox.setRange(1, 30)
        self.shutdown_time_spinbox.setValue(5)
        self.shutdown_time_spinbox.setSuffix(" 分钟")
        self.shutdown_time_spinbox.setEnabled(False)
        shutdown_layout.addWidget(self.shutdown_time_spinbox)
        
        shutdown_layout.addStretch()
        
        main_layout.addWidget(shutdown_group)
        
        # 连接信号
        self.direct_radio.toggled.connect(self.toggle_start_type)
        self.countdown_radio.toggled.connect(self.toggle_start_type)
        self.time_point_radio.toggled.connect(self.toggle_start_type)
        self.shutdown_checkbox.toggled.connect(self.toggle_shutdown)
        
        main_layout.addStretch()
    
    def toggle_start_type(self, checked):
        """切换启动类型"""
        self.countdown_hours_spinbox.setEnabled(self.countdown_radio.isChecked())
        self.countdown_minutes_spinbox.setEnabled(self.countdown_radio.isChecked())
        self.time_point_edit.setEnabled(self.time_point_radio.isChecked())
    
    def toggle_shutdown(self, checked):
        """切换自动关机设置"""
        self.shutdown_time_spinbox.setEnabled(checked)
    
    def get_settings(self):
        """获取设置"""
        start_type = 'direct'
        if self.countdown_radio.isChecked():
            start_type = 'countdown'
        elif self.time_point_radio.isChecked():
            start_type = 'time_point'
        
        return {
            'start_type': start_type,
            'countdown_hours': self.countdown_hours_spinbox.value(),
            'countdown_minutes': self.countdown_minutes_spinbox.value(),
            'time_point': self.time_point_edit.time().toString("HH:mm"),
            'auto_shutdown': self.shutdown_checkbox.isChecked(),
            'shutdown_time': self.shutdown_time_spinbox.value()
        }
    
    def set_unlocked(self, unlocked):
        """设置解锁状态"""
        self.is_unlocked = unlocked
        
        # 更新组标题
        layout = self.layout()
        start_group = layout.itemAt(0).widget()
        shutdown_group = layout.itemAt(1).widget()
        
        start_group.setTitle("启动方式" if unlocked else "")
        shutdown_group.setTitle("自动关机设置" if unlocked else "")
        
        # 更新标签
        self.direct_radio.setText("直接启动" if unlocked else "")
        self.countdown_radio.setText("倒计时启动" if unlocked else "")
        self.time_point_radio.setText("时间点启动" if unlocked else "")
        self.shutdown_checkbox.setText("队列执行完毕后自动关机" if unlocked else "")
        
        shutdown_layout = shutdown_group.layout()
        shutdown_time_label = shutdown_layout.itemAt(1).widget()
        shutdown_time_label.setText("关机倒计时:" if unlocked else "")
