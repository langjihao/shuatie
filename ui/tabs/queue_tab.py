#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
队列管理标签页
"""

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QGroupBox,
    QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
    QAbstractItemView, QLabel
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon


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

        # 创建队列组
        queue_group = QGroupBox("任务队列")
        queue_layout = QVBoxLayout(queue_group)
        queue_layout.setContentsMargins(15, 20, 15, 15)
        queue_layout.setSpacing(10)

        # 创建表格
        self.queue_table = QTableWidget()
        self.queue_table.setColumnCount(5)
        self.queue_table.setHorizontalHeaderLabels(["序号", "网址", "状态", "上次执行", "操作"])
        self.queue_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.queue_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.queue_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.queue_table.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.queue_table.verticalHeader().setVisible(False)

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

        # 上移按钮
        self.up_button = QPushButton("上移")
        self.up_button.setIcon(QIcon("resources/up.png"))
        self.up_button.setIconSize(QSize(16, 16))
        self.up_button.clicked.connect(self._on_move_up)

        # 下移按钮
        self.down_button = QPushButton("下移")
        self.down_button.setIcon(QIcon("resources/down.png"))
        self.down_button.setIconSize(QSize(16, 16))
        self.down_button.clicked.connect(self._on_move_down)

        # 清空按钮
        self.clear_button = QPushButton("清空队列")
        self.clear_button.clicked.connect(self._on_clear)

        # 添加按钮到布局
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.up_button)
        button_layout.addWidget(self.down_button)
        button_layout.addStretch()
        button_layout.addWidget(self.clear_button)

        # 添加按钮布局到队列布局
        queue_layout.addLayout(button_layout)

        # 创建统计组
        stats_group = QGroupBox("任务统计")
        stats_layout = QHBoxLayout(stats_group)
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
        main_layout.addWidget(queue_group)
        main_layout.addWidget(stats_group)

    def _on_add_task(self):
        """添加任务按钮点击事件"""
        from PyQt5.QtWidgets import QInputDialog, QMessageBox

        # 获取任务URL
        url, ok = QInputDialog.getText(self, "添加任务", "请输入网址:")

        if ok and url.strip():
            # 这里应该添加URL验证逻辑
            if not url.startswith(("http://", "https://")):
                url = "https://" + url

            # 添加到表格
            row_count = self.queue_table.rowCount()
            self.queue_table.insertRow(row_count)

            # 序号
            self.queue_table.setItem(row_count, 0, QTableWidgetItem(str(row_count + 1)))
            # 网址
            self.queue_table.setItem(row_count, 1, QTableWidgetItem(url))
            # 状态
            self.queue_table.setItem(row_count, 2, QTableWidgetItem("等待中"))
            # 上次执行
            self.queue_table.setItem(row_count, 3, QTableWidgetItem("--"))

            # 更新统计
            self._update_stats()

            QMessageBox.information(self, "添加成功", f"已添加任务: {url}")

    def _update_stats(self):
        """更新统计信息"""
        total = self.queue_table.rowCount()
        completed = 0
        failed = 0

        # 统计完成和失败的任务
        for row in range(total):
            status = self.queue_table.item(row, 2).text()
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
        from PyQt5.QtWidgets import QMessageBox

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
        from PyQt5.QtWidgets import QMessageBox

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
        from PyQt5.QtWidgets import QMessageBox

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
