import socket
import threading

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
            if msg.startswith("registro") and msg != anterior:
                mensagem = input('Digite seu nome e sobrenome: ')
                enviar("nome " + mensagem)
            elif msg.startswith('id') and volta:
                id = msg[2:]
                print(f"ID recebido: {id}")
                volta = False
                thread2.start()
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
            enviar('inicia')
            inicio = False
        mensagem = input("[1] Enviar mensagens \n[2] Adicionar Contato \n[3] Criar Grupo \nO que deseja?")
        if mensagem == '1':
            # enviar mensagens
            a = 0
        elif mensagem == '2':
            # ler mensagens
            a = 0
        elif mensagem == '3':
            #criar grupo
            a = 0
        # para quem deseja enviar mensagem?

        # envie mensagem
        

def enviar_nome():
    registro = input('Deseja se registrar? (s/n): ')
    if registro.lower() == 's':
        mensagem = input('Digite seu nome e sobrenome: ')
        enviar("nome" + mensagem)
    else:
        ja_esteve = input('Você já esteve aqui antes? (s/n): ')
        if ja_esteve.lower() == 's':
            nome = input("Digite seu Nome e Sobrenome: ")
            enviar("conecta" + nome)
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
