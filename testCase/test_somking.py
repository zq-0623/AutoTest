'''
[
  {
    "url": "http://58.63.252.60:32041/v2/sh1/mink/",  #����url��
                                                       ���ö�̬����������д��ͬ������url
    "code": "$csv{code}",      #��Ʊ����Ķ�̬����������value��д��csv��
    "field": "kline",          #�ӿڷ������ݵ�keyֵ�������day����mink���ø���
    "field_list": [            #�ӿڷ������ݵ�˳�򼰸��ֶ���������day��minkʱ��select�е��ֶ����ƣ�
                                ˳����ͬ�����Զ���
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
    "method": "get",    #�ӿ�����ʽ
    "csv_path": "../testCase/mds/mds.csv",  #��������·��
    "request": {
      "queryParam": {   #���������param
        "select": "date,ref,open,high,low,close,volume,amount,iopv,fp_volume,fp_amount,avg",
        "begin": 0,
        "end": -1,
        "period": 1,
        "date": "20230222"
      }
    },
    "customName": {
      "epic": "mds���ݱȶ�",
      "feature": "��ʷK��",
      "story": "mink"��
      "title":"$csv{code}"
    }
  }
]
'''