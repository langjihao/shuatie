#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
浏览器控制器 - 使用Playwright实现
"""

import sys
import time
import random
import threading
import subprocess
from datetime import datetime, timedelta
from PyQt5.QtCore import QObject, pyqtSignal
from .browser_resources import get_browser_path
try:
    from playwright.sync_api import sync_playwright
    PLAYWRIGHT_INSTALLED = True
except ImportError:
    PLAYWRIGHT_INSTALLED = False


def install_playwright():
    """安装Playwright及浏览器"""
    try:
        # 安装playwright库
        subprocess.run([sys.executable, "-m", "pip", "install", "playwright"], check=True)

        # 安装浏览器
        subprocess.run([sys.executable, "-m", "playwright", "install"], check=True)

        return True
    except Exception as e:
        print(f"安装Playwright失败: {e}")
        return False


class BrowserController(QObject):
    """浏览器控制器"""

    status_changed = pyqtSignal(int, str)  # 状态变化信号
    log_message = pyqtSignal(str)  # 日志信息信号

    def __init__(self):
        super().__init__()
        self.browser = None
        self.page = None
        self.playwright = None
        self.is_running_flag = False
        self.thread = None
        self.current_queue_index = 0
        self.current_loop_count = 0
        self.start_time = None
        self.browser_type = "chromium"  # 默认使用Chromium浏览器
        self.queue_completed = False  # 标记队列是否完成一轮
        self.headless = False  # 无头模式标志
        self.is_paused = False
        self._pause_event = threading.Event()
        self._pause_event.set()  # 初始状态为未暂停

    def set_headless(self, headless):
        """设置无头模式"""
        self.headless = headless

    def pause(self):
        """暂停任务执行"""
        self.is_paused = True
        self._pause_event.clear()

    def resume(self):
        """恢复任务执行"""
        self.is_paused = False
        self._pause_event.set()

    def _log(self, message):
        """输出日志"""
        print(message)  # 始终在控制台打印
        self.log_message.emit(message)  # 发送日志信号

    def _update_status(self, row, status):
        """更新任务状态"""
        self.status_changed.emit(row, status)  # 发送状态更新信号

    def is_running(self):
        """检查是否正在运行"""
        return self.is_running_flag

    def start(self, queue_data):
        """启动浏览器控制器
        
        Args:
            queue_data (list): 任务队列数据
        """
        if self.is_running_flag:
            return

        # 检查Playwright是否已安装
        global sync_playwright, PLAYWRIGHT_INSTALLED
        if not PLAYWRIGHT_INSTALLED:
            self._log("Playwright未安装，尝试安装...")
            raise Exception("无法找到Playwright，请手动安装: pip install playwright")

        self.is_running_flag = True
        self.current_queue_index = 0
        self.current_loop_count = 0

        # 创建线程
        self.thread = threading.Thread(target=self._run_task, args=(queue_data,))
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """停止浏览器控制器"""
        self.is_running_flag = False
        self._pause_event.set()  # 确保线程不会卡在暂停状态
        self.is_paused = False

        # 清理资源
        if self.page:
            try:
                self.page.close()
            except:
                pass
            self.page = None

        if self.context:
            try:
                self.context.close()
            except:
                pass
            self.context = None

        if self.browser:
            try:
                self.browser.close()
            except:
                pass
            self.browser = None

        if self.playwright:
            try:
                self.playwright.stop()
            except:
                pass
            self.playwright = None

    def _install_browser(self, browser_type):
        """安装指定类型的浏览器"""
        try:
            self._log(f"正在安装{browser_type}浏览器...")
            
            # 首先尝试普通安装
            result = subprocess.run(
                [sys.executable, "-m", "playwright", "install", browser_type],
                capture_output=True,
                text=True
            )
            
            # 如果输出中包含已安装的提示，使用--force参数重新安装
            if "is already installed" in result.stderr:
                self._log(f"检测到{browser_type}已安装，尝试强制重新安装...")
                self._log("请确保已关闭所有相关的浏览器窗口")
                
                # 使用force参数重新安装
                result = subprocess.run(
                    [sys.executable, "-m", "playwright", "install", "--force", browser_type],
                    capture_output=True,
                    text=True,
                    check=True
                )
            
            self._log(f"{browser_type}浏览器安装成功")
            return True
        except Exception as e:
            self._log(f"安装{browser_type}浏览器失败: {e}")
            return False

    def _initialize_browser(self):
        """初始化浏览器"""
        print("正在启动Playwright...")
        self.playwright = sync_playwright().start()
        
        print("正在启动浏览器...")
        try:
            # 获取浏览器可执行文件路径
            executable_path = get_browser_path(self.headless)
            print(f"使用浏览器: {executable_path}")
            
            # 启动浏览器，添加必要的启动参数
            self.browser = self.playwright.chromium.launch(
                headless=self.headless,
                executable_path=executable_path,
                args=[
                    '--no-sandbox',                    # 禁用沙箱模式
                    '--disable-dev-shm-usage',         # 禁用/dev/shm
                    '--disable-gpu',                   # 禁用GPU加速
                    '--disable-setuid-sandbox',        # 禁用setuid沙箱
                    '--no-first-run',                  # 跳过首次运行界面
                    '--no-default-browser-check',      # 禁用默认浏览器检查
                    '--disable-notifications',         # 禁用通知
                    '--disable-popup-blocking',        # 禁用弹窗拦截
                    '--disable-infobars',             # 禁用信息栏
                    '--ignore-certificate-errors',     # 忽略证书错误
                    '--window-position=0,0',          # 窗口位置：左上角
                    '--window-size=960,1080'          # 窗口大小：半屏宽度，全屏高度
                ]
            )
            print("浏览器启动成功！")
            
            print("创建浏览器上下文...")
            # 设置浏览器上下文视口大小为半屏
            self.context = self.browser.new_context(
                viewport={'width': 960, 'height': 1080},  # 半屏宽度，全屏高度
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36'
            )
            
            print("创建新页面...")
            self.page = self.context.new_page()
            
            print("浏览器初始化成功！")
            return True
        except Exception as e:
            print(f"浏览器初始化失败: {str(e)}")
            self.stop()
            return False

    def _run_task(self, queue_data):
        """运行任务
        
        Args:
            queue_data (list): 任务队列数据
        """
        try:
            # 初始化浏览器
            self._initialize_browser()

            # 开始执行队列
            self._log("开始执行浏览任务...")
            while self.is_running_flag and queue_data:
                # 暂停时等待恢复
                while not self._pause_event.is_set():
                    time.sleep(0.5)

                # 获取当前队列项
                if self.current_queue_index >= len(queue_data):
                    self._log("队列已完成一轮")
                    self.queue_completed = True
                    # 更新所有任务状态为已完成
                    for i in range(len(queue_data)):
                        self._update_status(i, "已完成")
                    break

                current_item = queue_data[self.current_queue_index]
                self._log(f"执行任务 {self.current_queue_index+1}/{len(queue_data)}: {current_item['url']}")

                # 更新当前任务状态为运行中
                self._update_status(self.current_queue_index, "运行中")

                # 执行浏览操作
                try:
                    self._browse_url(current_item)
                    # 检查是否有循环设置
                    loop_type = current_item.get('loop_type', 'count')
                    loop_count = current_item.get('loop_count', 1)
                    loop_time = current_item.get('loop_time', 5)

                    # 更新计数器或检查时间
                    if loop_type == 'count':
                        self.current_loop_count += 1
                        self._log(f"循环次数: {self.current_loop_count}/{loop_count}")
                        if self.current_loop_count >= loop_count:
                            self.current_loop_count = 0
                            self.current_queue_index += 1
                            # 更新当前任务状态为已完成
                            self._update_status(self.current_queue_index - 1, "已完成")
                            self._log("完成循环次数，进入下一任务")
                    else:  # 时间循环
                        if self.start_time is None:
                            self.start_time = time.time()

                        elapsed_minutes = (time.time() - self.start_time) / 60
                        self._log(f"循环时间: {elapsed_minutes:.1f}/{loop_time}分钟")
                        if elapsed_minutes >= loop_time:
                            self.start_time = None
                            self.current_queue_index += 1
                            # 更新当前任务状态为已完成
                            self._update_status(self.current_queue_index - 1, "已完成")
                            self._log("完成循环时间，进入下一任务")
                except Exception as e:
                    self._log(f"任务执行失败: {e}")
                    # 更新当前任务状态为失败
                    self._update_status(self.current_queue_index, "失败")
                    self.current_queue_index += 1

            # 关闭浏览器
            self._log("任务完成，关闭浏览器...")
            self.stop()

        except Exception as e:
            self._log(f"任务执行过程出错: {e}")
        finally:
            self.is_running_flag = False
            self._log("浏览器控制器已停止")

    def _browse_url(self, item):
        """浏览URL"""
        if not self.is_running_flag:
            return

        try:
            # 关闭之前的页面（如果存在）
            if self.page:
                try:
                    self.page.close()
                    self.page = None
                except:
                    pass

            if not self.browser:
                self._initialize_browser()
            
            # 创建新的页面
            self._log("创建新页面...")
            context = self.browser.new_context(
                viewport={"width": 960, "height": 1080},  # 设置半屏视口大小
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
            )
            self.page = context.new_page()

            # 确保浏览器可见
            self._ensure_browser_visible()

            # 设置滚动速度
            self.page.evaluate(f"window.__scroll_speed = {item.get('scroll_speed', 1.0)}")

            # 打开URL
            self._log(f"正在打开: {item['url']}")
            self.page.goto(item['url'], wait_until="domcontentloaded", timeout=60000)

            # 等待页面加载
            if item['wait_time'] > 0:
                self._log(f"等待页面加载: {item['wait_time']}秒")
                time.sleep(item['wait_time'])

            # 浏览页面
            if item['browse_time'] > 0:
                if item['scroll_enabled']:
                    self._log(f"浏览页面并滚动: {item['browse_time']}秒")
                    self._simulate_scrolling(item['browse_time'])
                else:
                    self._log(f"浏览页面: {item['browse_time']}秒")
                    time.sleep(item['browse_time'])

            # 关闭页面
            self._log("关闭页面...")
            self.page.close()
            self.page = None

            # 关闭页面后等待
            if item['close_wait_time'] > 0:
                self._log(f"等待: {item['close_wait_time']}秒")
                time.sleep(item['close_wait_time'])

        except Exception as e:
            self._log(f"浏览URL失败: {e}")
            # 确保出错时也关闭页面
            if self.page:
                try:
                    self.page.close()
                    self.page = None
                except:
                    pass

    def _simulate_scrolling(self, duration):
        """模拟滚动"""
        start_time = time.time()
        scroll_speed = self.page.evaluate("() => window.__scroll_speed || 1.0")  # 获取滚动速度

        while time.time() - start_time < duration and self.is_running_flag:
            try:
                # 暂停时等待恢复
                while not self._pause_event.is_set():
                    time.sleep(0.5)

                # 获取页面高度
                page_height = self.page.evaluate("document.body.scrollHeight")

                # 根据滚动速度调整滚动步长
                scroll_step = int(page_height * 0.1 * scroll_speed)  # 基础步长的倍数

                # 随机滚动位置
                scroll_y = random.randint(0, page_height)

                # 执行滚动
                self.page.evaluate(f"window.scrollTo(0, {scroll_y})")

                # 随机等待一小段时间，考虑滚动速度
                wait_time = random.uniform(0.5, 2.0) / scroll_speed
                time.sleep(wait_time)

            except Exception as e:
                self._log(f"滚动失败: {e}")
                time.sleep(0.5)

    def _ensure_browser_visible(self):
        """确保浏览器窗口可见"""
        if not self.page:
            return

        try:
            # 使用JavaScript将窗口带到前台
            self.page.evaluate("""
            () => {
                window.focus();
                // 尝试闪烁标题以吸引注意
                let originalTitle = document.title;
                document.title = '【正在浏览】' + originalTitle;
                setTimeout(() => {
                    document.title = originalTitle;
                }, 3000);
            }
            """)

        except Exception as e:
            self._log(f"确保浏览器可见失败: {e}")




