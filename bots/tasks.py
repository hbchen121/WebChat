from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from parsel import Selector
import requests
import sys
sys.path.append('')

DEBUG = False
channel_layer = get_channel_layer()


@shared_task
def add(channel_name, x, y):
    message = '{}+{}={}'.format(x, y, int(x) + int(y))
    async_to_sync(channel_layer.send)(channel_name, {"type": "chat.message", "message": message})
    print(message)


from bots.chatGPT.gpt_robot import GPT_Robot

try:
    print("ChatGPT 启动中")
    chatGPT = GPT_Robot(name="ChatGPT")
    print("ChatGPT 启动成功")
except:
    chatGPT = None
    print("启动 GPT 超时")


@shared_task
def reply_by_chatgpt(channel_name, text):
    if chatGPT is None:
        message = "ChatGPT 暂时存在问题，可以先与 小微（xiaoV）互动"
    else:
        message = chatGPT.send(text, debug=DEBUG)
    async_to_sync(channel_layer.send)(channel_name, {"type": "chat.message", "message": message, 'source': 'chatGPT'})
    print(message)


# 先用这个机器人测试
from bots.online_robots.xiaov import get_answer as xiao_answer

@shared_task
def reply_by_xiaov(channel_name, text):
    message = xiao_answer(text, debug=DEBUG)
    # message = "xiaov" # xiao_answer(text, debug=DEBUG)
    async_to_sync(channel_layer.send)(channel_name, {"type": "chat.message", "message": message, 'source': 'xiaov'})
    print(message)


# @shared_task
# def search(channel_name, name):
#     spider = PoemSpider(name)
#     result = spider.parse_page()
#     async_to_sync(channel_layer.send)(channel_name, {"type": "chat.message", "message": str(result)})
#     print(result)


#
# class PoemSpider(object):
#     def __init__(self, keyword):
#         self.keyword = keyword
#         self.url = "https://so.gushiwen.cn/search.aspx"
#
#     def parse_page(self):
#         params = {'value': self.keyword}
#         response = requests.get(self.url, params=params)
#         if response.status_code == 200:
#             # 创建Selector类实例
#             selector = Selector(response.text)
#             # 采用xpath选择器提取诗人介绍
#             intro = selector.xpath('//textarea[starts-with(@id,"txtareAuthor")]/text()').get()
#             print("{}介绍:{}".format(self.keyword, intro))
#             if intro:
#                 return intro
#
#         print("请求失败 status:{}".format(response.status_code))
#         return "未找到诗人介绍。"

