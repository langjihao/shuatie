#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
主窗口
"""

import os
from PyQt5.QtWidgets import (
    QMainWindow, QTabWidget, QWidget, QVBoxLayout,
    QHBoxLayout, QLabel, QPushButton, QStatusBar, QTableWidgetItem, QCheckBox
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon

from ui.tabs.queue_tab import QueueTab
from ui.tabs.settings_tab import SettingsTab
from ui.dialogs.message_box import HighDPIMessageBox
from core.browser_controller import BrowserController
from ui.tabs.log_tab import LogTab


class MainWindow(QMainWindow):
    """主窗口"""

    def __init__(self, is_unlocked=False):
        super().__init__()

        # 设置解锁状态
        self.is_unlocked = is_unlocked

        # 创建浏览器控制器
        self.browser_controller = BrowserController()
        # 连接信号
        self.browser_controller.status_changed.connect(self._on_status_changed)
        self.browser_controller.log_message.connect(self._on_log_message)

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

        # 初始化标签页列表
        self.tabs = []

        # 添加队列标签页
        self.queue_tab = QueueTab(self)
        self.tab_widget.addTab(self.queue_tab, "队列管理")
        self.tabs.append(self.queue_tab)

        # 添加日志标签页
        self.log_tab = LogTab(self)
        self.tab_widget.addTab(self.log_tab, "运行日志")
        self.tabs.append(self.log_tab)

        # 添加设置标签页
        self.settings_tab = SettingsTab(self)
        self.settings_tab.unlocked_changed.connect(self.on_unlock_changed)
        self.tab_widget.addTab(self.settings_tab, "软件设置")
        self.tabs.append(self.settings_tab)

        # 添加标签页到主布局
        main_layout.addWidget(self.tab_widget)

        # 创建底部操作栏
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 0, 0, 0)
        bottom_layout.setSpacing(10)

        # 解锁状态标签
        self.unlock_status_label = QLabel()
        self.unlock_status_label.setStyleSheet("font-weight: bold;")

        # 无头模式选项
        self.headless_checkbox = QCheckBox("启用无头模式")
        self.headless_checkbox.setToolTip("启用后浏览器将在后台运行，不显示界面")

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
        bottom_layout.addWidget(self.headless_checkbox)
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
        self._update_ui_state()

    def _update_ui_state(self):
        """更新UI状态"""
        # 根据解锁状态启用/禁用相关功能
        for tab in self.tabs:
            if hasattr(tab, 'set_enabled'):
                tab.set_enabled(self.is_unlocked)
        
        # 更新菜单栏状态
        if hasattr(self, 'menu_bar'):
            self.menu_bar.setEnabled(self.is_unlocked)

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
                    'wait_time': float(self.queue_tab.queue_table.item(row, 2).text()),
                    'browse_time': float(self.queue_tab.queue_table.item(row, 3).text()),
                    'scroll_enabled': self.queue_tab.queue_table.item(row, 4).text() == "是",
                    'close_wait_time': float(self.queue_tab.queue_table.item(row, 5).text()),
                    'loop_type': 'time' if "时间" in self.queue_tab.queue_table.item(row, 6).text() else 'count',
                    'loop_time': int(self.queue_tab.queue_table.item(row, 6).text().split(":")[1].strip().replace("分钟", "")) if "时间" in self.queue_tab.queue_table.item(row, 6).text() else 60,
                    'loop_count': int(self.queue_tab.queue_table.item(row, 6).text().split(":")[1].strip().replace("次", "")) if "次数" in self.queue_tab.queue_table.item(row, 6).text() else 1,
                    'scroll_speed': self.queue_tab.scroll_speed.value(),
                    'random_click': self.queue_tab.random_click_checkbox.isChecked()
                })

        # 获取定时设置
        timer_settings = {
            'start_type': 'direct',  # 默认直接启动
            'countdown_hours': 0,
            'countdown_minutes': 0,
            'time_point': '00:00',
            'auto_shutdown': self.queue_tab.shutdown_checkbox.isChecked(),
            'shutdown_time': self.queue_tab.shutdown_time.value()
        }

        # 根据队列标签页的启动方式设置更新
        if self.queue_tab.countdown_radio.isChecked():
            timer_settings['start_type'] = 'countdown'
            timer_settings['countdown_hours'] = self.queue_tab.countdown_hours.value()
            timer_settings['countdown_minutes'] = self.queue_tab.countdown_minutes.value()
        elif self.queue_tab.timepoint_radio.isChecked():
            timer_settings['start_type'] = 'time_point'
            timer_settings['time_point'] = self.queue_tab.time_edit.time().toString('HH:mm')

        # 检查队列是否为空
        if not queue_data:
            HighDPIMessageBox.warning(self, "队列为空", "请先添加至少一个任务到队列中。")
            return

        try:
            # 设置无头模式
            self.browser_controller.set_headless(self.headless_checkbox.isChecked())
            
            # 启动浏览器控制器
            self.browser_controller.start(queue_data, timer_settings)

            # 更新UI状态
            self.status_bar.showMessage("正在运行...")
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            
            # 切换到日志标签页
            self.tab_widget.setCurrentWidget(self.log_tab)
        except Exception as e:
            HighDPIMessageBox.critical(self, "启动失败", f"启动浏览器失败: {str(e)}")
            self.status_bar.showMessage(f"启动失败: {str(e)}")

    def _on_status_changed(self, row, status):
        """处理状态变化信号"""
        if 0 <= row < self.queue_tab.queue_table.rowCount():
            # 设置状态列的文本和样式
            status_item = QTableWidgetItem(status)
            if status == "运行中":
                status_item.setForeground(Qt.green)
            elif status == "已完成":
                status_item.setForeground(Qt.blue)
            elif status == "失败":
                status_item.setForeground(Qt.red)
            self.queue_tab.queue_table.setItem(row, 7, status_item)

            # 更新任务统计信息
            self.queue_tab._update_stats()

            # 如果所有任务都完成了，启用开始按钮并禁用停止按钮
            completed = True
            for r in range(self.queue_tab.queue_table.rowCount()):
                item = self.queue_tab.queue_table.item(r, 7)
                if item and item.text() not in ["已完成", "失败"]:
                    completed = False
                    break

            if completed:
                self.start_button.setEnabled(True)
                self.stop_button.setEnabled(False)
                self.status_bar.showMessage("队列已完成一轮")

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

    def _on_log_message(self, message):
        """处理日志信息信号"""
        self.log_tab.append_log(message)
        self.status_bar.showMessage(message)

    def on_unlock_changed(self, is_unlocked):
        """处理解锁状态变化"""
        self.is_unlocked = is_unlocked
        self._update_unlock_status()


