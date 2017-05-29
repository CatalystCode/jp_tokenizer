#!/usr/bin/env python3
# coding: utf-8

from MeCab import Tagger
from sanic import Sanic 
from sanic.response import text
 
tagger = Tagger('-d /usr/lib/mecab/dic/mecab-ipadic-neologd/')
app = Sanic(__name__) 
 

@app.route('/tokenize/', methods=['POST'])
async def tokenize(request):
    sentence = request.body.decode('utf-8')
    tokens = _tokenize(sentence)
    return text(' '.join(tokens))


@app.route('/lemmatize/', methods=['POST'])
async def lemmatize(request):
    sentence = request.body.decode('utf-8')
    lemmas = _lemmatize(sentence)
    return text(' '.join(lemmas))


def _tokenize(sentence):
    parsed = tagger.parseToNode(sentence)
    while parsed:
        token = parsed.surface
        yield token
        parsed = parsed.next


def _lemmatize(sentence):
    parsed = tagger.parseToNode(sentence)
    while parsed:
        features = parsed.feature.split(',')
        if features[0] != 'BOS/EOS':
            yield features[-3]
        parsed = parsed.next


if __name__ == '__main__':
    from argparse import ArgumentParser
    from multiprocessing import cpu_count

    parser = ArgumentParser()
    parser.add_argument('-h', '--host', default='0.0.0.0')
    parser.add_argument('-p', '--port', type=int, default=80)
    args = parser.parse_args()

    app.run(host=args.host, port=args.port, workers=cpu_count())
