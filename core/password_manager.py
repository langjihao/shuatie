#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
密码管理器
"""

import os
import json
import datetime
import hashlib


class PasswordManager:
    """密码管理器"""
    
    def __init__(self):
        self.config_file = os.path.join(os.path.expanduser("~"), ".auto_browser_config")
        self.unlocked = self._check_unlocked()
    
    def is_unlocked(self):
        """检查是否已解锁"""
        return self.unlocked
    
    def _check_unlocked(self):
        """检查配置文件中是否已解锁"""
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('unlocked', False)
            except:
                pass
        return False
    
    def _save_unlocked_state(self, unlocked):
        """保存解锁状态"""
        config = {}
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
            except:
                pass
        
        config['unlocked'] = unlocked
        
        try:
            with open(self.config_file, 'w') as f:
                json.dump(config, f)
        except:
            pass
    
    def _generate_password(self):
        """生成当天的密码"""
        # 使用北京时间（UTC+8）
        now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=8)))
        date_str = now.strftime("%y%m%d")  # 年月日，例如 250508
        
        # 计算密码
        password_int = int(date_str) * 2
        
        # 根据时间调整密码
        if now.hour >= 12:
            password_int -= 12
        
        # 确保是6位数
        password_str = str(password_int).zfill(6)
        
        return password_str
    
    def verify_password(self, password):
        """验证密码"""
        correct_password = self._generate_password()
        
        if password == correct_password:
            self.unlocked = True
            self._save_unlocked_state(True)
            return True
        
        return False

