# Overview

参考ChatGPT [git](https://github.com/acheong08/ChatGPT/wiki/Setup)

## install (in server)

`pip3 install revChatGPT --upgrade`

然后需要安装 playwright, 安装完成后测试一下是否正确：`from playwright.async_api import async_playwright`
(我在笔记本上安装失败了，会出现错误，但是服务器正常。)

下面需要在服务器上模拟桌面环境，问一下chatGPT
```
How to use Xvfb to emulate a desktop environment in ubuntu.
```

gpt 也说的不明显，我们直接参考这个[网址](https://www.cnblogs.com/lantai/p/9657822.html) （或者见Others） 安装谷歌和xvfb，如果出现提示，需要
`sudo apt --fix-broken install` 修改，还可能需要安装 
```shell 
sudo apt-get install zip
sudo apt-get install unzip
```

安装完成后，可以参考[这个网址](https://blog.csdn.net/chengly0129/article/details/72229537) 
看一下如何运行 chrome,
或者直接 用xvfb 运行你的程序，记得要配置 config.
```shell
xvfb-run --auto-servernum --server-num=1 --server-args='-screen 0, 1920x1080x24' python3 xxx
```

如果出现别的错误，比如`wrong response` 或者 `cf challenge fail`，应该是 config 不对，注意配置。

比如本项目的测试方法为：
```shell
xvfb-run --auto-servernum --server-num=1 --server-args='-screen 0, 1920x1080x24' python3 bots/chatGPT/gpt_robot.py
```

如果config 没问题还报错`cf challenge fail`，可以重复执行下，下一次执行可能就正确了。

此外，可能第一次get response 正常，第二次就会报错。这个目前等待 openai 修复，参考[issue](https://github.com/acheong08/ChatGPT/issues/359).

别的安装问题参考 ChatGPT [git](https://github.com/acheong08/ChatGPT).

## Others

```shell
# Chrome Repo
sudo apt-get install fonts-liberation xdg-utils libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb

sudo apt-get update

# Download
wget https://chromedriver.storage.googleapis.com/2.22/chromedriver_linux64.zip

#Extract
unzip chromedriver_linux64.zip

# Deploy + Permissions
sudo cp ./chromedriver /usr/bin/
sudo chmod ugo+rx /usr/bin/chromedriver

# Install Google Chrome:
sudo apt-get -y install libxpm4 libxrender1 libgtk2.0-0 libnss3 libgconf-2-4

# Dependencies to make "headless" chrome/selenium work:
sudo apt-get -y install xorg xvfb gtk2-engines-pixbuf
sudo apt-get -y install dbus-x11 xfonts-base xfonts-100dpi xfonts-75dpi xfonts-cyrillic xfonts-scalable

# Optional but nifty: For capturing screenshots of Xvfb display:
sudo apt-get -y install imagemagick x11-apps

# Make sure that Xvfb starts everytime the box/vm is booted:
echo "Starting X virtual framebuffer (Xvfb) in background..."
Xvfb -ac :99 -screen 0 1280x1024x16 &
export DISPLAY=:99

# Optionally, capture screenshots using the command:
#xwd -root -display :99 | convert xwd:- screenshot.png
```