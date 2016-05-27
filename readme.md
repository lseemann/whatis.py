# whatis.py
A Twitter bot to retweet tweets that begin with "_____ is…", as used by [@whatschicago](http://www.twitter.com/whatschicago). Read about this bot in [this _Atlantic_ story](http://www.theatlantic.com/technology/archive/2014/02/can-a-twitter-bot-capture-chicagos-essence/283789/).
## Installation
Save anywhere with 24-hour Internet connection. An EC2 instance works great.
## Usage
First you will need to create an app within the Twitter account you intend to use to retweet. Do that [here](https://apps.twitter.com/), and then retrieve the *Consumer Key* and *Consumer Secret*, plus an *Access Token* and an *Access Token Secret*. Add these to the whatis.py file.

To run the script: `python whatis.py search_term` or `python whatis.py "search term"`.

For each search term, logs will be generated to avoid repeat retweets of the same Twitter user.

There is an option to prevent certain words or expressions from being retweeted, such as profanity. Add such words to the bannedTerms array within whatis.py.

Finally you will want to set up a cronjob to run this script at given intervals. I recommend no more than twice an hour. Your cron command will need the entire path to the whatis.py file: `python /path/to/whatis.py search_term`.
## Credits
Luke Seemann, 2016