'''
[
  {
    "url": "http://58.63.252.60:32041/v2/sh1/mink/",  #请求url，
                                                       可用动态参数代替填写不同环境的url
    "code": "$csv{code}",      #股票代码的动态参数，具体value填写在csv中
    "field": "kline",          #接口返回数据的key值，如果是day或者mink则不用更改
    "field_list": [            #接口返回数据的顺序及各字段名，请求day与mink时与select中的字段名称，
                                顺序相同，可自定义
      "date",
      "ref",
      "open",
      "high",
      "low",
      "close",
      "volume",
      "amount",
      "iopv",
      "fp_volume",
      "fp_amount",
      "avg"
    ],
    "method": "get",    #接口请求方式
    "csv_path": "../testCase/mds/mds.csv",  #用例数据路径
    "request": {
      "queryParam": {   #请求所需的param
        "select": "date,ref,open,high,low,close,volume,amount,iopv,fp_volume,fp_amount,avg",
        "begin": 0,
        "end": -1,
        "period": 1,
        "date": "20230222"
      }
    },
    "customName": {
      "epic": "mds数据比对",
      "feature": "历史K线",
      "story": "mink"，
      "title":"$csv{code}"
    }
  }
]
'''