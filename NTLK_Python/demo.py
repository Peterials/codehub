from nltk.tag.stanford import CoreNLPNERTagger,CoreNLPPOSTagger
from nltk.tokenize.stanford import CoreNLPTokenizer

stpos, stner =CoreNLPPOSTagger('http://localhost:9001'),CoreNLPNERTagger('http://localhost:9001')
sttok = CoreNLPTokenizer('http://localhost:9001')

sttok.tokenize(u'你好')

stpos.tag(u'basf')


stpos.tag(sttok.tokenize(u'text'))


stner.tag(u'你好')


stner.tag(sttok.tokenize(u'你好'))