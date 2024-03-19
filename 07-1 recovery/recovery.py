from navegators_history import navegators_history
import os
import ctypes, sys
import sqlite3
import json
from sqlite3 import Error
import datetime
import msvcrt
from datetime import datetime
from os import path, remove
import chrome_history
import mozilla_history

#encoding: utf-8

#inicio open_programs

def create_connection(db_file):
	conn = None
	try:
		conn = sqlite3.connect(db_file)
	except Error as e:
		print(e)

	return conn


def select_task_by_type(conn, priority, date_start, date_end):
	cur = conn.cursor()
	cur.execute("SELECT StartTime, Payload, AppId FROM Activity WHERE ActivityType=?", (priority,))

	rows = cur.fetchall()

	fecha_ini = date_start
	fecha_fin = date_end
	utc_time_strt = datetime.strptime(fecha_ini, "%Y-%m-%d")
	utc_time_end = datetime.strptime(fecha_fin, "%Y-%m-%d")
	fecha_ini_x = (utc_time_strt - datetime(1970, 1, 1)).total_seconds()
	fecha_fin_x = (utc_time_end - datetime(1970, 1, 1)).total_seconds() + (24*60*60)

	for row in rows:
		cadena = row[1].decode()
		fecha = row[0]
		dt = datetime.fromtimestamp(row[0])
		if fecha >= fecha_ini_x and fecha <= fecha_fin_x:
			cadena2 = json.loads(row[1])
			cadena_app = json.loads(row[2])
			cadena_app_2 = cadena_app[0]
			res = {cadena2[key] for key in cadena2.keys() & {'appDisplayName'}}
			res2 = {cadena_app_2[key] for key in cadena_app_2.keys() & {'application'}}
			dt_new = dt.strftime("%Y-%m-%d %H:%M:%S")
			file = open("04_open_programs.txt", "a")
			file.write(dt_new)
			file.write("\t")
			file.write(*res2)
			file.write("\n")
			file.close()

def open_programs(date_start, date_end):
	database = r"C:\\Users\\" + os.getlogin() + "\\AppData\\Local\\ConnectedDevicesPlatform\\L." + os.getlogin() + "\\ActivitiesCache.db"

	# create a database connection
	conn = create_connection(database)
	
	with conn:
		print("\nFichero de programas ejecutados creado")
		select_task_by_type(conn, 6, date_start, date_end)

#fin de open_programs

def get_date():
	from datetime import date
	date = date.today()
	return date

def get_date_less1():
	from datetime import date, timedelta
	dateless1 = date.today()+timedelta(days=-1)
	return dateless1

def salir():
	while True:
		print("Presione enter para salir ")
		m = str(msvcrt.getch(),'utf -8')
		if m == "\r":
			sys.exit()
 
def fecha():
	numargument = len(sys.argv) - 1

	if numargument != 2:
		fecha_inicio = get_date_less1()
		fecha_fin = get_date()
	else:
		fecha_inicio = str(sys.argv[1])
		fecha_fin = str(sys.argv[2])
		if fecha_inicio[4] == "/":
			split1 = fecha_inicio.split("/")
			join1 = "-".join(split1)
			fecha_inicio = join1
		elif fecha_inicio[2] == "-":
			split1 = fecha_inicio.split("-")
			join1 = "-".join(reversed(split1))
			fecha_inicio = join1
		elif fecha_inicio[2] == "/":
			split1 = fecha_inicio.split("/")
			join1 = "-".join(reversed(split1))
			fecha_inicio = join1
		elif fecha_inicio[4] == "-":
			fecha_inicio = sys.argv[1]


		if fecha_fin[4] == "/":
			split2 = fecha_fin.split("/")
			join2 = "-".join(split2)
			fecha_fin = join2
		elif fecha_fin[2] == "-":
			split2 = fecha_fin.split("-")
			join2 = "-".join(reversed(split2))
			fecha_fin = join2
		elif fecha_fin[2] == "/":
			split2 = fecha_fin.split("/")
			join2 = "-".join(reversed(split2))
			fecha_fin = join2
		elif fecha_fin[4] == "-":
			fecha_fin = sys.argv[2]
		# else:
		# 	print("Wrong date format")
		

	fecha_inicio = str(fecha_inicio)
	fecha_fin = str(fecha_fin)
	print(f"The chosen date range is from {fecha_inicio} to {fecha_fin}")
#encoding: utf-8  

	if path.exists("01_current_version.txt"):
		remove('01_current_version.txt')
	if path.exists("02_recent_files.txt"):
		remove('02_recent_files.txt')
	if path.exists("03_installed_programs.txt"):
		remove('03_installed_programs.txt')
	if path.exists("04_open_programs.txt"):
		remove('04_open_programs.txt')
	if path.exists("05_navegator_history.txt"):
		remove('05_navegator_history.txt')
	if path.exists("06_log_events.txt"):
		remove('06_log_events.txt')

	#01_CURRENT_VERSION

	cmd_first = "powershell.exe ./Get-RegKeyLastWriteTime.ps1 HKLM SOFTWARE\Microsoft\Windows\CurrentVersion"
	cmd_second = " >> 01_current_version.txt"
	os.system(cmd_first + " " + fecha_inicio + " " + fecha_fin + cmd_second)
	
	#02_RECENT_FILES
	
	cmd_first = "FOR /F \"tokens=*\" %A IN ('forfiles /p \"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Recent\" /d -"
	cmd_second = "') DO (FOR /F \"tokens=*\" %B IN (' forfiles /m %A /p \"C:\\Users\\%USERNAME%\\AppData\\Roaming\\Microsoft\\Windows\\Recent\" /d +"
	cmd_third = "  /C \"cmd /c echo @FDATE\t@file\"') DO (ECHO %B >> 02_recent_files.txt))"
	partes = fecha_inicio.split("-")
	fecha_modif_inicio = "/".join(reversed(partes))
	partes = fecha_fin.split("-")
	fecha_modif_fin = "/".join(reversed(partes))
	
	os.system(cmd_first + fecha_modif_fin + cmd_second + fecha_modif_inicio + cmd_third)
 
	
	#03_INSTALLED_PROGRAMS
	
	cmd_first = "FOR /F \"tokens=*\" %A IN ('forfiles /p \"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\" /d -"
	cmd_second = "') DO (FOR /F \"tokens=*\" %B IN (' forfiles /m %A /p \"C:\\ProgramData\\Microsoft\\Windows\\Start Menu\\Programs\" /d +"
	cmd_third = "  /C \"cmd /c echo @FDATE\t@file\"') DO (ECHO %B >> 03_installed_programs.txt))"
	partes = fecha_inicio.split("-")
	fecha_modif_inicio = "/".join(reversed(partes))
	partes = fecha_fin.split("-")
	fecha_modif_fin = "/".join(reversed(partes))
	
	os.system(cmd_first + fecha_modif_fin + cmd_second + fecha_modif_inicio + cmd_third)

	
	#04_OPEN_PROGRAMS
	
	open_programs(fecha_inicio, fecha_fin)

	#05_HISTORY_CHROME

	year = fecha_inicio.split("-")[0]
	month = fecha_inicio.split("-")[1]
	day = fecha_inicio.split("-")[2]
	year_final = fecha_fin.split("-")[0]
	month_final = fecha_fin.split("-")[1]
	day_final = fecha_fin.split("-")[2]

	sys.stdout = open('05_navegator_history.txt', 'w')

	if numargument == 2:
		chrome_history.chrome_history(year, month, day, year_final, month_final, day_final)
		mozilla_history.mozilla_history(year, month, day, year_final, month_final, day_final)
	else:
		chrome_history.without_arg()
		mozilla_history.mozilla_without_arg()

	sys.stdout = sys.__stdout__
	
	#06_LOG_EVENTS

	cmd_first = "FOR /F \"delims=*\" %A IN ('forfiles /p \"C:\\Windows\\System32\\winevt\\Logs\" /d -"
	cmd_second = "') DO (FOR /F \"delims=*\" %B IN (' forfiles /m %A /p \"C:\\Windows\\System32\\winevt\\Logs\" /d +"
	cmd_third = "  /C \"cmd /c echo @FDATE\t@file\"') DO (ECHO %B >> 06_log_events.txt))"

	partes = fecha_inicio.split("-")
	fecha_modif_inicio = "/".join(reversed(partes))
	partes = fecha_fin.split("-")
	fecha_modif_fin = "/".join(reversed(partes))
	
	os.system(cmd_first + fecha_modif_fin + cmd_second + fecha_modif_inicio + cmd_third)
 
def is_admin():
	try:
		return ctypes.windll.shell32.IsUserAnAdmin()
	except:
		return False
		
if is_admin():
	os.system("powershell.exe Set-ExecutionPolicy Unrestricted -Scope CurrentUser")
	os.system("powershell.exe ./date_format_yyyyMMdd.ps1")
	fecha()
	salir()

else:
	ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
