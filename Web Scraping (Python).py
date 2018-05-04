# Author: Anshul Verma

# Web Scraping

from bs4 import BeautifulSoup
import urllib2 as ur
import re
from operator import itemgetter

# to get the html of the webpage and load into beautifulsoup
base_url = "https://www.rottentomatoes.com/m/inception/reviews/"
webpage = ur.urlopen(base_url)
soup = BeautifulSoup(webpage,'lxml')

# to identify total number of pages
total = soup.find('span',{'class':re.compile('pageInfo')}).text.strip().split(' ')[3]

page = 1
score = []

# to create a list of reviews and ratings by looping through all the pages
while page <= int(total):
    
    base_url = "https://www.rottentomatoes.com/m/inception/reviews/?page="+str(page)
    webpage = ur.urlopen(base_url)
    soup = BeautifulSoup(webpage,'lxml')
    reviews = soup.findAll('div',{'class':re.compile('review_desc')})
    for i in reviews:
        review = i.find('div',{'class':re.compile('the_review')}).text.strip()
        try:
            rating = i.find('div',{'class':re.compile('small subtle')}).text.strip()
            if "Original Score" in rating:
                rating = re.split('[|:/]',rating)
                rating = float(rating[2].strip())/float(rating[3].strip())
            else:
                continue
        except:
            continue
        score.append([review, rating])
    page += 1

# to print top 20 reviews list
top = sorted(score, key=itemgetter(1), reverse = True)
print "\nTop 20 reviews:\n", top[:20]

# to print bottom 20 reviews list
bottom = sorted(score, key=itemgetter(1))
print "\nBottom 20 reviews:\n", bottom[:20]

# Bonus: to create word clouds for top 20 and bottom 20 reviews
from wordcloud import WordCloud
import matplotlib.pyplot as plt

file= open("stopwords_en.txt", "r")
stop = file.read()
stop.replace('\n', ' ')

wordlist1 = []
for i in top[:20]:
    words = i[0].split(' ')
    for word in words:
        if word not in stop:
            wordlist1.append(word)    

wordlist2 = []
for i in bottom[:20]:
    words = i[0].split(' ')
    for word in words:
        if word not in stop:
            wordlist2.append(word)    

string1 = ' '.join(wordlist1)                        
string2 = ' '.join(wordlist2)
wc1 = WordCloud(background_color="white", max_words=20, stopwords=stop)
wc2 = WordCloud(background_color="white", max_words=20, stopwords=stop)
wc1.generate(string1)
wc2.generate(string2)

plt.subplot(1, 2, 1)
plt.imshow(wc1)
plt.axis('off')
plt.title('Top 20 Reviews')
plt.subplot(1, 2, 2)
plt.imshow(wc2)
plt.axis('off')
plt.title('Bottom 20 Reviews')
plt.show()
