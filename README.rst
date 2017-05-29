jp_tokenizer
============

This repository contains a tiny web service that lets you tokenize and lemmatize Japanese text.

The service is implemented by wrapping the `MeCab <http://taku910.github.io/mecab/>`_ tokenizer in a `Sanic <https://github.com/channelcat/sanic/>`_ app.

Usage
`````

.. sourcecode :: sh

  # install all dependencies on the machine and start the service
  curl 'https://raw.githubusercontent.com/CatalystCode/jp_tokenizer/master/setup_server.sh' | bash

  # call the API
  curl -X POST 'http://localhost/tokenize' --data 'サザエさんは走った'
  curl -X POST 'http://localhost/lemmatize' --data 'サザエさんは走った'

The API will respond with a space-delimited string of tokens/lemmas.
