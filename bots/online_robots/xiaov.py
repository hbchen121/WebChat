# encoding: utf-8
"""
@author: chenhaobo.1013
@contact: haobochen@buaa.edu.cn
@time: 2022/10/26 14:05
@description:
    小v 机器人: https://openai.weixin.qq.com/@your9db8e/platform/publishManage/applicationBinding?active=api
"""

import requests
import json

# 机器人名称: 公众号
_appid = "L4RpTOZrifSqAj1"
_token = "2Tpn87851gjjw9T8qNLgea59kj3vq8"


def get_signature(vid, username):
    data = {
        "userid": str(vid),
        "username": username
    }
    url = f'https://openai.weixin.qq.com/openapi/sign/{_token}'
    response = requests.post(url=url, data=data)
    response.encoding = 'utf-8'
    result = response.json()
    return result['signature']


def get_answer(text, vid='0', username='', debug=True):
    if text == '':
        return u"不要发送空内容哦"

    data = {
        "signature": get_signature(vid, username),
        "query": text,
        "env": "debug" if debug else "online",
    }
    url = f'https://openai.weixin.qq.com/openapi/aibot/{_token}'
    # response = requests.post(url=url, data=data, headers=headers)
    response = requests.post(url=url, data=data)
    response.encoding = 'utf-8'
    result = response.json()
    answer = result['answer']
    # print(result)
    # IPython.embed()
    if answer == '':
        print(result)
        answer = 'back: ' + result['msg'][0]['content']
    else:
        answer = answer_format(answer)

    if debug:
        # print(answer)
        answer = str(answer) + "(小v debug)"
    return answer


def answer_format(answer):
    """
    判断需要回复的消息类型，转换为需要返回的类型
    """
    try:
        if "news" in answer:
            text = json.loads(answer)
            data = text["news"]["articles"][0]
            format_rep = {
                "type": "link_card",
                'title': data['title'],
                'desc': data['description'],
                'url': data['url'],
                'image_url': data['picurl']
            }
            return format_rep
    except Exception as e:
        # IPython.embed()
        print(e)
    return answer


if __name__ == '__main__':
    import IPython
    # IPython.embed()
    # get_answer('你好')
    # get_answer(u'你是谁')
    print(get_answer(u'七里香'))

