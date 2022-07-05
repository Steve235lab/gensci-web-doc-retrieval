# email_sender.py
# 通过SMTP协议发送电子邮件
# Written on 2022/5/7 by Steve D. J.
# Modified on 2022/7/3 by Steve D. J. for gensci-web-doc-retrieval

import smtplib
from email.mime.text import MIMEText
from email.header import Header
import numpy as np
from controller import CONTROLLER


class EmailSender:
    auth_passport = CONTROLLER.email_auth_passport
    sender = CONTROLLER.email_sender
    subject = CONTROLLER.email_subject

    def __init__(self, receiver_address, username):
        self.receivers = []
        self.receivers.append(receiver_address)
        self.username = username
        self.server = smtplib.SMTP()
        self.server.connect(CONTROLLER.smtp_host)
        self.server.login(CONTROLLER.email_sender, self.auth_passport)
        self.message = None
        self.content = None
        self.confirm_code = None

    def generate_sign_up_content(self):
        # 生产随机8位验证码
        confirm_code = ''
        base = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f',
                'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q',
                'r', 'R', 's', 'S', 't', 'T', 'u', 'U', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z']
        base_len = len(base)
        for i in range(8):
            base_index = np.random.randint(0, base_len)
            confirm_code += base[base_index]
        # 拼接邮件正文内容
        self.content = self.username + '，你好！\n' \
                                       '之所以会收到这封电子邮件是因为你刚刚在gensci-web-doc-retrieval网站使用这个邮箱注册了账号。\n' \
                                       '如果你没有进行注册操作，请忽略此邮件。\n' \
                                       '你的验证码为：' + confirm_code + '\n' \
                                       '该邮件由程序自动生成并发送，请勿回复此邮件。'
        # 设定邮件正文和标题
        self.message = MIMEText(self.content, 'plain', 'utf-8')
        self.message['Subject'] = Header(self.subject, 'utf-8')

        # 保存验证码
        self.confirm_code = confirm_code

    def generate_search_completed_content(self, keywords):
        # 拼接邮件正文内容
        self.content = self.username + '，你好！\n' \
                                       '您在gensci-web-doc-retrieval网站对关键词 ' + keywords + ' 的搜索已完成，请登录网站查看结果\n' \
                                       '该邮件由程序自动生成并发送，请勿回复此邮件。'
        # 设定邮件正文和标题
        self.message = MIMEText(self.content, 'plain', 'utf-8')
        self.message['Subject'] = Header(self.subject, 'utf-8')

    def generate_reset_password_content(self):
        # 生产随机8位验证码
        confirm_code = ''
        base = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'A', 'b', 'B', 'c', 'C', 'd', 'D', 'e', 'E', 'f',
                'G', 'h', 'H', 'i', 'I', 'j', 'J', 'k', 'K', 'l', 'L', 'm', 'M', 'n', 'N', 'o', 'O', 'p', 'P', 'q', 'Q',
                'r', 'R', 's', 'S', 't', 'T', 'u', 'U', 'v', 'V', 'w', 'W', 'x', 'X', 'y', 'Y', 'z', 'Z']
        base_len = len(base)
        for i in range(8):
            base_index = np.random.randint(0, base_len)
            confirm_code += base[base_index]
        # 拼接邮件正文内容
        self.content = self.username + '，你好！\n' \
                                       '之所以会收到这封电子邮件是因为你刚刚在gensci-web-doc-retrieval网站试图重置账号的密码。\n' \
                                       '你的验证码为：' + confirm_code + '\n' \
                                       '该邮件由程序自动生成并发送，请勿回复此邮件。'
        # 设定邮件正文和标题
        self.message = MIMEText(self.content, 'plain', 'utf-8')
        self.message['Subject'] = Header(self.subject, 'utf-8')

        # 保存验证码
        self.confirm_code = confirm_code

    def send(self):
        self.server.sendmail(self.sender, self.receivers, self.message.as_string())
        print("已向用户" + self.username + "的电子邮箱" + self.receivers[0] + "发送邮件")


if __name__ == "__main__":
    my_sender = EmailSender("steve235lab@hotmail.com", "Steve")
    my_sender.generate_search_completed_content('114514')
    my_sender.send()
