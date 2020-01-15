import hashlib
import os
import re

from sklearn.externals import joblib


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
    # 推文集合，放置推文的 md5 编码值，去重用
    tweets_set = set()
    # 遍历 folder 文件夹中的每一个文件
    file_list = []
    for root, dirs, files in os.walk(folder):
        file_list = files
    # 对于 file_list 中的每一个文件，按行读取，存入 res 列表
    res = []
    for file in file_list:
        with open(os.path.join(folder, file), 'r', encoding='utf-8') as f:
            for line in f:
                if '#' in line and len(line) >= 50:
                    line = clean(line)
                    md5 = hashlib.md5()
                    md5.update(line.encode('utf-8'))
                    md5_str = md5.hexdigest()
                    if md5_str not in tweets_set:
                        # print(line)
                        tweets_set.add(md5_str)
                        res.append(line)
    print('处理推文 %d 条' % len(res))
    return res


if __name__ == '__main__':
    # 读所有推文
    tweets = read('./tweets_by_month')

    # 加载模型
    language_model = joblib.load('./models/language_model')
    classifier_model = joblib.load('./models/classifier_model')

    # 对推文分类，结果存储在 result 列表中
    result = classifier_model.predict(language_model.transform(tweets))

    # 创建存储目录
    if not os.path.exists('./classifier_result'):
        os.makedirs('./classifier_result')

    # 写结果
    with open('./classifier_result/leave', 'w', encoding='utf-8') as leave, \
            open('./classifier_result/remain', 'w', encoding='utf-8') as remain:
        for i, e in enumerate(result):
            if e == 'leave':
                leave.write(tweets[i] + '\n')
            elif e == 'remain':
                remain.write(tweets[i] + '\n')
