import sqlite3


def get_db_connection():
    conn = sqlite3.connect('banco.db')
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            nome TEXT NOT NULL, 
            idade INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()


def criar(user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO usuarios (nome, idade) VALUES (?, ?)',
                   (user['nome'], user['idade']))
    conn.commit()  # Faz o commit da transação
    cursor.close()
    conn.close()   # Fecha a conexão corretamente


def listar():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    rows = cursor.fetchall()  # Obtém todas as linhas
    cursor.close()
    conn.close()
    for rows in rows:
        print(dict(rows))  # Fecha a conexão corretamente
    return


def deletar(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()  # Faz o commit da transação
    cursor.close()
    conn.close()   # Fecha a conexão corretamente
    return


def editar(id, user):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('UPDATE usuarios SET nome = ?, idade = ? WHERE id = ?',
                   (user['nome'], user['idade'], id))
    conn.commit()  # Faz o commit da transação
    cursor.close()


init_db()

listar()
