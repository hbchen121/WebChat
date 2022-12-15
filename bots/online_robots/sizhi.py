# encoding: utf-8
"""
@author: chenhaobo.1013
@contact: haobochen@buaa.edu.cn
@time: 2022/10/26 14:05
@description:
    思知机器人: https://console.ownthink.com/dashboard
"""

import requests

# GRobot
_appid = "3df9e2c5410a9a3c812f45ef8ab2e0a0"
_user = "tOU2FqWI"


def get_data(text):
  # 请求思知机器人API所需要的一些信息
    data = {
        "appid": _appid,
        "userid": _user,
        "spoken": text,
    }
    return data


def get_answer(text):
    if text == '':
        return u"不要发送空内容哦"
    # 获取思知机器人的回复信息
    data = get_data(text)
    url = 'https://api.ownthink.com/bot'  # API接口
    # response = requests.post(url=url, data=data, headers=headers)
    response = requests.post(url=url, data=data)
    response.encoding = 'utf-8'
    result = response.json()
    answer = result['data']['info']['text']
    return answer


if __name__ == '__main__':
    import IPython
    IPython.embed()
    get_answer('你好')
    get_answer(u'你是谁')

