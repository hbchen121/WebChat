import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from . import tasks

COMMANDS = {
    'help': {
        'help': '命令帮助信息.',
    },
    'add': {
        'args': 2,
        'help': '计算两个数之和, 例子: `add 12 32`.',
        'task': 'add'
    },
    'search': {
        'args': 1,
        'help': '通过名字查找诗人介绍，例子: `search 李白`.',
        'task': 'search'
    },
}

help_content = """
    目前支持 ChatGPT (OpenAI) 和 XiaoV (Tencent公众平台) 两种机器人，其中 ChatGPT 部署较为麻烦，可能存在错误。
    可以尝试使用 XiaoV 进行调试。有问题欢迎交流，github:  
"""


class BotConsumer(WebsocketConsumer):

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        src = text_data_json['source']

        response_message = '请输入`help`获取命令帮助信息。'
        source = '系统'
        message_parts = message.split()
        if message_parts:
            if message == 'help':
                response_message = help_content
            else:
                # getattr(tasks, "reply_by_xiaov").delay(self.channel_name, message)
                getattr(tasks, f"reply_by_{src}").delay(self.channel_name, message)
                source = '用户'
                response_message = message

        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                'type': 'chat.message',
                'message': response_message,
                'source': source,
            }
        )

    def chat_message(self, event):
        msg_type = event['source']
        message = event['message']

        # Send message to WebSocket
        self.send(json.dumps({
                'message': f'[{msg_type}]: {message}'
            }))


class BotConsumer_back(WebsocketConsumer):

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        response_message = '请输入`help`获取命令帮助信息。'
        message_parts = message.split()
        if message_parts:
            command = message_parts[0].lower()
            if command == 'help':
                response_message = '支持的命令有:\n' + '\n'.join(
                    [f'{command} - {params["help"]} ' for command, params in COMMANDS.items()])
            elif command in COMMANDS:
                if len(message_parts[1:]) != COMMANDS[command]['args']:
                    response_message = f'命令`{command}`参数错误，请重新输入.'
                else:
                    getattr(tasks, COMMANDS[command]['task']).delay(self.channel_name, *message_parts[1:])
                    response_message = f'收到`{message}`任务.'

        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                'type': 'chat.message',
                'message': response_message
            }
        )

    def chat_message(self, event):
        message = event['message']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'message': f'[机器人]: {message}'
        }))