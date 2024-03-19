#!/usr/bin/env python3

from pickle import NONE, TRUE
import tkinter as tk #pip3 install tk
import qrcode #pip3 install qrcode"[pil]" en Mac
from dataclasses import dataclass
from fileinput import filename
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad,unpad
import argparse # Para poder crear el menu de ayuda
import os, sys
import hmac, base64, struct, hashlib, time

##############################################################################################
def get_hotp_token(secret, intervals_no):
	try:
		key = base64.b16decode(secret, True)
	except:
		print("Non-base16 digit found")
		raise SystemExit
	#decodificar la key
	msg = struct.pack(">Q", intervals_no)
	#conversiones entre valores de Python y estructuras C representadas
	h = hmac.new(key, msg, hashlib.sha1).digest()
	o = h[19] & 15
	#genera un hash usando ambos. El algoritmo hash es HMAC
	h = (struct.unpack(">I", h[o:o+4])[0] & 0x7fffffff) % 1000000
	#unpacking
	return h

def get_totp_token(secret):
	#asegurarse de dar el mismo otp
	x = str(get_hotp_token(secret, intervals_no=int(time.time())//30))
	while len(x)!=6:
		x = str(x).zfill(6)
	return x
def encrypt(date, key):
		date = pad(date.encode(),16)
		cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
		return base64.b64encode(cipher.encrypt(date))

def decrypt(enc, key):
		enc = base64.b64decode(enc)
		cipher = AES.new(key.encode('utf-8'), AES.MODE_ECB)
		return unpad(cipher.decrypt(enc),16)

def k_key(otp_key):
	try:
		with open(".key", "rb") as file_key:
			key = file_key.read().decode(encoding = 'utf-8')
		with open(otp_key, 'rb') as file_opt:
			otp_key = file_opt.read()
		otp_key = decrypt(otp_key, key)
		num_otp_key = len(otp_key) - 1
		otp_key = otp_key[2:num_otp_key]
		with open("./key1.hex", "wb") as file:
			file.write(otp_key)
	except:
		print("There is an error with the encrypted key")
		raise SystemExit
	totp = get_totp_token(otp_key)
	print(totp)
	return(totp)

##############################################################################################
def g_key(key_file):
	try:
		with open(key_file, "rb") as file:
			data = file.read()
		hex_key = int(data, 16)
	except ValueError:
		print("./ft_otp: error: invalid value in " + key_file)
		raise SystemExit
	except:
		print("There is an error with the " + key_file + " file")
		raise SystemExit
	hex_key = str(data)
	if len(hex_key) < 64:
		print("./ft_otp: error: key must be 64 hexadecimal characters.")
		raise SystemExit
	with open(".key", "rb") as file_key:
		key = file_key.read().decode(encoding = 'utf-8')
	with open("./ft_otp.key", "wb") as file:
		file.write(encrypt(hex_key, key))
		print("Key was successfully saved in ft_otp.key.")
	return(1)

##############################################################################################
def i_key():
	frame = tk.Tk() #obligatorio para crear ventana
	frame.title("OTP INTERACTIVE")
	frame.geometry('400x600+500+500') #resumem para colocar el frame

	def printInput(key_file):
		#data = inputtxt.get(1.0, "end") #"1.0" means the input should be read from line one. END is an imported constant which is set to the string "end". The END part means to read until the end. The -1c deletes 1 character.
		#lbl.config(text = "Provided Input: " + data) #devuelve lo escrito en la ventana
		filename = "qrcode.png"
		message_i_k = k_key(key_file)
		img = qrcode.make(message_i_k)
		img.save(filename)
		image_QR = tk.PhotoImage(file="qrcode.png")
		b = tk.Label(frame, image = image_QR, compound="left")
		b.after(10000, b.destroy)
		b.pack(side="top")

	def i_g_key(key_file):
		message_i_g = g_key(key_file)
		if message_i_g != None:
			lbl = tk.Label(frame, text = "Key was successfully saved in ft_otp.key.")
			lbl.after(3000, lbl.destroy)
			lbl.pack()

	def i_k_key(key_file):
		message_i_k = k_key(key_file)
		if message_i_k != 1:
			lbl = tk.Label(frame, text = message_i_k)
			lbl.pack()

	# Button Creation
	bottom_g = tk.Button(frame,
						text = "ft_otp -g key.hex",
						command = lambda: i_g_key("key.hex"))
	bottom_g.pack()
	bottom_k = tk.Button(frame,
						text = "ft_otp -k ft_otp.key",
						command = lambda: i_k_key("ft_otp.key"))
	bottom_k.pack()
	bottom_QR = tk.Button(frame,
							text = "Create a QR code",
							command = lambda: printInput("ft_otp.key"))
	bottom_QR.pack()
	bottom_close = tk.Button(frame,
							text = 'Close the window',
							command = frame.quit)
	bottom_close.pack()
	frame.mainloop() #obligatorio para mantener la ventana

##############################################################################################
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-g", help="The program will receive as an argument a hexadecimal key of at least 64 characters. The program will keep this key safely in a file called ft_otp.key, which will be encrypted at all times.")
	parser.add_argument("-k", help="The program will generate a new temporary password and display it to standard output.")
	parser.add_argument("-i", help="The program will be transformated an interactive program.", action="store_true")
	args = parser.parse_args()
	if args.g:
		file = args.g
		g_key(file)
	elif args.k:
		file = args.k
		k_key(file)
	elif args.i:
		i_key()
	else:
		print ("Please indicate what action you want when executing the program. Consult the help (-h or --help) if you want to know what options there are.")
if __name__ == "__main__":
	main()