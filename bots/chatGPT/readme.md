# ChatGPT 接口安装 (Server)

首先参考ChatGPT [git](https://github.com/acheong08/ChatGPT/wiki/Setup) 
对 config 进行配置，设置 session token

安装 `revChatGPT`

```shell
pip install --upgrade revChatGPT
```

安装 `Xcfb`

```shell
# Chrome Repo
sudo apt-get install fonts-liberation xdg-utils libxss1 libappindicator1 libindicator7
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome*.deb

sudo apt-get update

# Download
wget https://chromedriver.storage.googleapis.com/2.22/chromedriver_linux64.zip

sudo apt --fix-broken install
sudo apt-get install zip
sudo apt-get install unzip
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

其他包安装: 
```shell
pip install func_timeout # 防止超时
```

运行 chatgpt，chatgpt启动有时间限制`bots/chatGPT/gpt_robot.py:16`，防止卡死，如果超时可能配置错误

```shell
xvfb-run --auto-servernum --server-num=1 --server-args='-screen 0, 720x360x24' python chatGPT/gpt_robot.py 
```