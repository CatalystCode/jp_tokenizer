#!/usr/bin/env bash

sudo apt-get install -y python3.5 python3-pip python3.5-dev build-essential
pip3 install --upgrade pip wheel

sudo apt-get install -y mecab mecab-ipadic libmecab-dev mecab-ipadic-utf8
sudo apt-get install -y git

git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
(cd mecab-ipadic-neologd; sudo ./bin/install-mecab-ipadic-neologd -n -y)

git clone --depth 1 https://github.com/CatalystCode/jp_tokenizer.git
(cd jp_tokenizer; pip3 install -r requirements.txt)
