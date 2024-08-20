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

def conectar_banco():
    return sqlite3.connect('banco.db')

def consultar_pessoa(nome_consulta, sobrenome_consulta):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT id FROM clientes 
    WHERE nome = ? AND sobrenome = ?
    ''', (nome_consulta, sobrenome_consulta))

    resultado = cursor.fetchone()
    conexao.close()
    if resultado:
        return resultado[0]
    return None

def adicionar_pessoa(nome, sobrenome):
    id_cliente = random.randint(10**12, 10**13 - 1)
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
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
        time.sleep(0.2)
        mensagens.remove(mensagens[i])

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
    conexoes.append(mapa_da_conexao)
    
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
                else:
                    mensagens.append("pessoa não encontrada")
                enviar_mensagem_individual(mapa_da_conexao)
            elif msg.startswith("nome"):
                msg = msg[4:]
                nome, sobrenome = msg.split(' ')
                registro(mapa_da_conexao, nome, sobrenome)
        except ConnectionResetError:
            break

    conexoes.remove(mapa_da_conexao)
    conn.close()

def registro(conexao, nome='', sobrenome=''):
    if nome == '':
        mensagens.append('registro')
        enviar_mensagem_individual(conexao)
    else:
        id_cliente = str(adicionar_pessoa(nome, sobrenome))
        mensagens.append(f'id{id_cliente}')
        enviar_mensagem_individual(conexao)

def start():
    print("[INICIANDO] Iniciando Socket")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clientes, args=(conn, addr))
        thread.start()

start()