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

def lista_usuarios():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("SELECT nome, sobrenome FROM clientes")
    usuarios = cursor.fetchall()
    conexao.close()
    return usuarios

def conecta(conexao):
    if mensagens:
        mensagem_de_envio = mensagens[0]
        conexao['conn'].send(mensagem_de_envio.encode(FORMATO))
        time.sleep(0.2)
        online.append(mensagem_de_envio[2:])
        mensagens.remove(mensagens[0])

def enviar_mensagem_individual(conexao, destinatario_id):
    for mensagem_de_envio in mensagens:
        if mensagem_de_envio.startswith(f"id{destinatario_id} "):
            conexao['conn'].send(mensagem_de_envio.encode(FORMATO))
            mensagens.remove(mensagem_de_envio)
            break

def handle_clientes(conn, addr):
    print(f"[NOVA CONEXAO] Um novo usuário se conectou pelo endereço {addr}")
    global conexoes
    global mensagens
    mapa_da_conexao = {
        "conn": conn,
        "addr": addr,
        "id": None
    }
    conexoes.append(mapa_da_conexao)
    while True:
        try:
            msg = conn.recv(1024).decode(FORMATO)
            if not msg:
                break
            print(f"Mensagem recebida do cliente: {msg}")  # Mensagem de depuração
            if msg.startswith("conecta"):
                nome_login = msg[7:].strip()
                nome, sobrenome = nome_login.split(' ')
                id_cliente = consultar_pessoa(nome, sobrenome)
                if id_cliente:
                    mapa_da_conexao['id'] = id_cliente
                    # Enviar mensagens pendentes para o usuário
                    for mensagem in mensagens:
                        if mensagem.startswith(f"id{id_cliente} "):
                            conn.send(mensagem.encode(FORMATO))
                            mensagens.remove(mensagem)
                conecta(mapa_da_conexao)
            elif msg.startswith("nome"):
                msg = msg[4:].strip()
                nome, sobrenome = msg.split(' ')
                id_cliente = adicionar_pessoa(nome, sobrenome)
                mapa_da_conexao['id'] = id_cliente
                mensagens.append(f"id{id_cliente}")
                conecta(mapa_da_conexao)
            elif msg.startswith("listar"):
                usuarios = lista_usuarios()
                resposta = "\n".join([f"{u[0]} {u[1]}" for u in usuarios])
                conn.send(resposta.encode(FORMATO))
            elif msg.startswith("limpar"):
                limpar_usuarios()
                conn.send("Todos os usuários foram removidos.".encode(FORMATO))
            elif msg.startswith("mensagem"):
                partes = msg.split(" ", 2)
                if len(partes) < 3:
                    conn.send("Formato de mensagem inválido.".encode(FORMATO))
                    continue
                try:
                    destinatario_nome, destinatario_sobrenome = partes[1].split()
                except ValueError:
                    conn.send("Formato de destinatário inválido.".encode(FORMATO))
                    continue
                mensagem = partes[2]
                destinatario_id = consultar_pessoa(destinatario_nome, destinatario_sobrenome)
                if destinatario_id:
                    mensagem_completa = f"id{destinatario_id} {mensagem}"
                    mensagens.append(mensagem_completa)
                    for c in conexoes:
                        if c['id'] == destinatario_id:
                            enviar_mensagem_individual(c, destinatario_id)
            elif msg.startswith("inicio"):
                espera = mensagemEspera(mapa_da_conexao['id'])
        except ConnectionResetError:
            break

    conexoes.remove(mapa_da_conexao)
    conn.close()

def start():
    print("[INICIANDO] Iniciando Socket")
    server.listen()
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_clientes, args=(conn, addr))
        thread.start()

start()
