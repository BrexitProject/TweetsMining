import re, collections
import os

def getCoOccurrence(filename):
	CoOccurenceFile = open("./co_coccurrence/testResult", 'a')
	path = './tweets_by_month/' + filename
	with open(path) as f:
		wordsBox = []
		for line in f:
			# get lower case
			line = line.lower()	
			# banish punctuation
			line = re.sub(r'\|\~|\`|\!|\$|\%|\^|\&|\*|\(|\)|\-|\_|\+|\=|\||\\|\[|\]|\{|\}|\;|\:|\"|\'|\,|\<|\.|\>|\/|\?', " ", line)
			wordsBoxByLine = line.strip().split()
			cnt = 0
			for word in wordsBoxByLine:
				# match hashtag
				flag = 0
				if re.match(r'(#)([a-zA-Z0-9])', word) and word != '#brexit':
					CoOccurenceFile.write(word)
					CoOccurenceFile.write('; ')
					flag = 1
			if (flag):
				#CoOccurenceFile.write('&')
				CoOccurenceFile.write('\n')



if __name__=='__main__':

	path = './tweets_by_month/'
	for root, dirs, files in os.walk(path):
		for filename in files:
			getCoOccurrence(filename)