from flask import Flask, render_template, request
import psycopg2
app = Flask(__name__)

def herokudb():
    Host='ec2-54-247-96-169.eu-west-1.compute.amazonaws.com'
    Database='d3a8gqg0padli2'
    User='jdyfyykhyozlly'
    Password='1d355ded77d6d943c0a5486518c564c97f3397b0e83239ae138ade8aa24ed7c4'
    return psycopg2.connect(host=Host, database=Database, user=User, password=Password, sslmode='require')

def gravar(v1, v2, v3):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("CREATE TABLE IF NOT EXISTS usr (nome text,email text, passe text)")
    db.execute("INSERT INTO usr VALUES (%s, %s, %s)", (v1, v2, v3))
    ficheiro.commit()
    ficheiro.close()


def existe(v1):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE nome = %s", (v1,))
    valor = db.fetchone()
    ficheiro.close()
    return valor


def log(v1, v2):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("SELECT * FROM usr WHERE nome = %s and passe = %s", (v1, v2,))
    valor = db.fetchone()
    ficheiro.close()
    return valor


@app.route('/registo', methods=['GET', 'POST'])
def route():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['email']
        v3 = request.form['passe']
        v4 = request.form['cpasse']
        if existe(v1):
            erro = 'O Utilizador já existe.'
        elif v3 != v4:
            erro = 'A palavra passe não coincide.'
        else:
            gravar(v1, v2, v3)
    return render_template('registo.html', erro=erro)


def alterar(v1, v2):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("UPDATE usr SET passe = %s WHERE nome = %s", (v2, v1))
    ficheiro.commit()
    ficheiro.close()


def apaga(v1):
    import sqlite3
    ficheiro = sqlite3.connect('db/Utilizadores.db')
    db = ficheiro.cursor()
    db.execute("DELETE FROM usr WHERE nome = %s", (v1,))
    ficheiro.commit()
    ficheiro.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif not log(v1, v2):
            erro = 'A palavra passe está errada.'
        else:
            erro = 'Bem-Vindo.'
    return render_template('login.html', erro=erro)


@app.route('/apagar', methods=['GET', 'POST'])
def apagar():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif not log(v1, v2):
            erro = 'A palavra passe está errada.'
        else:
            apaga(v1)
            erro = 'Conta Eliminada com Sucesso.'
    return render_template('apagar.html', erro=erro)


@app.route('/newpasse', methods=['GET', 'POST'])
def newpasse():
    erro = None
    if request.method == 'POST':
        v1 = request.form['utilizador']
        v2 = request.form['passe']
        v3 = request.form['cpasse']
        if not existe(v1):
            erro = 'O Utilizador não existe.'
        elif v2 != v3:
            erro = 'A palavra passe não coincide.'
        else:
            alterar(v1, v2)
    return render_template('newpasse.html', erro=erro)


if __name__ == '__main__':
    app.run(debug=True)
