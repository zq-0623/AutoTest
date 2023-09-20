from bs4 import BeautifulSoup
import urllib.request,urllib.error

def getData(baseurl):
    datalist = []
    askUrl(baseurl)
    soup = BeautifulSoup(baseurl,'lxml')
    div_list = soup.find_all("div",class_= "panel primary-panel")
    print(div_list)




def askUrl(requesturl):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
    }
    request = urllib.request.Request(url,headers=header)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e,"code"):
            print("status ===>",e.code)
        if hasattr(e,"reason"):
            print("reason ===>",e.reason)
    return html


if __name__ == '__main__':
    url = "https://caipiao.eastmoney.com/pub/Result/History/ssq?page=1"
    getData(url)