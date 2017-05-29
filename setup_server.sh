#!/usr/bin/env bash

# install python
sudo apt-get install -y python3.5 python3.5-venv python3.5-dev build-essential

# install mecab tokenizer
sudo apt-get install -y mecab mecab-ipadic libmecab-dev mecab-ipadic-utf8
sudo apt-get install -y git
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
(cd mecab-ipadic-neologd; sudo ./bin/install-mecab-ipadic-neologd -n -y)

# install service
python3.5 -m venv jp_tokenizer-env
jp_tokenizer-env/bin/pip install -U pip wheel
git clone --depth 1 https://github.com/CatalystCode/jp_tokenizer.git
jp_tokenizer-env/bin/pip install -r jp_tokenizer/requirements.txt

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
command=/usr/bin/authbind $PWD/jp_tokenizer-env/bin/python $PWD/jp_tokenizer/run_server.py
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
