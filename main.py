from flask import Flask, render_template, redirect, request, flash, send_from_directory
import os
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'JORGE'

logado = False

@app.route('/')
def home():
    global logado
    logado = False
    return render_template('login.html')

@app.route('/adm')
def adm():
    if logado == True:
        conn = sqlite3.connect('usuarios.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        conn.close()
        return render_template('administrador.html', usuarios=usuarios)
    if logado == False:
        return redirect('/')

@app.route('/usuarios')
def usuarios():
    if logado == True:
        arquivos = []
        for documento in (os.listdir('arquivos/')):
            arquivos.append(documento)
        return render_template("user.html", arquivos=arquivos)
    else:
        return redirect('/')

@app.route('/logado', methods=['POST'])
def login():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    email = request.form.get('email')

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios WHERE nome = ? AND senha = ? AND email = ?", (nome, senha, email))
    usuario = cursor.fetchone()

    conn.close()

    if usuario is not None:
        logado = True
        return redirect('/usuarios')
    elif nome == 'adm' and senha == '000' and email == 'adm@gmail.com':
        logado = True
        return redirect('/adm')
    else:
        flash('USUÁRIO OU SENHA INVÁLIDOS')
        return redirect('/')

@app.route('/cadastrarUsuario', methods=['POST'])
def cadastrarUsuario():
    global logado
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    email = request.form.get('email')

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome, senha, email) VALUES (?, ?, ?)", (nome, senha, email))
    conn.commit()
    conn.close()

    logado = True
    flash(f'"{nome}" FOI CADASTRADO(A)!!!')
    return redirect('/adm')

@app.route('/excluirUsuario', methods=['POST'])
def excluirUsuario():
    global logado
    logado = True
    usuario_id = request.form.get('usuario_id')

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    conn.commit()
    conn.close()

    flash(f'USUÁRIO FOI EXCLUÍDO COM SUCESSO')
    return redirect('/adm')

@app.route("/upload", methods=['POST'])
def upload():
    global logado
    logado = True

    arquivo = request.files.get('documento')
    nome_arquivo = arquivo.filename.replace(" ", "-")
    arquivo.save(os.path.join("arquivos/", nome_arquivo))

    flash('Arquivo Salvo')
    return redirect('/adm')

@app.route('/download', methods=['POST'])
def download():
    nome_arquivo = request.form.get('arquivosParaDownload')  # Corrigido para 'arquivosParaDownload'

    if nome_arquivo:
        return send_from_directory('arquivos/', nome_arquivo, as_attachment=True)
    else:
        return "Arquivo não encontrado"


@app.route('/cadastre_se', methods=['POST'])
def cadastre_se():
    return render_template('cadastro.html')

@app.route('/cadastro-1', methods=['POST'])
def cadastro_1():
    nome = request.form.get('nome')
    senha = request.form.get('senha')
    email = request.form.get('email')

    conn = sqlite3.connect('usuarios.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nome, senha, email) VALUES (?, ?, ?)", (nome, senha, email))
    conn.commit()
    conn.close()

    flash(f'USUÁRIO FOI CADASTRADO COM SUCESSO')
    return redirect('/')

@app.route('/signup', methods=['POST'])
def signup():
    if logado == logado:
        return render_template('cadastro.html')
    
if __name__ == "__main__":
    app.run(debug=True)
