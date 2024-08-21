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
    resultado = cursor.fetchall()
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
    resultado = cursor.fetchall()
    conexao.close()
    return resultado

def mensagensAntigas(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    print(id)
    cursor.execute('''
    SELECT idUm, idDois, mensagens FROM conexoes
    WHERE idUm = ? 
    ''', (id,))
    resultado = cursor.fetchall()
    conexao.close()
    mostra = []
    for x in enumerate(resultado):
        x_lista = list(x[1])
        x_lista[2] = x_lista[2].strip('[]').split(',')
        mostra.append(x_lista)
        return resultado

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

    cursor.execute('''
    SELECT grupos FROM clientes
    WHERE id = ? 
    ''', (id_cliente,))
    grupos = cursor.fetchall()
    print(grupos)
    if grupos[0] == None:
        grupos = []
        grupos.append(id_grupo)
        grupos = str(grupos)
        cursor.execute('''
        UPDATE clientes
        SET grupos = ?
        WHERE id = ?
        ''', (grupos, id_cliente))
    else:
        grupos = list(grupos[0].strip('[]').split(', '))
        for x, y in enumerate(grupos):
            grupos[x] = int(y)
        grupos.append((id_grupo))
        grupos = str(grupos)
        cursor.execute('''
        UPDATE clientes
        SET grupos = ?
        WHERE id = ?
        ''', (grupos, id_cliente))
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

