import os
from os import path
import mozilla_history
import chrome_history
import sys

def navegators_history(a1, m1, d1, a, m, d):

	#Ruta Mac
	#user = os.environ.get("USER")
	#data_chrome = "/Users/"+user+"/Library/Application Support"

	sys.stdout = open('05_navegator_history.txt', 'w')

	#Ruta Windows
	data_chrome = path.expandvars(r"%LOCALAPPDATA%")

	path_compr = os.path.join(data_chrome, 'Google')

	age1 = int(a1)
	mes1 = int(m1)
	day1 = int(d1)
	age = int(a)
	mes = int(m)
	day = int(d)

	print("GOOGLE CHROME HISTORY \n")
	if os.path.exists(path_compr) == True:
		chrome_history.chrome_history(age1, mes1, day1, age, mes, day)
	else:
		print("You have no instaled Google chrome")
		

	print(" \n \n ---------------------------------  \n \n")

	#Ruta Mac
	#data_firefox = "/Users/"+user+"/Library/Application Support"
	#fire_compr = os.path.join(data_firefox, 'Firefox')

	#Ruta Windows
	data_firefox = path.expandvars(r'%APPDATA%')
	fire_compr = os.path.join(data_firefox, 'Mozilla')

	if os.path.exists(fire_compr) == True:
                mozilla_history.mozilla_history(age1, mes1, day1, age, mes, day)
	else:
		print("You have no installed Firefox \n")

	sys.stdout = sys.__stdout__
	

#navegators_history("2022", "07", "29", "2022", "08", "03")
