每逢过年过节，微信送上祝福总是必要的，只是群发总是不可取的，首先一眼看上去就是千篇一律的群发信息，送上的并不是祝福，而是骚扰了；其次微信的群发助手，有诸多限制，用起来也各种不便。

itchat是一个python框架，专门用于扩展部分微信功能。这里写了个简单的脚本，基于微信中对你对朋友的备注名称，做了少许的定制化信息。

#### 安装python3 及 itchat

在这里使用python3.6，在deepin linux下安装环境：

```bash
sudo apt-get install python3 python3-pip
```

安装完成后，使用pip3 安装itchat

```bash
pip3 install itchat
```

关于itchar，可以参考这里：https://itchat.readthedocs.io/zh/latest/

#### 配置pycharm开发环境

下载pycharm CE版，免费的就好，下载地址：https://www.jetbrains.com/pycharm/download/download-thanks.html?code=PCC  下载后，解压，bash中执行 pycharm***\bin\pycharm.sh，打开pycharm IDE

然后创建一个project，比如这里叫做wechat-robot，注意选择python的版本，如下图所示：

![wechat-robot.png](https://upload-images.jianshu.io/upload_images/2143704-a175f1964915bf87.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/1240)

#### 编写工具代码

创建一个python脚本文件 local_file_handle.py ，用于提供写一个dict入文本文件、以及从文本文件中获取dict结构的方法，供代码中使用。

```python
#coding=utf8
# 读取自定义文件
import json


def getDictFromFriendFile(filename):
    local_friend_file = open(filename,'r')
    nickNameAsKeyDict = eval(local_friend_file.read())  # 读取的str转换为字典
    return nickNameAsKeyDict


# 写入文件
def writeToFriendFile(filename,nameDict):
    fw = open(filename, 'w+')
    # 格式化json文件，并处理中文数据
    json_dicts = json.dumps(nameDict, indent=4, ensure_ascii=False)
    fw.write(str(json_dicts))  # 把字典转化为str
    fw.close()


```

#### 编写逻辑代码

下面是大头，先说下思路：

1、运行当前代码，扫码登陆后，获取用户的所有朋友列表

2、使用friend['NickName']作为key，也就是昵称，这个是肯定都有数据的；使用对friend标注的RemarkName作为value，如果为空，则使用friend['DisplayName']替代，依然为空，则保底使用friend['NickName']

3、将这个dict字典写入到本地，文件命名规则是 本人微信账户昵称--wechat-friends.json。如果已经存在这个文件，则会直接走到发送逻辑，否则是写入文件的逻辑。

4、修改文件中每行冒号后面的数据，也就是你希望在祝福话中的对方的称呼，比如：

```json
{
  '时尚': '时尚哥-',
  '杰克': '杰克大神-',
  '玉儿': '玉儿姐姐-',
  'Anson Ｘ': '张老板-',
  'sisi': '思思',
  'Edson': 'E神'
}
```

这里注意下，冒号前面的东西千万别动，这个是从微信中直接获取的，直接修改后面单引号中的内容。这里做了个通用处理，如果不包含"-"这个横杠，则统一在后面添加“同学”二字，比如“思思同学”；如果包括，则不添加任何后缀，只替换掉“-”。

另外，如果不想给某人发祝福，直接把json文件中的某人那一行删掉就好了，会自动跳过的。

5、修改完成后，再次运行代码，就会发现已经在发送祝福信息了。

附上代码：

```python
#coding=utf8
import itchat, time, os

from local_file_handle import getDictFromFriendFile
from local_file_handle import writeToFriendFile

itchat.auto_login(hotReload=True) # 记录登录数据

SINCERE_WISH = u'2019万事如意 春节快乐呀，%s'

Title = '同学'

allFriendList = itchat.get_friends(update=True)

myself = allFriendList[0]

friendList = allFriendList[1:]

print("total friends:", len(friendList))

# 发送数目统计
send_count=0

filePath = myself['NickName'] + "-wechat-friends.json"

namesDict = {}
totalDict = {}
if os.path.exists(filePath):
    namesDict = getDictFromFriendFile(filePath)

else:
    print("您的friend列表文件尚不存在，创建中...")
    for friend in friendList:
        # 如果是演示目的，把下面的方法改为print即可
        # itchat.send()
        totalDict[friend['NickName']] = friend['RemarkName'] or friend['DisplayName'] or friend['NickName']

    writeToFriendFile(filePath, totalDict)
    print("您的friend列表文件已经创建成功，文件名：", filePath)
    print("现在可以去修改文件中冒号后面的称呼，切记，单引号要存在，冒号之前的数据千万不要修改!")
    print("如果希望直接以称呼名为准，请在称呼名后加入‘-’，否则默认在称呼名后加上”同学“二字!")
    print("如果不希望给某人发信息，直接删除对应行即可")
    print("修改完成后，请重新运行当前脚本")
    # 记得手动在里面改文件里面冒号后面的称呼，如果希望直接以称呼名为准，请在称呼名后加入‘-’，否则默认在称呼名后加上”同学“二字
    # namesDict = getDictFromFriendFile(filePath)

notSendList = []

if namesDict:
    print(u"您要发送 %s 条数据" % len(namesDict))
    print("开始发送微信消息...")

for friend in friendList:
    # 如果是演示目的，把下面的方法改为print即可
    #itchat.send()
    if namesDict.get(friend['NickName']):
        showName = namesDict[friend['NickName']]

        # 如果包含“-”，则直接replace掉“-”，不添加Title
        if '-' in showName:
            print(SINCERE_WISH % showName.replace('-',''), friend['UserName'])
        else:
            newHappyNewYear = SINCERE_WISH + Title
            # print(SINCERE_WISH % showName,Title)
            print(newHappyNewYear % showName, friend['UserName'])

        send_count = send_count + 1
        time.sleep(.5)
    else:
        notSendList.append(friend)

    # print(SINCERE_WISH % (friend['DisplayName']
    #      or friend['NickName']), friend['UserName'])
    # time.sleep(.5)

if namesDict:
    print("send count",send_count)

    print("unsend count",len(notSendList))
    print(notSendList)
```

最终运行后，结果如下：

```
total friends: 6
2019万事如意 春节快乐呀，时尚哥 @7119bba52a3b183a945c30cee6a64eb58
2019万事如意 春节快乐呀，杰克大神 @3b05adce56650c65cd2031d839741
2019万事如意 春节快乐呀，玉儿姐姐 @503ef5fe2c2132cd2a6c82fd7
2019万事如意 春节快乐呀，张老板 @0f4a4847a4f57f8c2af3cb647
2019万事如意 春节快乐呀，思思同学 @91bde667b213cdf56e0f1f76fcbb82
2019万事如意 春节快乐呀，E神同学 @7c0d54fe32dd342b2c4f5f5e9ab
send count: 6
unsend count: 0
```

@XXXX那一串数据不用管，只是发送的目标对象。

到这里就OK啦！另外，测试时，千万要将 itchat.send 替换成print，否则...真的是骚扰了...
