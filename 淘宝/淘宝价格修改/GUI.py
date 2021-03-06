# -*- coding: utf-8 -*-
# @Time    : 2019/6/4 8:51
# @Author  : project
# @File    : GUI.py
# @Software: PyCharm

import sys
import subprocess
import configparser

import os
from PyQt5.QtGui import QIcon
from PyQt5.QtMultimedia import QSound
from PyQt5.QtCore import QThread, pyqtSignal, QFile, QTextStream
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QTextBrowser, QLineEdit

import res
from 毒APP爬虫.淘宝价格修改.TaoBaoLoginApi import Spider
from 毒APP爬虫.淘宝价格修改 import Main_PIPE


class CrawlWindow(QWidget):
    def __init__(self):
        super(CrawlWindow, self).__init__()
        self.resize(600, 400)
        self.setWindowTitle('淘宝在售商品价格修改')
        self.setWindowIcon(QIcon(':reson/maoyan.ico'))

        # 初始化增减价文本框
        self.price = QLineEdit(self)
        # 初始化运行时间间隔文本框
        self.counts = QLineEdit(self)
        # 初始化启动按钮
        self.start_btn = QPushButton(self)
        # 初始化输出文本框
        self.log_browser = QTextBrowser(self)

        # 初始化水平布局
        self.h_layout = QHBoxLayout()
        # 初始化垂直布局
        self.v_layout = QVBoxLayout()

        # 初始化音频播放
        self.btn_sound = QSound(':reson/btn.wav', self)
        self.finish_sound = QSound(':reson/finish.wav', self)

        # 实例化线程
        self.worker = MyThread()

        # 实例化
        self.movie_init()
        self.start_btn_init()
        self.remove_init()
        self.layout_init()
        self.set_log_init()

    def movie_init(self):
        """增减价格输入框默认配置"""
        # 设置文本框尺寸
        self.price.setFixedSize(150, 30)
        # 设置默认文本
        self.price.setPlaceholderText("输入增减价格(元)")
        # 限制10个中文字符
        self.price.setMaxLength(10)

    def remove_init(self):
        """运行时间间隔文本框默认配置"""
        # 设置文本框尺寸
        self.counts.setFixedSize(150, 30)
        # 设置默认文本
        self.counts.setPlaceholderText("输入程序运行间隔(默认10)")
        # 限制10个中文字符
        self.counts.setMaxLength(10)

    def start_btn_init(self):
        """ 启动按钮按钮 配置"""
        self.start_btn.setText('启动')
        # self.start_btn.setFixedSize(300, 30)
        self.start_btn.clicked.connect(self.start_btn_slot)

    def layout_init(self):
        """页面布局"""
        self.h_layout.addWidget(self.price)
        self.h_layout.addWidget(self.counts)
        self.h_layout.addWidget(self.start_btn)

        self.v_layout.addWidget(self.log_browser)
        self.v_layout.addLayout(self.h_layout)
        self.setLayout(self.v_layout)

    def start_btn_slot(self):
        """程序启动"""

        self.btn_sound.play()
        self.log_browser.append('<font color="green">{}程序启动{}</font>'.format('*'*20, '*'*20))
        self.input_process()
        # 设置按钮状态
        self.start_btn.setEnabled(False)
        # 启动线程
        self.worker.start()
        self.finish_sound.play()
        self.start_btn.setEnabled(True)

    def set_log_init(self):
        self.worker.log_signal.connect(self.set_log_slot)

    def set_log_slot(self, log):
        self.log_browser.append(log)

    def input_process(self):
        if self.counts.text():
            counts = int(self.counts.text())
        else:
            counts = 10

        if self.price.text():
            price = int(self.price.text())
        else:
            price = 0

        # 配置文件修改 set修改类型必须为str set后必须write写入保存
        cf = configparser.ConfigParser()
        path = os.path.abspath('.') + '\config\config.ini'
        cf.read(path, encoding='utf-8')
        cf.set('brower', 'price', str(price))
        cf.set('brower', 'counts', str(counts))
        cf.write(open(path, "r+"))
        self.log_browser.append('<font color="red">增减价：{}元,运行间隔：{}</font>'.format(price, counts))


class MyThread(QThread):

    log_signal = pyqtSignal(str)
    counts = None
    price = None

    def __init__(self):
        super(MyThread, self).__init__()

    def run(self):
        # 重写run方法
        # stdout PIPE 输出信息管道（把print信息重定向至管道）
        # stderr STDOUT 错误和日志信息管道
        # bufsize 缓冲设置默认值0 -- 表示不缓冲 1 -- 表示缓冲  NOTE: 如果遇到性能问题，建议将bufsize设置成 -1 或足够大的正数(如 4096）
        # r.poll()   检查子进程状态
        # r.kill()   终止子进程
        # r.send_signal() 向子进程发送信号
        # r.terminate()   终止子进程
        # r.returncode 子进程的退出状态
        # r.stdout.flush() 如果出现子进程假死 管道阻塞 手动刷新缓冲

        r = subprocess.Popen(['python', r'Main_PIPE.py'],  # 需要执行的文件路径
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT,
                             bufsize=0)
        while r.poll() is None:
            line = str(r.stdout.readline(), encoding='utf-8')
            line = line.strip()
            if line:
                self.log_signal.emit(line)
        # 判断子进程状态
        if r.returncode == 0:
            self.log_signal.emit('<font color="green">Subprogram success</font>')
        else:
            self.log_signal.emit('<font color="red">Subprogram failed</font>')


def read_qss(style):
    file = QFile(style)
    file.open(QFile.ReadOnly)
    return QTextStream(file).readAll()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CrawlWindow()
    qss_style = read_qss(':reson/style.qss')
    window.setStyleSheet(qss_style)
    window.show()
    sys.exit(app.exec_())