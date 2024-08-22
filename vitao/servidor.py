import socket
import threading
import time
from funcoes import *

SERVER_IP = "127.0.0.1"
PORT = 1234
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
        if msg[:2] == '05':
            conexao['conn'].send(msg.encode())
        if msg[:2] == '12':
            conexao['conn'].send(msg.encode())
        elif mensagem_de_envio.startswith('id'):
            online.append(mensagem_de_envio[2:])
            mensagem_de_envio = mensagens[0]
            conexao['conn'].send(mensagem_de_envio.encode())
            time.sleep(0.2)
            
        
        # Use uma cópia da lista ao remover itens

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
            if msg.startswith("03"):
                nome_login = msg[2:]
                nome = nome_login
                id_cliente = consultar_pessoa(nome)
                online.append(id_cliente)
                id_cliente = 'id' + str(id_cliente)
                print(id_cliente)
                if id_cliente:
                    mapa_da_conexao['conn'].send(id_cliente.encode())
            elif msg.startswith("01"):
                nome, sobrenome = msg.split(' ')
                registro(mapa_da_conexao, nome, sobrenome)
            elif msg.startswith("05") and id_cliente:
                id2 = msg[15:28]
                if int(id2) in online:
                    for x, y in enumerate(online):
                        if str(y) == id2:
                            enviar_mensagem_individual(conexoes[x], msg)
                            print('foi')
                            break
                else:
                    adicionar_pendentes(msg)
                    print('salvo')
            elif msg.startswith("12"):
                id1 = msg[2:15]
                resultado = consultar_pendentes(int(id1))
                for x, y in enumerate(online):
                    if id1 == str(y):
                        for mensagem in resultado:
                            enviar_mensagem_individual(conexoes[x], mensagem)
            elif msg.startswith("4"):
                print(online)

        except ConnectionResetError:
            break

    with lock:
        conexoes.remove(mapa_da_conexao)
    conn.close()

def registro(conexao, nome='', sobrenome=''):
    global id_cliente
    if nome == '':
        mensagens.append('registro')
        enviar_mensagem_individual(conexao, [])
    else:
        id_cliente = str(adicionar_pessoa(nome, sobrenome))
        mensagens.append(f'id{id_cliente}')
        conecta(conexao)

def start():
    print("[INICIANDO] Iniciando Socket")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clientes, args=(conn, addr))
        thread.start()

start()
