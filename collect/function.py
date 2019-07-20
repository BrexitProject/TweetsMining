import csv
import os
import re

from bs4 import BeautifulSoup

index = 0
headers = []
tweet_data = []
retweet_data = []


# extract irrelevent text embeded
def clean_all(soup):
    for pc in soup.find_all('p', attrs={'class': ['TweetTextSize', 'js-tweet-text', 'tweet-text']}):
        for ac in pc.find_all('span'):
            ac.extract()
    for pc in soup.find_all('a', attrs={'class': ['twitter-timeline-link u-hidden']}):
        pc.extract()

def func(root, files):
	global headers
	global index

    # 初始化列名日期
	if not headers:
		headers.append('hashtag')
		headers += files
	for file in files:
		with open(os.path.join(root, file), 'r', errors='ignore') as f:
			soup = BeautifulSoup(f, 'lxml')
			soup.encode('utf-8')
			clean_all(soup)
            # 推文列表, 转发量列表
			tweets = 0
			recnt = 0
			for pc in soup.find_all('p', attrs={'class': ['TweetTextSize', 'js-tweet-text', 'tweet-text']}):
				tweets += 1
			for pc in soup.find_all('span', attrs={'class': ['ProfileTweet-action--retweet u-hiddenVisually']}):
				recnt += int(pc.text.replace('\n', '').replace(',', '').split()[0])
		tweet_data[index].append(tweets)
		retweet_data[index].append(recnt)
	index += 1

for root, dirs, files in os.walk('crawl'):
    if not dirs and files:
    	print(root, files)
    	func(root, files)
    elif dirs:
        # 初始化行名hashtag
    	for e in dirs:
	        tweet_data.append([e])
	        retweet_data.append([e])

with open('tweet_data.csv', 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)
    csv_writer.writerows(tweet_data)

with open('retweet_data.csv', 'w', encoding='utf-8', newline='') as f:
    csv_writer = csv.writer(f)
    csv_writer.writerow(headers)
    csv_writer.writerows(retweet_data)
