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


def getData(baseurl):
    html_url = askUrl(baseurl)
    soup = BeautifulSoup(html_url, 'html.parser')
    panel_title = soup.find_all('span',class_="panel-title")
    sheet_name = re.findall('>(.*?)</span>',str(panel_title))
    print("表sheet名字=====》",sheet_name)
    num_tags = soup.find_all('table', class_="table table-bordered table-history")
    title = re.findall(r'>([^<]+)</th>', str(num_tags))
    print("表头=====》",title)
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
        span_elements = row.find_all('span')
        for span in span_elements:
            print(span.get_text())
        print(td_content)
        print(a_content)


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


# def write_excel(json1,title):
#     excel_path = curPath + f'\\result\\{time1}_走势数据.xlsx'
#     if not os.path.exists(excel_path):
#         wr = pd.ExcelWriter(excel_path)
#         ew = pd.DataFrame(json1,columns=title)
#         ew.to_excel(wr,sheet_name=date,index=False)
#         wr.close()
#     else:
#         wr = pd.ExcelWriter(excel_path,mode="a",engine='openpyxl')
#         ew = pd.DataFrame(json1,columns=title)
#         ew.to_excel(wr,sheet_name=date,index=False)
#         wr.close()

if __name__ == '__main__':
    url = "https://caipiao.eastmoney.com/pub/Result/History/ssq?page=1"
    getData(url)
