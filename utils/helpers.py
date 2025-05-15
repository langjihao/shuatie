#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
辅助函数
"""

import os
import sys
import json
import time
import datetime
import subprocess


def get_app_data_dir():
    """获取应用数据目录"""
    if sys.platform == 'win32':
        app_data = os.path.join(os.environ['APPDATA'], 'AutoBrowser')
    else:
        app_data = os.path.join(os.path.expanduser('~'), '.auto_browser')
    
    if not os.path.exists(app_data):
        os.makedirs(app_data)
    
    return app_data


def save_config(config):
    """保存配置"""
    config_file = os.path.join(get_app_data_dir(), 'config.json')
    
    try:
        with open(config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"保存配置失败: {e}")
        return False


def load_config():
    """加载配置"""
    config_file = os.path.join(get_app_data_dir(), 'config.json')
    
    if not os.path.exists(config_file):
        return {}
    
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"加载配置失败: {e}")
        return {}


def format_time(seconds):
    """格式化时间"""
    if seconds < 60:
        return f"{seconds:.1f}秒"
    elif seconds < 3600:
        minutes = seconds / 60
        return f"{minutes:.1f}分钟"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}小时"


def shutdown_computer(minutes=1):
    """关闭计算机"""
    if sys.platform == 'win32':
        # Windows系统
        cmd = f'shutdown /s /t {minutes * 60}'
        subprocess.Popen(cmd, shell=True)
        return True
    else:
        # Linux/Mac系统
        cmd = f'shutdown -h +{minutes}'
        subprocess.Popen(cmd, shell=True)
        return True


def cancel_shutdown():
    """取消关机"""
    if sys.platform == 'win32':
        # Windows系统
        cmd = 'shutdown /a'
        subprocess.Popen(cmd, shell=True)
        return True
    else:
        # Linux/Mac系统
        cmd = 'shutdown -c'
        subprocess.Popen(cmd, shell=True)
        return True
