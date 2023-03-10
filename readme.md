# WebChat

> 网页版的聊天机器人，兼容 OpenAI 的 ChatGPT，腾讯公众平台的聊天 XiaoV 等。
> 
> 选择网页版，而不是植入微信公众号或者个人微信，是因为本人尝试过后面两种，需要的权限更多，网页版则要求更少，更加可行。

## Notices

> 2023-01-02 最新：ChatGPT 已正常工作
> > 本项目的 ChatGPT 借助 [acheong08/ChatGPT](https://github.com/acheong08/ChatGPT) 实现，
但是 `The project has been archived due to severe limitations by Cloudflare.`， 所以 ChatGPT 暂时不可用。
我将持续关注其进度。

## 项目总览

目前项目部署在服务器[Link](http://101.42.32.28:8081/bots/) 中，参考[聊天机器人博客](https://www.jb51.net/article/213763.htm) 以及他的 [github 代码](https://github.com/shiyunbo/django-channels-chatbot) 进行修改, 作者提到原理：

- 用户在聊天界面调用Celery异步任务，Celery异步任务执行完毕后发送结果给channels，
  然后channels通过websocket将结果实时推送给用户。
  对于简单的算术运算，Celery一般自行计算就好了。
  对于网上查找诗人简介这样的任务，Celery会调用Python爬虫(requests+parsel)
  爬取古诗文网站上的诗人简介，把爬取结果实时返回给用户。

- 这个作者的机器人有两个，bots 和 chat，我们只需要用 Bots 就行。聊天界面等代码继承他的就行。

- 将 ChatGPT, xiaov 嵌入到 bots 中即可;

### install

下载本项目： `git clone git@github.com:hbchen121/WebChat.git`

根据 git 中的 requirements.txt 进行安装：
```shell 
cd WebChat
pip3 install -r requirements.txt
```

### Bots

- 如果使用ChatGPT, 则要进行 ChatGPT 安装[参考](./bots/chatGPT/readme.md)，其中包含了在服务器上部署安装 ChatGPT。

- XiaoV 不需要安装，直接运行后面即可。

### redis

使用了 redis做数据存储，根据[教程](https://www.runoob.com/redis/redis-install.html) 安装

- win 下载解压后执行 `redis-server.exe redis.windows.conf`
- ubuntu 通过 `sudo apt install redis-server` 安装，运行 `redis-server`;
  1. 若已开启则需要 `redis-cli shutdown; redis-server` 重启；
  2. 或者需要kill掉重启，参考[这个](https://blog.csdn.net/weixin_43493397/article/details/120342624) 
  ，即`ps -ef|grep redis`拿到pid，然后无缝运行 `kill -9 xxxx; redis-server`

## Celery

同样，按照博客安装后，需要开一个shell 在本文件夹下运行 Celery:
```shell 
# windows
Celery -A WebChat worker -l info -P eventlet

# Linux 不使用 ChatGPT 时
celery -A WebChat worker -l info
# linux 下需要安装图像界面，因为用了chatGPT，具体参考ChatGPT
xvfb-run --auto-servernum --server-num=1 --server-args='-screen 0, 720x360x24' celery -A WebChat worker -l info
```

如果运行出错，可能需要`pip install importlib-metadata==4.13.0`

## Django 
最后按那个教程运行 django，
```shell 
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py runserver
```

如果是服务器记得开放 8081 端口，将服务器ip添加到allowed_host里`WebChat/settings.py:30`，同时执行ip为`0.0.0.0`（见下面），不然无法外网访问：（参考 [csdn](https://blog.csdn.net/hlx20080808/article/details/121474156) ）
```shell 
# 不使用ChatGPT 时
python3 manage.py runserver 0.0.0.0:8081

# 使用ChatGPT 时服务器端要使用 xvfg
xvfb-run --auto-servernum --server-num=1 --server-args='-screen 0, 720x360x24' python3 manage.py runserver 0.0.0.0:8081
```

### issue

- html 可参考 [配置](./bots/templates/readme.md).

- `Exception inside application: [Errno 10061] Connect call failed` 错误是因为没有安装/启动 redis

- 如果发现网页报警`Socket closed unexpectedly, please reload the page.`，可能是 requirements.txt 没安装完，也可能是其他错误，在
`python manage.py` 的 terminal 里查询问题。
  
- 如果出现`aioredis.errors.ReplyError: ERR unknown command 'BZPOPMIN'`错误，可能是redis版本不到5.x，需要升级。参考[link](https://blog.csdn.net/guotianqing/article/details/114103122) 进行卸载
  `apt-get purge --auto-remove redis-server`， 然后使用源码安装方法进行redis安装，仍然参考[link](https://www.runoob.com/redis/redis-install.html),
  最后添加server的环境路径`export PATH=$PATH:/data/softwares/redis-6.0.8/src`, 这样就能直接
  `redis-server`
  

- 微信公众号有 5s 回复限制，超时回复会导致错误，因此ChatGPT 很难接入。

- 微信个人号要么需要网页登录，要么需要 windows 接口拦截，同时存在封号风险，慎用。

## others

其他好玩的东西：

- [WebChat 网页聊天机器人](https://github.com/hbchen121/WebChat)
- [QQChatGPT 聊天机器人](https://github.com/hbchen121/QQChatGPT)
- [WXSA_ROBOT 微信公众平台机器人](https://github.com/hbchen121/wxsa_robot)

### 欢迎大家关注我的公众号：

![QCode](bots/static/images/qcode.png)