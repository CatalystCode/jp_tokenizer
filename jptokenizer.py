# coding: utf-8

from MeCab import Tagger
from sanic import Sanic 
from sanic.response import json
 
_tagger = Tagger('-d /usr/lib/mecab/dic/mecab-ipadic-neologd/')
#_tagger = Tagger()

app = Sanic(__name__) 
 
@app.route('/tokenize/', methods=['POST'])
async def tokenize(request):
    sentence = request.body.decode('utf-8')
    print(sentence)
    results = list(_tokenizer(sentence))
    return json({'tokens': results})

def _tokenizer(sentence):
    parsed = _tagger.parseToNode(sentence)
    while parsed:
        token = parsed.surface
        yield token
        parsed = parsed.next

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)

