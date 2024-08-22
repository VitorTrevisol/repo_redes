import socket
import threading
import time
from funcoes import *
import time

data = int(time.time())
PORT = 1234
FORMATO = 'utf-8'
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def recebe_mensagens():
    thread2 = threading.Thread(target=enviar_mensagem)
    volta = True
    anterior = ''
    global id
    while True:
        try:
            msg = client.recv(1024).decode(FORMATO)
            if msg.startswith("registro") and msg != anterior:
                mensagem = input('Digite seu nome e sobrenome: ')
                enviar("nome" + mensagem)
            elif msg.startswith('id') and volta:
                id = msg[2:]
                print(f"ID recebido: {id}")
                volta = False
                thread2.start()
            elif msg.startswith('recebeu'):
                id = msg[20:33]
                print(f"usuario {consultar_nome(int(id))[0][0]} recebeu")
            elif msg.startswith('05'):
                nome = consultar_nome(int(msg[2:15]))
                print(f'\n {nome[0][0]}: {msg[38:]}')
                enviar(f'recebeu{msg[2:]}')
            elif msg.startswith('12'):
                nome = consultar_nome(int(msg[15:28]))
                print(f'\n {nome[0][0]}: {msg[38:]}')

            elif msg != anterior:
                print(f"Mensagem recebida: {msg}")
            anterior = msg
        except ConnectionResetError:
            print("Conexão com o servidor foi fechada.")
            break

def enviar(mensagem):
    client.send(mensagem.encode(FORMATO))

def enviar_mensagem():
    inicio = True
    while True:
        if inicio:
            print('O que deseja?')
            print('1 - Enviar mensagem')
            print('2 - Ver mensagens pendentes')
            print('3 - Criar Grupo')
            print('3 - Ver Grupos')
            time.sleep(0.3)
            inicio = False
        mensagem = input("o que deseja?")
        if mensagem == '1':
            print('Contatos antigos')
            antigas = mensagensAntigas(id)
            print(antigas)
            for x in antigas:
                nome = consultar_nome(x[0])[0][0]
                print(f'----{nome}----')
                for y in x[1]:
                    print(y)
            envia = input('Enviar para quem? ')
            oque = input('Enviar o que? ')
            quem = consultar_pessoa(envia)
            if quem:
                enviar(f'05{id}{quem}{data}{oque}')
            else:
                enviar(f'05{id}{envia}{data}{oque}')
            time.sleep(0.2)
        elif mensagem == '2':
            enviar(f'12{id}')
            # enviar mensagens 05
            time.sleep(0.2)
        elif mensagem == '3':
            enviar(f'04{id}')
            # adicionar contato 10
            a = 0
        elif mensagem == '4':
            enviar(f'05{id}')
            # ler mensagens 03
            a = 0
        # para quem deseja enviar mensagem?

        # envie mensagem
        

def enviar_nome():
    registro = input('Deseja se registrar? (s/n): ')
    if registro.lower() == 's':
        mensagem = input('Digite seu nome e sobrenome: ')
        enviar("01" + mensagem)
    else:
        ja_esteve = input('Você já esteve aqui antes? (s/n): ')
        if ja_esteve.lower() == 's':
            nome = input("Digite seu Nome: ")
            enviar("03" + nome)
        else:
            print('Espero poder te atender em outro momento.')
            client.close()
            return

    # Começa a thread para enviar mensagens após o registro ou conexão
    
def iniciar():
    # Começa a thread para receber mensagens
    thread1 = threading.Thread(target=recebe_mensagens)
    thread1.start()
    # Executa a função de registro/conexão
    enviar_nome()

iniciar()
