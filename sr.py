
#see documentation
#https://pypi.org/project/SpeechRecognition/

# BEFORE YOU START MAC
# 1. enter xcode-select -p into your terminal to check to see if you have xcode command line tools installed.
# 2. if it gives back the number 2, you need to install xcode command line tools.
# 3. if it gives back a directory, then you are good to skip step 4
# 4. if you need to install xcode command line tools, do so using the link below...
# https://www.embarcadero.com/starthere/xe5/mobdevsetup/ios/en/installing_the_commandline_tools.html
# 5. enter pip3 install cmake into your terminal to install cmake. 


#STEP BY STEP SETUP INSTRUCTIONS MAC
# 1. if homebrew already installed, skip step 2
# 2. enter /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)" into your terminal to install homebrew
# 3. enter brew install portaudio into your terminal
# 4. enter pip3 install pyaudio into your terminal
# 5. enter pip3 install google-api-python-client into your terminal
# 6. enter pip3 install SpeechRecognition into your terminal


#ON WINDOWS:
# 1. pip install pipwin
# 2. pipwin install pyaudio
# 3. if error occurs, you may be missing Build Tools for Visual Studio which you can find in the link below below...
# https://visualstudio.microsoft.com/downloads/
# or download directly from...
# https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools&rel=16
# 4. After installing the Build Tools, try step 2 again.  If that fails, you may need to download and use Anaconda to install pyaudio
# 5. pip install google-api-python-client
# 6. pip install SpeechRecognition



import speech_recognition as sr
from helper import say

# will listen for the keyphrase indefinitely then return True once it hears it.
# usage: if woken_up("hello robot"): do something...
def woken_up(keyphrase = "hello robot"):
	what_said = "$$$"
	while keyphrase not in what_said:
		r = sr.Recognizer()
		with sr.Microphone() as source:
			audio = r.listen(source)

		try:
			what_said = str(r.recognize_google(audio)).lower()
			if keyphrase.lower() in what_said:
				return True
		except sr.UnknownValueError:
			useless = 0
		except sr.RequestError as e:
			print("Could not request results; {0}".format(e))


# will listen for a limited amount of time then return what it hears as string
# usage: thing_said = listen()
def listen():
	what_said = "$$$"
	while what_said == "$$$":
		r = sr.Recognizer()
		with sr.Microphone() as source:
			audio = r.listen(source)

		try:
			what_said = str(r.recognize_google(audio)).lower()
			if what_said != "$$$" and what_said != None:
				return what_said
		except sr.UnknownValueError:
			userless = 0
		except sr.RequestError as e:
			print("Could not request results; {0}".format(e))


# will listen indefinitely for a keyword, then return everthing it hears after that keyword
# usage: thing_said = selectivelisten("hello robot")
def selectivelisten(keyword):
	what_said = "$$$"
	while what_said == "$$$" or keyword not in what_said:
		r = sr.Recognizer()
		with sr.Microphone() as source:
			audio = r.listen(source)

		try:
			what_said = str(r.recognize_google(audio)).lower()
			if what_said != "$$$" and keyword in what_said:
				# new = what_said.replace(keyword,"",1)
				new = []
				start = False
				for word in what_said.split():
					if start:
						new.append(word)
					if word == keyword:
						start = True
				new2 = " ".join(new)
				if new2 == " " or new2 == "":
					new2 = what_said.replace(keyword,"",1)
				if len(new2)>1 and new2[0] == " ":
					return new2[1:]
				# if new2.split()[0] == "s" and len(new2.split()) > 2:
				# 	new2 = " ".join(new2.split()[1:])
				return new2
		except sr.UnknownValueError:
			userless = 0
		except sr.RequestError as e:
			print("Could not request results; {0}".format(e))












