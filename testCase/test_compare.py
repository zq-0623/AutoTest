'''
[
  {
    "url1": "http://114.80.155.47:22013/v2/stockreportlist",
    "url2": "http://114.80.155.57:22013/v2/stockreportlist",
    "method": "get",
    "csv_path": "../testCase/compare/compare.csv",
    "request": {
      "header": {
        "Content-Type": "application/json",
        "Token": "MitakeWeb",
        "Symbol": "$csv{Symbol}",
        "Param": "$csv{Param}",
        "src": "d"
      }
    },
    "customName": {
      "epic": "数据比对",
      "feature": "F10",
      "story": "xx接口",
      "title": "xx用例1"
    }
  }
]
'''