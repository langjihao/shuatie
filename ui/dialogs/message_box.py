#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
高DPI消息框
"""

from PyQt5.QtWidgets import QMessageBox


class HighDPIMessageBox(QMessageBox):
    """高DPI消息框"""

    @staticmethod
    def information(parent, title, text, buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok):
        """显示信息消息框"""
        msg_box = QMessageBox(QMessageBox.Information, title, text, buttons, parent)
        msg_box.setDefaultButton(defaultButton)
        return msg_box.exec_()

    @staticmethod
    def warning(parent, title, text, buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok):
        """显示警告消息框"""
        msg_box = QMessageBox(QMessageBox.Warning, title, text, buttons, parent)
        msg_box.setDefaultButton(defaultButton)
        return msg_box.exec_()

    @staticmethod
    def critical(parent, title, text, buttons=QMessageBox.Ok, defaultButton=QMessageBox.Ok):
        """显示错误消息框"""
        msg_box = QMessageBox(QMessageBox.Critical, title, text, buttons, parent)
        msg_box.setDefaultButton(defaultButton)
        return msg_box.exec_()

    @staticmethod
    def question(parent, title, text, buttons=QMessageBox.Yes | QMessageBox.No, defaultButton=QMessageBox.No):
        """显示问题消息框"""
        msg_box = QMessageBox(QMessageBox.Question, title, text, buttons, parent)
        msg_box.setDefaultButton(defaultButton)
        return msg_box.exec_()





