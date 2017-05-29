jp_tokenizer
============

This repository contains a tiny web service that lets you tokenize and lemmatize Japanese text.

The service is implemented by wrapping the `MeCab <http://taku910.github.io/mecab/>`_ tokenizer in a `Sanic <https://github.com/channelcat/sanic/>`_ app.

Usage
`````

First, we need to set up the service:

.. sourcecode :: sh

  # install all dependencies on the machine
  sudo ./setup_server.sh

  # run the api on port 80
  authbind python3 ./run_server.py

Now, we can call the API:

.. sourcecode :: sh

  curl -X POST 'http://localhost/tokenize' --data 'サザエさんは走った'
  curl -X POST 'http://localhost/lemmatize' --data 'サザエさんは走った'

The API will respond with a space-delimited string of tokens/lemmas.
