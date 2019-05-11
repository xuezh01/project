# -*- coding: utf-8 -*-
# @Time    : 2019/5/5 16:09
# @Author  : project
# @File    : group_chat.py
# @Software: PyCharm
"""
自动添加群聊好友
"""

from appium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from appium.webdriver.connectiontype import ConnectionType
from selenium.webdriver.support import expected_conditions as EC
import time
import re


class GroupChat:
    def __init__(self):
        self.desired_caps = {
            "platformName": "Android",
            "deviceName": "OS105",
            "appPackage": "com.tencent.mm",
            "appActivity": ".ui.LauncherUI",
            "noReset": True  # 获取登录状态
        }
        self.driver_server = 'http://127.0.0.1:4723/wd/hub'
        print('微信启动...')
        # 启动微信
        self.driver = webdriver.Remote(self.driver_server, self.desired_caps)
        # 设置等待
        self.wait = WebDriverWait(self.driver, 30, 1, AttributeError)
        # 计数
        self.temp = []
        # 获取网络方式
        self.network = self.driver.network_connection

    def login(self):
        """登录模块"""

        print("-----点击登录-----")
        login = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/e4g')))
        login.click()

        # 输入手机号
        print("-----账号输入-----")
        phone = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/kh')))
        phone.click()
        phone_num = ""
        # phone_num = input('请输入账号：')
        # phone.send_keys(phone_num)
        phone.send_keys(phone_num)

        # 点击下一步
        print("-----点击下一步-----")
        button = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/axt')))
        button.click()

        # 输入密码
        print("-----密码输入-----")
        # pass_w = input('请输入密码：')
        pass_w = ""
        # presence_of_element_located 元素加载出，传入定位元组，如(By.ID, 'p')
        password = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/kh')))
        password.send_keys(pass_w)

        # 点击登录
        print("-----登录中-----")
        login = self.wait.until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/axt')))
        login.click()

        print("-----关闭通讯录弹窗-----")
        # WebDriverWait 10秒内每隔2秒运行一次直到找到元素 规定时间内找不到则报错 element_to_be_clickable 元素可点击
        tip = WebDriverWait(self.driver, 10, 2).until(EC.element_to_be_clickable((By.ID, 'com.tencent.mm:id/az9')))
        tip.click()

    def group_page(self):
        """进入群聊页面"""

        # 通讯录
        tab = self.wait.until(EC.presence_of_element_located((By.XPATH,
             '//*[@resource-id="com.tencent.mm:id/bq"]/android.widget.LinearLayout/android.widget.RelativeLayout[2]')))
        print('获取到通讯录按钮')
        tab.click()
        print("-----点击通讯录-----")

        # 群聊
        group = self.wait.until(EC.presence_of_element_located((By.XPATH,
             '//*[@resource-id="com.tencent.mm:id/mi"]/android.widget.LinearLayout/android.widget.RelativeLayout[2]')))
        print('获取到群聊按钮')
        group.click()
        print("-----点击群聊-----")

    def group_get(self):
        """获取群聊信息"""
        # 初始化返回按钮
        # self.driver.keyevent(4) = self.driver.find_element_by_accessibility_id("返回")

        # 获取群聊数量
        group_amount = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/b0p")))
        amount = group_amount.get_attribute("text")
        if int(amount[:1]) == 0:
            return print("该账号共有{}，退出系统。".format(amount))
        print("该账号共有{}".format(amount))

    def add_friend(self):
        """添加好友"""

        # 进入群聊页面 获取群列表
        group_item = self.driver.find_elements_by_id('com.tencent.mm:id/mz')
        for group in group_item:
            print('获取群聊:{}中...'.format(group.get_attribute("text")))
            group.click()

            # 进入群成员页面
            member = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/jy")))
            member.click()
            print("成功获取群成员")

            # 获取当前群聊成员数量
            member_number = self.wait.until(EC.presence_of_element_located((By.ID, "android:id/text1")))
            member_number = member_number.get_attribute("text")
            amount = re.search(r'\d+', member_number).group()
            print("该群共有：{}人".format(amount))

            # 判断当前页面是否有“查看全部群成员”标签
            view_all = self.driver.find_elements_by_id('android:id/title')
            # 群聊人数较少直接添加
            if len(view_all) != 0 and view_all[0].get_attribute("text") != '查看全部群成员':
                print("已显示全部群成员")

                # 获取当前群聊成员列表 发送添加请求 find_elements_by_id 此方法返回一个列表
                details = self.driver.find_elements_by_id('com.tencent.mm:id/e0c')
                for detail in details:
                    time.sleep(0.5)
                    # 判断"+"号 name = accessibility id
                    if detail.get_attribute("name") == "添加成员":
                        break
                    else:
                        detail.click()  # 进入个人详情

                    # 获取"添加到通讯录"标签
                    time.sleep(2)
                    friend_add = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/cs')))

                    # 判断是否已是好友
                    if friend_add.get_attribute('text') == '发消息':
                        wechat_number = self.driver.find_element_by_id('com.tencent.mm:id/b45')
                        print("{}：已经是您的好友".format(wechat_number.get_attribute("text")))
                        time.sleep(0.5)
                        self.driver.keyevent(4)
                        continue
                    else:
                        friend_add.click()  # 点击"添加到通讯录"
                        time.sleep(2)

                    # 判断对方是否设置隐私
                    privacy = self.driver.find_elements_by_id("com.tencent.mm:id/az_")
                    if len(privacy) != 0:
                        privacy[0].click()
                        time.sleep(0.5)
                        self.driver.keyevent(4)
                        continue

                    # 清空默认验证申请文本
                    clear_text = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/e0o")))
                    clear_text.clear()
                    time.sleep(0.5)

                    # 发送添加请求
                    # send = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/jx')))
                    # if not send.is_enabled():
                    #     send = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/jx')))
                    # time.sleep(0.5)
                    # send.click()
                    # time.sleep(0.5)
                    # self.driver.keyevent(4)
                    while True:
                        send = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/jx')))
                        if send.get_attribute("text") == "发送":
                            time.sleep(0.5)
                            send.click()
                            time.sleep(2)
                            self.driver.keyevent(4)
                            break

                        time.sleep(0.5)
                        self.driver.keyevent(4)
                        friend_add.click()

                time.sleep(0.5)
                self.driver.keyevent(4)
                time.sleep(0.5)
                self.driver.keyevent(4)
                self.group_page()

            elif len(view_all) == 0:
                self.driver.swipe(500, 1800, 500, 500, 2000)  # 向上滑一屏
                view_all = self.driver.find_elements_by_id('android:id/title')
                view = view_all[0].get_attribute("text")
                if view == "查看全部群成员":
                    view_all[0].click()
                    time.sleep(1)
                    self.driver.swipe(1000, 500, 1000, 1800, 2000)
                    time.sleep(0.5)
                    # 添加好友
                    while True:
                        flag = True
                        details = self.driver.find_elements_by_id('com.tencent.mm:id/auq')

                        for detail in details:
                            detail_text = detail.get_attribute("text")
                            time.sleep(0.5)
                            if len(self.temp) == int(amount):
                                flag = False
                                break
                            elif detail_text in self.temp:
                                continue

                            # 进入个人详情 获取"添加到通讯录"标签
                            detail.click()
                            time.sleep(3)
                            friend_add = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/cs')))

                            # 判断是否已是好友
                            if friend_add.get_attribute("text") == '发消息':
                                wechat_number = self.driver.find_element_by_id('com.tencent.mm:id/b45')
                                print("{}：已经是您的好友".format(wechat_number.get_attribute("text")))
                                self.temp.append(detail_text)
                                time.sleep(0.5)
                                self.driver.keyevent(4)
                                continue

                            # 点击添加到通讯录
                            friend_add.click()
                            time.sleep(1)

                            # 判断对方是否设置隐私
                            privacy = self.driver.find_elements_by_id("com.tencent.mm:id/az_")

                            if len(privacy) != 0:
                                privacy[0].click()
                                time.sleep(0.5)
                                self.driver.keyevent(4)
                                self.temp.append(detail_text)
                                continue

                            # 清空默认验证申请文本
                            clear_text = self.wait.until(EC.presence_of_element_located((By.ID, "com.tencent.mm:id/e0o")))
                            clear_text.clear()

                            # 发送
                            while True:
                                send = self.wait.until(EC.presence_of_element_located((By.ID, 'com.tencent.mm:id/jx')))
                                if send.get_attribute("text") == "发送":
                                    time.sleep(1)
                                    send.click()
                                    self.temp.append(detail_text)
                                    print("添加好友:{},消息发送成功".format(detail_text))
                                    time.sleep(2)
                                    self.driver.keyevent(4)
                                    break

                                time.sleep(0.5)
                                self.driver.keyevent(4)
                                friend_add.click()

                        if flag is False:
                            self.temp.clear()
                            break
                        self.driver.swipe(500, 1800, 500, 500, 2000)

                    time.sleep(0.5)
                    self.driver.keyevent(4)
                    time.sleep(0.5)
                    self.driver.keyevent(4)
                    self.group_page()

    def main(self):
        # self.login()
        self.group_page()
        self.group_get()
        self.add_friend()


if __name__ == '__main__':
    add = GroupChat()
    add.main()
