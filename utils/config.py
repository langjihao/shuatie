#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
配置管理
"""

import os
import json
from utils.helpers import get_app_data_dir


class Config:
    """配置类"""
    
    def __init__(self):
        self.config_file = os.path.join(get_app_data_dir(), 'config.json')
        self.config = self.load()
    
    def load(self):
        """加载配置"""
        if not os.path.exists(self.config_file):
            return self.get_default_config()
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config
        except Exception as e:
            print(f"加载配置失败: {e}")
            return self.get_default_config()
    
    def save(self):
        """保存配置"""
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
    
    def get_default_config(self):
        """获取默认配置"""
        return {
            'browser_type': 'edge',  # 浏览器类型: edge, chrome
            'default_wait_time': 2.0,  # 默认等待时间
            'default_browse_time': 5.0,  # 默认浏览时间
            'default_scroll_enabled': True,  # 默认启用滚动
            'default_close_wait_time': 1.0,  # 默认关闭后等待时间
            'auto_shutdown': False,  # 自动关机
            'shutdown_time': 5,  # 关机倒计时（分钟）
            'queue': []  # 队列
        }
    
    def get(self, key, default=None):
        """获取配置项"""
        return self.config.get(key, default)
    
    def set(self, key, value):
        """设置配置项"""
        self.config[key] = value
        return self.save()
    
    def get_queue(self):
        """获取队列"""
        return self.config.get('queue', [])
    
    def set_queue(self, queue):
        """设置队列"""
        self.config['queue'] = queue
        return self.save()
    
    def add_queue_item(self, item):
        """添加队列项"""
        queue = self.get_queue()
        queue.append(item)
        return self.set_queue(queue)
    
    def remove_queue_item(self, index):
        """删除队列项"""
        queue = self.get_queue()
        if 0 <= index < len(queue):
            queue.pop(index)
            return self.set_queue(queue)
        return False
    
    def clear_queue(self):
        """清空队列"""
        return self.set_queue([])
    
    def get_browser_settings(self):
        """获取浏览器设置"""
        return {
            'browser_type': self.get('browser_type', 'edge'),
            'default_wait_time': self.get('default_wait_time', 2.0),
            'default_browse_time': self.get('default_browse_time', 5.0),
            'default_scroll_enabled': self.get('default_scroll_enabled', True),
            'default_close_wait_time': self.get('default_close_wait_time', 1.0)
        }
    
    def set_browser_settings(self, settings):
        """设置浏览器设置"""
        for key, value in settings.items():
            self.set(key, value)
        return self.save()
