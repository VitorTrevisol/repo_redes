import socket
import threading
import time
from funcoes import *

SERVER_IP = "127.0.0.1"
PORT = 1235
ADDR = (SERVER_IP, PORT)
FORMATO = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

conexoes = []
mensagens = []
online = []
lock = threading.Lock()

def conecta(conexao):
    with lock:
        if mensagens:
            mensagem_de_envio = mensagens.pop(0)
            conexao['conn'].send(mensagem_de_envio.encode())
            time.sleep(0.2)
            online.append(mensagem_de_envio[2:])

def enviar_mensagem_individual(conexao,msg):
    with lock:
        if msg[:2] == '01':
            conexao['conn'].send(msg.encode())
        elif msg[:2] == '02':
            conexao['conn'].send(msg.encode())
        elif msg[:2] == '03':
            conexao['conn'].send(msg.encode())
        elif msg[:2] == '05':
            conexao['conn'].send(msg.encode())
        elif msg[:2] == '06':
            conexao['conn'].send(msg.encode())
        elif msg[:2] == '07':
            conexao['conn'].send(msg.encode())
        elif msg[:2] == '12':
            conexao['conn'].send(msg.encode())
        elif msg.startswith('07'):
            conexao['conn'].send(msg.encode())
        elif msg.startswith('11'):
            conexao['conn'].send(msg.encode())
        print(msg)


def notificar_grupo(id_grupo, timestamp, membros_list):
    print(membros_list)
    notificacao = f'11{id_grupo}{timestamp}'
    print('chegou no notificar')
    for ind in membros_list:
        notificacao += str(ind)
        print(ind)
        if int(ind) or ind in online:
            for x, y in enumerate(online):
                if str(y) == ind:
                    enviar_mensagem_individual(conexoes[x], notificacao)
                    break
        else:
            adicionar_pendentes(notificacao)


def handle_clientes(conn, addr):
    print(f"[NOVA CONEXÃO] Um novo usuário se conectou pelo endereço {addr}")
    global conexoes, mensagens, online
    mapa_da_conexao = {
        "conn": conn,
        "addr": addr,
        "last": 0
    }
    with lock:
        conexoes.append(mapa_da_conexao)
    
    id_cliente = None

    while True:
        try:
            msg = conn.recv(1024).decode(FORMATO)
            if not msg:
                break
            if msg.startswith("01"):
                nome= msg[2:]
                if nome == '':
                    enviar_mensagem_individual(mapa_da_conexao, msg)
                else:
                    nome, sobrenome = msg.split(' ')
                    registro(msg, mapa_da_conexao, nome, sobrenome)
            elif msg.startswith("03"):
                id_cliente = msg[2:]
                online.append(id_cliente)
                print(id_cliente)
                msg= f'03{id_cliente}'
                if id_cliente:
                    enviar_mensagem_individual(mapa_da_conexao, msg)

            elif msg.startswith("05") and id_cliente:
                destinatario = msg[15:28]
                print(destinatario)
                print(online)
                if int(destinatario) in online:
                    print('entrou no if')
                    for x, y in enumerate(online):
                        print('entrou no for')
                        if str(y) == destinatario:
                            print(msg)
                            enviar_mensagem_individual(conexoes[x], msg)
                else:
                    adicionar_pendentes(msg)
                remetente= msg[2:15]
                for x, y in enumerate(online):
                    print('entrou no for')
                    if str(y) == remetente:
                        new_msg= '07'+msg[2:]
                        enviar_mensagem_individual(conexoes[x], new_msg)

            elif msg.startswith('06'):
                remetente = msg[15:28]
                print('começou 06')
                if int(remetente) or remetente in online:
                    print('ta online')
                    for x, y in enumerate(online):
                        print(f'x={x}\ny={y}\nonline={online}')
                        if str(y) == remetente:
                            print(conexoes[x])
                            enviar_mensagem_individual(conexoes[x], msg)

            elif msg.startswith("07"):
                remetente = msg[2:15]
                if int(remetente) in online:
                    for x, y in enumerate(online):
                        print(f'x={x}\ny={y}\nonline={online}')
                        if str(y) == remetente:
                            print(conexoes[x])
                            enviar_mensagem_individual(conexoes[x], msg)
            elif msg.startswith("10"):
                criador = msg[2:15]
                timestamp = msg[15:25]
                membros = [criador] + [msg[i:i+13] for i in range(25, len(msg), 13)]
                id_grupo= criar_grupo(criador, membros)
                notificar_grupo(id_grupo, timestamp, membros)

            elif msg.startswith("12"):
                destinatario = msg[2:15]
                resultado = consultar_pendentes(int(destinatario))
                for x, y in enumerate(online):
                    if destinatario == str(y):
                        print(f'{conexoes}')
                        print(resultado)
                        for mensagem in resultado:
                            print(f'conexoes em x: {x}')
                            enviar_mensagem_individual(conexoes[x], mensagem)
                            apagar_mensagem_do_banco(int(destinatario))
                            
            elif msg.startswith("4"):
                print(online)
                

        except ConnectionResetError:
            break

    with lock:
        conexoes.remove(mapa_da_conexao)
    conn.close()

def registro(msg, conexao, nome='', sobrenome=''):
    global id_cliente
    nome = nome[2:]
    id_cliente = str(adicionar_pessoa(nome, sobrenome))
    mensagens.append(f'id{id_cliente}')
    conecta(conexao)
    new_msg= f'02{id_cliente}'
    enviar_mensagem_individual(conexao, new_msg)


def start():
    print("[INICIANDO] Iniciando Socket")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clientes, args=(conn, addr))
        thread.start()



start()
