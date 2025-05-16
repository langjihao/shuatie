#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
高DPI样式表 - PyQt5版本
"""

def get_high_dpi_stylesheet():
    """获取高DPI样式表"""
    return """
    /* 全局样式 */
    QWidget {
        font-family: "Microsoft YaHei UI", "Microsoft YaHei", "Segoe UI", Arial;
        font-size: 14px;
    }

    /* 主窗口样式 */
    QMainWindow {
        min-width: 1280px;
        min-height: 720px;
    }

    /* 按钮样式 */
    QPushButton {
        min-height: 40px;
        min-width: 100px;
        padding: 8px 20px;
        border: none;
        border-radius: 6px;
        background-color: #f0f0f0;
        color: #333333;
    }

    QPushButton:hover {
        background-color: #e0e0e0;
    }

    QPushButton[primary=true] {
        background-color: #007bff;
        color: white;
    }

    QPushButton[primary=true]:hover {
        background-color: #0056b3;
    }

    /* 输入框样式 */
    QLineEdit, QTextEdit, QPlainTextEdit {
        min-height: 40px;
        padding: 8px 12px;
        border: 2px solid #ddd;
        border-radius: 6px;
        background-color: white;
    }

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border-color: #66afe9;
    }

    /* 标签页样式 */
    QTabWidget::pane {
        border: 1px solid #ddd;
        border-radius: 6px;
        padding: 15px;
    }

    QTabBar::tab {
        min-width: 160px;
        min-height: 40px;
        padding: 8px 16px;
        margin-right: 4px;
        border-top-left-radius: 6px;
        border-top-right-radius: 6px;
        background: #f8f9fa;
    }

    QTabBar::tab:selected {
        background: white;
        border-bottom: 3px solid #007bff;
    }

    /* 表格样式 */
    QTableView {
        gridline-color: #eee;
        selection-background-color: #e8f0fe;
    }

    QTableView::item {
        padding: 12px;
        min-height: 40px;
    }

    QHeaderView::section {
        padding: 12px;
        background-color: #f8f9fa;
        border: none;
        border-bottom: 2px solid #dee2e6;
        font-weight: bold;
        min-height: 40px;
    }

    /* 分组框样式 */
    QGroupBox {
        margin-top: 24px;
        font-weight: bold;
        border: 2px solid #ddd;
        border-radius: 8px;
        padding: 24px;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        left: 12px;
        padding: 0 8px;
    }

    /* 状态栏样式 */
    QStatusBar {
        background: #f8f9fa;
        min-height: 40px;
        padding: 0 16px;
    }
    """