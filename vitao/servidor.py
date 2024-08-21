import socket
import threading
import time
import sqlite3
import random
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

def enviar_mensagem_individual(conexao, nome_amigo):
    with lock:
        for i in range(len(mensagens)):
            mensagem_de_envio = mensagens[i]
            if nome_amigo:
                mensagem_de_envio = f'{nome_amigo[i]} historico {mensagens[i]}'
            conexao['conn'].send(mensagem_de_envio.encode())
            time.sleep(0.2)
            if mensagem_de_envio.startswith('id'):
                online.append(mensagem_de_envio[2:])
            
        
        # Use uma cópia da lista ao remover itens
        mensagens[:] = [msg for i, msg in enumerate(mensagens) if i >= len(nome_amigo)]

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
            if msg.startswith("conecta"):
                nome_login = msg[7:]
                nome, sobrenome = nome_login.split(' ')
                id_cliente = consultar_pessoa(nome, sobrenome)
                if id_cliente:
                    mensagens.append(f'id{id_cliente}')
                conecta(mapa_da_conexao)
            elif msg.startswith("nome"):
                msg = msg[4:]
                nome, sobrenome = msg.split(' ')
                registro(mapa_da_conexao, nome, sobrenome)
            elif msg.startswith("1") and id_cliente:
                nome_amigo = []
                historico = mensagensAntigas(int(id_cliente[0]))
                for x in historico:
                    amigo = consultar_nome(x[1])
                    if amigo:
                        nome_amigo.append(amigo[0][0])
                        mensagens.append(x[2])
                enviar_mensagem_individual(mapa_da_conexao, nome_amigo)
                print(nome_amigo)
                print(online)
            elif msg.startswith("2"):
                print(online)
            elif msg.startswith("3"):
                print(online)
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
        mensagens.append(f'02{id_cliente}')
        conecta(conexao)

def start():
    print("[INICIANDO] Iniciando Socket")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clientes, args=(conn, addr))
        thread.start()

start()
