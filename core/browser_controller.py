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

    def start(self, queue_data, timer_settings):
        """启动浏览器控制器"""
        if self.is_running_flag:
            return

        # 检查Playwright是否已安装
        global sync_playwright, PLAYWRIGHT_INSTALLED
        if not PLAYWRIGHT_INSTALLED:
            self._log("Playwright未安装，尝试安装...")
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
        self._pause_event.set()  # 确保线程不会卡在暂停状态
        self.is_paused = False

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

    def _init_browser(self):
        """初始化浏览器"""
        try:
            self._log("正在启动Playwright...")
            self.playwright = sync_playwright().start()

            self._log(f"正在启动{self.browser_type}浏览器...")
            # 浏览器启动选项
            browser_options = {
                "headless": self.headless,
                "args": [
                    "--disable-gpu",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--disable-setuid-sandbox",
                    "--window-size=1920,1080",
                ]
            }

            # 尝试启动Chromium浏览器
            try:
                self._log("尝试启动Chromium浏览器...")
                self.browser = self.playwright.chromium.launch(**browser_options)
                self._log("成功启动Chromium浏览器")
                self.browser_type = "chromium"
            except Exception as e:
                self._log(f"启动Chromium失败: {e}")
                # 尝试安装Chromium
                if self._install_browser("chromium"):
                    try:
                        self.browser = self.playwright.chromium.launch(**browser_options)
                        self._log("成功启动新安装的Chromium浏览器")
                        self.browser_type = "chromium"
                    except Exception as e:
                        self._log(f"启动新安装的Chromium失败: {e}")
                        raise e

            # 如果Chromium未成功启动，尝试Edge
            if not self.browser:
                try:
                    self._log("尝试启动Edge浏览器...")
                    self.browser = self.playwright.chromium.launch(
                        channel="msedge",
                        **browser_options
                    )
                    self._log("成功启动Edge浏览器")
                    self.browser_type = "msedge"
                except Exception as e:
                    self._log(f"启动Edge失败: {e}")
                    # 尝试安装Edge
                    if self._install_browser("msedge"):
                        try:
                            self.browser = self.playwright.chromium.launch(
                                channel="msedge",
                                **browser_options
                            )
                            self._log("成功启动新安装的Edge浏览器")
                            self.browser_type = "msedge"
                        except Exception as e:
                            self._log(f"启动新安装的Edge失败: {e}")
                            raise e

            # 如果Edge也未成功启动，尝试Chrome
            if not self.browser:
                try:
                    self._log("尝试启动Chrome浏览器...")
                    self.browser = self.playwright.chromium.launch(
                        channel="chrome",
                        **browser_options
                    )
                    self._log("成功启动Chrome浏览器")
                    self.browser_type = "chrome"
                except Exception as e:
                    self._log(f"启动Chrome失败: {e}")
                    # 尝试安装Chrome
                    if self._install_browser("chrome"):
                        try:
                            self.browser = self.playwright.chromium.launch(
                                channel="chrome",
                                **browser_options
                            )
                            self._log("成功启动新安装的Chrome浏览器")
                            self.browser_type = "chrome"
                        except Exception as e:
                            self._log(f"启动新安装的Chrome失败: {e}")
                            raise e

            if not self.browser:
                raise Exception("无法启动任何浏览器，请确保系统中已安装了Chrome、Edge或Chromium中的至少一个")

            self._log("创建浏览器上下文...")
            # 设置固定视口大小和位置
            context = self.browser.new_context(
                viewport={"width": 1920, "height": 1080},  # 固定视口大小为1920*1080
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"
            )

            self._log("创建新页面...")
            self.page = context.new_page()

            if not self.headless:
                # 非无头模式才设置窗口大小和位置
                self.page.evaluate("""
                () => {
                    // 将窗口移动到左上角并设置大小
                    window.moveTo(0, 0);
                    window.resizeTo(1920, 1080);
                    // 确保内容区域也是1920*1080
                    document.documentElement.style.width = '1920px';
                    document.documentElement.style.height = '1080px';
                    document.body.style.width = '1920px';
                    document.body.style.height = '1080px';
                }
                """)
            self._log("浏览器初始化成功！")

        except Exception as e:
            error_msg = f"初始化浏览器失败: {e}"
            self._log(error_msg)
            if self.playwright:
                try:
                    self.playwright.stop()
                except:
                    pass
                self.playwright = None
            raise Exception(error_msg)

    def _run_task(self, queue_data, timer_settings):
        """运行任务"""
        try:
            # 根据启动方式处理
            if timer_settings['start_type'] == 'countdown':
                # 倒计时启动
                total_minutes = timer_settings['countdown_hours'] * 60 + timer_settings['countdown_minutes']
                if total_minutes > 0:
                    self._log(f"将在{total_minutes}分钟后启动...")
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
                    self._log(f"将在{target_time}启动，等待{wait_seconds/60:.1f}分钟...")
                    time.sleep(wait_seconds)

            # 初始化浏览器
            self._init_browser()

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

            # 处理自动关机
            if timer_settings.get('auto_shutdown', False) and self.queue_completed:
                self._log("准备自动关机...")
                shutdown_minutes = timer_settings.get('shutdown_time', 5)
                from utils.helpers import shutdown_computer
                shutdown_computer(shutdown_minutes)

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
                self._init_browser()
            
            # 创建新的页面
            self._log("创建新页面...")
            context = self.browser.new_context(
                viewport={"width": 1920, "height": 1080},  # 设置固定视口大小
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36"  # 设置UA
            )
            self.page = context.new_page()

            if not self.headless:
                # 非无头模式才最大化窗口
                self.page.evaluate("() => { window.moveTo(0, 0); window.resizeTo(window.screen.availWidth, window.screen.availHeight); }")

            # 确保浏览器可见
            self._ensure_browser_visible()

            # 设置滚动速度和随机点击选项
            self.page.evaluate(f"window.__scroll_speed = {item.get('scroll_speed', 1.0)}")
            self.page.evaluate(f"window.__random_click = {str(item.get('random_click', False)).lower()}")

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

                # 如果启用随机点击
                if self.page.evaluate("() => window.__random_click || false"):
                    try:
                        # 获取可见元素
                        elements = self.page.evaluate("""
                        () => {
                            const elements = document.querySelectorAll('a, button, input[type="button"]');
                            return Array.from(elements).filter(el => {
                                const rect = el.getBoundingClientRect();
                                return rect.width > 0 && rect.height > 0 && 
                                       rect.top >= 0 && rect.left >= 0 &&
                                       rect.bottom <= window.innerHeight &&
                                       rect.right <= window.innerWidth;
                            }).map(el => ({
                                x: el.getBoundingClientRect().left + el.getBoundingClientRect().width / 2,
                                y: el.getBoundingClientRect().top + el.getBoundingClientRect().height / 2
                            }));
                        }
                        """)
                        
                        # 随机选择一个元素点击
                        if elements and random.random() < 0.1:  # 10%的几率点击
                            element = random.choice(elements)
                            self.page.mouse.click(element['x'], element['y'])
                    except Exception as e:
                        self._log(f"随机点击失败: {e}")

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

            # 模拟用户交互，通常会使窗口前置
            self.page.mouse.move(100, 100)
            self.page.mouse.click(100, 100)

        except Exception as e:
            self._log(f"确保浏览器可见失败: {e}")




