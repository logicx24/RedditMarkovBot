import random


class Markov(object):

	def __init__(self, string):
		self.cache = {}
		self.words = string.replace("\n", ' ').split()
		#self.words = self.initialize()
		self.cache = self.database()
		#print("Congrats, you have initialized. Methods you can try are count_phrase(phrase), count_freq(word), or text_gen()")
		#self.title = self.accumulate_text.title

	#Rudimentary Spell Check: Find the string distance between the proposed word and every word in the corpus, and then just suggest a random word
	# that has the smallest distance. 
	# Maybe give people a way to say the thing was wrong, so it can learn and improve over time?

	#Implement depth first search to scour all of your files for text files, and add the ones it finds to the corpus.
	#Add a web crawler to constantly add files from the internet. Create a massive corpus, and use it for something cool.       
		
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
				self.cache[key].append(w3)
			else:
				self.cache[key] = [w3]
		return self.cache

	def text_gen(self):
		gen_words = []
		first1 = random.randint(0,len(self.words)-1)
		first, next = self.words[first1], self.words[first1+1]
		for w in range(750):
			if (first, next) in self.cache:
				gen_words.append(random.choice(self.cache[(first, next)]))
				first, next = next, random.choice(self.cache[(first,next)])
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


			


			

