import socket
import threading

PORT = 1235
FORMATO = 'utf-8'
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

# Lista para armazenar as mensagens recebidas
mensagens_recebidas = []

def enviar(mensagem):
    print(f"Enviando mensagem: {mensagem}")  # Mensagem de depuração
    client.send(mensagem.encode(FORMATO))

def enviar_mensagem():
    destinatario = input("Digite o nome e sobrenome do destinatário: ")
    while True:
        mensagem = input("Digite a mensagem para enviar ou 'sair' para finalizar: ")
        if mensagem.lower() == 'sair':
            print("Encerrando a conexão...")
            break
        enviar(f"mensagem {destinatario} {mensagem}")

def recebe_mensagens():
    while True:
        try:
            msg = client.recv(1024).decode(FORMATO)
            if msg:
                print(f"Mensagem recebida: {msg}")
                # Armazena a mensagem recebida na lista
                mensagens_recebidas.append(msg)
        except ConnectionAbortedError:
            print("Conexão com o servidor foi encerrada.")
            break

def listar_usuarios():
    enviar("listar")
    msg = client.recv(1024).decode(FORMATO)
    print(f"Usuários cadastrados:\n{msg}")

def limpar_usuarios():
    enviar("limpar")
    msg = client.recv(1024).decode(FORMATO)
    print(msg)

def ver_mensagens_recebidas():
    if mensagens_recebidas:
        print("Mensagens recebidas:")
        for mensagem in mensagens_recebidas:
            print(mensagem)
    else:
        print("Nenhuma mensagem recebida ainda.")

def menu():
    print("Bem-vindo ao Chat")
    print("1. Registrar-se")
    print("2. Conectar-se")
    print("3. Listar usuários")
    print("4. Limpar todos os usuários")
    print("5. Ver mensagens recebidas")
    print("6. Sair")

    opcao = input("Escolha uma opção: ")

    if opcao == '1':
        registrar()
    elif opcao == '2':
        conectar()
    elif opcao == '3':
        listar_usuarios()
    elif opcao == '4':
        limpar_usuarios()
    elif opcao == '5':
        ver_mensagens_recebidas()
    elif opcao == '6':
        print("Saindo...")
        client.close()
        return
    else:
        print("Opção inválida. Tente novamente.")
    
    menu()

def registrar():
    mensagem = input('Digite seu nome e sobrenome para registro: ')
    enviar("nome " + mensagem)
    iniciar_recebimento()

def conectar():
    nome = input("Digite seu Nome e Sobrenome para conectar: ")
    enviar("conecta " + nome)
    iniciar_recebimento()

def iniciar_recebimento():
    thread1 = threading.Thread(target=recebe_mensagens)
    thread1.start()
    enviar_mensagem()

def iniciar():
    while True:
        menu()

iniciar()
