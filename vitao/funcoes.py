import sqlite3
import random
from datetime import datetime

def conectar_banco():
    return sqlite3.connect('banco.db')

def consultar_pessoa(nome_consulta):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT id FROM clientes 
    WHERE nome = ?
    ''', (nome_consulta,))
    resultado = cursor.fetchall()
    conexao.close()
    if resultado:
        return resultado[0][0]
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

def mensagens_antigas(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    print(id)
    cursor.execute('''
    SELECT idDois, mensagens FROM conexoes
    WHERE idUm = ? 
    ''', (id,))
    resultado = cursor.fetchall()
    conexao.close()
    mostra = []
    for x in enumerate(resultado):
        x_lista = list(x[1])
        x_lista[1] = x_lista[1].strip('[]').split(',')
        mostra.append(x_lista)
    return mostra

def apagar_mensagem_do_banco(destinatario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute('''
    DELETE FROM mensagemEspera
    WHERE destinatario = ? 
    ''', (destinatario,))
    
    conexao.commit()
    conexao.close()
    print('passou aqui')


def grupos(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT * FROM clientes
    WHERE id = ? 
    ''', (id,))
    idGrupos = cursor.fetchall()
    idGrupos = idGrupos[3].strip('[]').split(', ')
    listaGrupos = []
    for x in idGrupos:
        cursor.execute('''
        SELECT * FROM grupos
        WHERE id = ? 
        ''', (int(x),))
        resultado = cursor.fetchall()
        listaGrupos.append(resultado)
    conexao.close()
    return resultado

def atualizar_clienteGrupos(id_cliente, id_grupo):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Recupera os grupos existentes do cliente
    cursor.execute('''
    SELECT grupos FROM clientes
    WHERE id = ? 
    ''', (id_cliente,))
    resultado = cursor.fetchone()

    if resultado and resultado[0]:
        grupos = resultado[0].strip('[]').split(', ')
    else:
        grupos = []

    # Adiciona o novo grupo à lista de grupos do cliente
    grupos.append(str(id_grupo))
    grupos_str = '[' + ', '.join(grupos) + ']'

    # Atualiza o banco de dados com a nova lista de grupos
    cursor.execute('''
    UPDATE clientes
    SET grupos = ?
    WHERE id = ?
    ''', (grupos_str, id_cliente))

    conexao.commit()
    conexao.close()


def adicionar_pendentes(mensagem):
    id_remetente = mensagem[2:15]
    id_destinatario = mensagem [15:28]
    mensagem_pendente = mensagem[38:]
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute('''
    INSERT INTO mensagemEspera (destinatario, remetente, mensagens)
    VALUES (?, ?, ?)
    ''', (id_destinatario, id_remetente, mensagem_pendente))
    
    conexao.commit()
    conexao.close()

def consultar_nome(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT nome FROM clientes
    WHERE id = ? 
    ''', (id,))
    resultado = cursor.fetchall()
    conexao.close()
    return resultado


def consultar_pendentes(destinatario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT * FROM mensagemEspera
    WHERE destinatario = ? 
    ''', (destinatario,))
    resultado = cursor.fetchall()
    resultado = ['12' + str(i[0]) + str(i[1]) + i[2] for i in resultado]
    conexao.close()
    return resultado

def ver_grupos(id_cliente):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Recupera os grupos associados ao cliente
    cursor.execute('''
    SELECT grupos FROM clientes 
    WHERE id = ?
    ''', (id_cliente,))
    resultado = cursor.fetchone()

    conexao.close()

    if resultado and resultado[0]:
        grupos = resultado[0].strip('[]').split(', ')
        return grupos
    else:
        return []
    
def atualizar_clienteGrupos(id_cliente, id_grupo):
    conexao = conectar_banco()
    cursor = conexao.cursor()

    # Recupera os grupos existentes do cliente
    cursor.execute('''
    SELECT grupos FROM clientes
    WHERE id = ? 
    ''', (id_cliente,))
    resultado = cursor.fetchone()
    
    if resultado:
        grupos = resultado[0]
        if grupos:
            grupos = grupos.strip('[]').split(', ')
        else:
            grupos = []
        grupos.append(str(id_grupo))
        grupos = str(grupos)
        
        cursor.execute('''
        UPDATE clientes
        SET grupos = ?
        WHERE id = ?
        ''', (grupos, id_cliente))
    else:
        # Se o cliente não tem nenhum grupo, cria uma nova entrada
        cursor.execute('''
        UPDATE clientes
        SET grupos = ?
        WHERE id = ?
        ''', (str([id_grupo]), id_cliente))

    conexao.commit()
    conexao.close()

