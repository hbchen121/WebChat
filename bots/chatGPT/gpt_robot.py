# encoding: utf-8
import sys
sys.path.append('')
from bots.chatGPT.config import config
from revChatGPT.ChatGPT import Chatbot
from func_timeout import func_set_timeout
import textwrap


def print_warp(instr):
    for i in textwrap.wrap(instr, width=50):
        print(i)


class GPT_Robot(object):
    @func_set_timeout(30)  # 超时装饰器
    def __init__(self, name='ChatGPT', conversation_id=None):
        self.chatbot = Chatbot(config, conversation_id=conversation_id)
        self.first_interact = True
        self.name = name
        self.reset()  # Forgets conversation
        self.text_length_limit = 50

    def reset(self):
        self.chatbot.reset_chat()
        self.chatbot.refresh_session()
        self.first_interact = True

    def send(self, user_action, conversation_i=None, parent_id=None, debug=False):
        try:

            if self.first_interact:
                if self.name != '':
                    prompt = """现在你想像自己是聊天机器人，你的名字叫""" + self.name + """。你在回答时要如果出现主语，
                            就用""" + self.name + """代替，每句话不要超过""" + str(self.text_length_limit) + \
                             """字，如果你没说完我会继续问你。现在我问你问题，问题是：""" + user_action
                else:
                    prompt = user_action
                self.first_interact = False
            else:
                prompt = """请继续以 """ + self.name + """ 为主语进行回应，每句话同样不要超过""" + str(self.text_length_limit) + \
                             """字，如果你没说完我会继续问你。问题是：""" + user_action
            resp = self.chatbot.ask(prompt, conversation_i, parent_id)  # Sends a request to the API and returns the response by OpenAI
            # print(resp)
            response = resp["message"]
        except Exception as e:
            print(f"{self.name} 错误: {e}")
            response = f"{self.name} 错误: {e}" + "(ChatGPT 目前存在问题，正在修复中)"
        if debug:
            response = response + f"({self.name} debug)"
        return response

    def interactive(self):
        print_warp(self.name)
        while True:
            action = input("")
            rep = self.send(action)
            # print_warp(rep)
            print(rep)


if __name__ == '__main__':


    try:
        print("ChatGPT 启动中")
        robot = GPT_Robot(name="小骨")
        print("ChatGPT 启动成功")
    except:
        robot = None

    if robot is None:
        print("启动 GPT 超时")
    else:
        text = "你在干啥"
        resp = robot.send(text)
        print(resp)
        robot.interactive()
    # import IPython
    # IPython.embed()
    pass
