import re
import os


#classified tweets according to hashtag
def isLeave(filename):
	leavePath = './labeled_tweets/leave'
	leaveTweets = open(leavePath, 'a')
	global leaveCnt

	remainPath = './labeled_tweets/remain'
	remainTweets = open(remainPath, 'a')
	global remainCnt

	sourcePath = './tweets_by_month/' + filename

	with open(sourcePath) as f:
		for line in f:
			line = line.lower()
			line = re.sub(r'\|\~|\`|\!|\$|\%|\^|\&|\*|\(|\)|\-|\_|\+|\=|\||\\|\[|\]|\{|\}|\;|\:|\"|\'|\,|\<|\.|\>|\/|\?', " ", line)
			if re.search('#voteleave|#leave|#takecontrol', line):
				leaveTweets.write(line)
				leaveCnt = leaveCnt + 1
			if re.search('#voteremain|#remain|#strongerin|#labourinforbritain|#intogether', line):
				remainTweets.write(line)
				remainCnt = remainCnt + 1

if __name__=='__main__':

	leaveCnt = 0
	remainCnt = 0
	path = './tweets_by_month/'
	for root, dirs, files in os.walk(path):
		for filename in files:
			isLeave(filename)
	print(leaveCnt)
	print(remainCnt)


