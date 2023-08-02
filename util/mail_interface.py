# -*-coding:GBK -*-
import smtplib
import time

from email.header import Header
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)


# app.debug = True
# CORS(app, supports_credentials=True)  # 设置参数


@app.route('/sendmail', methods=["POST"])
def calculate_post():
    date1 = time.strftime('%Y%m%d', time.localtime())  # 当前日期
    # 接受curl发送的文件
    data = request.files
    # print(type(data))
    # print(data)
    file = data['log']
    content = file.read().decode('utf-8')
    print(content)
    # 收件人邮箱
    to_list = ['1977857241@qq.com', '2364617489@qq.com', '103060318@qq.com']
    # to_list = ['qukun@farben.com.cn', 'huangzhen@farben.com.cn', 'gerry.xu@farben.com.cn',
    #            'huangzhenfeng@farben.com.cn', 'liubin@farben.com.cn,weicheng1289@163.com',
    #            '103060318@qq.com']
    try:
        # 创建 SMTP 对象
        smtp = smtplib.SMTP()
        # 连接（connect）指定服务器
        smtp.connect("smtp.qq.com", port=25)
        # 登录，需要：登录邮箱和授权码
        smtp.login(user="1977857241@qq.com", password="btujayflvxfbcjfa")

        message = MIMEMultipart()
        message['From'] = Header("法本测试", 'utf-8')  # 发件人的昵称
        # message['To'] = Header("jack", 'utf-8')  # 收件人的昵称
        message['Subject'] = Header('资源监控异常', 'utf-8')  # 定义主题内容
        # 邮件正文内容
        message.attach(MIMEText(content, 'plain', 'utf-8'))
        # 构造附件2，传送文件
        att2 = MIMEText(content, 'utf-8', 'utf-8')
        att2["Content-Type"] = 'application/octet-stream'
        att2["Content-Disposition"] = f'attachment; filename="{date1}_monitor.log"'
        message.attach(att2)
        # print(message)
        smtp.sendmail(from_addr="1977857241@qq.com",
                      to_addrs=to_list,
                      msg=message.as_string())
    except smtplib.SMTPException as e:
        print(e)
        print("Error: 无法发送邮件")
        return "Error: 无法发送邮件\n" + str(e)
    print("Success：邮件发送成功")
    return "Success：邮件发送成功"


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=False, port=8072)
