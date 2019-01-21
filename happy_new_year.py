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
    time.sleep(.2)
    print("现在可以去修改文件中冒号后面的称呼，切记，单引号要存在，冒号之前的数据千万不要修改!")
    time.sleep(.3)
    print("如果希望直接以称呼名为准，请在称呼名后加入‘-’，否则默认在称呼名后加上”同学“二字!")
    time.sleep(.2)
    print("如果不希望给某人发信息，直接删除对应行即可")
    time.sleep(.3)
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