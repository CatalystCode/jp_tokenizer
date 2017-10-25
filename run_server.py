#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""A simple webservice to tokenize and lemmatize Japanese text.

"""
from functools import lru_cache
from os import getenv
from typing import Iterable
from typing import Callable
from typing import Text

from MeCab import Tagger
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.response import json
from sanic.response import text
from sanic_cors import CORS

NLPFunc = Callable[[Text], Iterable[Text]]

app = Sanic(__name__)
CORS(app)


@app.route('/tokenize/', methods=['POST'])
async def tokenize(request: Request) -> HTTPResponse:
    return _process_single(request, _tokenize)


@app.route('/batch/tokenize/', methods=['POST'])
async def tokenize_batch(request: Request) -> HTTPResponse:
    return _process_batch(request, _tokenize, 'tokens')


@app.route('/lemmatize/', methods=['POST'])
async def lemmatize(request: Request) -> HTTPResponse:
    return _process_single(request, _lemmatize)


@app.route('/batch/lemmatize/', methods=['POST'])
async def lemmatize_batch(request: Request) -> HTTPResponse:
    return _process_batch(request, _lemmatize, 'lemmas')


def _process_single(request: Request, nlpfunc: NLPFunc):
    sentence = request.body.decode('utf-8')
    tokens = nlpfunc(sentence)
    return text(' '.join(tokens))


def _process_batch(request: Request, nlpfunc: NLPFunc, tokens_key: Text):
    sentences = (_['jp'] for _ in request.json['sentences'])
    tokens = [{'jp': _, tokens_key: list(nlpfunc(_))} for _ in sentences]
    return json({'sentences': tokens})


@lru_cache(maxsize=1)
def _get_tagger() -> Tagger:
    opts = getenv('MECAB_OPTS', '-d /usr/lib/mecab/dic/mecab-ipadic-neologd/')
    tagger = Tagger(opts)
    # for some reason the first request to the tagger doesn't produce output
    # so pre-warming it here once to avoid serving daft results later
    parsed = tagger.parseToNode('サザエさんは走った')
    while parsed:
        parsed = parsed.next
    return tagger


def _tokenize(sentence: Text) -> Iterable[Text]:
    parsed = _get_tagger().parseToNode(sentence)
    while parsed:
        token = parsed.surface.strip()
        if token:
            yield token
        parsed = parsed.next


def _lemmatize(sentence: Text) -> Iterable[Text]:
    parsed = _get_tagger().parseToNode(sentence)
    while parsed:
        # The format of parsed.features is:
        #
        # Original Form\tPart of Speech,
        # Part of Speech section 1,
        # Part of Speech section 2,
        # Part of Speech section 3,
        # Conjugated form,
        # Inflection,
        # Reading,
        # Pronounciation
        #
        features = parsed.feature.split(',')
        if features[0] != 'BOS/EOS':
            yield features[-3]
        parsed = parsed.next


if __name__ == '__main__':
    from argparse import ArgumentParser
    from multiprocessing import cpu_count
    from os import chdir
    from tempfile import gettempdir

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=80)
    args = parser.parse_args()

    chdir(gettempdir())
    app.run(host=args.host, port=args.port, workers=cpu_count())
