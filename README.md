### PyQt5 - 使用 Qt 设计器生成对应的python文件
    pyuic5 -x demo.ui -o demo.py

### git pull拉取服务器代码时报错
    Your local changes will be overwritten by merge
        这是因为本地有文件改动未提交，并且该文件和git服务器最新版本有冲突，此时pull更新就会提示报错，无法更新、
    ## 处理方法一
        保留本地改动的同时，并且把git服务器上的代码pull下来：
            1、先把本地改动暂存到本地仓库，pull代码后再把这部分改动代码拿出来
            通过 git-->Uncommitted Changes-->Stash Changes,将本地的所有改动暂存到本地仓库
            2、开始pull服务器代码
            3、如果想把自己修改的代码从本地仓库中再拿出来，可以通过git-->unStash Changes把之前的改动合并到本地。
    ## 处理方法二
            直接覆盖本地的代码，放弃自己本地的改动，只保留服务端的代码
            1、直接git-->Reset head
            2、选择需要的reset模式
                git reset --soft 只是将HEAD引用指向指定的提交，工作区跟暂存区的内容不会改变
                git reset --mixed（默认选项）将HEAD指向指定的提交，暂存区的内容随之改变，工作区内容不变
                git reset --hard 将HEAD指向指定的提交，暂存区跟工作区都会改变

### 本地代码上传到GitHub
    1、为Github账户设置SSH key
        通过$ ssh-keygen -t rsa -C “1209405215@qq.com”来生成
        首先检查是否已生成密钥 cd ~/.ssh，ls如果有2个文件，则密钥已经生成，id_rsa.pub就是公钥
        也可以打开我的电脑C:\Users\Y\ .ssh 里面找到
    2、为github账号配置ssh key
        切换到github，展开个人头像的小三角，点击settings
        然后打开SSH keys菜单， 点击Add SSH key新增密钥，填上标题，跟仓库保持一致吧，好区分。
        接着将id_rsa.pub文件中key粘贴到此，最后Add key生成密钥吧。

### pycharm连接GitHub
    1、启动PyCharm，点击【File】→【Settings】→【Version Control】→【Git】，
    选择Git可执行文件路径（系统安装git后此处会默认显示路径），点击【Test】，
    路径下会显示当前Git版本
    
    2、点击【File】→【Settings】→【Version Control】→【GitHub】，点击【Log In via GitHub】
    
    3、授权GitHub给PyCharm：
    ①点击【Authorize in GitHub】，②登录GitHub，③输入收到的GitHub验证码，进行验证
    ②验证通过后回到PyCharm中，选择GitHub账号，修改连接超时时间，点击【OK】


### git本地上传代码命令
    ssh-keygen -t rsa -C "email"        //生成ssh key
    git init            //把这个目录变成Git可以管理的仓库
    git add README.md        //文件添加到仓库
    git add .             //不但可以跟单一文件，还可以跟通配符，更可以跟目录。一个点就把当前目录下所有未追踪的文件全部add了
    git commit -m "first commit"    //把文件提交到仓库
    git remote add origin git@github.com:zq-0623/AutoTest.git      //关联远程仓库
    git push -u origin master        //把本地库的所有内容推送到远程库上

###  当上传需要识别身份时：
        git config --global user.email "you@example.com"
        git config --global user.name "Your Name"

### git近期进行了版本升级，添加了新的目录安全限制。造成在进行git常规操作时，或在各类编辑器如VSCode中无法发现.git文件，报错：
        fatal: unsafe repository(xxx is owned by someone else.)
        To add an exception for this directory, call
        git config –global –add safe.directory  
        解决方法：git config --global --add safe.directory "*"

## 一.冒烟测试
### 1.模板编写
接口请求模板在testCase目录下自定义json文件中编写，如果需要填写动态参数，模板json中需添加csv_path,动态参数均在$csv{}中填写
![image.png](https://cdn.nlark.com/yuque/0/2023/png/25452916/1676625915197-d7630f73-36eb-491b-a203-81ea2cf2d82b.png#averageHue=%237e784d&clientId=u4c50f125-5bc0-4&from=paste&height=511&id=u624b94ea&name=image.png&originHeight=511&originWidth=1567&originalType=binary&ratio=1&rotation=0&showTitle=false&size=73519&status=done&style=none&taskId=u15ace0ed-b7f5-4cfa-9511-d5eeec96279&title=&width=1567)
冒烟测试的用例样式及说明如下：
```
#用例1：get请求
- "url": "http://114.80.155.437:22013/v2/stockreportlist" #请求地址
  "method": "get" #请求方式
  "request": {    #请求参数，需要填写header则添加相应参数，需要填写queryParam则添加相应参数
    "header": {  
      'Content-Type': 'application/json', 
      'Token': 'MitaykeWeb',
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

#用例2：post请求
- "url": "http://172.34.80.13:9000/api/testPlan/new"
  "method": "post"
  "request": {
    "header": {
      'Content-Type': 'application/json',
    },
    "body": {    
      "filterFactors": [ ],
      "location": "",
      "type": "update",
      "content": [
        {
          "confirmFlag": "1"
        }
      ]
    }

  }
  "customName": {
    "epic": "冒烟测试",
    "feature": "post",
    "story": "xx接口",
    "title": "xx用例1",
  }

```
customName下各字段值在测试报告中的意义如下图所示：
![image.png](https://cdn.nlark.com/yuque/0/2023/png/25452916/1676451920939-2f46cb6a-b180-4ad0-99c8-0a3eef98e836.png#averageHue=%23f1efea&clientId=uefef8773-1b5e-4&from=paste&height=479&id=HUoYS&name=image.png&originHeight=479&originWidth=1533&originalType=binary&ratio=1&rotation=0&showTitle=false&size=53443&status=done&style=none&taskId=u8a231ac6-c6c6-4950-9f16-22b63a50eb9&title=&width=1533)
### 2.用例编写
测试用例在testCase目录下自定义csv编写
![image.png](https://cdn.nlark.com/yuque/0/2023/png/25452916/1676625774096-f2feece8-ad11-452b-8624-3112e54ec236.png#averageHue=%23927b57&clientId=u4c50f125-5bc0-4&from=paste&height=663&id=u3d5b0b8b&name=image.png&originHeight=663&originWidth=1718&originalType=binary&ratio=1&rotation=0&showTitle=false&size=61079&status=done&style=none&taskId=ue71b63c6-6073-4f21-ac51-899c43a19a9&title=&width=1718)
### 2.程序运行
找到interface目录下的build_report.py
运行需要填写
```
# runType 可填两种值，smoke代表冒烟测试，compare代表数据比对
runType = "smoke"
# 线程数
num = 5
# 用例模板路径
model_path = '../testCase/F10/F10.json'
# 新生成的用例yaml路径
new_path = '../testCase/F10/F10.yaml'
# 报告名称
name = "接口自动化测试报告"
```
![image.png](https://cdn.nlark.com/yuque/0/2023/png/25452916/1676626147802-53d18f05-3ada-4e5c-9083-bb7db2b518bf.png#averageHue=%237d6d4a&clientId=u4c50f125-5bc0-4&from=paste&height=644&id=u320cd7cc&name=image.png&originHeight=644&originWidth=1731&originalType=binary&ratio=1&rotation=0&showTitle=false&size=104168&status=done&style=none&taskId=ubbb62823-9be7-4c5c-983c-b5f20df9ee8&title=&width=1731)
（2）report_name可自定义报告名称
![image.png](https://cdn.nlark.com/yuque/0/2023/png/25452916/1676452412260-e7c37aa4-d815-41f7-a2a0-5ebc1f7cbcea.png#averageHue=%23eae9e9&clientId=uefef8773-1b5e-4&from=paste&height=513&id=u83e43080&name=image.png&originHeight=513&originWidth=1695&originalType=binary&ratio=1&rotation=0&showTitle=false&size=43340&status=done&style=none&taskId=u84222816-e141-451c-a35d-9aba15df080&title=&width=1695)
完成上述操作后点击运行则可生成测试报告
![image.png](https://cdn.nlark.com/yuque/0/2023/png/25452916/1676452640810-4e3871df-9ab5-4a75-9acc-e7cb88d30de7.png#averageHue=%2377744a&clientId=uefef8773-1b5e-4&from=paste&height=514&id=u5c043a21&name=image.png&originHeight=514&originWidth=1318&originalType=binary&ratio=1&rotation=0&showTitle=false&size=70792&status=done&style=none&taskId=u034f81c8-71b8-4922-aa4a-bf5784217ba&title=&width=1318)
![image.png](https://cdn.nlark.com/yuque/0/2023/png/25452916/1676626361915-afb75374-f3ed-47ff-813d-13da5780b230.png#averageHue=%23ebebeb&clientId=u239630ff-e459-4&from=paste&height=881&id=u5e34c21c&name=image.png&originHeight=881&originWidth=1920&originalType=binary&ratio=1&rotation=0&showTitle=false&size=57381&status=done&style=none&taskId=u64f44551-b838-45c8-94b8-84101af7d90&title=&width=1920)
![image.png](https://cdn.nlark.com/yuque/0/2023/png/25452916/1676626348486-785a92ba-2cb7-4fe4-bdb1-50e8a5f039ed.png#averageHue=%23e6e5e4&clientId=u239630ff-e459-4&from=paste&height=725&id=ub4d8c6c6&name=image.png&originHeight=725&originWidth=1718&originalType=binary&ratio=1&rotation=0&showTitle=false&size=143918&status=done&style=none&taskId=ucfd0f4f9-3c02-4a2b-9d40-d705ea07581&title=&width=1718)
## 二.接口数据比对
### 1.模板编写
接口请求模板在testCase目录下自定义json文件中编写，如果需要填写动态参数，模板json中需添加csv_path,动态参数均在$csv{}中填写
![image.png](https://cdn.nlark.com/yuque/0/2023/png/25452916/1676940757597-7536a39c-4c13-45d0-bdf3-6bf1e571566b.png#averageHue=%237c774c&clientId=u63ad9558-d5f4-4&from=paste&height=629&id=u3dbaf0d1&name=image.png&originHeight=629&originWidth=1473&originalType=binary&ratio=1&rotation=0&showTitle=false&size=106648&status=done&style=none&taskId=u38075d5f-4594-4326-9f4d-11509b61889&title=&width=1473)
用例样式及说明如下：
```
[
  {
    "url1": "http://114.80.155.437:22013/v2/stockreportlist",
    "url2": "http://114.80.155.547:22013/v2/stockreportlist",
    "method": "get",
    "csv_path": "../testCase/compare/compare.csv",
    "request": {
      "header": {
        "Content-Type": "application/json",
        "Token": "MitaykeWeb",
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
```
### 2.程序运行
找到interface目录下的build_report.py
运行需要填写
```
# runType 可填两种值，smoke代表冒烟测试，compare代表数据比对
runType = "compare"
# 线程数
num = 5
# 用例模板路径
model_path = '../testCase/compare/compare.json'
# 新生成的用例yaml路径
new_path = '../testCase/compare/compare.yaml'
# 报告名称
name = "接口自动化测试报告"
```
## 三.mds接口数据与csv数据比对
### 1.模板编写
接口请求模板在testCase目录下自定义json文件中编写，如果需要填写动态参数，模板json中需添加csv_path,动态参数均在$csv{}中填写，
![image.png](https://cdn.nlark.com/yuque/0/2023/png/25452916/1677286716537-03e007ad-a20f-4e2e-b486-28993d6af58c.png#averageHue=%232d2b2b&clientId=u273e6aef-7ee7-4&from=paste&height=714&id=uf439260a&name=image.png&originHeight=714&originWidth=1602&originalType=binary&ratio=1&rotation=0&showTitle=false&size=89975&status=done&style=none&taskId=u2d374f84-7223-44d2-8d7e-4f42f2a2276&title=&width=1602)
冒烟测试的用例样式及说明如下：
```
[
  {
    "url": "http://58.63.252.68:32041/v2/sh1/mink/",  #请求url，
    "url": "http://58.63.252.68:32041/v2/sh1/mink/",  #请求url，
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
```
customName下各字段值在测试报告中的意义如下图所示：
![image.png](https://cdn.nlark.com/yuque/0/2023/png/25452916/1677287587225-ec8321b9-1838-4104-b48b-5f37a8a414e3.png#averageHue=%23eeeae8&clientId=u273e6aef-7ee7-4&from=paste&height=759&id=u9fa02678&name=image.png&originHeight=759&originWidth=1829&originalType=binary&ratio=1&rotation=0&showTitle=false&size=106674&status=done&style=none&taskId=u296a18ae-ef8b-4cf8-9c15-0033eb75eb9&title=&width=1829)
### 2.程序运行
找到mds目录下的build_report.py
运行需要填写
```
# 线程数
num = 5
# 用例模板路径
model_path = '../testCase/mds/mds.json'
# 新生成的用例yaml路径
new_path = '../testCase/mds/mds.yaml'
# 清洗数据路径
data_path = 'E:\\code\\20230222-sh1\\Minute.csv'
# 清洗文件csv的各列名称，如果需要删除或者忽略某一列数据则命名为删除
columns_name = ['code', 'date', 'ref', 'open', 'high', 'low', 'close', 'volume', 'amount', 'iopv', 'fp_volume',
                'fp_amount','avg', '删除', '删除']
# 报告名称
name = "接口自动化测试报告"
```
3.结果展示
测试结果展示在report目录下自动产出的测试报告中。
数据一直时结果展示为：
![image.png](https://cdn.nlark.com/yuque/0/2023/png/25452916/1677288066172-a3fd0111-36c2-4ef3-925c-f4ef06890251.png#averageHue=%23f3f2f0&clientId=u273e6aef-7ee7-4&from=paste&height=586&id=u4f9a3569&name=image.png&originHeight=586&originWidth=1781&originalType=binary&ratio=1&rotation=0&showTitle=false&size=62214&status=done&style=none&taskId=ub34769da-9e35-4500-9ec6-a0233f3caa1&title=&width=1781)
数据不一致时结果展示为
![image.png](https://cdn.nlark.com/yuque/0/2023/png/25452916/1677288209552-69caefd6-ff62-47b0-9205-e7731db62157.png#averageHue=%23fbf7f5&clientId=u273e6aef-7ee7-4&from=paste&height=854&id=uee9b7fe0&name=image.png&originHeight=854&originWidth=1741&originalType=binary&ratio=1&rotation=0&showTitle=false&size=119675&status=done&style=none&taskId=u2efccf85-ba15-4314-9e94-d4d2ac3fd8e&title=&width=1741)
![image.png](https://cdn.nlark.com/yuque/0/2023/png/25452916/1677288247892-686fd466-1356-47b3-b0d3-0f01c5a93958.png#averageHue=%23f1f1f1&clientId=u273e6aef-7ee7-4&from=paste&height=717&id=u52bba5cc&name=image.png&originHeight=717&originWidth=1529&originalType=binary&ratio=1&rotation=0&showTitle=false&size=144709&status=done&style=none&taskId=u8390308b-35a9-4b0f-b0e0-0b8cb1446d0&title=&width=1529)
