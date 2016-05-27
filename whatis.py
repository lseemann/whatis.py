#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re, sys, os
from twython import Twython

# Allows for paths to be relative to where the script is, not to the cron
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)

# Two things need to be configured:

# 1. Create keys for each keyword/account that will use this script
twitterAuth = {
  'term' : {
    'APP_KEY' : 'XXXXXXXXXXXXXXXXXXXXX',
    'APP_SECRET' : 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'OAUTH_TOKEN' : 'XXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'OAUTH_TOKEN_SECRET' : 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
  },
  'another term' : {
    'APP_KEY' : 'XXXXXXXXXXXXXXXXXXXXX',
    'APP_SECRET' : 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'OAUTH_TOKEN' : 'XXXXXXXXXX-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX',
    'OAUTH_TOKEN_SECRET' : 'XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX'
  }
}

# 2. Create an array of strings to exclude (case insensitive).
#    Recommended for profanity or to avoid excessive RT's of the same text
bannedTerms = ['kkk','xxx']

# That is all.

def retweet(term):
  term = term.lower()
  slug = term.replace(' ','')

  twitter = Twython(twitterAuth[slug]['APP_KEY'], twitterAuth[slug]['APP_SECRET'], twitterAuth[slug]['OAUTH_TOKEN'], twitterAuth[slug]['OAUTH_TOKEN_SECRET'], )

  # Each term has a couple of logs:
  #   1. Of the most recent tweet (by id)
  if not os.path.exists('./logs/whats' + slug + '-latest.txt'):
    open('./logs/whats' + slug + '-latest.txt', 'w').close()
  last_check_log = open('./logs/whats' + slug + '-latest.txt','r')

  #   2. and the handles of the 100 most recent users
  if not os.path.exists('./logs/whats' + slug + '-log.txt'):
    open('./logs/whats' + slug + '-log.txt', 'w').close()
  recent_log     = open('./logs/whats' + slug + '-log.txt','r')


  counter      = 0
  max          = 1 # Maximum number of tweets to retweet at a time
  recent_limit = 100 # Don't retweet someone if they've been retweeted in the past n retweets
  last_check   = last_check_log.read()
  last_check_log.close()

  # Get the matching tweets from twitter, and if successful update one of the logs
  query  = '"' + term + ' is"'
  tweets = twitter.search(q=query,count=1000,since_id=last_check)['statuses']
  last_check_log = open('./logs/whats' + slug + '-latest.txt','w')
  if len(tweets) > 0:
    latest = tweets[0]['id']
    last_check_log.write(str(latest))
  last_check_log.close()

  # Read in the log of most recent users
  past = []
  for line in recent_log:
    past.append(line.replace('\n',''))
  while len(past) > recent_limit:
    past.pop(0)
  recent_log.close()

  # Go through the tweets until we find one that matches our requirements
  emojiFilter = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
  for tweet in tweets:
    tweet['text'] = emojiFilter.sub(u'', tweet['text'])
    if isMatch(tweet['text'], term) and (isNotBanned(tweet['text']) and isNotRepeated(tweet['user']['screen_name'], past) and counter < max):
      try:
        twitter.retweet(id=tweet['id'])
        counter += 1
        past.append('@' + tweet['user']['screen_name'])
        print tweet['text']
        print tweet['user']['screen_name']
      except:
        pass
  if counter == 0:
    print 'No eligible tweets found.'
    sys.exit()

  # Update the log of users with whichever user we found
  recent_log = open('./logs/whats' + slug + '-log.txt','w')
  for user in past:
    recent_log.write(user + '\n')
  recent_log.close()


def isMatch(tweet, term):
  if (tweet.lower().find(term + ' is ') == 0 or tweet.lower().find('"' + term + ' is ') == 0):
    return True
  else:
    return False

def isNotBanned(tweet):
  for term in bannedTerms:
    if tweet.lower().find(term.lower()) > 1:
      return False
  return True

def isNotRepeated(user, past):
  for pastUser in past:
    if user == pastUser.replace('@',''):
      return False
  else:
    return True

if __name__ == "__main__":
  try:
    term = sys.argv[1]
    if term:
      retweet(term)
  except:
    pass