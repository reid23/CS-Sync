

from sr import *
from helper import *
from windows_tts import *

awake = True

while awake:
	# user_input = input("You: ")
	print("I am listening...")
	user_input = selectivelisten("computer")
	if user_input == "hello":
		print("hi there")
		win_say("hi there")
	elif user_input == "goodbye":
		print("goodbye")
		win_say("goodbye")
		awake = False
	else:
		print("I dont know what to say")
		say("I dont know what to say")

print("end of program")