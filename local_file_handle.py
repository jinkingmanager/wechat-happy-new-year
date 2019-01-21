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

