import pandas as pd
import praw
import nltk
import random
from pprint import pprint

# Enter your own client_id, client_secret, username and password, or follow this quick start guide: https://github.com/reddit-archive/reddit/wiki/OAuth2-Quick-Start-Example#first-steps  
reddit = praw.Reddit(user_agent='Comment Extraction (by /u/USERNAME)',client_id='enter_here',client_secret="enter_here",username='enter_here', password='enter_here')

from textblob import TextBlob
import matplotlib.pyplot as plt
from wordcloud import WordCloud


def subreddit_hot(subreddit):
    
    print('Commonly used words displayed as a Word Cloud for the 50 most recent hot posts in: ', subreddit)
    
 #     open new file and write in data
    with open('%s_hot.txt' % subreddit, 'a') as file:
        posts = subreddit.hot(limit=50)

    with open('%s_hot.txt' % subreddit, 'w') as file:
        for post in posts:
            file.write(post.title + '\n')
    
    with open('%s_hot.txt' % subreddit, 'r') as file:
        wordcloud_data = file.read()

# generate wordcloud        
    from wordcloud import WordCloud, STOPWORDS
    stopwords = set(STOPWORDS)
    stopwords.update(['It','This','be'])

    wordcloud = WordCloud(stopwords=stopwords,height=1000, width=3000, max_words=40, \
                      background_color='white').generate(wordcloud_data)

    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.margins(x=0, y=0)
    plt.show()
    
 # begin sentiment analysis
    with open('%s_hot.txt' % subreddit, 'r') as file:
        for w in file:
            if w not in stopwords:
                file_posts = file.readlines()  
    
        
    labels = ['Negative', 'Neutral', 'Positive']
    values = [0,0,0]

    
    for posts in file_posts:
        sentiment = TextBlob(posts)
        polarity = round((sentiment.polarity + 1) * 3) % 3
        values[polarity] = values[polarity] + 1
    
    print('\n\n','Sentiment breakdown for 50 most recent hot posts in: ', subreddit, '\n\n')

    colors = ['red','gray','green']
    plt.pie(values, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')
    plt.show()
    
# print hot post titles
    
    print('\n\n','This week\'s top posts in ' , subreddit)
    
    for submission in subreddit.top("week", limit=10):
        print(submission.title)
       

# Add subreddits you want to analyze below.
subreddit_hot(reddit.subreddit('apple'))
subreddit_hot(reddit.subreddit('microsoft'))

