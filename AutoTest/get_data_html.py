from bs4 import BeautifulSoup
import urllib.request,urllib.error

def getData():
    datalist = []
    pass


def askUrl(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    request = urllib.request.Request(url,headers=header)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("GB2312")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("status ===>",e.code)
        if hasattr(e,"reason"):
            print("reason ===>",e.reason)
    print(html)


if __name__ == '__main__':
    url = "http://www.cwl.gov.cn/ygkj/wqkjgg/ssq/"
    askUrl(url)