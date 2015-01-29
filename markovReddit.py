#A reddit bot that talks like you do. (Trains a markov chain on your comments).

"""
Basic functionality done. 

TODO:
Make a database to store viewed comments.
Make the main process multi-threaded.
Set up handling for crashes (store data in database)
Make better system to handle repeats on same thread.
"""

from markov_bot import Markov
import praw
import os
import time
from praw.handlers import MultiprocessHandler
import multiprocessing
import cPickle as pickle
import sys

handler = MultiprocessHandler()

#observed_submissions = []


def initialize():
	reddit = praw.Reddit(user_agent="Make markov chains from user comments", handler=handler)
	#reddit.login(os.getenv("username"), os.getenv("password"))
	reddit.login(username="RedditMarkovBot", password="starscream")
	return reddit

def get_monitored_subs():
	return ['test']

def monitor_and_train(reddit, monitored):
	"""Should monitor a given list of subreddits, look for a post with MarkovME, and then get that user's data,
		train the markov bot, use the text_gen() method, and pass it into post_comment to make the comment. It should
		then store the Markov object in the hashtable. Eventually, there'll be a database to pull user info from so you 
		don't have to do this expensive operation each time."""

	observed_comments = []
	user_to_markov = {}
	user_to_comments = {}
	comment_buffer = []
	search_string = "MarkovME"

	if (os.path.isfile("./pickled_files/read_comments.pkl")):
		observed_comments = pickle.load(open("./pickled_files/read_comments.pkl", 'rb'))
	if (os.path.isfile("./pickled_files/comment_buffer.pkl")):
		comment_buffer = pickle.load(open("./pickled_files/comment_buffer.pkl", 'rb'))
	if (os.path.isfile("./pickled_files/markov_instances.pkl")):
		user_to_markov = pickle.load(open("./pickled_files/markov_instances.pkl", 'rb'))
	
	#monitored = get_monitored_subs()
	start = 0

	while True:
		try:
			for sub in monitored:
				subData = reddit.get_subreddit(sub)
				for submission in subData.get_hot(limit=50):
					#if str(submission.id) not in observed_submissions:
					flat_comments = praw.helpers.flatten_tree(submission.comments)
					for comment in flat_comments:
						if str(comment.id) not in observed_comments and search_string in comment.body:
							if str(comment.author.id) in user_to_markov:
								userMarkov = user_to_markov[str(comment.author.id)]
							else:
								user_comments = comment.author.get_comments()
								user_text = ""
								for user_comment in user_comments:
									user_text += " " + user_comment.body.replace("MarkovME","")
								userMarkov = Markov(user_text)
								commentText = userMarkov.text_gen()
								user_to_markov[str(comment.author.id)] = userMarkov
							try:
								comment.reply(commentText)
							except praw.errors.RateLimitExceeded:
								start = time.time()
								comment_buffer.append((commentText, comment))
						observed_comments.append(str(comment.id))
					#observed_submissions.append(str(submission.id))
			if comment_buffer: 
				for comment_tup in comment_buffer:
					if (time.time() - start) >= 600:
						try:
							comment_tup[1].reply(comment_tup[0])
						except praw.errors.RateLimitExceeded:
							break
						comment_buffer.remove(comment_tup)
		except:
			with open("./pickled_files/read_comments.pkl", 'wb') as output:
				pickle.dump(observed_comments, output, -1)
			with open("./pickled_files/comments_buffer.pkl", 'wb') as output:
				pickle.dump(comment_buffer, output, -1)
			with open("./pickled_files/markov_instances.pkl", 'wb') as output:
				pickle.dump(user_to_markov, output, -1)
			sys.exit()


if __name__ == "__main__":
	# reddits = []
	# for sub in get_monitored_subs():
	# 	reddits.append((initialize(),sub))
	# pool = multiprocessing.Pool(processes=multiprocessing.cpu_count())
	# for sub in reddits:
	# 	print(sub)
	# 	pool.apply_async(monitor_and_train(sub[0],sub[1]))

	monitor_and_train(initialize(), get_monitored_subs())










