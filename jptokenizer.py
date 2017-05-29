# coding: utf-8

from MeCab import Tagger
from sanic import Sanic 
from sanic.response import text
 
_tagger = Tagger('-d /usr/lib/mecab/dic/mecab-ipadic-neologd/')

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
    parsed = _tagger.parseToNode(sentence)
    while parsed:
        token = parsed.surface
        yield token
        parsed = parsed.next


def _lemmatize(sentence):
    node = _tagger.parseToNode(sentence)
    text_data_parsed_lemmatized = ''
    while node:
        node_list = node.feature.split(',')
        if node_list[0] == 'BOS/EOS':
            node = node.next
            continue
        else:
            text_data_parsed_lemmatized += node_list[-7]
            text_data_parsed_lemmatized += ' '
            node = node.next
    return text_data_parsed_lemmatized


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
