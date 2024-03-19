OTP

DEFINITION:

	The ft_otp program allows you to register an initial key, and is capable of generating a new password every x seconds.

	•With the -g option, the program must receive as an argument a hexadecimal key of at least 64 characters. The program safely stores this key in a file called ft_otp.key, which will be encrypted at all times.

	•With the -k option, the program generates a new temporary password and prints it to standard output

USAGE:

	$ ./ft_otp -g key.hex
	Key was successfully saved in ft_otp.key.
	$ ./ft_otp -k ft_otp.key
	836492
	$ sleep 60
	$ ./ft_otp -k ft_otp.key
	123518
	$ oathtool --totp $(cat key.hex)			<- With this command it is verified that the authenticate is correct, if it gives the same value
	123518

REQUIREMENTS:

	docker run -it -v /System/Volumes/Data/sgoinfre/goinfre/Perso/ruramire/Ciberseguridad/Proyectos/04_ft_otp:/home debian

	apt -y update && apt -y upgrade && apt install python3 && apt install -y python3-pip && pip install pycryptodome && apt install -y oathtool && pip install tk

	MAC:
	pip3 install pycryptodome
	brew install oath-toolkit
	pip3 install tk
	pip3 install qrcode"[pil]"
