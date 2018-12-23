import re, collections

#get frequency of certain hashtag
def getTag(filename):
	with open(filename) as f:
		wordsBox = []
		for line in f:
			# get lower case
			line = line.lower()	
			# banish punctuation
			line = re.sub(r'\|\~|\`|\!|\$|\%|\^|\&|\*|\(|\)|\-|\_|\+|\=|\||\\|\[|\]|\{|\}|\;|\:|\"|\'|\,|\<|\.|\>|\/|\?]', " ", line)
			wordsBoxByLine = line.strip().split()
			for word in wordsBoxByLine:
				# match hashtag
				if re.match(r'(#)([a-zA-Z0-9])', word):
					wordsBox.append(word)

	# get the frequency and store in list c
	c = collections.Counter(wordsBox)

	# 如果只需要高频词可以用most_common
	# collections.Counter(wordsBox).most_common(300)

	# print frequency of certain hashtag
	for word in ['#tory', '#tories']: 
		print(str(c[word]))

 
if __name__=='__main__':

	#start month
	min = 1
	#end month
	max = 6

	for num in range(min, max):
		filename = str(num)
		getTag(filename)

