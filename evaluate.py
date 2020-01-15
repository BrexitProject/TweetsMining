import math
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB


def read(folder):
    file_list = []
    for root, dirs, files in os.walk(folder):
        file_list = files
    # 读文件，不解释
    corpus = []
    target = []
    for file in file_list:
        with open(os.path.join(folder, file), 'r', encoding='utf-8') as f:
            for line in f:
                corpus.append(line)
                target.append(file)
    return corpus, target


def load_hashtag(filename):
    # 只有在这个文件里面的 hashtag 才是我们需要的，只给这些打分就行了。
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().strip().split()


if __name__ == '__main__':
    # 读分类完的结果
    corpus, target = read('./classifier_result')
    # 读要打分的几个 hashtag
    tags = load_hashtag('./tag')

    # 构造文本向量化模型
    vectorizer = TfidfVectorizer(analyzer='word', token_pattern=r'[\w|\#]\w+\b', min_df=3, stop_words='english')
    corpus = vectorizer.fit_transform(corpus)

    # 构造朴素贝叶斯（多项式，不学习先验概率）
    clf = MultinomialNB(fit_prior=False)
    clf.fit(corpus, target)
    features = vectorizer.get_feature_names()

    print('##############################')
    score = clf.predict_proba(vectorizer.transform(tags))
    prob_dict = {}
    for i, tag in enumerate(tags):
        prob_dict[tag] = score[i][0]

    for e in sorted(prob_dict.items(), key=lambda x: x[1], reverse=True):
        print(e[0], e[1])

    print('##############################')
    # 这两种方法做出来的数值是相同的

    prob_dict = {}
    for tag in tags:
        # tmp = clf.coef_[0][features.index(e)]
        # prob_dict[e] = math.e ** tmp
        a = math.e ** clf.feature_log_prob_[0][features.index(tag)]  # 这个特征能够为它是第一类提供的证据
        b = math.e ** clf.feature_log_prob_[1][features.index(tag)]  # 第二类
        tmp = a / b
        # 下面解一个方程 x / y = tmp 且 x + y = 1，结果如下
        prob_dict[tag] = 1 - 1 / (tmp + 1)

    for e in sorted(prob_dict.items(), key=lambda x: x[1], reverse=True):
        print(e[0], e[1])
    print('##############################')
