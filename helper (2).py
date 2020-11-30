import fnmatch
import os
from os import system
import time
import getpass
import turtle
import time
from multiprocessing import Process
import shelve
import smtplib
import random
import json
import csv
from datetime import datetime
from datetime import date





#_______________________________________________________PATH REFERENCE VARIABLES
# Home is the path to your user directory
# Desktop is the path to your User Desktop directory
# Here is the path to the current directory that the python program is running from

Home = ''
if os.name == 'nt':
	Home = os.path.join("C:\\Users",getpass.getuser())
else:
	Home = os.path.join("/Users",getpass.getuser())
Desktop = ''
if os.name == 'nt':
	Desktop = os.path.join("C:\\Users",getpass.getuser(),"Desktop")
else:
	Desktop = os.path.join("/Users",getpass.getuser(),"Desktop")

Here = os.getcwd()
MyUserName = getpass.getuser()

#_______________________________________________________PATH REFERENCE VARIABLES




#_______________________________________________________TIME AND DATES

# returns the day of the week as a lowercase string
def weekday():
	d = date.today().weekday()
	days = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
	return days[d]

# returns the current time: example: '07:45 AM'
def current_time():
	t = datetime.now()
	d = datetime.strptime(t.strftime("%I:%M"), "%H:%M")
	return d.strftime("%I:%M %p")

# waits for the given number of seconds
def wait(seconds):
	time.sleep(seconds)



#_______________________________________________________TIME AND DATES







#_______________________________________________________EMAIL AUTOMATION
# functions to send emails
# sender email must allow "less secure app access" in security settings
# how to use examples is comments below

# sends an email to multiple email addresses
# send_emails("sender@example.com",["reciever1@example.com","reciever2@example.com"],["CC these emails"],"Email Header","Email body message","your email username","your email password")
def send_emails(from_addr, to_addr_list, cc_addr_list,subject, message,login, password,smtpserver='smtp.gmail.com:587'):  
	header  = 'From: ' + from_addr
	header += '\nTo: ' + ','.join(to_addr_list)
	header += '\nCc: ' + ','.join(cc_addr_list)
	header += '\nSubject: ' + subject
	message = header + "\n" + message
	server = smtplib.SMTP(smtpserver)
	server.starttls()
	server.login(login,password)
	problems = server.sendmail(from_addr, to_addr_list, message)
	server.quit()

# sends an email to a single email address
# send_email("sender@example.com","reciever@example.com","Email Header","Email body","sender username","sender password")
def send_email(from_addr, to_addr, subject, message,login, password,smtpserver='smtp.gmail.com:587'):  
	header  = 'From: ' + from_addr
	header += '\nTo: ' + ',' + to_addr
	header += '\nSubject: ' + subject
	message = header + "\n" + message
	server = smtplib.SMTP(smtpserver)
	server.starttls()
	server.login(login,password)
	problems = server.sendmail(from_addr, [to_addr], message)
	server.quit()

#_______________________________________________________EMAIL AUTOMATION










#_______________________________________________________FILE AND FOLDER/DIRECTORY MANIPULATION


# returns True if the given string parameter is a path
# is_path("/Users/Bob/Desktop/file_name") == True
# is_path("file_name") == False
# is_path(Desktop) == True
# is_path("Desktop") == False
def is_path(path_or_folder_or_file):
	if os.name == 'nt':
		if '\\' not in path_or_folder_or_file:
			return False
		else:
			return True
	else:
		if "/" not in path_or_folder_or_file:
			return False
		else:
			return True


# returns a string that represents the given string path parameter in a corrected format to account for spaces
# to be used when paths with spaces are not being recognized by your os
# fixed_path("/Users/Bob/Desktop/file name") == '/Users/Bob/Desktop/"file name"'
def fixed_path(path):
	answer = []
	if os.name == "nt":
		for item in path.split("\\"):
			if " " in item:
				answer.append('"' + item + '"')
			else: 
				answer.append(item)
	else:
		for item in path.split("/"):
			if " " in item:
				answer.append('"' + item + '"')
			else: 
				answer.append(item)
	final_answer = answer[0]
	for item in answer[1:]:
		if os.name == 'nt':
			final_answer += '\\' + item
		else:
			final_answer += '/' + item
	return final_answer


# returns a string path to the desired file
# path_to_file("file_name") == "/Users/YourUserName/FileLocation/file_name"
def path_to_file(file_name,rootPath = Home,fix_path = True):
	parts = file_name.split(".")
	name = ".".join(parts[0:-1])
	kind = "." + parts[-1]
	pattern = '*' + kind
	for root, dirs, files in os.walk(rootPath):
		for filename in fnmatch.filter(files, pattern):
			if filename == file_name:
				if fix_path:
					return fixed_path(str(os.path.join(root, filename)))
				else:
					return str(os.path.join(root, filename))			
	return None


# returns a string path to the desired directory/folder
# path_to_dir("folder_name") == "/Users/YourUserName/FolderLocation/folder_name"
def path_to_dir(dir_name,rootPath = Home,fix_path = True):
	username = getpass.getuser()
	for root, dirs, files in os.walk(rootPath):
		if dir_name in dirs:
			if fix_path:
				return fixed_path(str(os.path.join(root, dir_name)))
			else:
				return str(os.path.join(root, dir_name))			
	return None



# returns a list of the contents of a given directory/folder
# contents_of("Desktop") == ["file1","file2","folder1","folder2"]
def contents_of(path_or_folder,include_file_paths = False):
	answer = []
	if not is_path(path_or_folder):
		path_or_folder = path_to_dir(path_or_folder)
	answer = os.listdir(path_or_folder)
	if include_file_paths:
		if os.name == "nt":
			for i in range(len(answer)):
				answer[i] = fixed_path(path_or_folder + "\\" +answer[i])
		else:
			for i in range(len(answer)):
				answer[i] = fixed_path(path_or_folder + "/" +answer[i])
	if '.DS_Store' in answer:
		answer.remove('.DS_Store')
	return answer 



# returns a list of just the folders in a given directory/folder
# folders_in("Desktop") == ["folder1","folder2"]
def folders_in(path_or_folder):
	if not is_path(path_or_folder):
		path_or_folder = path_to_dir(path_or_folder)
	answer = []
	for root, dirs, files in os.walk(path_or_folder):
		if len(dirs) > 0:
			return dirs
	

# returns a list of just the files in a given directory/folder
# files_in("Desktop") == ["file1","file2"]
def files_in(path_or_folder):
	if not is_path(path_or_folder):
		path_or_folder = path_to_dir(path_or_folder)
	answer = []
	for root, dirs, files in os.walk(path_or_folder):
		return files
	

# returns True if the given directory/folder is in fact a folder that exists on your computer
# is_folder("Desktop") == "True"
def is_folder(path_or_folder): 
	if not is_path(path_or_folder):
		if path_or_folder in folders_in(Here):
			return True
		path_or_folder = path_to(path_or_folder)
	if os.name == "nt":
		temp = path_or_folder.split("\\")
		folder_name = temp[-1]
		folder_location = "\\".join(temp[0:-1])
		print(folder_location)
		if folder_name in folders_in(folder_location):
			return True
		else:
			return False
	else:
		temp = path_or_folder.split("/")
		folder_name = temp[-1]
		folder_location = "/" + "/".join(temp[0:-1])
		if folder_name in folders_in(folder_location):
			return True
		else:
			return False


# returns True if the given files is in fact a file that exists on your computer
# is_folder("Desktop") == "True"
def is_file(path_or_file): 
	if not is_path(path_or_file):
		if path_or_folder in files_in(Here):
			return True
		path_or_file = path_to(path_or_file)
	return not is_folder(path_or_file)


# returns a string that is the path to given file of folder name
# path_to("Desktop") == "/Users/YourUserName/Desktop"
# path_to("FileOnDesktop") == /Users/YourUserName/Desktop/FileOnDesktop"
def path_to(file_or_dir,rootPath = Home, fix_path = True):
	if not is_path(rootPath):
		rootPath = path_to_dir(rootPath)
	if file_or_dir in contents_of(os.getcwd()):
		return os.path.join(os.getcwd(),file_or_dir)
	for root, dirs, files in os.walk(rootPath):
		if file_or_dir in dirs:
			if fix_path:
				return fixed_path(str(os.path.join(root, file_or_dir)))
			else:
				return str(os.path.join(root, file_or_dir))
		if file_or_dir in files:
			if fix_path:
				return fixed_path(str(os.path.join(root, file_or_dir)))
			else:
				return str(os.path.join(root, file_or_dir))


# returns a list of strings that are the different paths to all of the instances of a files or folder with the given name
# paths_to("examplefile") == ["/Users/YourUserName/Location1/examplefile","/Users/YourUserName/Location2/examplefile"]
def paths_to(file_or_dir,rootPath = Home, fix_path = True):
	if not is_path(rootPath):
		rootPath = path_to_dir(rootPath)
	answer = []	
	for root, dirs, files in os.walk(rootPath):
		if file_or_dir in dirs:
			if fix_path:
				answer.append(fixed_path(str(os.path.join(root, file_or_dir))))
			else:
				answer.append(str(os.path.join(root, file_or_dir)))
		if file_or_dir in files:
			if fix_path:
				answer.append(fixed_path(str(os.path.join(root, file_or_dir))))
			else:
				answer.append(str(os.path.join(root, file_or_dir)))
	return answer



# creates a folder in the given directory with the given name
# create_folder("foldername") creates a folder called foldername in the current directory/folder
# create_folder("foldername","Desktop")
def create_folder(folder,to_dir = Here):
	if not is_path(to_dir):
		to_dir = path_to_dir(to_dir)
	if os.name == "nt":
		if to_dir != None:
			os.system("md " + fixed_path(to_dir + "\\" + folder))
	else:
		if to_dir != None:
			os.system("mkdir " + fixed_path(to_dir + "/" + folder))


# creates a file given the file name and directory/folder where it should be created
# if no directory/folder is given, it will be created in the current working directory(i.e. Here)
# create_file("test.txt") == creates a test.txt file in the current working directory/folder
# create_file("test.txt","Desktop") == creates a test.txt file in the Desktop directory/folder
def create_file(file_name_or_path,to_dir = Here):
	if os.name == "nt":
		if not is_path(file_name_or_path):
			if not is_path(to_dir):
				to_dir = path_to(to_dir)
			file_name_or_path = to_dir + "\\" + file_name_or_path
		if file_name_or_path != None:
			os.system("fsutil file createnew " + file_name_or_path + " 1000")
	else:
		if not is_path(file_name_or_path):
			if not is_path(to_dir):
				to_dir = path_to(to_dir)
			file_name_or_path = to_dir + "/" + file_name_or_path
		if file_name_or_path != None:
			os.system("touch " + file_name_or_path)


# reads in the contents of a file and returns it as a string
# unless the file is a .csv, in which case a 2d array will be returned
# read_file("file_name.txt") == the data saved in file_name.txt
def read_file(file_name_or_path):
	if file_name_or_path in contents_of(Here):
		file_name_or_path = os.path.join(Here,file_name_or_path)
	if len(file_name_or_path) > 4 and file_name_or_path[-4:] == ".csv":
		if not is_path(file_name_or_path):
			file_name_or_path = path_to(file_name_or_path)
		data = list(csv.reader(open(file_name_or_path)))
		return data
	if not is_path(file_name_or_path):
		with open(path_to_file(file_name_or_path), 'r') as myfile: 
			data = myfile.read()
		return data
	else:
		with open(file_name_or_path, 'r') as myfile: 
			data = myfile.read()
		return data

# rewrites the data stored in a given file
# write_file("file_name.txt","new content") == resets to data stored in file_name.txt to be "new content"
def write_file(file_name_or_path, content):
	if file_name_or_path in contents_of(Here):
		file_name_or_path = os.path.join(Here,file_name_or_path)
	if len(file_name_or_path) > 4 and file_name_or_path[-4:] == ".csv" and type(content) == list:
		to_write = ''
		for line in content:
			to_write += ",".join(str(line)) + '\n'
		content = to_write
	if not is_path(file_name_or_path):
		with open(path_to_file(file_name_or_path), 'w') as myfile: 
			myfile.write(content)
	else:
		with open(file_name_or_path, 'w') as myfile: 
			myfile.write(content)



def update_file(file_name_or_path,content):
	if file_name_or_path in contents_of(Here):
		file_name_or_path = os.path.join(Here,file_name_or_path)
	if not is_path(file_name_or_path):
		file_name_or_path = path_to_file(file_name_or_path)
	cur_content = read_file(file_name_or_path)
	if len(file_name_or_path) > 4 and file_name_or_path[-4:] == ".csv" and type(content) == list and type(cur_content) == list:
		for i in range(len(content)):
			content[i] = str(content[i])
		write_file(file_name_or_path,cur_content + [content])
	else:
		write_file(file_name_or_path,cur_content + content)



def delete_file(file_name_or_path):
	if file_name_or_path in contents_of(Here):
		file_name_or_path = os.path.join(Here,file_name_or_path)
	if os.name == "nt":
		if not is_path(file_name_or_path):
			file_name_or_path = path_to_file(file_name_or_path)
			if file_name_or_path != None:
				os.system("del " + file_name_or_path)
		else:
			os.system("del " + file_name_or_path)
	else:
		if not is_path(file_name_or_path):
			file_name_or_path = path_to_file(file_name_or_path)
			if file_name_or_path != None:
				os.system("rm " + file_name_or_path)
		else:
			os.system("rm " + file_name_or_path)

def delete_folder(folder_or_path):
	if folder_or_path in contents_of(Here):
		folder_or_path = os.path.join(Here,folder_or_path)
	if os.name == "nt":
		if not is_path(folder_or_path):
			folder_or_path = path_to_dir(folder_or_path)
			if folder_or_path != None:
				os.system("rmdir /Q /S " + folder_or_path)
		else:
			os.system("rmdir /Q /S " + folder_or_path)
	else:
		if not is_path(folder_or_path):
			folder_or_path = path_to_dir(folder_or_path)
			if folder_or_path != None:
				os.system("rm -r " + folder_or_path)
		else:
			os.system("rm -r " + folder_or_path)


def move_file(file_name_or_path,to_dir):
	if file_name_or_path in contents_of(Here):
		file_name_or_path = os.path.join(Here,file_name_or_path)
	if os.name == "nt":
		if not is_path(file_name_or_path):
			file_name_or_path = path_to_file(file_name_or_path)
		if not is_path(to_dir):
			to_dir = path_to_dir(to_dir)
		if to_dir != None and file_name_or_path != None:
			os.system("move " + file_name_or_path + " " + to_dir)
	else:
		if not is_path(file_name_or_path):
			file_name_or_path = path_to_file(file_name_or_path)
		if not is_path(to_dir):
			to_dir = path_to_dir(to_dir)
		if to_dir != None and file_name_or_path != None:
			os.system("mv " + file_name_or_path + " " + to_dir)

def move_folder(folder_or_path,to_dir):
	if folder_or_path in contents_of(Here):
		folder_or_path = os.path.join(Here,folder_or_path)
	if os.name == "nt":
		if not is_path(folder_or_path):
			folder_or_path = path_to_dir(folder_or_path)
		if not is_path(to_dir):
			to_dir = path_to_dir(to_dir)
		if to_dir != None and folder_or_path != None:
			os.system("move " + folder_or_path + " " + to_dir)
	else:		
		if not is_path(folder_or_path):
			folder_or_path = path_to_dir(folder_or_path)
		if not is_path(to_dir):
			to_dir = path_to_dir(to_dir)
		if to_dir != None and folder_or_path != None:
			os.system("mv " + folder_or_path + " " + to_dir)


def rename_file(file_name_or_path, new_name):
	if os.name == "nt":
		if not is_path(file_name_or_path) and file_name_or_path not in Here:
			file_name_or_path = path_to_file(file_name_or_path)
		os.system("rename " + file_name_or_path + " " + new_name)
	else:
		if not is_path(file_name_or_path):
			file_name_or_path = path_to_file(file_name_or_path)
		os.system("mv " + file_name_or_path + " " + "/".join(file_name_or_path.split("/")[:-1]) + "/" + new_name)


def rename_folder(folder_name_or_path, new_name):
	if os.name == "nt":
		if not is_path(folder_name_or_path) and file_name_or_path not in Here:
			folder_name_or_path = path_to_dir(folder_name_or_path)
		os.system("move " + folder_name_or_path + " " + new_name)

	if not is_path(folder_name_or_path):
		folder_name_or_path = path_to_dir(folder_name_or_path)
	os.system("mv " + folder_name_or_path + " " + "/".join(folder_name_or_path.split("/")[:-1]) + "/" + new_name)



def open_file(file_name_or_path):
	if file_name_or_path in contents_of(Here):
		file_name_or_path = os.path.join(Here,file_name_or_path)
	if not is_path(file_name_or_path):
		file_name_or_path = path_to_file(file_name_or_path)
	if file_name_or_path != None:
		if os.name == "nt":
			os.system(file_name_or_path)
		else:
			os.system("open " + file_name_or_path)


def get_files(kind,path = Here):
	if not is_path(path):
		path = path_to_dir(path)
	files = []
	if path != None:
		for file in contents_of(path):
			if kind.lower() in file.lower():
				files.append(file)
	return files


def find_files(kind,path = Home):
	if not is_path(path):
		path = path_to_dir(path)
	answer = []
	rootPath = path
	pattern = kind
	for root, dirs, files in os.walk(rootPath):
		for filename in files:
			if kind.lower() in filename.lower():
				answer.append(fixed_path(str(os.path.join(root, filename))))
	return answer



def copy_file(file_name_or_path,to_dir = Here):
	if file_name_or_path in contents_of(Here):
		file_name_or_path = os.path.join(Here,file_name_or_path)
	if os.name == "nt":
		if not is_path(file_name_or_path):
			file_name_or_path = path_to_file(file_name_or_path)
		if not is_path(to_dir):
			to_dir = path_to_dir(to_dir)
		if file_name_or_path != None:
			os.system("copy " + file_name_or_path + " " + to_dir)
	else:
		if not is_path(file_name_or_path):
			file_name_or_path = path_to_file(file_name_or_path)
		if not is_path(to_dir):
			to_dir = path_to_dir(to_dir)
		if file_name_or_path != None:
			os.system("cp " + file_name_or_path + " " + to_dir)

def copy_folder(folder_name_or_path,to_dir = Here):
	if folder_name_or_path in contents_of(Here):
		folder_name_or_path = os.path.join(Here,folder_name_or_path)

	if os.name == "nt":
		if not is_path(folder_name_or_path):
			folder_name_or_path = path_to_dir(folder_name_or_path)
		if not is_path(to_dir):
			to_dir = path_to_dir(to_dir)
		if folder_name_or_path != None:
			copyname = folder_name_or_path.split("\\")[-1]
			create_folder(copyname,to_dir)
			os.system("xcopy /E " + folder_name_or_path + " " + to_dir + "\\" + copyname)
	else:
		if not is_path(folder_name_or_path):
			folder_name_or_path = path_to_dir(folder_name_or_path)
		if not is_path(to_dir):
			to_dir = path_to_dir(to_dir)
		if folder_name_or_path != None:
			os.system("cp -r " + folder_name_or_path + " " + to_dir)


#_______________________________________________________FILE AND FOLDER/DIRECTORY MANIPULATION







def open_url(url):
	if os.name == "nt":
		os.system("start " + url)
	else:
		os.system("open " + url)

def google(search_this): 
	if(len(search_this.split()) == 1):
		open_url("https://www.google.com/search?q=" + search_this)
	else:
		open_url("https://www.google.com/search?q=" + "+".join(search_this.split()))



def run_python(file_name_or_path,background = False):
	if ".py" not in file_name_or_path:
		file_name_or_path += ".py"
	if file_name_or_path in contents_of(Here):
		file_name_or_path = os.path.join(Here,file_name_or_path)
	if not is_path(file_name_or_path):
		file_name_or_path = path_to_file(file_name_or_path)
	if file_name_or_path != None:
		if not background:
			if os.name == "nt":
				os.system("python " + file_name_or_path)
			else:
				os.system("python3 " + file_name_or_path)
		else:
			if os.name == "nt":
				os.system("pythonw " + file_name_or_path)
			else:
				os.system("python3 " + file_name_or_path  + " &")




def easy_input(prompt = "Enter Input Here: ", title = "Input"):
	screen = turtle.Screen()
	screen.setup(0,0)
	user_input = screen.textinput(title,prompt)
	turtle.bye()
	return user_input



# runs any number of functions in parallel
# must be run inside of an if statement like so...
# if __name__ == "__main__":
#	run_parallel([say,easy_input],[("prompting",),("prompting",)])
def run_parallel(functlist,paramlist = [(),()]): 
	processes = []
	i = 0
	for f in functlist:
		processes.append(Process(target=f,args=paramlist[i]))
		i += 1
	for p in processes:
		p.start()
	for p in processes:
		p.join()






def chance(percent): # is percent likely to return True and returns False otherwise
	p = random.random() * 100
	if percent > 100:
		percent = 100
	if percent < 0:
		percent = 0
	if percent >= p:
		return True
	else:
		return False


def contains_any(of_these,from_this):
	if type(from_this) != list:
		from_this = from_this.split()
	for item in from_this:
		if item in of_these:
			return True
	return False
	

def one_contained(of_these,from_this):
	if type(from_this) != list:
		from_this = from_this.split()
	for item in from_this:
		if item in of_these:
			return item
	return None





def make_executable(file_name_or_path):
	if os.name == "nt":
		print("this command is for Mac OS only")
		return None
	if not is_path(file_name_or_path):
		file_name_or_path = path_to_file(file_name_or_path)
	at_top = "#!/usr/bin/env python3"
	write_file(file_name_or_path,at_top + "\n" + read_file(file_name_or_path))
	new_name = "".join(file_name_or_path.split("/")[-1].split(".")[:-1]) + ".command"
	rename_file(file_name_or_path,new_name)
	os.system("chmod +x " + new_name)












def simplify(phrase): # simplifies a phrase by removing punctuation and caps then returns it
	alphabet = "abcdefghijklmnopqrstuvwxyz "
	new_phrase = ""
	for letter in phrase.lower():
		if letter in alphabet:
			new_phrase += letter
	return new_phrase



def talkable(phrase):
	alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz123456789,.?! "
	new_phrase = ""
	for letter in phrase.lower():
		if letter in alphabet:
			new_phrase += letter
	return new_phrase



def similar(a,b,min_sim = 1): # returns true if two phrases are similar and false otherwise
	simple_a = simplify(a.lower())
	simple_b = simplify(b.lower())
	if simple_a == simple_b:
		return True
	if len(simple_a.split()) == 1 and len(simple_b.split()) == 1:
		if len(simple_a) == len(simple_b) and len(simple_a) > 4:
			matches = 0
			for i in range(len(simple_a)):
				if simple_a[i] == simple_b[i]:
					matches += 1
			if matches >= len(simple_a) - 1:
				return True
			else:
				return False
		else:
			return False
	if len(simple_a) == len(simple_b):
		matches = 0
		for i in range(len(simple_a)):
			if simple_a[i] == simple_b[i]:
				matches += 1
		if matches/len(simple_a) > min_sim:
			return True
	if len(simple_a.split()) == len(simple_b.split()) and len(simple_a.split()) >= 5: 
		matches = 0
		wrong_word_index = 0;
		for i in range(len(simple_a.split())):
			if simple_a.split()[i] == simple_b.split()[i]:
				matches += 1
			else:
				wrong_word_index = i
		if matches/len(simple_a) > min_sim:
			return True
		if matches == len(simple_a.split()) - 1:
			letter_match = 0
			for j in range(len(simple_a.split()[wrong_word_index])):
				if simple_a.split()[wrong_word_index][j] in simple_b.split()[wrong_word_index]:
					letter_match += 1
			if letter_match == len(simple_a.split()[wrong_word_index]):
				return True
	return False


def any_similar(this,lst):
	if len(lst) == 0:
		return (False,"no match")
	for s in lst:
		if similar(s,this):
			return (True,s)
	return (False,"no match")




def say(phrase,voice = None,):
	if os.name == "nt":
		print("say function not available")
	else:
		if voice == None:
			os.system("say " + talkable(phrase))
		else:
			os.system("say -v " + voice + " " + talkable(phrase))
	return phrase

def say2(phrase,voice = None):
	run_parallel([say,print],[(phrase,),(phrase,)])






def make_database(name = "database",location = Here):
	if not is_path(location):
		location = path_to_dir(location)
	return shelve.open(os.path.join(location, name))



class pdict:
	def __init__(self,file_name = "database",location = Here):
		self.data = make_database(file_name,location)
		self.location = location
		self.file_name = file_name

	def __getitem__(self,i):
		return self.data[i]

	def __setitem__(self,i,val):
		self.data[i] = val

	def __str__(self):
		answer = '{'
		for key, value in self.data.items(): 
			answer +=  "'" + key + "'" + " : " + str(value) + ", "
		return answer[:-2] + "}"

	def __repr__(self):
		return self.__str__()

	def keys(self):
		return list(self.data.keys())

	def items(self):
		return list(self.data.items())

	def values(self):
		vals = []
		for key, value in self.data.items():
			vals.append(value)
		return vals			

	def contains(self,item):
		if item in self.data.keys():
			return True
		else:
			return False

	def key_with_val(self,val): 
		for key, value in self.data.items(): 
			if val == value: 
				return key 
		return None

	def all_keys_with_val(self,val):
		keys = []
		for key, value in self.data.items(): 
			if val == value: 
				keys += [key]
		if len(keys) > 0:
			return keys
		else: 
			return None

	def average(self):
		vals = self.values()
		total = len(vals)
		s = sum(vals)
		return s/total

	def max(self):
		val = max(self.values())
		key = self.key_with_val(val)
		return (key,val)

	def min(self):
		val = min(self.values())
		key = self.key_with_val(val)
		return (key,val)












































class pv:
	def __init__(self,file_name = "pv",file_location = Here,start_data = None):
		if not is_path(file_location):
			file_location = path_to(file_location)
		self.data = start_data
		self.file_name = file_name + ".txt"
		self.file_location = file_location
		self.file_path = os.path.join(self.file_location,self.file_name)
		if self.file_name not in contents_of(self.file_location):
			create_file(self.file_path)
			self.save()
		else:
			self.data = eval(read_file(self.file_path))


	def save(self):
		write_file(self.file_path,str(self.data.__repr__()))

	def load(self):
		self.data = eval(read_file(self.file_path))

	def set(self,val):
		self.data = val
		self.save()

	def is_new(self):
		return self.data == None

	def is_empty(self):
		return self.is_new()

	def __repr__(self):
		return self.data.__repr__()

	def __str__(self):
		return str(self.data)

	def __int__(self):
		return int(self.data)

	def __float__(self):
		return float(self.data)

	def __getitem__(self,i):
		return self.data[i]

	def __setitem__(self,i,value):
		if type(i) == int and self.data == None:
			self.data = []
		if type(i) == str and self.data == None:
			self.data = {}
		self.data[i] = value
		self.set(self.data)

	def __len__(self):
		return len(self.data)

	def __ior__(self,val):
		self.set(val)
		return self

	def type(self):
		return type(self.data)

	def __eq__(self,other):
		if type(other) == pv:
			return self.data == other.data
		else:
			return self.data == other

	def __lt__(self,other):
		if type(other) == pv:
			return self.data < other.data
		else:
			return self.data < other

	def __gt__(self,other):
		if type(other) == pv:
			return self.data > other.data
		else:
			return self.data > other


	def __add__(self,other):
		if type(other) == pv:
			return self.data + other.data
		else:
			return self.data + other

	def __radd__(self,other):
		if type(other) == pv:
			return self.other + self.data
		else:
			return other + self.data

	def __iadd__(self,other):
		if self.data == None and type(other) == int or self.data == None and type(other) == float:
			self.data = 0
		if type(other) == pv:
			self.set(self.data + other.data)
			return self
		else:
			self.set(self.data + other)
			return self


	def __sub__(self,other):
		if type(other) == pv:
			return self.data - other.data
		else:
			return self.data - other

	def __rsub__(self,other):
		if type(other) == pv:
			return self.other - self.data
		else:
			return other - self.data

	def __isub__(self,other):
		if self.data == None and type(other) == int or self.data == None and type(other) == float:
			self.data = 0
		if type(other) == pv:
			self.set(self.data - other.data)
			return self
		else:
			self.set(self.data - other)
			return self



	def __mul__(self,other):
		if type(other) == pv:
			return self.data * other.data
		else:
			return self.data * other

	def __rmul__(self,other):
		if type(other) == pv:
			return self.other * self.data
		else:
			return other * self.data

	def __imul__(self,other):
		if type(other) == pv:
			self.set(self.data * other.data)
			return self
		else:
			self.set(self.data * other)
			return self



	def __truediv__(self,other):
		if type(other) == pv:
			return self.data / other.data
		else:
			return self.data / other

	def __rtruediv__(self,other):
		if type(other) == pv:
			return self.other / self.data
		else:
			return other / self.data

	def __itruediv__(self,other):
		if type(other) == pv:
			self.set(self.data / other.data)
			return self
		else:
			self.set(self.data / other)
			return self

	def keys(self):
		if self.data == None:
			self.data = {}
			self.save()
			return []
		if self.data == {}:
			return []
		return list(self.data.keys())

	def items(self):
		if self.data == None:
			self.data = {}
			self.save()
			return []
		if self.data == {}:
			return []
		return list(self.data.items())

	def values(self):
		if self.data == None:
			self.data = {}
			return []
		if self.data == {}:
			return []
		vals = []
		for key, value in self.items():
			vals.append(value)
		return vals

	def contains(self,item):
		if self.data == None:
			self.data = {}
			return False
		if self.data == {}:
			return False
		if item in self.keys():
			return True
		else:
			return False

	def key_with_val(self,val): 
		if self.data == None:
			self.data = {}
		for key, value in self.items(): 
			if val == value: 
				return key 
		return None

	def keys_with_val(self,val):
		if self.data == None:
			self.data = {}
		keys = []
		for key, value in self.items(): 
			if val == value: 
				keys += [key]
		if len(keys) > 0:
			return keys
		else: 
			return None

	def average(self):
		if self.type() == dict:
			vals = self.values()
			total = len(vals)
			s = sum(vals)
			return s/total
		if self.type() == list or self.type == tuple:
			s = sum(self.data)
			t = len(self.data)
			return s/t

	def max(self):
		if self.type() == dict:
			val = max(self.values())
			key = self.key_with_val(val)
			return (key,val)
		if self.type() == list or self.type() == tuple:
			return max(self.data)

	def min(self):
		if self.type() == dict:
			val = min(self.values())
			key = self.key_with_val(val)
			return (key,val)
		if self.type() == list or self.type() == tuple:
			return min(self.data)

	def append(self,item):
		if self.data == None:
			self.data = []
		self.data.append(item)
		self.save()

	def pop(self,i):
		if self.data == None:
			self.data = []
		return self.data.pop(i)

	def remove(self,index):
		if index == len(self.data) - 1 or index == -1:
			self.set(self.data[:-1])
		elif index == 0:
			self.set(self.data[1:])
		else:
			self.set(self.data[0:index] + self.data[index + 1:])

	def insert(self,item,index):
		if self.type() == list:
			if index == 0:
				self.set([item] + self.data)
			elif index == len(self.data):
				self.append(item)
			else:
				self.set(self.data[:index] + [item] + self.data[index:])
		if self.type() == str:
			if index == 0:
				self.set(item + self.data)
			elif index == len(self.data):
				self.set(self.data + item)
			else:
				self.set(self.data[:index] + item + self.data[index:])


	def split(self,by = " "):
		return self.data.split(by)

	def join(self,by = " "):
		return by.join(self.data)

	def sort(self,funct = None,rev = False):
		if funct == None:
			self.data.sort(reverse = rev)
			self.save()
		else:
			self.data.sort(reverse = rev,key = funct)
			self.save()


	def lower(self):
		return self.data.lower()

	def upper(self):
		return self.data.upper()

	def replace(self,this,that):
		return self.data.replace(this,that)









