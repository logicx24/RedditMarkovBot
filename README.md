A Markov Chain for Reddit Comments

To run your own instance of this, just do "pip install -r requirements.txt" and then run "python markovReddit.py". This runs on Python 2.7. 

Also, ignore all the random notes I wrote to myself while I code. Though, if you'd like to implement any of my TODO's, I'd be
delighted. 

To use on reddit, just type in MarkovME for a generation of past comments, and MarkovME: freqCount for an analysis of your most used words.

Better formatted TODOs:
1. I want this bot to have threads. Specifically, I want it to have a separate instance for each group of subreddits. Now, praw supports this with praw-multiprocess. I'm working on making the bot run in several different processes. It's easy because it doesn't share state.
2. I want a database, eventually, so I can start collecting info on users. 
3. I need to handle exceptions less jenkily.
4. I want to eventually add a feature that'll tell you the user that's most similar to you (Jaccard similarity between subscribed subreddits). This will take an incredible amount of data gathering, so it's a long term goal.
5. The whole thing right now feels kind of jenky and unreliable. I don't feel confident that if I left it to run in the morning, it wouldn't crash in an hour. That's a multitutde of issues that I'll work on. 
