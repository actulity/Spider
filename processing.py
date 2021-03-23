import jieba
import jieba.analyse
from optparse import OptionParser
import sys
sys.path.append('../')

# fR = open('demand.txt', 'r', encoding='UTF-8')

# sent = fR.read()
# sent_list = jieba.cut(sent, )

# fW = open('cutWord.txt', 'w', encoding='UTF-8')
# fW.write(' '.join(sent_list))

# fR.close()
# fW.close()

# USAGE = "usage:    python extract_tags.py [file name] -k [top k]"

# parser = OptionParser(USAGE)
# parser.add_option("-k", dest="topK")
# opt, args = parser.parse_args()

# if len(args) < 1:
#     print(USAGE)
#     sys.exit(1)

# file_name = args[0]

# if opt.topK is None:
#     topK = 10
# else:
#     topK = int(opt.topK)

content = open('cutWord.txt', 'rb').read()

jieba.analyse.set_stop_words('cutWord.txt') 
# jieba.analyse.TFIDF(idf_path='cutWord.txt') 
tags = jieba.analyse.extract_tags(content, topK=20)

print(",".join(tags))