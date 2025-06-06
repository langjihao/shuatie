# 自动化浏览器操作软件

这是一个基于Python、PyQt5和Selenium的自动化浏览器操作软件，可以按照设定的参数自动打开网页、浏览并关闭。

## 功能特点

1. **定时启动功能**
   - 直接启动：设定好参数后，点击开始直接运行
   - 倒计时启动：设定0.5~24小时的倒计时，精度1分钟
   - 时间点启动：设定24小时制的启动时间点

2. **浏览器操作**
   - 打开链接后等待时间：0~20秒，精度0.5秒
   - 浏览时间设置：0~30秒，精度0.5秒
   - 模拟滚动功能：随机起点和终点的滚动模拟
   - 关闭网页后等待时间：0~120秒，精度0.5秒

3. **队列管理**
   - 支持最多10个链接的队列
   - 每个链接可单独设置循环时间或次数
   - 空链接自动跳过处理

4. **自动关机功能**
   - 队列执行完毕后可选择自动关机
   - 关机前倒计时1~30分钟，可取消

5. **密码保护**
   - 基于当天日期计算的动态密码
   - 解锁前UI显示但无标注，且队列限制为1

## 系统要求

- Windows 10/11
- Microsoft Edge 或 360浏览器

## 安装方法

### 方法一：使用安装包

1. 下载最新的安装包
2. 运行安装程序，按照提示完成安装
3. 启动软件，输入密码解锁（密码规则见下文）

### 方法二：从源码运行

1. 安装Python 3.8或更高版本
2. 安装依赖项：`pip install -r requirements.txt`
3. 运行主程序：`python main.py`

## 密码规则

软件安装后需要密码解锁。密码规则如下：

- 密码基于当天日期计算：年月日数字乘以2的后6位数
- 如果解锁时间在当日中午12:00前（不含12:00），使用上述计算结果
- 如果解锁时间在当日中午12:00后（含12:00），使用上述计算结果减去12

例如：
- 当天日期为2025年5月8日，计算：250508×2=501016
- 如果在12:00前解锁，密码为：501016
- 如果在12:00后解锁，密码为：501016-12=501004

如果计算结果不足6位，在前面补0。

## 使用说明

1. 启动软件并输入密码解锁
2. 在队列管理选项卡中设置浏览参数和链接队列
3. 在定时设置选项卡中设置启动方式和自动关机选项
4. 点击"开始"按钮启动任务
5. 任务运行时可以最小化到系统托盘

## 注意事项

- 软件支持后台运行，可以最小化到系统托盘
- 每次重新安装或更换电脑后需要重新输入密码解锁
- 解锁前可以设置参数，但无法看到标签文字，且队列限制为1个

## 开发者信息

本软件基于以下技术开发：
- Python 3.8+
- PyQt5
- Selenium WebDriver
