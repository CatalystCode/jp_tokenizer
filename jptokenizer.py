# coding: utf-8

from MeCab import Tagger
from sanic import Sanic 
from sanic.response import json
 
_tagger = Tagger('-d /usr/lib/mecab/dic/mecab-ipadic-neologd/')

app = Sanic(__name__) 
 

@app.route('/tokenize/', methods=['POST'])
async def tokenize(request):
    sentence = request.body.decode('utf-8')
    results = list(_tokenizer(sentence))
    return json({'tokens': results})


def _tokenizer(sentence):
    parsed = _tagger.parseToNode(sentence)
    while parsed:
        token = parsed.surface
        yield token
        parsed = parsed.next


def _parse_to_lemmatized_whitespaced(sentence):
    node = _tagger.parseToNode(sentence)
    text_data_parsed_lemmatized = ""
    while node:
        node_list = node.feature.split(",")
        if node_list[0] == "BOS/EOS":
            node = node.next
            continue
        else:
            text_data_parsed_lemmatized += node_list[-7]
            text_data_parsed_lemmatized += " "
            node = node.next
    return text_data_parsed_lemmatized


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
