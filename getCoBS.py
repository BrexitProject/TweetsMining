import re, collections
import os

def getCoOccurrence(filename):
	CoOccurenceFile = open("./co_occurrence/tweetsBrexitShambles", 'a')
	path = './tweets_by_month/' + filename
	with open(path) as f:
		for line in f:
			# get lower case
			newline = line.lower()	
			if re.search('#brexitshambles', newline):
				CoOccurenceFile.write(line)

def getFre():
	with open("./co_occurrence/tweetsBrexitShambles", 'r') as f:
		content = f.read()
		content = content.lower()
		content = re.sub(r'\|\~|\`|\!|\$|\%|\^|\&|\*|\(|\)|\-|\_|\+|\=|\||\\|\[|\]|\{|\}|\;|\:|\"|\'|\,|\<|\.|\>|\/|\?', " ", content)
		wordsBox = content.strip().split()

	freFile = open("./co_occurrence/coBrexitShambles", "w")

	c = collections.Counter(wordsBox).most_common(200)
	#print(c)
	for tup in c:
		freFile.write(tup[0] + " " + str(tup[1]) + "\n")

	freFile.close()
	f.close()


if __name__=='__main__':

	path = './tweets_by_month/'
	for root, dirs, files in os.walk(path):
		for filename in files:
			getCoOccurrence(filename)

	getFre()