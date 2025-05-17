#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
高DPI样式
"""

def get_high_dpi_style():
    """获取高DPI样式"""
    return """
        /* 全局样式 */
        QWidget {
            font-size: 12px;
            font-family: "Microsoft YaHei", "SimHei", sans-serif;
        }
        
        /* 按钮样式 */
        QPushButton {
            min-height: 32px;
            padding: 4px 12px;
            border: 1px solid #dcdfe6;
            border-radius: 4px;
            background-color: #ffffff;
        }
        
        QPushButton:hover {
            background-color: #ecf5ff;
            border-color: #409eff;
            color: #409eff;
        }
        
        QPushButton:pressed {
            background-color: #3a8ee6;
            border-color: #3a8ee6;
            color: #ffffff;
        }
        
        QPushButton[primary="true"] {
            background-color: #409eff;
            border-color: #409eff;
            color: #ffffff;
        }
        
        QPushButton[primary="true"]:hover {
            background-color: #66b1ff;
            border-color: #66b1ff;
            color: #ffffff;
        }
        
        QPushButton[primary="true"]:pressed {
            background-color: #3a8ee6;
            border-color: #3a8ee6;
        }
        
        /* 表格样式 */
        QTableWidget {
            border: 1px solid #dcdfe6;
            border-radius: 4px;
            background-color: #ffffff;
            gridline-color: #ebeef5;
        }
        
        QTableWidget::item {
            padding: 8px;
            border-bottom: 1px solid #ebeef5;
        }
        
        QTableWidget::item:selected {
            background-color: #ecf5ff;
            color: #409eff;
        }
        
        QHeaderView::section {
            background-color: #f5f7fa;
            padding: 8px;
            border: none;
            border-bottom: 1px solid #dcdfe6;
            border-right: 1px solid #dcdfe6;
            font-weight: bold;
            min-height: 32px;
        }
        
        /* 标签页样式 */
        QTabWidget::pane {
            border: 1px solid #dcdfe6;
            border-radius: 4px;
            background-color: #ffffff;
        }
        
        QTabBar::tab {
            min-width: 120px;
            min-height: 36px;
            padding: 8px 16px;
            border: 1px solid #dcdfe6;
            border-bottom: none;
            border-top-left-radius: 4px;
            border-top-right-radius: 4px;
            margin-right: 2px;
            background-color: #f5f7fa;
        }
        
        QTabBar::tab:selected {
            background-color: #ffffff;
            border-bottom: 2px solid #409eff;
            color: #409eff;
        }
        
        QTabBar::tab:hover:!selected {
            background-color: #ecf5ff;
        }
        
        /* 输入框样式 */
        QLineEdit, QTextEdit, QSpinBox, QDoubleSpinBox {
            padding: 6px 12px;
            border: 1px solid #dcdfe6;
            border-radius: 4px;
            background-color: #ffffff;
            min-height: 32px;
        }
        
        QLineEdit:focus, QTextEdit:focus, QSpinBox:focus, QDoubleSpinBox:focus {
            border-color: #409eff;
        }
        
        /* 滚动条样式 */
        QScrollBar:vertical {
            border: none;
            background-color: #f5f7fa;
            width: 12px;
            margin: 0px;
        }
        
        QScrollBar::handle:vertical {
            background-color: #c0c4cc;
            border-radius: 6px;
            min-height: 20px;
        }
        
        QScrollBar::handle:vertical:hover {
            background-color: #909399;
        }
        
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
            height: 0px;
        }
        
        /* 状态栏样式 */
        QStatusBar {
            background-color: #f5f7fa;
            min-height: 32px;
            padding: 4px;
            border-top: 1px solid #dcdfe6;
        }
    """

# 添加别名以保持与导入语句的一致性
get_high_dpi_stylesheet = get_high_dpi_style