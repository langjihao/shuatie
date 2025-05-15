#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
队列管理UI
"""

from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QGridLayout,
                            QLabel, QLineEdit, QSpinBox, QDoubleSpinBox,
                            QComboBox, QPushButton, QGroupBox, QScrollArea,
                            QFrame, QRadioButton, QButtonGroup)
from PyQt5.QtCore import Qt


class QueueItem(QFrame):
    """队列项目组件"""
    
    def __init__(self, index, is_unlocked=False, parent=None):
        super().__init__(parent)
        
        self.index = index
        self.is_unlocked = is_unlocked
        
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        self.setFrameShape(QFrame.StyledPanel)
        
        layout = QGridLayout(self)
        
        # 序号标签
        index_label = QLabel(f"序号 {self.index}:")
        layout.addWidget(index_label, 0, 0)
        
        # URL输入框
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("请输入网页链接")
        layout.addWidget(self.url_input, 0, 1, 1, 3)
        
        # 循环类型选择
        self.loop_type_group = QButtonGroup(self)
        
        self.time_radio = QRadioButton("循环时间")
        self.time_radio.setChecked(True)
        self.loop_type_group.addButton(self.time_radio)
        layout.addWidget(self.time_radio, 1, 0)
        
        self.count_radio = QRadioButton("循环次数")
        self.loop_type_group.addButton(self.count_radio)
        layout.addWidget(self.count_radio, 1, 1)
        
        # 循环时间设置
        self.time_spinbox = QSpinBox()
        self.time_spinbox.setRange(1, 1440)  # 最多24小时（1440分钟）
        self.time_spinbox.setSuffix(" 分钟")
        layout.addWidget(self.time_spinbox, 1, 2)
        
        # 循环次数设置
        self.count_spinbox = QSpinBox()
        self.count_spinbox.setRange(1, 10000)
        self.count_spinbox.setSuffix(" 次")
        self.count_spinbox.setEnabled(False)
        layout.addWidget(self.count_spinbox, 1, 3)
        
        # 连接信号
        self.time_radio.toggled.connect(self.toggle_loop_type)
        self.count_radio.toggled.connect(self.toggle_loop_type)
        
        # 如果未解锁，隐藏标签文本
        if not self.is_unlocked:
            index_label.setText("")
            self.time_radio.setText("")
            self.count_radio.setText("")
    
    def toggle_loop_type(self, checked):
        """切换循环类型"""
        self.time_spinbox.setEnabled(self.time_radio.isChecked())
        self.count_spinbox.setEnabled(self.count_radio.isChecked())
    
    def get_data(self):
        """获取数据"""
        return {
            'index': self.index,
            'url': self.url_input.text().strip(),
            'loop_type': 'time' if self.time_radio.isChecked() else 'count',
            'loop_time': self.time_spinbox.value(),
            'loop_count': self.count_spinbox.value()
        }
    
    def set_data(self, data):
        """设置数据"""
        if 'url' in data:
            self.url_input.setText(data['url'])
        
        if 'loop_type' in data:
            if data['loop_type'] == 'time':
                self.time_radio.setChecked(True)
            else:
                self.count_radio.setChecked(True)
        
        if 'loop_time' in data:
            self.time_spinbox.setValue(data['loop_time'])
        
        if 'loop_count' in data:
            self.count_spinbox.setValue(data['loop_count'])
    
    def set_unlocked(self, unlocked):
        """设置解锁状态"""
        self.is_unlocked = unlocked
        
        # 更新标签文本
        layout = self.layout()
        index_label = layout.itemAtPosition(0, 0).widget()
        
        if unlocked:
            index_label.setText(f"序号 {self.index}:")
            self.time_radio.setText("循环时间")
            self.count_radio.setText("循环次数")
        else:
            index_label.setText("")
            self.time_radio.setText("")
            self.count_radio.setText("")


class QueueManagerWidget(QWidget):
    """队列管理组件"""
    
    def __init__(self, is_unlocked=False, parent=None):
        super().__init__(parent)
        
        self.is_unlocked = is_unlocked
        self.queue_items = []
        
        self.init_ui()
    
    def init_ui(self):
        """初始化UI"""
        main_layout = QVBoxLayout(self)
        
        # 浏览设置组
        browse_group = QGroupBox("浏览设置" if self.is_unlocked else "")
        browse_layout = QGridLayout(browse_group)
        
        # 默认等待时间
        wait_label = QLabel("打开链接后默认等待时间:" if self.is_unlocked else "")
        browse_layout.addWidget(wait_label, 0, 0)
        
        self.wait_spinbox = QDoubleSpinBox()
        self.wait_spinbox.setRange(0, 20)
        self.wait_spinbox.setSingleStep(0.5)
        self.wait_spinbox.setSuffix(" 秒")
        browse_layout.addWidget(self.wait_spinbox, 0, 1)
        
        # 浏览时间
        browse_time_label = QLabel("默认浏览时间:" if self.is_unlocked else "")
        browse_layout.addWidget(browse_time_label, 0, 2)
        
        self.browse_time_spinbox = QDoubleSpinBox()
        self.browse_time_spinbox.setRange(0, 30)
        self.browse_time_spinbox.setSingleStep(0.5)
        self.browse_time_spinbox.setSuffix(" 秒")
        browse_layout.addWidget(self.browse_time_spinbox, 0, 3)
        
        # 滑动浏览开关
        scroll_label = QLabel("滑动浏览:" if self.is_unlocked else "")
        browse_layout.addWidget(scroll_label, 1, 0)
        
        self.scroll_combo = QComboBox()
        self.scroll_combo.addItems(["开启", "关闭"])
        browse_layout.addWidget(self.scroll_combo, 1, 1)
        
        # 关闭后等待时间
        close_wait_label = QLabel("关闭后等待时间:" if self.is_unlocked else "")
        browse_layout.addWidget(close_wait_label, 1, 2)
        
        self.close_wait_spinbox = QDoubleSpinBox()
        self.close_wait_spinbox.setRange(0, 120)
        self.close_wait_spinbox.setSingleStep(0.5)
        self.close_wait_spinbox.setSuffix(" 秒")
        browse_layout.addWidget(self.close_wait_spinbox, 1, 3)
        
        main_layout.addWidget(browse_group)
        
        # 队列项目
        queue_group = QGroupBox("链接队列" if self.is_unlocked else "")
        queue_layout = QVBoxLayout(queue_group)
        
        # 使用滚动区域
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        
        scroll_content = QWidget()
        self.queue_layout = QVBoxLayout(scroll_content)
        
        # 创建队列项目
        max_queue = 10 if self.is_unlocked else 1
        for i in range(1, max_queue + 1):
            queue_item = QueueItem(i, self.is_unlocked)
            self.queue_items.append(queue_item)
            self.queue_layout.addWidget(queue_item)
        
        scroll_area.setWidget(scroll_content)
        queue_layout.addWidget(scroll_area)
        
        main_layout.addWidget(queue_group)
    
    def get_queue_data(self):
        """获取队列数据"""
        queue_data = []
        
        for item in self.queue_items:
            data = item.get_data()
            if data['url']:  # 只添加有URL的项目
                data['wait_time'] = self.wait_spinbox.value()
                data['browse_time'] = self.browse_time_spinbox.value()
                data['scroll_enabled'] = self.scroll_combo.currentText() == "开启"
                data['close_wait_time'] = self.close_wait_spinbox.value()
                queue_data.append(data)
        
        return queue_data
    
    def set_unlocked(self, unlocked):
        """设置解锁状态"""
        self.is_unlocked = unlocked
        
        # 更新组标题
        layout = self.layout()
        browse_group = layout.itemAt(0).widget()
        queue_group = layout.itemAt(1).widget()
        
        browse_group.setTitle("浏览设置" if unlocked else "")
        queue_group.setTitle("链接队列" if unlocked else "")
        
        # 更新标签
        browse_layout = browse_group.layout()
        browse_layout.itemAtPosition(0, 0).widget().setText("打开链接后默认等待时间:" if unlocked else "")
        browse_layout.itemAtPosition(0, 2).widget().setText("默认浏览时间:" if unlocked else "")
        browse_layout.itemAtPosition(1, 0).widget().setText("滑动浏览:" if unlocked else "")
        browse_layout.itemAtPosition(1, 2).widget().setText("关闭后等待时间:" if unlocked else "")
        
        # 更新队列项目
        for item in self.queue_items:
            item.set_unlocked(unlocked)
        
        # 如果解锁，添加更多队列项目
        if unlocked and len(self.queue_items) == 1:
            for i in range(2, 11):
                queue_item = QueueItem(i, unlocked)
                self.queue_items.append(queue_item)
                self.queue_layout.addWidget(queue_item)
