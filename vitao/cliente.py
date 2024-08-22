import socket
import threading
import time
from funcoes import *

data = int(time.time())
PORT = 1235
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
            if not msg:
                break

            if msg.startswith("registro") and msg != anterior:
                mensagem = input('Digite seu nome e sobrenome: ')
                enviar("nome" + mensagem)

            elif msg.startswith('id') and volta:
                id = msg[2:]
                print(f"ID recebido: {id}")
                volta = False
                thread2.start()

            elif msg.startswith('recebeu'):
                id2 = msg[20:33]
                print(f"Usuário {consultar_nome(int(id2))[0][0]} recebeu")

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
        except Exception as e:
            print(f"Ocorreu um erro: {e}")
            break

def enviar(mensagem):
    try:
        client.send(mensagem.encode(FORMATO))
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

def enviar_mensagem():
    inicio = True
    while True:
        if inicio:
            print('O que deseja?')
            print('1 - Enviar mensagem')
            print('2 - Ver mensagens pendentes')
            print('3 - Criar Grupo')
            print('4 - Ver Grupos')
            time.sleep(0.3)
            inicio = False
        
        mensagem = input("O que deseja? ")
        if mensagem == '1':
            print('Contatos antigos')
            antigas = mensagensAntigas(id)
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
            time.sleep(0.2)

        elif mensagem == '3':
            membros = []
            for i in range(7):
                membro = input(f'ID do membro {i+1} (ou deixe vazio para terminar): ')
                if membro:
                    membros.append(membro.zfill(13))
                else:
                    break
            enviar(f'10{id}{data}{"".join(membros)}')

        elif mensagem == '4':
            grupos = ver_grupos(id)
            if grupos:
                print('Você está nos seguintes grupos:')
                for grupo in grupos:
                    print(f'Grupo ID: {grupo}')
            else:
                print('Você não está em nenhum grupo.')

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
