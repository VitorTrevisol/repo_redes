import sqlite3

def conectar_banco():
    return sqlite3.connect('banco.db')

def adicionar_cliente(id, nome, sobrenome, grupos):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    INSERT INTO clientes (id, nome, sobrenome, grupos)
    VALUES (?, ?, ?, ?)
    ''', (id, nome, sobrenome, grupos))
    conexao.commit()
    conexao.close()

def remover_cliente(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    DELETE FROM clientes WHERE id = ?
    ''', (id,))
    conexao.commit()
    conexao.close()

def consultar_cliente(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT * FROM clientes WHERE id = ?
    ''', (id,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado

def adicionar_conexao(id, idUm, idDois, mensagens):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    INSERT INTO conexoes (id, idUm, idDois, mensagens)
    VALUES (?, ?, ?, ?)
    ''', (id, idUm, idDois, mensagens))
    conexao.commit()
    conexao.close()

def remover_conexao(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    DELETE FROM conexoes WHERE id = ?
    ''', (id,))
    conexao.commit()
    conexao.close()

def consultar_conexao(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT * FROM conexoes WHERE id = ?
    ''', (id,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado

def adicionar_grupo(id, nome, mensagens):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    INSERT INTO grupos (id, nome, mensagens)
    VALUES (?, ?, ?)
    ''', (id, nome, mensagens))
    conexao.commit()
    conexao.close()

def remover_grupo(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    DELETE FROM grupos WHERE id = ?
    ''', (id,))
    conexao.commit()
    conexao.close()

def consultar_grupo(id):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT * FROM grupos WHERE id = ?
    ''', (id,))
    resultado = cursor.fetchone()
    conexao.close()
    return resultado

def adicionar_mensagem_espera(destinatario, remetente, mensagens):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    INSERT INTO mensagemEspera (destinatario, remetente, mensagens)
    VALUES (?, ?, ?)
    ''', (destinatario, remetente, mensagens))
    conexao.commit()
    conexao.close()

def remover_mensagem_espera(destinatario, remetente):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    DELETE FROM mensagemEspera WHERE destinatario = ? AND remetente = ?
    ''', (destinatario, remetente))
    conexao.commit()
    conexao.close()

def consultar_mensagem_espera(destinatario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''
    SELECT * FROM mensagemEspera WHERE destinatario = ?
    ''', (destinatario,))
    resultado = cursor.fetchall()
    conexao.close()
    return resultado
