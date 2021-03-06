# -*- coding: utf-8 -*-
# @Time    : 2019/6/28 13:18
# @Author  : project
# @File    : chat.py
# @Software: PyCharm
import os
import time
import itchat
import logging
from datetime import datetime

"""
微信自动回复
pip install itchat

"""
class Itchat:
    def __init__(self):
        # 登录微信enableCmdQR表示的是当完全的命令行界面可以弹出文本绘制的二维码
        # 可以让你得以扫码登录，hotReload表示的连续几次运行不需要再次扫码
        itchat.auto_login(hotReload=True)
        self.flight_MD5()
        self.remarks = self.conf()

    # def log_init(self):
    #     """日志模块"""
    #     path = os.path.abspath('.') + r'\log\Push_record.txt'
    #     formatter = logging.Formatter('%(asctime)s | %(name)-6s | %(levelname)-6s| %(message)s')
    #     console = logging.StreamHandler()
    #     console.setLevel(logging.DEBUG)
    #     fh = logging.FileHandler(path, encoding='utf-8', mode='a+')
    #     fh.setLevel(logging.DEBUG)
    #     fh.setFormatter(formatter)
    #     console.setFormatter(formatter)
    #     # 如果需要同時需要在終端上輸出，定義一個streamHandler
    #     # print_handler = logging.StreamHandler()  # 往屏幕上输出
    #     # print_handler.setFormatter(formatter)  # 设置屏幕上显示的格式
    #     logger = logging.getLogger("Spider")
    #     # logger.addHandler(print_handler)
    #     logger.setLevel(logging.DEBUG)
    #     logger.addHandler(console)
    #     logger.addHandler(fh)
    #     return logger

    # def Login(self):
    #     content = itchat.search_friends()
    #     name = content['NickName']
    #     self.log.info("登录成功：{}".format(name))

    # def SendChatRoomsMsg(self, msg):
    #     """群组"""
    #     # 获取所有群的相关信息，update=True表示信息更新 name根据群名称获取指定群信息
    #     # myroom = itchat.get_chatrooms(update=True)
    #     path = os.path.abspath('.') + r'\log\Push_record.txt'
    #     myroom = itchat.search_chatrooms(name='蛋蛋')
    #     for room in myroom:
    #         if room['NickName'] == '蛋蛋':
    #             username = room['UserName']
    #             itchat.send_msg(msg, username)
    #             with open(path, 'a+', encoding='utf-8') as f:
    #                 f.write(msg + '\n')
    #             self.log.info("消息发送成功")
    #         else:
    #             self.log.info('No groups found')

    def conf(self):
        """读取配置文件"""
        path = os.path.abspath('.') + '\config\config.txt'
        with open(path, 'r', encoding='utf-8') as f:
            remarks = [i.replace('\n', '') for i in f.readlines()]

        # print('<font color="green">配置文件读取成功!推送好友：[{}]</font>'.format(remarks))
        return remarks

    def GetUserName(self):
        """获取用户UUID"""

        UID = []
        remarks = self.remarks
        for i in remarks:
            # 获取好友信息
            users = itchat.search_friends(i)
            if not users:
                # print('没有此好友')
                continue
            userName = users[0]['UserName']
            UID.append(userName)
        return UID

    def SendFriend(self, msg):
        """个人"""
        path = os.path.abspath('.') + r'\log\Push_record.txt'
        uaername = self.GetUserName()
        for i in uaername:
            itchat.send(msg, toUserName=i)
            # print("发送成功")
        with open(path, 'a+', encoding='utf-8') as f:
            f.write(msg + '\n')

    def flight_MD5(self):
        """"
        效验当日已发送短信航班信息 避免重复读取
        flight  航班号
        """

        # 短信发送日志信息
        path = os.path.abspath('.') + r'\log\Push_record.txt'
        if os.path.exists(path):
            # 获取文件创建日期
            filetime = os.path.getctime(path)
            mailtime = datetime.fromtimestamp(filetime).strftime('%Y-%m-%d')
            # 当前系统日期
            currdate = time.time()
            mailtime1 = datetime.fromtimestamp(currdate).strftime('%Y-%m-%d')
            # 判断文件创建日期是否等于当前系统日期 如不相等 删除前一天的发送记录
            if mailtime != mailtime1:
                os.remove(path)
                print("<font color='red'>日期更新,删除已推送航班信息记录文件!</font>")
                print("<font color='red'>文件删除中...等待5秒刷新系统缓存</font>")
                time.sleep(5)
            else:
                print("<font color='red'>航班发送记录文件日期没有更新!</font>")


# if __name__ == '__main__':
#     a = Itchat()
#     a.SendFriend('蛋蛋')