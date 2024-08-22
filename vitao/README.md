Descrição do Projeto - Aplicação - "WhatsApp"

Implementar uma versão simplificada de um aplicativo de comunicação por mensagens similiar ao Whatsapp, seguindo um modelo cliente-servidor e utilizando o protocolo TCP para troca das mensagens. Além disso, deve suportar as seguintes funções: registrar cliente, conectar cliente, enviar mensagem, confirmação de entrega de mensagem para o servidor, confirmação de entrega de mensagem para o cliente, confirmação de leitura da mensagem pelo cliente e criar grupo. 

Conteúdo:

1. Arquitetura

|
|- servidor.py
|- funcoes.py
|- cliente.py
|- banco.db
|
|-README.md

2. Funcionalidades:

- Login
- Registro do cliente
- Envio de mensagem instantânea
- Envio de mensagem pendente
- Confirmação de recebimento
- Consulta grupo
- Salva mensagens no banco de dados

3. Bibliotecas e uso:

- Socket
- Time
- SQLite

4. Descrição dos códigos: 

- Arquivo servidor.py: Este código implementa o lado do servidor de um sistema de comunicação baseado em sockets. O servidor aceita conexões de clientes, gerencia as mensagens e mantém informações sobre os clientes conectados.

Variáveis:
SERVER_IP: Endereço IP do servidor.
PORT: Porta na qual o servidor vai escutar as conexões.
ADDR: Tupla combinando IP e Porta.
FORMATO: Formato de codificação das mensagens (UTF-8).

Funções:
conecta(conexao): Envia mensagens pendentes para a conexão especificada e adiciona o cliente à lista de usuários online.
enviar_mensagem_individual(conexao, nome_amigo): Envia mensagens individualmente para o cliente, com suporte para enviar histórico de mensagens.
handle_clientes(conn, addr): Gerencia as conexões dos clientes, recebendo e tratando mensagens. Esta função é executada em uma thread separada para cada cliente conectado.
registro(conexao, nome='', sobrenome=''): Registra um novo cliente no banco de dados e inicia a conexão com o servidor.
start(): Inicia o servidor e escuta por novas conexões. Cada nova conexão é tratada em uma nova thread.

Fluxo Principal:
O servidor é iniciado com a função start(), que escuta conexões de clientes. Quando um cliente se conecta, uma nova thread é criada para lidar com a comunicação desse cliente através da função handle_clientes. A comunicação entre o servidor e o cliente envolve registro de clientes, envio de mensagens e gerenciamento do histórico de mensagens.


- Arquivo cliente.py: Este código implementa o lado do cliente de um sistema de comunicação baseado em sockets. O cliente se conecta ao servidor, envia e recebe mensagens e lida com registros de usuário.

Constantes:
PORT: Porta na qual o cliente se conecta.
FORMATO: Formato de codificação das mensagens (UTF-8).
SERVER: Endereço IP do servidor.
ADDR: Tupla combinando IP e Porta.

Funções:
recebe_mensagens(): Escuta e processa as mensagens recebidas do servidor. Pode iniciar o processo de registro do usuário ou outras interações conforme a mensagem recebida.
enviar(mensagem): Envia uma mensagem para o servidor.
enviar_mensagem(): Captura a entrada do usuário para enviar diferentes tipos de mensagens ao servidor.
enviar_nome(): Gerencia o processo de registro ou reconexão do usuário ao sistema.
iniciar(): Inicia a thread para receber mensagens e executa a função de registro ou reconexão.

Fluxo Principal:
O cliente é iniciado com a função iniciar(), que primeiro gerencia o registro ou reconexão do usuário e, em seguida, inicia a escuta por mensagens do servidor em uma thread separada. O cliente pode enviar diferentes tipos de mensagens ao servidor com base na entrada do usuário.

- Arquivo funcoes.py: Este código contém funções auxiliares que realizam operações no banco de dados SQLite, como consultar, adicionar e atualizar registros de clientes, bem como recuperar mensagens.

Funções:
conectar_banco(): Conecta-se ao banco de dados SQLite banco.db.
consultar_pessoa(nome_consulta, sobrenome_consulta): Retorna o ID do cliente com o nome e sobrenome fornecidos.
adicionar_pessoa(nome, sobrenome): Adiciona um novo cliente ao banco de dados e retorna o ID gerado.
mensagemEspera(id): Retorna as mensagens na fila de espera para um determinado ID de cliente.
mensagensAntigas(id): Retorna mensagens antigas do cliente especificado.
grupos(id): Retorna os grupos associados a um determinado cliente.
atualizar_clienteGrupos(id_cliente, id_grupo): Atualiza a lista de grupos de um cliente no banco de dados.
consultar_nome(id): Retorna o nome do cliente com o ID fornecido.

Fluxo Principal
Estas funções são usadas pelo servidor (servidor.py) para realizar operações no banco de dados relacionadas ao gerenciamento de clientes e mensagens. Por exemplo, o servidor usa essas funções para consultar o ID de um cliente ao se conectar, adicionar novos clientes ao banco de dados e recuperar mensagens pendentes para um cliente.