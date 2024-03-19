STOCKHOLM

DEFINITION:

	File encryptor and decryptor in Linux with Python. Using the same file extensions than Wannacry.
	The key with which they are encrypted must have at least 16 characters.
	The key with which it is decrypted has to be the same as the one used to encrypt.

USAGE:

	Encrypt files:			python3 stockholm.py
	Encrypt files silent:	python3 stockholm.py -s
	Decrypt files:			python3 stockholm.py -r
	
	optional arguments:		-h, --help     show this help message and exit
  							-v, --version  show version information
  							-s, --silent   silent mode
  							-r, --reverse  decrypt the files

REQUIREMENTS:

	Install Docker on your computer and create an account

	Create a Docker container with a Debian image, set the path where the folder you want to share with the Docker container is located, and the path where to put the access inside Debian, in this case /home:

		docker run -it -v [Path_your_computer]:[Path_debian] image

		example: docker run -it -v /System/Volumes/Data/sgoinfre/goinfre/Perso/ruramire/Ciberseguridad/Proyectos/05-1_stockholm:/home debian

	Debian:		apt update && apt upgrade		<- update apt in the Debian terminal
				apt install python3				<- install python3 in the Debian terminal
				apt install python3-pip			<- install pip to install and manage python packages
				pip install -U PyCryptodome		<- install package for cryptography for stockholm.py
												   PyCryptodome is a fork of PyCrypto that brings improvements on top of the PyCrypto library
