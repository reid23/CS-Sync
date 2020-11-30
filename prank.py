from helper import *

counter = 0
while True:
	if counter >= 1:
		break
	if weekday() == "monday" and current_time() == "10:02 AM":
		open_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
		counter += 1

