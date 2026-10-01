# Programar no Blue

O foco do Blue é desenvolvimento de software. A instalação de outras ferramentas e programas permanece permitida.

## Instalar programas

Use APT pelo terminal ou abra Synaptic pelo menu:

```sh
sudo apt update
sudo apt install nome-do-pacote
```

Substitua `nome-do-pacote` por um pacote disponível nos repositórios configurados. Com persistência, a instalação permanece após reiniciar. Em uma sessão Live sem persistência, ela é temporária.

## Python

Crie um ambiente virtual para as dependências de cada projeto:

```sh
mkdir meu-projeto
cd meu-projeto
python3 -m venv .venv
. .venv/bin/activate
python -m pip install requests
```

O Debian protege o Python do sistema contra instalações globais pelo pip. Use o ambiente virtual para manter as dependências do projeto separadas.

## JavaScript e Node.js

```sh
mkdir meu-projeto-js
cd meu-projeto-js
npm init -y
node -e 'console.log("Olá, Blue!")'
```

Instale bibliotecas pelo npm dentro da pasta do projeto. A versão de Node.js incluída é a fornecida pelo conjunto de pacotes Debian usado na compilação; consulte o manifesto da release para a versão exata.

## C e C++

Com um arquivo `main.c` salvo no editor:

```sh
gcc -Wall -Wextra main.c -o meu-programa
./meu-programa
```

Para C++, use `g++` e um arquivo `.cpp`. CMake e GDB também estão incluídos para projetos com construção automatizada e depuração.

## Git e editor

Geany pode ser aberto pelo menu ou pela barra inferior. Use Git normalmente dentro do projeto:

```sh
git init
git status
```

Configure seu nome e endereço de autoria antes de criar commits. Essa identidade pertence a cada usuário, não é definida pelo Blue.

## Conferir as ferramentas

```sh
blue-check-tools
```

O comando compila e executa exemplos e verifica 20 operações de desenvolvimento. Ele retorna falha se alguma verificação não passar. Os resultados da imagem publicada estão em [VALIDACAO.md](../VALIDACAO.md).
