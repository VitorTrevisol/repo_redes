
import socket
import threading
import time
import sqlite3
import random

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
    print(resultado)
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

def mensagemEspera(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT * FROM mensagemEspera
    WHERE destinatario = ? 
    ''', (id,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado

def mensagensAntigas(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT * FROM conexoes
    WHERE idUm = ? 
    ''', (id,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado

def grupos(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT * FROM clientes
    WHERE id = ? 
    ''', (id,))
    idGrupos = cursor.fetchone()
    idGrupos = idGrupos[3].strip('[]').split(', ')
    listaGrupos = []
    for x in idGrupos:
        cursor.execute('''
        SELECT * FROM grupos
        WHERE id = ? 
        ''', (int(x),))
        resultado = cursor.fetchone()
        listaGrupos.append(resultado)
    conexao.close()
    return resultado

def limpar_usuarios():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM clientes")
    conexao.commit()
    conexao.close()
    print("Todos os usuários foram removidos.")