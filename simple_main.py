#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
简化版主程序 - 用于测试PyQt5是否正常工作
"""

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget

class SimpleWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("简单测试窗口")
        self.setGeometry(100, 100, 400, 200)

        # 创建中央部件
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # 创建布局
        layout = QVBoxLayout(central_widget)

        # 添加标签
        label = QLabel("PyQt5测试窗口 - 如果您能看到此窗口，说明PyQt5正常工作！")
        label.setStyleSheet("font-size: 14px; color: green;")
        layout.addWidget(label)

def main():
    app = QApplication(sys.argv)
    window = SimpleWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()