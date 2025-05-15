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
        font-family: "Microsoft YaHei", "Segoe UI", Arial;
        font-size: 10pt;
    }

    /* 按钮样式 */
    QPushButton {
        min-height: 32px;
        padding: 6px 12px;
        background-color: #f0f0f0;
        border: 1px solid #c0c0c0;
        border-radius: 4px;
    }

    QPushButton:hover {
        background-color: #e0e0e0;
    }

    QPushButton:pressed {
        background-color: #d0d0d0;
    }

    QPushButton:disabled {
        background-color: #f8f8f8;
        color: #a0a0a0;
    }

    /* 主要按钮样式 */
    QPushButton[primary=true] {
        background-color: #007bff;
        color: white;
        border: 1px solid #0069d9;
    }

    QPushButton[primary=true]:hover {
        background-color: #0069d9;
    }

    QPushButton[primary=true]:pressed {
        background-color: #0062cc;
    }

    /* 输入框样式 */
    QLineEdit, QTextEdit, QPlainTextEdit {
        min-height: 32px;
        padding: 4px 8px;
        border: 1px solid #c0c0c0;
        border-radius: 4px;
        background-color: white;
    }

    QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {
        border: 1px solid #80bdff;
    }

    /* 下拉框样式 */
    QComboBox {
        min-height: 32px;
        padding: 4px 8px;
        border: 1px solid #c0c0c0;
        border-radius: 4px;
        background-color: white;
    }

    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left: 1px solid #c0c0c0;
    }

    /* 复选框样式 */
    QCheckBox {
        spacing: 8px;
        min-height: 24px;
    }

    QCheckBox::indicator {
        width: 18px;
        height: 18px;
    }

    /* 单选框样式 */
    QRadioButton {
        spacing: 8px;
        min-height: 24px;
    }

    QRadioButton::indicator {
        width: 18px;
        height: 18px;
    }

    /* 标签页样式 */
    QTabWidget::pane {
        border: 1px solid #c0c0c0;
        border-radius: 4px;
        padding: 10px;
    }

    QTabBar::tab {
        background: #f0f0f0;
        border: 1px solid #c0c0c0;
        border-bottom-color: #c0c0c0;
        border-top-left-radius: 4px;
        border-top-right-radius: 4px;
        min-width: 120px;
        min-height: 32px;
        padding: 6px 12px;
        margin-right: 2px;
    }

    QTabBar::tab:selected {
        background: white;
        border-bottom-color: white;
    }

    /* 表格样式 */
    QTableView {
        gridline-color: #e0e0e0;
        selection-background-color: #e0f0ff;
        font-size: 10pt;
    }

    QTableView::item {
        padding: 6px;
        min-height: 32px;
    }

    QHeaderView::section {
        background-color: #f5f5f5;
        padding: 6px;
        font-weight: bold;
        border: 1px solid #e0e0e0;
        min-height: 32px;
        font-size: 10pt;
    }

    /* 滚动条样式 */
    QScrollBar:vertical {
        border: none;
        background: #f0f0f0;
        width: 16px;
        margin: 0px;
        border-radius: 8px;
    }

    QScrollBar::handle:vertical {
        background: #c0c0c0;
        min-height: 30px;
        border-radius: 8px;
    }

    QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
        height: 0px;
    }

    QScrollBar:horizontal {
        border: none;
        background: #f0f0f0;
        height: 16px;
        margin: 0px;
        border-radius: 8px;
    }

    QScrollBar::handle:horizontal {
        background: #c0c0c0;
        min-width: 30px;
        border-radius: 8px;
    }

    QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
        width: 0px;
    }

    /* 分组框样式 */
    QGroupBox {
        font-weight: bold;
        border: 1px solid #c0c0c0;
        border-radius: 4px;
        margin-top: 20px;
        padding-top: 24px;
    }

    QGroupBox::title {
        subcontrol-origin: margin;
        subcontrol-position: top left;
        padding: 0 5px;
        left: 10px;
    }

    /* 状态栏样式 */
    QStatusBar {
        background-color: #f8f8f8;
        color: #505050;
        min-height: 32px;
    }

    QStatusBar QLabel {
        padding: 0 10px;
    }

    /* 菜单样式 */
    QMenuBar {
        background-color: #f8f8f8;
        min-height: 32px;
    }

    QMenuBar::item {
        padding: 6px 12px;
        background: transparent;
    }

    QMenuBar::item:selected {
        background: #e0e0e0;
    }

    QMenu {
        background-color: white;
        border: 1px solid #c0c0c0;
    }

    QMenu::item {
        padding: 6px 30px 6px 20px;
        min-height: 24px;
    }

    QMenu::item:selected {
        background-color: #e0f0ff;
    }
    """