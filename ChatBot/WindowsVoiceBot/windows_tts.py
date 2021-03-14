# https://pypi.org/project/pyttsx3/
# pip install pyttsx3

import pyttsx3
engine = pyttsx3.init()
voices = engine.getProperty('voices')

def win_say(this, gender = None):
	if gender == None:
		engine.say(this)
		engine.runAndWait()
		return this
	else:
		if gender.lower() == "male":
			engine.setProperty('voice', voices[0].id)
		if gender.lower() == "female":
			engine.setProperty('voice', voices[1].id)
		engine.say(this)
		engine.runAndWait()
		return this


