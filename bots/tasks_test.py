from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from parsel import Selector
import requests
import sys
sys.path.append('')
from bots.chatGPT.gpt_robot import GPT_Robot


DEBUG = False
# channel_layer = get_channel_layer()
chatGPT = GPT_Robot(name="ChatGPT")


# @shared_task
# def add(channel_name, x, y):
#     message = '{}+{}={}'.format(x, y, int(x) + int(y))
#     async_to_sync(channel_layer.send)(channel_name, {"type": "chat.message", "message": message})
#     print(message)
#
#
# @shared_task
# def reply_by_chatGPT(channel_name, text):
#     message = chatGPT.send(text, debug=DEBUG)
#     async_to_sync(channel_layer.send)(channel_name, {"type": "chat.message", "message": message, 'source': 'chatGPT'})
#     print(message)


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

if __name__ == "__main__":

    text = "测试一下能连接吗"
    print(chatGPT.send(text, debug=DEBUG))
