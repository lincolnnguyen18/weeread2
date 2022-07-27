# import spacy

# nlp = spacy.load('ja_ginza')
# doc = nlp('その有様は、まるで幻想でも見ている様な気分になる。こんな事が本当に起こり得るのかと、視界に映っているものの理解を脳が拒否してしまいそうだ。しかし、頬が触れる熱は紛れもなく真実であり、そうして今俺の命へと指先を掛けている。')
# for sent in doc.sents:
#     for token in sent:
#         print(token.i, token.orth_, token.lemma_, token.pos_, token.tag_, token.dep_, token.head.i)
#     print('EOS')

import MeCab
tagger = MeCab.Tagger("-Ochasen")
print(tagger.parse(u'これはテストです。'))