# -*- coding: utf-8 -*-
"""A simple webservice to tokenize and lemmatize Japanese text.

"""
from functools import lru_cache
from os import chdir
from os import getenv
from tempfile import gettempdir
from typing import Iterable
from typing import Callable
from typing import Text

from MeCab import Tagger
from sanic import Sanic
from sanic.request import Request
from sanic.response import HTTPResponse
from sanic.response import json
from sanic.response import text

NLPFunc = Callable[[Text], Iterable[Text]]

chdir(gettempdir())
app = Sanic(__name__)


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
        token = parsed.surface
        yield token
        parsed = parsed.next


def _lemmatize(sentence: Text) -> Iterable[Text]:
    parsed = _get_tagger().parseToNode(sentence)
    while parsed:
        features = parsed.feature.split(',')
        if features[0] != 'BOS/EOS':
            yield features[-3]
        parsed = parsed.next


if __name__ == '__main__':
    from argparse import ArgumentParser
    from multiprocessing import cpu_count

    parser = ArgumentParser(description=__doc__)
    parser.add_argument('--host', default='0.0.0.0')
    parser.add_argument('--port', type=int, default=80)
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, workers=cpu_count())
