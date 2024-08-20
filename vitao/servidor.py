import socket
import threading
import time
import sqlite3
import random

SERVER_IP = "127.0.0.1"
PORT = 1235
ADDR = (SERVER_IP, PORT)
FORMATO = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

conexoes = []
mensagens = []

def adicionar_pessoa(nome, sobrenome):
    # Gerar um ID aleatório de 13 dígitos
    id_cliente = random.randint(10**12, 10**13 - 1)
    
    # Conectar ao banco de dados
    conexao = sqlite3.connect('banco.db')
    cursor = conexao.cursor()
    
    # Inserir os dados na tabela clientes
    cursor.execute('''
    INSERT INTO clientes (id, nome, sobrenome)
    VALUES (?, ?, ?)
    ''', (id_cliente, nome, sobrenome))
    
    conexao.commit()
    conexao.close()

    return id_cliente

def enviar_mensagem_individual(conexao):
    print(f"[ENVIANDO] Enviando mensagens para {conexao['addr']}")
    for i in range(conexao['last'], len(mensagens)):
        mensagem_de_envio = mensagens[i]
        conexao['conn'].send(mensagem_de_envio.encode())
        conexao['last'] = i + 1
        time.sleep(0.2)

def enviar_mensagem_todos():
    global conexoes
    for conexao in conexoes:
        enviar_mensagem_individual(conexao)

def handle_clientes(conn, addr):
    print(f"[NOVA CONEXAO] Um novo usuario se conectou pelo endereço {addr}")
    global conexoes
    global mensagens
    mapa_da_conexao = {
        "conn": conn,
        "addr": addr,
        "last": 0
    }

    while True:
        msg = conn.recv(1024).decode(FORMATO)
        if msg:
            if msg.startswith("conecta"):
                id_cliente = msg[8:]
                # Buscar o cliente no banco de dados usando o ID (não implementado no exemplo)
                # Carregar informações necessárias
            elif msg.startswith("registro"):
                mensagens.append("registro")
                enviar_mensagem_individual(mapa_da_conexao)
            elif msg.startswith("nome"):
                msg = msg[4:]
                nome, sobrenome = msg.split(' ')
                registro(mapa_da_conexao, nome, sobrenome)

def registro(conexao, nome='', sobrenome=''):
    if nome == '':
        mensagens.append('registro')
        enviar_mensagem_individual(conexao)
    else:
        id_cliente = str(adicionar_pessoa(nome, sobrenome))
        mensagens.append(id_cliente)
        enviar_mensagem_individual(conexao)

def start():
    print("[INICIANDO] Iniciando Socket")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clientes, args=(conn, addr))
        thread.start()

start()
