#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Script to verify the behavior of a running jp_tokenizer server.

"""
from json import dumps
from json import loads
from typing import ByteString
from typing import Dict
from typing import Text
from unittest import TestCase
from urllib.request import Request
from urllib.request import urlopen


def _post(url: Text, body: ByteString, headers: Dict) -> Text:
    request = Request(url, body, headers)
    with urlopen(request) as connection:
        response = connection.read().decode('utf-8')
    return response


def _post_text(url: Text, payload: Text) -> Text:
    headers = {'Content-Type': 'text/plain; charset=utf-8'}
    body = payload.encode('utf-8')
    return _post(url, body, headers)


def _post_json(url: Text, payload: Dict) -> Text:
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    body = dumps(payload).encode('utf-8')
    return _post(url, body, headers)


class ServerTests(TestCase):
    url_base = 'http://localhost'

    def test_tokenize(self):
        url = self.url_base + '/tokenize'
        sentence = 'サザエさんは走った'

        response = _post_text(url, sentence)

        self.assertEqual(len(response.split(' ')), 4)

    def test_lemmatize(self):
        url = self.url_base + '/lemmatize'
        sentence = 'サザエさんは走った'

        response = _post_text(url, sentence)

        self.assertEqual(len(response.split(' ')), 4)

    def test_tokenize_batch(self):
        url = self.url_base + '/batch/tokenize'
        sentences = {'sentences': [{'jp': 'サザエさんは走った'}]}

        response = loads(_post_json(url, sentences))

        self.assertEqual(len(response['sentences']), 1)
        self.assertEqual(len(response['sentences'][0]['tokens']), 4)

    def test_lemmatize_batch(self):
        url = self.url_base + '/batch/lemmatize'
        sentences = {'sentences': [{'jp': 'サザエさんは走った'}]}

        response = loads(_post_json(url, sentences))

        self.assertEqual(len(response['sentences']), 1)
        self.assertEqual(len(response['sentences'][0]['lemmas']), 4)


if __name__ == '__main__':
    from sys import argv
    from unittest import main

    if len(argv) > 1:
        url_base = argv.pop(1)
        ServerTests.url_base = url_base

    main()
