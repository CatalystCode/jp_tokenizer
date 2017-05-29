#!/usr/bin/env bash

sudo apt-get install -y python3 python3-pip
sudo apt-get install -y mecab mecab-ipadic libmecab-dev mecab-ipadic-utf8
sudo apt-get install -y git

git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
cd mecab-ipadic-neologd
sudo ./bin/install-mecab-ipadic-neologd -n

pip3 install mecab-python3 sanic
