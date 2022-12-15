# encoding: utf-8
import sys
sys.path.append('')
from bots.chatGPT.config import config
from revChatGPT.revChatGPT import Chatbot
# from bots.revChatGPT.revChatGPT import Chatbot  # 本地测试用
import textwrap


def print_warp(instr):
    for i in textwrap.wrap(instr, width=50):
        print(i)


class GPT_Robot(object):
    def __init__(self, name='ChatGPT', conversation_id=None):
        self.chatbot = Chatbot(config, conversation_id=conversation_id)
        self.chatbot.reset_chat()  # Forgets conversation
        self.chatbot.refresh_session()  # Uses the session_token to get a new bearer token
        self.first_interact = True
        self.name = name

    def reset(self):
        self.chatbot.reset_chat()
        self.chatbot.refresh_session()
        self.first_interact = True

    def send(self, user_action, debug=False):
        try:

            if self.first_interact:
                if self.name != '':
                    prompt = """现在你想像自己是聊天机器人，你的名字叫""" + self.name + """。你在回答时要如果出现主语，
                            就用""" + self.name + """代替，现在我问你问题，问题是：""" + user_action
                else:
                    prompt = user_action
                self.first_interact = False
            else:
                prompt = """请继续以 ChatGPT 为主语进行回应，问题是：""" + user_action
            resp = self.chatbot.get_chat_response(prompt)  # Sends a request to the API and returns the response by OpenAI
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


def check_gpt(text):
    if "开启智能小骨" == text:
        return 1, "智能小骨已开启，关闭请输入‘关闭智能小骨’"
    elif "重置智能小骨" == text:
        return 1, "智能小骨已重置，关闭请输入‘关闭智能小骨’"
    elif "关闭智能小骨" == text:
        return 0, "智能小骨关闭，开启请输入‘开启智能小骨’"
    return None


if __name__ == '__main__':
    robot = GPT_Robot(name="小骨")
    text = "你在干啥"
    resp = robot.send(text)
    print(resp)
    robot.interactive()
    # IPython.embed()
    pass
