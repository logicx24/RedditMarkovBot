import random
import re

class Markov(object):

	def __init__(self, string):
		self.cache = {}
		self.words = [word for word in re.sub(r'^https?:\/\/.*[\r\n]*', '', string.replace("\n", ' '), flags=re.MULTILINE).split() if not word.startswith("http")]
		#self.words = self.initialize()
		self.cache = self.database()
		#print("Congrats, you have initialized. Methods you can try are count_phrase(phrase), count_freq(word), or text_gen()")
		#self.title = self.accumulate_text.title

	#Rudimentary Spell Check: Find the string distance between the proposed word and every word in the corpus, and then just suggest a random word
	# that has the smallest distance.       
		
	def triples(self):
		if len(self.words) < 3:
			return
		else:
			r = []
			for w in range(len(self.words)-3):
				for i in range(3):
					self.words[w+i] = self.words[w+i].replace(',','')
					if self.words[w+i] != 'I':
						self.words[w+i] = self.words[w+i].lower()
				yield (self.words[w],self.words[w+1],self.words[w+2])


	def database(self):
		for w1, w2, w3 in self.triples():
			key = (w1, w2)
			if key in self.cache:
				if w3 in self.cache[key]:
					self.cache[key][w3] += 1
				else:
					self.cache[key][w3] = 1.0
			else:
				self.cache[key] = {w3: 1.0}
		return self.cache

	def text_gen(self):
		gen_words = []
		if len(self.words) <= 1:
			return "You didn't have enough publicly available comments for text_gen to work."
		first1 = random.randint(0,len(self.words)-2)
		first, next = self.words[first1], self.words[first1+1]
		for w in range(150):
			if (first, next) in self.cache:
				gen_words.append(self.weighted_choice(self.cache[(first, next)].items()))
				first, next = next, self.weighted_choice(self.cache[(first,next)].items())
				if '.' in gen_words[-1][-1]:
					if len(gen_words) < 40:
						gen_words[-1] = gen_words[-1].replace('.','')
					else:
						break
		#print(self.cache)
		gen_words[0] = gen_words[0].title()
		gen_words[-1] += "." if gen_words[-1][-1] != "." else ""
		gen_words = ' '.join(gen_words)
		#gen_words = self.remove_char(' '.join(gen_words))

		return gen_words


	def weighted_choice(self, choices):
		total = sum(w for c, w in choices)
		r = random.uniform(0, total)
		upto = 0
		for c, w in choices:
			if upto + w >= r:
				return c
			upto += w
		assert False, "Shouldn't get here"

	def count_freq(self, word):
		counter = 0
		word.lower()
		for string in self.words:
			if string.lower().replace('.',',') == word:
				counter += 1
		return counter

	def count_words(self):
		counter = 0
		for word in self.words:
			counter +=1
		return counter

	def count_phrase(self, phrase):
		counter = 0
		i = 0
		while i < len(self.words) - 1:
			i, shouldCount = self.phrase_check(phrase, i)
			if shouldCount:
				counter+=1
		return counter

	def phrase_check(self, phrase, index):
		phrase = ''.join(letter for letter in phrase if letter.isalnum() or letter == ' ')
		phrasing = phrase.split()
		boolean = True
		for i in range(len(phrasing)):
			if phrasing[i] != 'I':
				phrasing[i] = phrasing[i].lower()
		i = 0
		while i < len(phrasing):
			wording = ''.join(letter for letter in self.words[index] if letter.isalnum())
			#print(wording)
			if wording == phrasing[i]:
				i+=1
				index+=1
			else:
				index+=1
				boolean = False
				break
		return (index, boolean)

	def count_uniques(self):
		unique_words = []
		counter = 0
		for word in self.words:
			if word not in unique_words:
				counter += 1
			unique_words.append(word)
		return counter

	# def initialize(self):
	# 	words = []
	# 	for file in self.files:
	# 		text = open(file)
	# 		words += str(text.read()).split()
	# 		text.close()
	# 	return words
			


	# def initialize(self):
	# 	bool1 = True
	# 	words = []
	# 	past = []
	# 	while bool1:
	# 		print('Write the filename here. Must be in this directory. Type n to stop entering files')
	# 		file1 = raw_input()
	# 		if file1 in ['n', '']:
	# 			bool1 = False
	# 		elif file1 in past:
	# 			print("You cannot use the same file twice.")
	# 		else:
	# 			try:
	# 				past.append(file1)
	# 				text = open(file1)
	# 				text = text.read()
	# 				str1 = str(text)
	# 				words += str1.split()
	# 			except FileNotFoundError:
	# 				print("That file does not exist. Try another file, or type n to exit.")
	# 	return words


	#def remove_char(self,text): return re.findall('[a-z]+', text.lower()) 


			


			

