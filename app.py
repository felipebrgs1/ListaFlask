from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Conectar ao banco de dados SQLite


def get_db_connection():
    conn = sqlite3.connect('meu_banco.db')
    conn.row_factory = sqlite3.Row
    return conn

# Criar a tabela se ela não existir


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

# Página inicial (READ - Lista de usuários)


@app.route('/')
def index():
    conn = get_db_connection()
    usuarios = conn.execute('SELECT * FROM usuarios').fetchall()
    conn.close()
    return render_template('index.html', usuarios=usuarios)

# Criar um novo usuário (CREATE)


@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']

        if nome and idade:
            conn = get_db_connection()
            conn.execute('INSERT INTO usuarios (nome, idade) VALUES (?, ?)',
                         (nome, idade))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
    return render_template('add.html')

# Atualizar um usuário (UPDATE)


@app.route('/edit/<int:id>', methods=('GET', 'POST'))
def edit(id):
    conn = get_db_connection()
    usuario = conn.execute(
        'SELECT * FROM usuarios WHERE id = ?', (id,)).fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']

        if nome and idade:
            conn.execute('UPDATE usuarios SET nome = ?, idade = ? WHERE id = ?',
                         (nome, idade, id))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))

    return render_template('edit.html', usuario=usuario)

# Deletar um usuário (DELETE)


@app.route('/delete/<int:id>', methods=('POST',))
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))


if __name__ == '__main__':
    init_db()
    app.run(debug=True)
