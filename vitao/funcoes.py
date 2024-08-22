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

def mensagemEspera(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT * FROM mensagemEspera
    WHERE destinatario = ? 
    ''', (id,))
    resultado = cursor.fetchall()
    conexao.close()
    return resultado

def mensagensAntigas(id):
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
    id_destinatario = mensagem[2:15]
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    cursor.execute('''
    INSERT INTO mensagemEspera (destinatario, mensagens)
    VALUES (?, ?)
    ''', (id_destinatario, mensagem))
    
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


def consultar_pendentes(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT * FROM mensagemEspera
    WHERE destinatario = ? 
    ''', (id,))
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



