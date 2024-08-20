import socket
import threading

PORT = 1235
FORMATO = 'utf-8'
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def recebe_mensagens():
    global teste
    while True:
        msg = client.recv(1024).decode(FORMATO)
        if msg.startswith("registro"):
            mensagem = input('Digite seu nome e sobrenome: ')
            enviar("nome" + mensagem)
            teste = True
        else:
            print(msg)

def enviar(mensagem):
    client.send(mensagem.encode(FORMATO))

def enviar_mensagem():
    while True:
        mensagem = input()
        print('-----')
        enviar("msg " + mensagem)

def enviar_nome():
    registro = input('Deseja se registrar? (s/n): ')
    if registro.lower() == 's':
        enviar("registro")
    else:
        teste = input('Você já esteve aqui antes? (s/n): ')
        if teste.lower() == 's':
            nome = input("Qual é o seu nome? ")
            enviar("conecta " + nome)
        else:
            print('Espero poder te atender em outro momento.')
            client.close()

def teste(teste):
    return teste

def iniciar():
    thread1 = threading.Thread(target=recebe_mensagens)
    thread2 = threading.Thread(target=enviar_mensagem)
    thread1.start()
    enviar_nome()
    if teste:
        thread2.start()

teste = False
iniciar()
