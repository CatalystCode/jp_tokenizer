#!/usr/bin/env bash

sudo add-apt-repository -y ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install -y python3.6 python3-pip python3-dev build-essential

sudo apt-get install -y mecab mecab-ipadic libmecab-dev mecab-ipadic-utf8
sudo apt-get install -y git

git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
(cd mecab-ipadic-neologd; sudo ./bin/install-mecab-ipadic-neologd -n -y)

git clone --depth 1 https://github.com/CatalystCode/jp_tokenizer.git
(cd jp_tokenizer; pip3 install -r requirements.txt)
