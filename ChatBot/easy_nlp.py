# Mac: execute the following terminal commands to install spacy
# pip3 install -U spacy
# python3 -m spacy download en_core_web_sm

# Windows: execute the following command prompt commands 
# pip install -U spacy
# python -m spacy download en_core_web_sm

# see documentation...
# https://spacy.io/usage



#Example Sentence

# Apple is looking at buying U.K. startup for $1 billion.

#TEXT		LEMMA	POS		TAG		DEP			SHAPE	ALPHA	STOP
#Apple		apple	PROPN	NNP		nsubj		Xxxxx	True	False
#is			be		AUX		VBZ		aux			xx		True	True
#looking	look	VERB	VBG		ROOT		xxxx	True	False
#at			at		ADP		IN		prep		xx		True	True
#buying		buy		VERB	VBG		pcomp		xxxx	True	False
#U.K.		u.k.	PROPN	NNP		compound	X.X.	False	False
#startup	startup	NOUN	NN		dobj		xxxx	True	False
#for		for		ADP		IN		prep		xxx		True	True
#$			$		SYM		$		quantmod	$		False	False
#1			1		NUM		CD		compound	d		False	False
#billion	billion	NUM		CD		pobj		xxxx	True	False





# List of DEP definitions

# acl	clausal modifier of noun (adjectival clause)
# acomp	adjectival complement
# advcl	adverbial clause modifier
# advmod	adverbial modifier
# agent	agent
# amod	adjectival modifier
# appos	appositional modifier
# attr	attribute
# aux	auxiliary
# auxpass	auxiliary (passive)
# case	case marking
# cc	coordinating conjunction
# ccomp	clausal complement
# compound	compound
# conj	conjunct
# cop	copula
# csubj	clausal subject
# csubjpass	clausal subject (passive)
# dative	dative
# dep	unclassified dependent
# det	determiner
# dobj	direct object
# expl	expletive
# intj	interjection
# mark	marker
# meta	meta modifier
# neg	negation modifier
# nn	noun compound modifier
# nounmod	modifier of nominal
# npmod	noun phrase as adverbial modifier
# nsubj	nominal subject
# nsubjpass	nominal subject (passive)
# nummod	numeric modifier
# oprd	object predicate
# obj	object
# obl	oblique nominal
# parataxis	parataxis
# pcomp	complement of preposition
# pobj	object of preposition
# poss	possession modifier
# preconj	pre-correlative conjunction
# prep	prepositional modifier
# prt	particle
# punct	punctuation
# quantmod	modifier of quantifier
# relcl	relative clause modifier
# root	root
# xcomp	open clausal complement






import spacy
import os

import random
from random import choice




nlp = spacy.load("en_core_web_sm")


def GetDep(sent,d):
	doc = nlp(no_punct(sent))
	sub_toks = [tok for tok in doc if (tok.dep_ == d) ]
	answer = []
	for item in sub_toks:
		answer.append(str(item))
	return answer


def parse(sent):
	sent = no_punct(sent)
	words = sent.split()
	doc = nlp(sent)
	answer = []
	i = 0
	for chunk in doc:
		if not i >= len(words):
			answer.append([words[i],str(chunk.dep_)])
		i += 1
	return answer





def GetNounPhrases(sent):
	doc = nlp(no_punct(sent))
	answer = []
	for item in doc.noun_chunks:
		answer.append(str(item))
	return answer

	


def no_punct(phrase): # simplifies a phrase by removing punctuation and caps then returns it
	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz123456789 "
	new_phrase = ""
	for letter in phrase:
		if letter in alphabet:
			new_phrase += letter
	return new_phrase


def simplify2(phrase): # simplifies a phrase by removing punctuation and caps then returns it
	alphabet = "abcdefghijklmnopqrstuvwxyz "
	new_phrase = ""
	for letter in phrase.lower():
		if letter in alphabet:
			new_phrase += letter
	return new_phrase


def perspective_switch(s): # switches the perspective of a sentence and returns it. "i like cake" becomes "you like cake"
	# if contains_any(simplify(s),["i","you","me","im","youre","your"])
	index = 0
	b = s.split()
	for word in b:
		word = simplify2(word)
		if word == "youre":
			b[index] = "you"
			b.insert(index + 1, "are")
		if word.lower() == "i" or word.lower() == "me":
			b[index] = "you"
		if word.lower() == "my":
			b[index] = "your"
		if word.lower() == "myself":
			b[index] = "yourself"
		if word.lower() == "am":
			b[index] = "are"
		if word.lower() == "was":
			b[index] = "were"
		if b[index] != b[-1] and word.lower() == "you" and b[index+1].lower() != "are":
			b[index] = "me"
		if word.lower() == "you":
				b[index] = "me"
		if b[index] != b[-1] and word.lower() == "you" and b[index+1].lower() == "are":
			b[index] = "i"
		if word.lower() == "im":
			b[index] = "you are"
		if word == "are":
			b[index] = "am"
		if word == "this":
			b[index] = "that"
		if word == "that":
			b[index] = "this"
		index += 1
	answer = " ".join(b)
	p = parse(answer)
	final_answer = []
	for item in p:
		if item[0] == "me" and item[1] == "nsubj":
			final_answer.append("i")
		else:
			final_answer.append(item[0])
	return " ".join(final_answer)




def dodge_question(q):
	q = no_punct(q).lower()
	response = perspective_switch(q)
	if response.split()[0] in ["would","could","will","can","wont","dont","are","do"]:
		return "should " + " ".join(response.split()[1:]) + "?"
	if len(q.split()) > 1 and q.split()[0] == "is" and q.split()[1] == "that":
		return "should it be " + " ".join(response.split()[2:]) + "?"
	else:
		return response









