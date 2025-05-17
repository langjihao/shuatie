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
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller打包后的路径
            return sys._MEIPASS
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
        # 检查文件是否存在
        if not os.path.exists(executable_path):
            print(f"浏览器可执行文件不存在: {executable_path}")
            return False
            
        browser_dir = os.path.dirname(executable_path)
        required_files = [
            'chrome.dll' if 'chrome.exe' in executable_path else 'headless_shell.exe',
            'icudtl.dat',
            'v8_context_snapshot.bin'
        ]
        
        for file in required_files:
            file_path = os.path.join(browser_dir, file)
            if not os.path.exists(file_path):
                print(f"缺少必要文件: {file_path}")
                return False
            
        print(f"浏览器目录 {browser_dir} 中的所有必要文件都存在")
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
    print(f"基础路径: {base_path}")
    
    # 尝试所有可能的浏览器路径
    possible_paths = []
    
    # 添加完整版Chrome路径
    chrome_paths = [
        os.path.join(base_path, 'resources', 'chromium-1169', 'chrome-win', 'chrome.exe'),
        os.path.join(base_path, 'chromium-1169', 'chrome-win', 'chrome.exe'),
        os.path.join(os.path.dirname(base_path), 'resources', 'chromium-1169', 'chrome-win', 'chrome.exe')
    ]
    
    # 添加无头版Chrome路径
    headless_paths = [
        os.path.join(base_path, 'resources', 'chromium_headless_shell-1169', 'chrome-win', 'headless_shell.exe'),
        os.path.join(base_path, 'chromium_headless_shell-1169', 'chrome-win', 'headless_shell.exe'),
        os.path.join(os.path.dirname(base_path), 'resources', 'chromium_headless_shell-1169', 'chrome-win', 'headless_shell.exe')
    ]
    
    # 根据模式选择要检查的路径
    paths_to_check = headless_paths + chrome_paths if headless else chrome_paths + headless_paths
    
    # 检查每个可能的路径
    for path in paths_to_check:
        print(f"检查路径: {path}")
        if os.path.exists(path):
            print(f"找到浏览器文件: {path}")
            if test_browser(path):
                print(f"浏览器可用: {path}")
                return path
            else:
                print(f"浏览器文件存在但不可用: {path}")
    
    # 如果所有路径都不可用，抛出异常
    raise Exception(
        f"找不到可用的浏览器。\n"
        f"已检查以下路径：\n" +
        "\n".join(f"{i+1}. {path}" for i, path in enumerate(paths_to_check))
    )