.. image:: https://travis-ci.org/CatalystCode/jp_tokenizer.svg?branch=master
  :target: https://travis-ci.org/CatalystCode/jp_tokenizer

.. image:: https://img.shields.io/docker/pulls/cwolff/jp_tokenizer.svg
  :target: https://hub.docker.com/r/cwolff/jp_tokenizer/

jp_tokenizer
============

This repository contains a tiny web service that lets you tokenize and lemmatize Japanese text.

The service is implemented by wrapping the `MeCab <http://taku910.github.io/mecab/>`_ tokenizer in a `Sanic <https://github.com/channelcat/sanic/>`_ app.

Usage
`````

Ensure that your server has at least 2-3GB of available RAM (e.g. `Azure Standard DS1_v2 <https://docs.microsoft.com/en-us/azure/virtual-machines/linux/sizes-general#dsv2-series>`_) and then run:

.. sourcecode :: sh

  # install all dependencies on the machine and start the service
  docker run -p 8080:80 cwolff/jp_tokenizer

  # call the API
  curl -X POST 'http://localhost:8080/tokenize' --data 'サザエさんは走った'
  curl -X POST 'http://localhost:8080/lemmatize' --data 'サザエさんは走った'

The API will respond with a space-delimited string of tokens/lemmas.
