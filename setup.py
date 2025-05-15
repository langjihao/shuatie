#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
打包脚本
"""

import sys
from cx_Freeze import setup, Executable

# 依赖项
build_exe_options = {
    "packages": [
        "os", "sys", "json", "time", "datetime", "random", 
        "threading", "subprocess", "selenium", "PyQt5"
    ],
    "excludes": [],
    "include_files": []
}

# 基本信息
base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="自动化浏览器操作软件",
    version="1.0.0",
    description="自动化浏览器操作软件",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base, target_name="AutoBrowser.exe", icon="icon.ico")]
)
