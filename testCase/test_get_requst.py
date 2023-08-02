'''
- "url": "http://114.80.155.47:22013/v2/stockreportlist" #请求地址
  "method": "get" #请求方式
  "request": {    #请求参数，需要填写header则添加相应参数，需要填写queryParam则添加相应参数
    "header": {
      'Content-Type': 'application/json',
      'Token': 'MitakeWeb',
      "Symbol": "600000.sh",
      "Param": "-1,,20",
      "src": "d"
    }，
   "queryParam": {
    }
  }
  "customName": {
    "epic": "冒烟测试",
    "feature": "F10",
    "story": "xx接口",
    "title": "xx用例1",
  }
'''