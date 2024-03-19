Instalamos brew en la terminal:
	rm -rf $HOME/.brew && git clone --depth=1 https://github.com/Homebrew/brew $HOME/.brew && echo 'export PATH=$HOME/.brew/bin:$PATH' >> $HOME/.zshrc && source $HOME/.zshrc && brew update

Instalamos openssl en la terminal:
	brew install openssl@3

Las librerías de openssl no las reconoce al compilar, para ello deberemos hacer lo siguiente al compilar:
		gcc -o corsair corsair.c -I/Users/vmachado/.brew/opt/openssl@3/include