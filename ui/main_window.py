#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主窗口
"""

import os
from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QStatusBar
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from ui.tabs.queue_tab import QueueTab
from ui.tabs.timer_tab import TimerTab
from ui.tabs.settings_tab import SettingsTab
from ui.dialogs.message_box import HighDPIMessageBox
from core.browser_controller import BrowserController


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, is_unlocked=False):
        super().__init__()

        # 设置解锁状态
        self.is_unlocked = is_unlocked

        # 创建浏览器控制器
        self.browser_controller = BrowserController()

        # 初始化UI
        self._init_ui()

    def _init_ui(self):
        """初始化UI"""
        # 设置窗口标题和大小
        self.setWindowTitle("自动化浏览器操作软件")
        self.setMinimumSize(800, 600)

        # 设置窗口图标
        if os.path.exists("resources/icon.png"):
            self.setWindowIcon(QIcon("resources/icon.png"))

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建主布局
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)

        # 创建标签页
        self.tab_widget = QTabWidget()
        self.tab_widget.setTabPosition(QTabWidget.North)
        self.tab_widget.setDocumentMode(True)

        # 添加队列标签页
        self.queue_tab = QueueTab(self)
        self.tab_widget.addTab(self.queue_tab, "队列管理")

        # 添加定时标签页
        self.timer_tab = TimerTab(self)
        self.tab_widget.addTab(self.timer_tab, "定时设置")

        # 添加设置标签页
        self.settings_tab = SettingsTab(self)
        self.tab_widget.addTab(self.settings_tab, "软件设置")

        # 添加标签页到主布局
        main_layout.addWidget(self.tab_widget)

        # 创建底部操作栏
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(10)

        # 解锁状态标签
        self.unlock_status_label = QLabel()
        self.unlock_status_label.setStyleSheet("font-weight: bold;")

        # 开始按钮
        self.start_button = QPushButton("开始任务")
        self.start_button.setIcon(QIcon("resources/start.png"))
        self.start_button.setIconSize(QSize(16, 16))
        self.start_button.setProperty("primary", True)
        self.start_button.setMinimumWidth(120)
        self.start_button.clicked.connect(self._on_start)

        # 停止按钮
        self.stop_button = QPushButton("停止任务")
        self.stop_button.setIcon(QIcon("resources/stop.png"))
        self.stop_button.setIconSize(QSize(16, 16))
        self.stop_button.setEnabled(False)
        self.stop_button.setMinimumWidth(120)
        self.stop_button.clicked.connect(self._on_stop)

        # 添加组件到底部布局
        bottom_layout.addWidget(self.unlock_status_label)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.start_button)
        bottom_layout.addWidget(self.stop_button)

        # 添加底部布局到主布局
        main_layout.addLayout(bottom_layout)

        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("就绪")

        # 更新解锁状态
        self._update_unlock_status()

    def _update_unlock_status(self):
        """更新解锁状态"""
        if self.is_unlocked:
            self.unlock_status_label.setText("状态：已解锁")
            self.unlock_status_label.setStyleSheet("color: green; font-weight: bold;")
        else:
            self.unlock_status_label.setText("状态：未解锁（功能受限）")
            self.unlock_status_label.setStyleSheet("color: red; font-weight: bold;")

    def _on_start(self):
        """开始按钮点击事件"""
        if not self.is_unlocked:
            HighDPIMessageBox.warning(self, "未解锁", "请先解锁软件再使用此功能。")
            return

        # 获取队列数据
        queue_data = []
        for row in range(self.queue_tab.queue_table.rowCount()):
            url = self.queue_tab.queue_table.item(row, 1).text()
            if url:
                queue_data.append({
                    'url': url,
                    'wait_time': 2.0,  # 默认等待时间
                    'browse_time': 5.0,  # 默认浏览时间
                    'scroll_enabled': True,  # 默认启用滚动
                    'close_wait_time': 1.0  # 默认关闭后等待时间
                })

        # 获取定时设置
        timer_settings = {
            'start_type': 'direct',  # 默认直接启动
            'countdown_hours': 0,
            'countdown_minutes': 0,
            'time_point': '00:00',
            'auto_shutdown': False
        }

        # 根据定时标签页的设置更新
        if self.timer_tab.countdown_radio.isChecked():
            timer_settings['start_type'] = 'countdown'
            timer_settings['countdown_hours'] = self.timer_tab.countdown_hours.value()
            timer_settings['countdown_minutes'] = self.timer_tab.countdown_minutes.value()
        elif self.timer_tab.timer_radio.isChecked():
            timer_settings['start_type'] = 'time_point'
            timer_settings['time_point'] = self.timer_tab.timer_time.time().toString('HH:mm')

        # 检查队列是否为空
        if not queue_data:
            HighDPIMessageBox.warning(self, "队列为空", "请先添加至少一个任务到队列中。")
            return

        try:
            # 启动浏览器控制器
            self.browser_controller.start(queue_data, timer_settings)

            # 更新UI状态
            self.status_bar.showMessage("正在运行...")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
        except Exception as e:
            HighDPIMessageBox.critical(self, "启动失败", f"启动浏览器失败: {str(e)}")
            self.status_bar.showMessage(f"启动失败: {str(e)}")

    def _on_stop(self):
        """停止按钮点击事件"""
        try:
            # 停止浏览器控制器
            self.browser_controller.stop()

            # 更新UI状态
            self.status_bar.showMessage("已停止")
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
        except Exception as e:
            HighDPIMessageBox.critical(self, "停止失败", f"停止浏览器失败: {str(e)}")
            self.status_bar.showMessage(f"停止失败: {str(e)}")

    def _on_settings(self):
        """设置按钮点击事件"""
        # 切换到设置标签页
        self.tab_widget.setCurrentWidget(self.settings_tab)

    def _on_help(self):
        """帮助按钮点击事件"""
        HighDPIMessageBox.information(self, "帮助", "这是一个自动化浏览器操作软件，可以帮助您自动执行浏览器任务。")


