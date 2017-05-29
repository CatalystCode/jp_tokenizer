import MeCab
import csv


text = input()
m = MeCab.Tagger ("-d /usr/local/lib/mecab/dic/unidic")
i = 0
text_data_parsed_lemmatized = ""
node = m.parseToNode(str(text))
while node:
    # print(node.feature)
    node_list = node.feature.split(",")
    if node_list[0] == "BOS/EOS":
        text_data_parsed_lemmatized += "BOS/EOS "
        node = node.next
        continue
    else:
        # print(node_list[-7])
        text_data_parsed_lemmatized += node_list[-7]
        text_data_parsed_lemmatized += " "
        node = node.next
print(text_data_parsed_lemmatized)

