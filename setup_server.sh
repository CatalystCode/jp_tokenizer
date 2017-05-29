#!/usr/bin/env bash

# install python
sudo apt-get install -y python3.5 python3-pip python3.5-dev build-essential
pip3 install --upgrade pip wheel

# install mecab tokenizer
sudo apt-get install -y mecab mecab-ipadic libmecab-dev mecab-ipadic-utf8
sudo apt-get install -y git
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
(cd mecab-ipadic-neologd; sudo ./bin/install-mecab-ipadic-neologd -n -y)

# install service
git clone --depth 1 https://github.com/CatalystCode/jp_tokenizer.git
(cd jp_tokenizer; pip3 install -r requirements.txt)

# enable service to run on port 80
sudo apt-get install -y authbind
sudo touch /etc/authbind/byport/80
sudo chown $USER:$USER /etc/authbind/byport/80
sudo chmod 755 /etc/authbind/byport/80

# auto-start service
sudo apt-get install -y supervisor
sudo service supervisor start
sudo tee /etc/supervisor/conf.d/jp_tokenizer.conf << EOF
[program:jp_tokenizer]
command=/usr/bin/authbind /usr/bin/python3 $(readlink -f jp_tokenizer/run_server.py)
directory=/tmp
autostart=true
autorestart=true
startretries=3
stderr_logfile=/var/log/jp_tokenizer.err.log
stdout_logfile=/var/log/jp_tokenizer.out.log
user=$USER
environment=
EOF
sudo supervisorctl reread
sudo supervisorctl update
