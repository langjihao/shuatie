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


class BrowserController:
    """浏览器控制器"""

    def __init__(self):
        self.browser = None
        self.page = None
        self.playwright = None
        self.is_running_flag = False
        self.thread = None
        self.current_queue_index = 0
        self.current_loop_count = 0
        self.start_time = None
        self.browser_type = "chromium"  # 默认使用Chromium浏览器

    def is_running(self):
        """检查是否正在运行"""
        return self.is_running_flag

    def start(self, queue_data, timer_settings):
        """启动浏览器控制器"""
        if self.is_running_flag:
            return

        # 检查Playwright是否已安装
        global sync_playwright, PLAYWRIGHT_INSTALLED
        if not PLAYWRIGHT_INSTALLED:
            print("Playwright未安装，尝试安装...")
            if not install_playwright():
                raise Exception("无法安装Playwright，请手动安装: pip install playwright")

            # 重新导入
            try:
                from playwright.sync_api import sync_playwright
                PLAYWRIGHT_INSTALLED = True
            except ImportError:
                raise Exception("安装Playwright后仍无法导入，请重启应用")

        self.is_running_flag = True
        self.current_queue_index = 0
        self.current_loop_count = 0

        # 创建线程
        self.thread = threading.Thread(target=self._run_task, args=(queue_data, timer_settings))
        self.thread.daemon = True
        self.thread.start()

    def stop(self):
        """停止浏览器控制器"""
        self.is_running_flag = False

        if self.page:
            try:
                self.page.close()
            except:
                pass
            self.page = None

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

    def _init_browser(self):
        """初始化浏览器"""
        try:
            print("正在启动Playwright...")
            self.playwright = sync_playwright().start()

            print(f"正在启动{self.browser_type}浏览器...")
            # 浏览器启动选项
            browser_options = {
                "headless": False,  # 确保浏览器可见
            }

            # 尝试启动浏览器，优先使用Chromium（内置浏览器）
            try:
                self.browser = self.playwright.chromium.launch(**browser_options)
                print("成功启动Chromium浏览器")
            except Exception as e:
                print(f"启动Chromium失败: {e}")

                # 尝试启动Edge
                try:
                    self.browser = self.playwright.chromium.launch(
                        channel="msedge",
                        **browser_options
                    )
                    print("成功启动Edge浏览器")
                except Exception as e:
                    print(f"启动Edge失败: {e}")

                    # 尝试启动Chrome
                    try:
                        self.browser = self.playwright.chromium.launch(
                            channel="chrome",
                            **browser_options
                        )
                        print("成功启动Chrome浏览器")
                    except Exception as e:
                        print(f"启动Chrome失败: {e}")
                        raise Exception("无法启动任何浏览器，请确保已安装Chromium、Edge或Chrome")

            print("创建浏览器上下文...")
            # 创建页面并设置为最大化
            context = self.browser.new_context(
                viewport=None,  # 不限制视口大小，允许最大化
                no_viewport=True  # 禁用固定视口
            )

            print("创建新页面...")
            self.page = context.new_page()

            # 确保窗口最大化
            self.page.evaluate("() => { window.moveTo(0, 0); window.resizeTo(window.screen.availWidth, window.screen.availHeight); }")
            print("浏览器初始化成功！")

        except Exception as e:
            print(f"初始化浏览器失败: {e}")
            if self.playwright:
                try:
                    self.playwright.stop()
                except:
                    pass
                self.playwright = None
            raise

    def _run_task(self, queue_data, timer_settings):
        """运行任务"""
        # 根据启动方式处理
        if timer_settings['start_type'] == 'countdown':
            # 倒计时启动
            total_minutes = timer_settings['countdown_hours'] * 60 + timer_settings['countdown_minutes']
            if total_minutes > 0:
                print(f"将在{total_minutes}分钟后启动...")
                time.sleep(total_minutes * 60)

        elif timer_settings['start_type'] == 'time_point':
            # 时间点启动
            target_time = datetime.strptime(timer_settings['time_point'], "%H:%M").time()
            now = datetime.now()
            target_datetime = datetime.combine(now.date(), target_time)

            # 如果目标时间已过，设置为明天
            if target_datetime < now:
                target_datetime = datetime.combine(now.date() + timedelta(days=1), target_time)

            # 等待到达目标时间
            wait_seconds = (target_datetime - now).total_seconds()
            if wait_seconds > 0:
                print(f"将在{target_time}启动，等待{wait_seconds/60:.1f}分钟...")
                time.sleep(wait_seconds)

        # 初始化浏览器
        try:
            self._init_browser()
        except Exception as e:
            print(f"初始化浏览器失败: {e}")
            self.is_running_flag = False
            return

        # 开始执行队列
        print("开始执行浏览任务...")
        while self.is_running_flag and queue_data:
            # 获取当前队列项
            if self.current_queue_index >= len(queue_data):
                self.current_queue_index = 0
                print("队列已完成一轮，重新开始...")

            current_item = queue_data[self.current_queue_index]
            print(f"执行任务 {self.current_queue_index+1}/{len(queue_data)}: {current_item['url']}")

            # 执行浏览操作
            self._browse_url(current_item)

            # 检查是否有循环设置
            loop_type = current_item.get('loop_type', 'count')
            loop_count = current_item.get('loop_count', 1)
            loop_time = current_item.get('loop_time', 5)

            # 更新计数器或检查时间
            if loop_type == 'count':
                self.current_loop_count += 1
                print(f"循环次数: {self.current_loop_count}/{loop_count}")
                if self.current_loop_count >= loop_count:
                    self.current_loop_count = 0
                    self.current_queue_index += 1
                    print("完成循环次数，进入下一任务")
            else:  # 时间循环
                if self.start_time is None:
                    self.start_time = time.time()

                elapsed_minutes = (time.time() - self.start_time) / 60
                print(f"循环时间: {elapsed_minutes:.1f}/{loop_time}分钟")
                if elapsed_minutes >= loop_time:
                    self.start_time = None
                    self.current_queue_index += 1
                    print("完成循环时间，进入下一任务")

        # 关闭浏览器
        print("任务完成，关闭浏览器...")
        self.stop()

        # 处理自动关机
        if timer_settings['auto_shutdown'] and self.is_running_flag:
            print("准备自动关机...")
            # 这里应该调用系统关机命令
            # 由于安全原因，这里不实现实际关机功能
            pass

        self.is_running_flag = False
        print("浏览器控制器已停止")

    def _browse_url(self, item):
        """浏览URL"""
        if not self.is_running_flag or not self.page:
            return

        try:
            # 确保浏览器可见
            self._ensure_browser_visible()

            # 打开URL
            print(f"正在打开: {item['url']}")
            self.page.goto(item['url'], wait_until="domcontentloaded", timeout=60000)

            # 等待页面加载
            if item['wait_time'] > 0:
                print(f"等待页面加载: {item['wait_time']}秒")
                time.sleep(item['wait_time'])

            # 浏览页面
            if item['browse_time'] > 0:
                if item['scroll_enabled']:
                    print(f"浏览页面并滚动: {item['browse_time']}秒")
                    self._simulate_scrolling(item['browse_time'])
                else:
                    print(f"浏览页面: {item['browse_time']}秒")
                    time.sleep(item['browse_time'])

            # 关闭页面后等待
            if item['close_wait_time'] > 0:
                print(f"等待: {item['close_wait_time']}秒")
                time.sleep(item['close_wait_time'])

        except Exception as e:
            print(f"浏览URL失败: {e}")

    def _simulate_scrolling(self, duration):
        """模拟滚动"""
        start_time = time.time()

        while time.time() - start_time < duration and self.is_running_flag:
            try:
                # 获取页面高度
                page_height = self.page.evaluate("document.body.scrollHeight")

                # 随机滚动位置
                scroll_y = random.randint(0, page_height)

                # 执行滚动
                self.page.evaluate(f"window.scrollTo(0, {scroll_y})")

                # 随机等待一小段时间
                time.sleep(random.uniform(0.5, 2.0))

            except Exception as e:
                print(f"滚动失败: {e}")
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

            # 模拟用户交互，通常会使窗口前置
            self.page.mouse.move(100, 100)
            self.page.mouse.click(100, 100)

        except Exception as e:
            print(f"确保浏览器可见失败: {e}")




