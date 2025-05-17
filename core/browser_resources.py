#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
浏览器资源管理模块
"""

import os
import sys
from pathlib import Path
import subprocess

def get_base_path():
    """获取基础路径"""
    if getattr(sys, 'frozen', False):
        # 打包后的路径
        return os.path.dirname(sys.executable)
    else:
        # 开发环境路径
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def test_browser(executable_path):
    """测试浏览器是否可用
    
    Args:
        executable_path (str): 浏览器可执行文件路径
        
    Returns:
        bool: 浏览器是否可用
    """
    try:
        # 只检查文件是否存在及其依赖文件
        if not os.path.exists(executable_path):
            return False
            
        browser_dir = os.path.dirname(executable_path)
        required_files = [
            'chrome.dll' if 'chrome.exe' in executable_path else 'headless_shell.exe',
            'icudtl.dat',
            'v8_context_snapshot.bin'
        ]
        
        for file in required_files:
            if not os.path.exists(os.path.join(browser_dir, file)):
                print(f"缺少必要文件: {file}")
                return False
        
        return True
        
    except Exception as e:
        print(f"测试浏览器失败: {str(e)}")
        return False

def get_browser_path(headless=False):
    """获取浏览器可执行文件路径
    
    Args:
        headless (bool): 是否使用无头浏览器
        
    Returns:
        str: 浏览器可执行文件的完整路径
    """
    base_path = get_base_path()
    
    # 首先尝试使用完整版Chrome
    chrome_path = os.path.join(base_path, 'resources', 'chromium-1169', 'chrome-win', 'chrome.exe')
    if os.path.exists(chrome_path):
        print(f"尝试完整版浏览器: {chrome_path}")
        if test_browser(chrome_path):
            print("完整版浏览器可用")
            return chrome_path
        else:
            print("完整版浏览器不可用，尝试其他选项")
    
    # 如果完整版不可用且需要无头模式，尝试使用headless_shell
    if headless:
        headless_path = os.path.join(base_path, 'resources', 'chromium_headless_shell-1169', 'chrome-win', 'headless_shell.exe')
        if os.path.exists(headless_path):
            print(f"尝试无头浏览器: {headless_path}")
            if test_browser(headless_path):
                print("无头浏览器可用")
                return headless_path
            else:
                print("无头浏览器不可用")
    
    # 如果都不可用，抛出异常
    raise Exception(
        f"找不到可用的浏览器。\n"
        f"已检查以下路径：\n"
        f"1. 完整版Chrome: {chrome_path}\n"
        f"2. 无头版本: {os.path.join(base_path, 'resources', 'chromium_headless_shell-1169', 'chrome-win', 'headless_shell.exe')}"
    )