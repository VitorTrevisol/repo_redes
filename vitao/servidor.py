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
        elif msg[:2] == '12':
            conexao['conn'].send(msg.encode())
        elif msg.startswith('recebeu'):
            conexao['conn'].send(msg.encode())
        print(msg)

            
        
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
                destinatario = msg[15:28]
                if int(destinatario) in online:
                    for x, y in enumerate(online):
                        if str(y) == destinatario:
                            enviar_mensagem_individual(conexoes[x], msg)
                            break
                else:
                    adicionar_pendentes(msg)
            elif msg.startswith("10"):
                criar_grupo(msg)  # Adiciona a chamada para criar o grupo
            elif msg.startswith("12"):
                destinatario = msg[2:15]
                resultado = consultar_pendentes(int(destinatario))
                for x, y in enumerate(online):
                    if destinatario == str(y):
                        for mensagem in resultado:
                            enviar_mensagem_individual(conexoes[x], mensagem)
                            apagar_mensagem_do_banco(int(destinatario))
                            
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
        nome = nome[2:]
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

def criar_grupo(mensagem):
    criador = mensagem[2:15]
    timestamp = mensagem[15:25]
    membros = [criador] + [mensagem[i:i+13] for i in range(25, len(mensagem), 13)]

    # Gerar um ID único para o grupo
    id_grupo = random.randint(10**12, 10**13 - 1)
    
    # Atualizar os membros no banco de dados
    for membro in membros:
        atualizar_clienteGrupos(membro, id_grupo)

    # Notificar os membros sobre a criação do grupo
    notificar_grupo(id_grupo, timestamp, membros)
    
def notificar_grupo(id_grupo, timestamp, membros):
    mensagem_notificacao = f'11{id_grupo}{timestamp}' + ''.join(membros)
    for membro in membros:
        if int(membro) in online:
            for x, y in enumerate(online):
                if str(y) == membro:
                    enviar_mensagem_individual(conexoes[x], mensagem_notificacao)
                    break


start()