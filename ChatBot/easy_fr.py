import face_recognition
import os
from helper import *
import getpass


# for these functions to work you will need the following...

# 1. install face_recognition using pip3 : requires cmake and xcode command line tools
# 2. install homebrew
# 3. use homebrew to install imagesnap


# Links:

# cmake: https://pypi.org/project/cmake/
# xcode command line tools: https://www.embarcadero.com/starthere/xe5/mobdevsetup/ios/en/installing_the_commandline_tools.html
# face_recognition: https://pypi.org/project/face-recognition/
# homebrew: https://brew.sh/
# imagesnap: https://davidwalsh.name/mac-camera


#STEP BY STEP SETUP INSTRUCTIONS
#1. enter xcode-select -p into your terminal to check to see if you have xcode command line tools installed.
#2. if it gives back the number 2, you need to install xcode command line tools.
#3. if it gives back a directory, then you are good to skip step 4
#4. if you need to install xcode command line tools, do so using the link below...
# https://www.embarcadero.com/starthere/xe5/mobdevsetup/ios/en/installing_the_commandline_tools.html
#5. enter pip3 install cmake into your terminal to install cmake. 
#6. enter /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)" into your terminal to install homebrew
#7. enter brew install imagesnap into your terminal to install imagesnap
#8. enter pip3 install face-recognition into your terminal to install face-recognition

#Note: if you are on Windows, These steps may not work for you, look at the link below instead...
#https://pypi.org/project/face-recognition/





def load_face(face):
	if not is_path(face):
		face = path_to(face)
	return face_recognition.load_image_file(face)


def is_loaded(face):
	if str(type(face)) == "<class 'numpy.ndarray'>" and str(type(face[0])) == "<class 'numpy.ndarray'>":
		return True
	else:
		return False

def encode_face(face):
	if not is_loaded(face):	
		return face_recognition.face_encodings(load_face(face))[0]
	else:
		return face_recognition.face_encodings(face)[0]

def is_encoded(face):
	if str(type(face)) == "<class 'numpy.ndarray'>" and str(type(face[0])) == "<class 'numpy.float64'>":
		return True
	else:
		return False

def compare_encodings(encoding1,encoding2):
	results = face_recognition.compare_faces([encoding1], encoding2)
	return results[0]

def compare_faces(face1,face2):
	if type(face1) == str and type(face2) == str:
		face1ok = False
		face2ok = False
		for item in [".png",".jpg",".jpeg"]:
			if item in face1:
				face1ok = True
			if item in face2:
				face2ok = True
		if not face1ok or not face2ok:
			return False
		if not is_path(face1):
			face1 = path_to(face1)
		if not is_path(face2):
			face2 = path_to(face2)
	if not is_loaded(face1) and not is_encoded(face1):
		face1 = load_face(face1)
		face1 = encode_face(face1)
	if not is_loaded(face2) and not is_encoded(face2):
		face2 = load_face(face2)
		face2 = encode_face(face2)

	if is_loaded(face1) and not is_encoded(face1):
		face1 = encode_face(face1)
	if is_loaded(face2) and not is_encoded(face2):
		face2 = encode_face(face2)

	return compare_encodings(face1,face2)




def take_photo(photo_name):
	os.system("imagesnap -w 1 " + photo_name)
	return Here + "/" + photo_name


def current_face_is(original_photo):
	current_face = take_photo("current_face.png")
	return compare_faces(path_to(original_photo),current_face)


def find_match(original_face,face_list,include_path = False):
	if not is_path(face_list):
		face_list = path_to(face_list)
	face_list = contents_of(face_list,True)
	if not is_path(original_face):
		original_face = path_to(original_face)
	if not is_path(face_list[0]):
		for item in face_list:
			item = path_to(item)
	for face in face_list:
		if ".png" in face or ".jpg" in face:
			if os.name == 'nt':
				if compare_faces(face,original_face) and face.split("\\")[-1] != original_face.split("\\")[-1]:
					if include_path:
						return face
					else:
						return face.split("\\")[-1]
			else:
				if compare_faces(face,original_face) and face.split("/")[-1] != original_face.split("/")[-1]:
					if include_path:
						return face
					else:
						return face.split("/")[-1]
	return None

















