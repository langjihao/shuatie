#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
自动化浏览器操作软件
主程序入口
"""

import sys
import os
import subprocess
from PyQt5.QtWidgets import QApplication, QMessageBox
from PyQt5.QtCore import QTranslator, QLocale, Qt

from ui.main_window import MainWindow
from core.password_manager import PasswordManager
from ui.styles.high_dpi_style import get_high_dpi_stylesheet


def check_playwright_browsers():
    """检查Playwright浏览器是否已安装"""
    try:
        # 尝试导入playwright
        import playwright
        from playwright.sync_api import sync_playwright

        # 尝试启动playwright，如果浏览器未安装会失败
        with sync_playwright() as p:
            try:
                # 尝试启动Edge浏览器
                browser = p.chromium.launch(channel="msedge", headless=False)
                browser.close()
                return True
            except Exception:
                # Edge浏览器启动失败，可能未安装
                return False
    except ImportError:
        # Playwright未安装
        return False


def install_playwright_browsers():
    """安装Playwright浏览器"""
    try:
        result = subprocess.run(
            ["playwright", "install", "chromium", "msedge"],
            capture_output=True,
            text=True
        )
        return result.returncode == 0
    except Exception:
        return False


def main():
    """主函数"""
    # 启用高DPI缩放 - PyQt5版本
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    # 创建应用
    app = QApplication(sys.argv)

    # 设置中文
    translator = QTranslator()
    translator.load(QLocale.system().name(), "translations")
    app.installTranslator(translator)

    # 应用高DPI样式表
    app.setStyleSheet(get_high_dpi_stylesheet())

    # 检查Playwright浏览器是否已安装
    if not check_playwright_browsers():
        reply = QMessageBox.question(
            None,
            "安装浏览器",
            "需要安装浏览器组件才能正常运行。是否现在安装？",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.Yes
        )

        if reply == QMessageBox.Yes:
            QMessageBox.information(None, "安装中", "正在安装浏览器组件，请稍候...")
            if install_playwright_browsers():
                QMessageBox.information(None, "安装完成", "浏览器组件安装成功！")
            else:
                QMessageBox.warning(None, "安装失败", "浏览器组件安装失败，程序可能无法正常运行。")

    # 检查是否已解锁
    password_manager = PasswordManager()
    is_unlocked = password_manager.is_unlocked()

    # 创建主窗口
    main_window = MainWindow(is_unlocked)
    main_window.show()

    # 运行应用
    sys.exit(app.exec_())  # 注意：PyQt5中是app.exec_()而不是app.exec()


if __name__ == "__main__":
    main()




