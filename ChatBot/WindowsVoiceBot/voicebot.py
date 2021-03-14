from helper import *
from windows_fr import *
from windows_tts import *
from easy_nlp import *
import time
from sr import *



myname = "computer"
talking_to = "unknown"

people = pv(myname+"_people")
responses = pv(myname+"_responses")
keywords = pv(myname+"_keywords")


# def open_app(name):
# 	auto.press('command')
# 	time.sleep(0.5)
# 	auto.press('command')
# 	auto.hotkey('command', 'space')
# 	auto.write(name, interval=0.0)
# 	auto.press('return')


def bot(user_listen):
	user_input = user_listen
	words = user_listen.split()
	
	#YOUR CODE HERE

	#YOUR CODE HERE

	# if len(words) > 2 and words[0] == "open" and words[1] == "application":
	# 	app = " ".join(user_listen.split()[2:])
	# 	open_app(app)
	# 	return "opening " + app

	
	if user_listen == "power off" or user_listen == "shutdown" or user_listen == "shut down":
		print(myname + ": " + win_say("going off line"))
		quit()

	if len(user_listen.split()) > 1 and user_listen.split()[0].lower() == "google":
		googling = " ".join(user_listen.split()[1:])
		google(googling)
		return "here is what I found on " + googling

	if user_listen == "bye" or user_listen == "goodbye" or similar(user_listen,"go to sleep"):
		return "going to sleep, win_say hello " + myname + " if you need me"

	if len(user_listen) > len("I like ") and user_listen[:7].lower() == "i like ":
		people[talking_to] += ["you like " + " ".join(user_listen.split()[2:])]
		return "good to know"

	if user_listen == "learn a response":
		print(myname + ": " + win_say("what phrase am i responding to? "))
		new_listen = selectivelisten(myname)
		print(myname + ": " + win_say("what is my response to " + new_listen + "? "))
		new_response = selectivelisten(myname)
		if responses.contains(new_listen):
			responses[new_listen] += [new_response]
			return "response upadated"
		else:
			responses[new_listen] = [new_response]
			return "response learned"

	if user_listen == "learn a key word" or user_listen == "learn a keyword":
		print(myname + ": " + win_say("what keyword am i responding to? "))
		new_listen = selectivelisten(myname)
		print(myname + ": " + win_say("what is my response to the keyword " + new_listen + "? "))
		new_response = selectivelisten(myname)
		if keywords.contains(new_listen):
			keywords[new_listen] += [new_response]
			return "key word upadated"
		else:
			keywords[new_listen] = [new_response]
			return "key word learned"

	any_sim = any_similar(user_listen,responses.keys())
	if any_sim[0]:
		return random.choice(responses[any_sim[1]])

	for keyword in keywords.keys():
		if keyword in user_listen:
			return random.choice(keywords[keyword])
	else:
		print(myname + ": " + win_say("Response unknown, please enter a response to " + user_listen + " "))
		new_response = selectivelisten(myname)
		responses[user_listen] = [new_response]
		return "response learned"




if __name__ == "__main__":


	#FACIAL RECOGNITION
	if people.is_empty():
		print(myname + ": " + win_say("Welcome, you are the first person I have met"))
		print(myname + ": " + win_say("What is your name? Please state my name, which is " + myname + " first, then your name"))
		name = selectivelisten(myname)
		print(myname + ": " + win_say("nice to meet you "+ name))
		people[name] = ["you have spoken with me before"]
		talking_to = name
		print(myname + ": " + win_say("please look at the camera so I can remember your face"))
		your_face = take_photo(name.replace(" ","_") + ".jpg")
		print(myname + ": " + win_say("face learned"))
	else:
		print(myname + ": " + win_say("Hello"))
		print(myname + ": " + win_say("Let me take a look at you"))
		your_face = take_photo("unknown" + ".jpg")
		print(myname + ": " + win_say("looking at your face"))
		match = find_match(your_face,Here)
		if match != None:
			talking_to = match.replace(".jpg","").replace("_"," ")
			print(myname + ": " + win_say("Welcome back " + talking_to))
			print(myname + ": " + win_say("I remember that " + random.choice(people[talking_to])))
		else:
			print(myname + ": " + win_say("I do not recognize your face"))
			print(myname + ": " + win_say("What is your name? "),end = '')
			name = listen()
			print(win_say("nice to meet you " + name))
			people[name] = ["you have spoken with me before"]
			talking_to = name
			rename_file("unknown.jpg",talking_to.replace(" ","_") + ".jpg")
	print(myname + ": " + win_say("going to sleep, if you need me just say the words hello " + myname))
	#FACIAL RECOGNITION




	while True:


		#WAKING UP
		if woken_up("hello " + myname):
			print("You: hello " + myname)
			print(myname + ": " + win_say("yes, what can i help you with? Begin each phrase with my name, which is " + myname))




		#PROGRAM BEGINS EXECUTION HERE

		while True:
			print("You: ",end = '')
			user_listen = selectivelisten(myname)
			print(user_listen)
			print(myname + ": " + win_say(bot(user_listen)))
			if user_listen == "bye" or user_listen == "goodbye" or similar(user_listen,"go to sleep"):
				break









