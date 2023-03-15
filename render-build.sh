#!/usr/bin/env bash
# exit on error


apt-get -y update
apt-get install -y wget gnupg curl wkhtmltopdf\
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list

cp /usr/bin/wkhtmltopdf /usr/local/bin/wkhtmltopdf

# install google chrome
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
apt-get -y update
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
apt-get install -y google-chrome-stable

# install chromedriver
apt-get install -yqq unzip
wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


# add your own build commands...

pip install --upgrade pip
pip install -r requirements.txt
