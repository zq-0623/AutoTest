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
# CORS(app, supports_credentials=True)  # ���ò���


@app.route('/sendmail', methods=["POST"])
def calculate_post():
    date1 = time.strftime('%Y%m%d', time.localtime())  # ��ǰ����
    # ����curl���͵��ļ�
    data = request.files
    # print(type(data))
    # print(data)
    file = data['log']
    content = file.read().decode('utf-8')
    print(content)
    # �ռ�������
    to_list = ['1977857241@qq.com', '2364617489@qq.com', '103060318@qq.com']
    # to_list = ['qukun@farben.com.cn', 'huangzhen@farben.com.cn', 'gerry.xu@farben.com.cn',
    #            'huangzhenfeng@farben.com.cn', 'liubin@farben.com.cn,weicheng1289@163.com',
    #            '103060318@qq.com']
    try:
        # ���� SMTP ����
        smtp = smtplib.SMTP()
        # ���ӣ�connect��ָ��������
        smtp.connect("smtp.qq.com", port=25)
        # ��¼����Ҫ����¼�������Ȩ��
        smtp.login(user="1977857241@qq.com", password="btujayflvxfbcjfa")

        message = MIMEMultipart()
        message['From'] = Header("��������", 'utf-8')  # �����˵��ǳ�
        # message['To'] = Header("jack", 'utf-8')  # �ռ��˵��ǳ�
        message['Subject'] = Header('��Դ����쳣', 'utf-8')  # ������������
        # �ʼ���������
        message.attach(MIMEText(content, 'plain', 'utf-8'))
        # ���츽��2�������ļ�
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
        print("Error: �޷������ʼ�")
        return "Error: �޷������ʼ�\n" + str(e)
    print("Success���ʼ����ͳɹ�")
    return "Success���ʼ����ͳɹ�"


if __name__ == '__main__':
    app.run(host='0.0.0.0', threaded=True, debug=False, port=8072)
