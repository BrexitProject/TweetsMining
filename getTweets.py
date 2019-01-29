from bs4 import BeautifulSoup 
import os


#extract irrelevent text embeded
def clean_all(soup):
	for pc in soup.find_all('p', attrs = {"class": ['TweetTextSize', 'js-tweet-text', 'tweet-text']}):
		for ac in pc.find_all('span'):
			ac.extract() 
	for pc in soup.find_all('a', attrs = {"class": ["twitter-timeline-link u-hidden"]}):
		pc.extract()

#get tweet and save it to result file 
def getTweets(filename, soup):
	filename = os.path.splitext(filename)[0]
	file = open(filename + "_result", "w")
	for pc in soup.find_all('p', attrs = {"class": ['TweetTextSize', 'js-tweet-text', 'tweet-text']}):
		result = pc.text
		result = result.replace("\n", "")
		result = result
		result += ' \n'
		file.write(result)

	file.close()

def tweet(filename):
	soup = BeautifulSoup(open(filename), "lxml")
	soup.encode('utf-8')
	clean_all(soup)
	getTweets(filename, soup)


if __name__=='__main__':

	path = './'
	for root, dirs, files in os.walk(path):
		for filename in files:
			tweet(filename)
