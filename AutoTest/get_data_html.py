# -*-coding:GBK -*-
import os
import time
import pandas as pd
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
time1 = time.strftime('%Y%m%d_%H%M%S', time.localtime())
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
numbers = None
sheet_name = None
title = ['�ں�', '��������', '���', '��������', '����(Ԫ)', 'ȫ��Ͷע��(Ԫ)', 'һ�Ƚ�ע��', 'һ�Ƚ�����(Ԫ)', '���Ƚ�ע��', '���Ƚ�����(Ԫ)', '�ܽ����(Ԫ)']


def getData(baseurl):
    global numbers
    global sheet_name
    global title
    global data_list
    data_list = []
    html_url = askUrl(baseurl)
    soup = BeautifulSoup(html_url, 'html.parser')
    panel_title = soup.find_all('span',class_="panel-title")
    sheet_name = re.findall('>(.*?)</span>',str(panel_title))[0]
    # print("��sheet����=====��",sheet_name)
    num_tags = soup.find_all('table', class_="table table-bordered table-history")
    # title = re.findall(r'>([^<]+)</th>', str(num_tags))
    pages_div = soup.find("div",class_="pagination pagination-default pagination-sm pagination-centered")
    pages_a = pages_div.find_all("a")
    numbers = pages_a[-2].text
    # print(type(numbers))
    # if last_page_a.isnumeric(): # ����Ƿ�Ϊ����
    # print("��ͷ=====��",title)
    tbody = soup.find('tbody')
    rows = tbody.find_all('tr')
    for row in rows:
        cells = row.find_all('td')
        td_content = [cell.get_text(strip=True) for cell in cells]
        link = row.find('a')
        if link:
            a_content = link.get_text(strip=True)
        else:
            a_content = 'N/A'
        # span_elements = row.find_all('span')
        # for span in span_elements:
        #     print(span.get_text())
        # print(td_content)
        data_list.append(td_content)
    return data_list


def askUrl(requesturl):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    request = urllib.request.Request(requesturl, headers=header)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print("status ===>", e.code)
        if hasattr(e, "reason"):
            print("reason ===>", e.reason)
    return html


def write_excel(json1, title):
    excel_path = f'{sheet_name}.xlsx'
    if not os.path.exists(excel_path):
        # ����ļ������ڣ��������ļ���д������
        wr = pd.ExcelWriter(excel_path)
        ew = pd.DataFrame(json1, columns=title)
        ew.to_excel(wr, sheet_name=sheet_name, index=False)
        wr.close()
    else:
        # ����ļ��Ѵ��ڣ�׷�����ݵ������ļ�
        ew = pd.DataFrame(json1, columns=title)
        with pd.ExcelWriter(excel_path, mode="a", engine='openpyxl') as wr:
            ew.to_excel(wr, sheet_name=sheet_name, index=False)


if __name__ == '__main__':
    initial_url = f"https://caipiao.eastmoney.com/pub/Result/History/ssq?page=1"
    data_list = getData(initial_url)  # ��ȡ��һҳ�����ݲ���ֵ�� data_list
    if numbers is not None:
        for i in range(2, int(numbers) + 1):  # �ӵڶ�ҳ��ʼѭ��
            url = f"https://caipiao.eastmoney.com/pub/Result/History/ssq?page={i}"
            data_list += getData(url)  # ��ȡ���ݲ���ӵ� data_list ��
    write_excel(data_list, title)