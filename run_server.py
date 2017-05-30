"""A simple webservice to tokenize and lemmatize Japanese text.

"""
from functools import lru_cache
from os import chdir
from os import getenv
from tempfile import gettempdir

from MeCab import Tagger
from sanic import Sanic
from sanic.response import text

chdir(gettempdir())
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


@lru_cache(maxsize=1)
def _get_tagger():
    opts = getenv('MECAB_OPTS', '-d /usr/lib/mecab/dic/mecab-ipadic-neologd/')
    return Tagger(opts)


def _tokenize(sentence):
    parsed = _get_tagger().parseToNode(sentence)
    while parsed:
        token = parsed.surface
        yield token
        parsed = parsed.next


def _lemmatize(sentence):
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
