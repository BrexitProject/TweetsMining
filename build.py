import hashlib
import os
import re

from sklearn import svm
from sklearn.externals import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report
from sklearn.model_selection import GridSearchCV, train_test_split


def clean(text):
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'\S+\.co\S+', '', text)
    text = re.sub(r'\S+\.uk\S+', '', text)
    text = re.sub(r'[#]', ' #', text)
    text = re.sub(r'[@]', ' @', text)
    text = re.sub(r'[^\w\s@#\'\-‘’]', ' ', text)
    text = re.sub(r'[\'‘’]', '', text)
    text = re.sub(r'\s+-\s+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = text.strip().lower()
    # print(text)
    return text


def read(folder):
    # 遍历 folder 文件夹
    file_list = []
    for root, dirs, files in os.walk(folder):
        file_list = files
    # 对于 file_list 中的每一个文件按行读取，记录内容和标签
    corpus = []
    target = []
    for file in file_list:
        with open(os.path.join(folder, file), 'r', encoding='utf-8') as f:
            # 推文集合，放置推文的 md5 编码值，去重用
            tweets = set()
            for line in f:
                line = clean(line)
                md5 = hashlib.md5()
                md5.update(line.encode('utf-8'))
                md5_str = md5.hexdigest()
                if md5_str not in tweets:
                    tweets.add(md5_str)
                    corpus.append(line)
                    target.append(file)
    # print(corpus)
    # print(target)
    return corpus, target


if __name__ == '__main__':
    # 读取语料和对应的标签；corpus 和 target 是两个长度相等的列表
    corpus, target = read('./labeled_tweets')

    # 分割训练集和验证集，可指定 test_size
    (x_train, x_test, y_train, y_test) = train_test_split(corpus, target, test_size=0.02)

    # 创建存放模型的目录
    if not os.path.exists('./models'):
        os.makedirs('./models')

    # 建立文本向量化模型
    vectorizer = TfidfVectorizer(analyzer='word', token_pattern=r'[\w|\#]\w+\b', min_df=3,
                                 stop_words='english').fit(corpus)
    joblib.dump(vectorizer, './models/language_model')

    # 建立分类模型
    svc = svm.LinearSVC(C=100).fit(vectorizer.transform(x_train), y_train)
    joblib.dump(svc, './models/classifier_model')

    # 验证精度
    corpus_test = vectorizer.transform(x_test)
    report = classification_report(svc.predict(corpus_test), y_test)
    print(report)
    print(svc.score(corpus_test, y_test))
