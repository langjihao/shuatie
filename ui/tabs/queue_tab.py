#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
队列管理标签页
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QLabel, QMessageBox, QFormLayout, QDoubleSpinBox,
    QCheckBox, QButtonGroup, QRadioButton, QSpinBox, QTimeEdit
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from ui.dialogs.task_dialog import TaskDialog


class QueueTab(QWidget):
    """队列管理标签页"""

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

        # 创建浏览器参数组
        browser_group = QGroupBox("浏览器参数")
        browser_layout = QFormLayout(browser_group)
        browser_layout.setContentsMargins(15, 20, 15, 15)
        browser_layout.setSpacing(10)

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

        main_layout.addWidget(browser_group)

        # 创建队列组
        self.queue_group = QGroupBox("任务队列")
        queue_layout = QVBoxLayout(self.queue_group)
        queue_layout.setContentsMargins(15, 20, 15, 15)
        queue_layout.setSpacing(10)

        # 创建表格
        self.queue_table = QTableWidget()
        self.queue_table.setColumnCount(8)
        self.queue_table.setHorizontalHeaderLabels([
            "序号", "网址", "等待时间(秒)", "浏览时间(秒)", 
            "滑动浏览", "关闭等待(秒)", "循环设置", "状态"
        ])
        self.queue_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.queue_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.queue_table.setEditTriggers(QAbstractItemView.DoubleClicked)
        self.queue_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.queue_table.verticalHeader().setVisible(False)

        # 设置列宽
        self.queue_table.setColumnWidth(0, 60)  # 序号
        self.queue_table.setColumnWidth(2, 100)  # 等待时间
        self.queue_table.setColumnWidth(3, 100)  # 浏览时间
        self.queue_table.setColumnWidth(4, 80)  # 滑动浏览
        self.queue_table.setColumnWidth(5, 100)  # 关闭等待
        self.queue_table.setColumnWidth(6, 120)  # 循环设置
        self.queue_table.setColumnWidth(7, 80)  # 状态

        # 添加表格到布局
        queue_layout.addWidget(self.queue_table)

        # 创建按钮布局
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.setSpacing(10)

        # 添加按钮
        self.add_button = QPushButton("添加任务")
        self.add_button.setIcon(QIcon("resources/add.png"))
        self.add_button.setIconSize(QSize(16, 16))
        self.add_button.clicked.connect(self._on_add_task)

        # 编辑按钮
        self.edit_button = QPushButton("编辑任务")
        self.edit_button.setIcon(QIcon("resources/edit.png"))
        self.edit_button.setIconSize(QSize(16, 16))
        self.edit_button.clicked.connect(self._on_edit_task)

        # 删除按钮
        self.delete_button = QPushButton("删除任务")
        self.delete_button.setIcon(QIcon("resources/delete.png"))
        self.delete_button.setIconSize(QSize(16, 16))
        self.delete_button.clicked.connect(self._on_delete_task)

        # 清空按钮
        self.clear_button = QPushButton("清空队列")
        self.clear_button.clicked.connect(self._on_clear)

        # 添加按钮到布局
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addStretch()
        button_layout.addWidget(self.clear_button)

        # 添加按钮布局到队列布局
        queue_layout.addLayout(button_layout)

        # 创建统计组
        self.stats_group = QGroupBox("任务统计")
        stats_layout = QHBoxLayout(self.stats_group)
        stats_layout.setContentsMargins(15, 20, 15, 15)
        stats_layout.setSpacing(30)

        # 总任务数
        self.total_tasks_label = QLabel("总任务数: 0")
        self.total_tasks_label.setStyleSheet("font-weight: bold;")

        # 已完成任务
        self.completed_tasks_label = QLabel("已完成: 0")
        self.completed_tasks_label.setStyleSheet("color: green; font-weight: bold;")

        # 失败任务
        self.failed_tasks_label = QLabel("失败: 0")
        self.failed_tasks_label.setStyleSheet("color: red; font-weight: bold;")

        # 添加标签到统计布局
        stats_layout.addWidget(self.total_tasks_label)
        stats_layout.addWidget(self.completed_tasks_label)
        stats_layout.addWidget(self.failed_tasks_label)
        stats_layout.addStretch()

        # 添加组件到主布局
        main_layout.addWidget(self.queue_group)
        main_layout.addWidget(self.stats_group)

        # 创建启动方式组
        start_group = QGroupBox("启动方式")
        start_layout = QHBoxLayout(start_group)
        start_layout.setContentsMargins(15, 20, 15, 15)
        start_layout.setSpacing(10)

        # 启动方式选择
        self.start_type_group = QButtonGroup(self)
        
        # 直接启动
        self.direct_radio = QRadioButton("直接启动")
        self.direct_radio.setChecked(True)
        self.start_type_group.addButton(self.direct_radio)
        start_layout.addWidget(self.direct_radio)
        
        # 倒计时启动
        countdown_layout = QHBoxLayout()
        self.countdown_radio = QRadioButton("倒计时启动")
        self.start_type_group.addButton(self.countdown_radio)
        countdown_layout.addWidget(self.countdown_radio)
        
        self.countdown_hours = QSpinBox()
        self.countdown_hours.setRange(0, 24)
        self.countdown_hours.setSuffix(" 小时")
        self.countdown_hours.setEnabled(False)
        countdown_layout.addWidget(self.countdown_hours)
        
        self.countdown_minutes = QSpinBox()
        self.countdown_minutes.setRange(0, 59)
        self.countdown_minutes.setSuffix(" 分钟")
        self.countdown_minutes.setEnabled(False)
        countdown_layout.addWidget(self.countdown_minutes)
        start_layout.addLayout(countdown_layout)
        
        # 时间点启动
        timepoint_layout = QHBoxLayout()
        self.timepoint_radio = QRadioButton("时间点启动")
        self.start_type_group.addButton(self.timepoint_radio)
        timepoint_layout.addWidget(self.timepoint_radio)
        
        self.time_edit = QTimeEdit()
        self.time_edit.setDisplayFormat("HH:mm")
        self.time_edit.setEnabled(False)
        timepoint_layout.addWidget(self.time_edit)
        start_layout.addLayout(timepoint_layout)

        # 添加自动关机选项
        self.shutdown_checkbox = QCheckBox("任务完成后自动关机")
        self.shutdown_time = QSpinBox()
        self.shutdown_time.setRange(1, 30)
        self.shutdown_time.setValue(5)
        self.shutdown_time.setSuffix(" 分钟")
        self.shutdown_time.setEnabled(False)
        start_layout.addWidget(self.shutdown_checkbox)
        start_layout.addWidget(self.shutdown_time)
        
        start_layout.addStretch()

        # 连接信号
        self.direct_radio.toggled.connect(self._on_start_mode_changed)
        self.countdown_radio.toggled.connect(self._on_start_mode_changed)
        self.timepoint_radio.toggled.connect(self._on_start_mode_changed)
        self.shutdown_checkbox.toggled.connect(lambda checked: self.shutdown_time.setEnabled(checked))

        # 添加启动方式组到主布局
        main_layout.addWidget(start_group)

        # 更新启用状态
        self.set_enabled(self.main_window.is_unlocked if hasattr(self.main_window, 'is_unlocked') else True)

    def _on_add_task(self):
        """添加任务按钮点击事件"""
        dialog = TaskDialog(self)
        if dialog.exec_() == TaskDialog.Accepted:
            task_data = dialog.get_task_data()
            
            # 验证URL
            if not task_data['url']:
                QMessageBox.warning(self, "输入错误", "请输入网址！")
                return
                
            if not task_data['url'].startswith(("http://", "https://")):
                task_data['url'] = "https://" + task_data['url']

            # 添加到表格
            row_count = self.queue_table.rowCount()
            self.queue_table.insertRow(row_count)
            
            # 更新表格内容
            self.queue_table.setItem(row_count, 0, QTableWidgetItem(str(row_count + 1)))
            self.queue_table.setItem(row_count, 1, QTableWidgetItem(task_data['url']))
            self.queue_table.setItem(row_count, 2, QTableWidgetItem(f"{task_data['wait_time']:.1f}"))
            self.queue_table.setItem(row_count, 3, QTableWidgetItem(f"{task_data['browse_time']:.1f}"))
            self.queue_table.setItem(row_count, 4, QTableWidgetItem("是" if task_data['scroll_enabled'] else "否"))
            self.queue_table.setItem(row_count, 5, QTableWidgetItem(f"{task_data['close_wait_time']:.1f}"))
            
            # 创建循环设置显示文本
            if task_data['loop_type'] == 'time':
                loop_text = f"时间: {task_data['loop_time']}分钟"
            else:
                loop_text = f"次数: {task_data['loop_count']}次"
            self.queue_table.setItem(row_count, 6, QTableWidgetItem(loop_text))
            
            # 设置状态
            self.queue_table.setItem(row_count, 7, QTableWidgetItem("等待中"))

            # 更新统计
            self._update_stats()

    def _on_edit_task(self):
        """编辑任务按钮点击事件"""
        current_row = self.queue_table.currentRow()
        if current_row < 0:
            QMessageBox.information(self, "提示", "请先选择要编辑的任务")
            return

        # 获取当前任务数据
        current_data = {
            'url': self.queue_table.item(current_row, 1).text(),
            'wait_time': float(self.queue_table.item(current_row, 2).text()),
            'browse_time': float(self.queue_table.item(current_row, 3).text()),
            'scroll_enabled': self.queue_table.item(current_row, 4).text() == "是",
            'close_wait_time': float(self.queue_table.item(current_row, 5).text()),
            'loop_type': 'time' if "时间" in self.queue_table.item(current_row, 6).text() else 'count',
            'loop_time': int(self.queue_table.item(current_row, 6).text().split(":")[1].strip().replace("分钟", "")) if "时间" in self.queue_table.item(current_row, 6).text() else 60,
            'loop_count': int(self.queue_table.item(current_row, 6).text().split(":")[1].strip().replace("次", "")) if "次数" in self.queue_table.item(current_row, 6).text() else 1
        }

        # 打开编辑对话框
        dialog = TaskDialog(self, current_data)
        if dialog.exec_() == TaskDialog.Accepted:
            task_data = dialog.get_task_data()
            
            # 验证URL
            if not task_data['url']:
                QMessageBox.warning(self, "输入错误", "请输入网址！")
                return
                
            if not task_data['url'].startswith(("http://", "https://")):
                task_data['url'] = "https://" + task_data['url']

            # 更新表格内容
            self.queue_table.setItem(current_row, 1, QTableWidgetItem(task_data['url']))
            self.queue_table.setItem(current_row, 2, QTableWidgetItem(f"{task_data['wait_time']:.1f}"))
            self.queue_table.setItem(current_row, 3, QTableWidgetItem(f"{task_data['browse_time']:.1f}"))
            self.queue_table.setItem(current_row, 4, QTableWidgetItem("是" if task_data['scroll_enabled'] else "否"))
            self.queue_table.setItem(current_row, 5, QTableWidgetItem(f"{task_data['close_wait_time']:.1f}"))
            
            # 创建循环设置显示文本
            if task_data['loop_type'] == 'time':
                loop_text = f"时间: {task_data['loop_time']}分钟"
            else:
                loop_text = f"次数: {task_data['loop_count']}次"
            self.queue_table.setItem(current_row, 6, QTableWidgetItem(loop_text))
            
            # 重置状态
            self.queue_table.setItem(current_row, 7, QTableWidgetItem("等待中"))

    def _on_delete_task(self):
        """删除任务按钮点击事件"""
        # 获取当前选中行
        current_row = self.queue_table.currentRow()

        if current_row < 0:
            QMessageBox.information(self, "提示", "未选中任务")
            return

        # 确认删除
        reply = QMessageBox.question(
            self,
            "确认删除",
            "确定要删除选中的任务吗？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.queue_table.removeRow(current_row)

            # 更新序号
            for row in range(self.queue_table.rowCount()):
                self.queue_table.setItem(row, 0, QTableWidgetItem(str(row + 1)))

            # 更新统计
            self._update_stats()

    def _update_stats(self):
        """更新统计信息"""
        total = self.queue_table.rowCount()
        completed = 0
        failed = 0

        # 统计完成和失败的任务
        for row in range(total):
            status = self.queue_table.item(row, 7).text()
            if status == "已完成":
                completed += 1
            elif status == "失败":
                failed += 1

        # 更新标签
        self.total_tasks_label.setText(f"总任务数: {total}")
        self.completed_tasks_label.setText(f"已完成: {completed}")
        self.failed_tasks_label.setText(f"失败: {failed}")

    def _on_move_up(self):
        """上移按钮点击事件"""
        # 获取当前选中行
        current_row = self.queue_table.currentRow()

        # 检查是否选中行以及是否可以上移
        if current_row <= 0:
            QMessageBox.information(self, "提示", "已经是第一行或未选中任务")
            return

        # 交换当前行和上一行的数据
        for col in range(self.queue_table.columnCount()):
            current_item = self.queue_table.takeItem(current_row, col)
            above_item = self.queue_table.takeItem(current_row - 1, col)

            self.queue_table.setItem(current_row - 1, col, current_item)
            self.queue_table.setItem(current_row, col, above_item)

        # 更新序号
        self.queue_table.setItem(current_row - 1, 0, QTableWidgetItem(str(current_row)))
        self.queue_table.setItem(current_row, 0, QTableWidgetItem(str(current_row + 1)))

        # 选中移动后的行
        self.queue_table.setCurrentCell(current_row - 1, 0)

    def _on_move_down(self):
        """下移按钮点击事件"""
        # 获取当前选中行
        current_row = self.queue_table.currentRow()

        # 检查是否选中行以及是否可以下移
        if current_row < 0 or current_row >= self.queue_table.rowCount() - 1:
            QMessageBox.information(self, "提示", "已经是最后一行或未选中任务")
            return

        # 交换当前行和下一行的数据
        for col in range(self.queue_table.columnCount()):
            current_item = self.queue_table.takeItem(current_row, col)
            below_item = self.queue_table.takeItem(current_row + 1, col)

            self.queue_table.setItem(current_row + 1, col, current_item)
            self.queue_table.setItem(current_row, col, below_item)

        # 更新序号
        self.queue_table.setItem(current_row + 1, 0, QTableWidgetItem(str(current_row + 1)))
        self.queue_table.setItem(current_row, 0, QTableWidgetItem(str(current_row + 2)))

        # 选中移动后的行
        self.queue_table.setCurrentCell(current_row + 1, 0)

    def _on_clear(self):
        """清空按钮点击事件"""
        # 确认是否清空
        reply = QMessageBox.question(
            self,
            "确认清空",
            "确定要清空所有任务吗？此操作不可恢复。",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            # 清空表格
            self.queue_table.setRowCount(0)

            # 更新统计
            self._update_stats()

            QMessageBox.information(self, "已清空", "所有任务已清空")

    def set_enabled(self, enabled):
        """设置启用状态"""
        # 更新表格标题
        self.queue_group.setTitle("任务队列" if enabled else "")
        self.stats_group.setTitle("任务统计" if enabled else "")
        
        # 启用/禁用功能按钮
        self.add_button.setEnabled(enabled)
        self.edit_button.setEnabled(enabled)
        self.delete_button.setEnabled(enabled)
        self.clear_button.setEnabled(enabled)

    def _on_start_mode_changed(self):
        """启动方式改变事件"""
        self.countdown_hours.setEnabled(self.countdown_radio.isChecked())
        self.countdown_minutes.setEnabled(self.countdown_radio.isChecked())
        self.time_edit.setEnabled(self.timepoint_radio.isChecked())
