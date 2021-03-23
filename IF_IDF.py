# import sklearn
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

wordslist = []
words = ""
with open("去掉无用词汇之后数据.txt", 'r', encoding='utf-8') as f:
    while True:
        ll = f.readline()
        if  not ll: break
        words += ll.strip()
        # words = ll.strip()
        # wordslist.append(words)
wordslist.append(words)
 
vectorizer = CountVectorizer()
word_frequence = vectorizer.fit_transform(wordslist)
words = vectorizer.get_feature_names()

transformer = TfidfTransformer()
tfidf = transformer.fit_transform(word_frequence)
weight = tfidf.toarray()

n = 100 # 前五位
for w in weight:
    # print u'{}:'.format(title)
    # 排序
    loc = np.argsort(-w)
    for i in range(n):
        print (u'-{}: {} {}'.format(str(i + 1), words[loc[i]], w[loc[i]]))
    print ('\n')