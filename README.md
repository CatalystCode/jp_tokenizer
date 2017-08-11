[![CI status](https://travis-ci.org/CatalystCode/jp_tokenizer.svg?branch=master)](https://travis-ci.org/CatalystCode/jp_tokenizer)
[![Docker status](https://img.shields.io/docker/pulls/cwolff/jp_tokenizer.svg)](https://hub.docker.com/r/cwolff/jp_tokenizer/)

[![Deploy to Azure](https://azuredeploy.net/deploybutton.svg)](https://azuredeploy.net/)

# jp_tokenizer #

This repository contains a tiny web service that lets you tokenize and lemmatize Japanese text.

The service is implemented by wrapping the [MeCab](http://taku910.github.io/mecab/) tokenizer in a [Sanic](https://github.com/channelcat/sanic/) app.

## Usage ##

Ensure that your server has at least 2-3GB of available RAM (e.g. [Azure Standard DS1_v2](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/sizes-general#dsv2-series)) and then run:

```bash
# start a container for the service and its dependencies
docker run -p 8080:80 cwolff/jp_tokenizer

# call the API
curl -X POST 'http://localhost:8080/tokenize' --data 'サザエさんは走った'
curl -X POST 'http://localhost:8080/lemmatize' --data 'サザエさんは走った'
```

The API will respond with a space-delimited string of tokens/lemmas.
