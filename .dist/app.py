from flask import Flask, render_template, request, session, redirect, url_for
import database
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__) # criando um objeto do flask chamado app
app.secret_key = "SENHA SECRETA"

@app.route('/')
def Pagina_inicial():
    return render_template('index.html')


@app.route('/home')
def home():
    if 'usuario' not in session:
        return redirect(url_for('login'))
    lista_personagens = database.buscar_personagens(session['usuario'])
    return render_template('home.html', personagens=lista_personagens)


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        form = request.form
        if database.fazer_login(form) == True:
            session['usuario'] = form['email'] # Armazena o email do usuário na sessão
            return redirect(url_for('home'))
        else:
            return render_template('login.html')
    else:
        return render_template('login.html')
    
    
@app.route('/cadastro', methods=["GET","POST"]) #rota para a página de login
def cadastro():
    if request.method == "POST":
        form = request.form
        if database.criar_usuario(form) == True:
            return render_template('login.html')
        else:
            return "Ocorreu um erro ao cadastrar o Usuário"
    else:
        return render_template('cadastro.html')
    
    
@app.route('/criar_personagem', methods=["GET","POST"]) #rota para a pagina de criação
def criar_personagem():
    if request.method == "POST":
        form = request.form
        if database.criar_personagem(form['nome'],form['variacao'], session['usuario']) == True:
            return redirect(url_for('home'))
        else:
            pass
    else:
        return render_template('criar.html')
    
    
@app.route('/personagens/editar/<int:id>', methods=["GET", "POST"])
def editar_personagem(id):
    # pega o e-mail da sessão para verificar se é o dono da tarefa
    email = session['usuario']
    if (request.method == "GET"):
        conteudo_personagem = database.buscar_conteudo_personagem(id)
        return render_template('editar.html', personagem=conteudo_personagem, id=id)
    if (request.method == "POST"):
        form = request.form
        novo_nome = form['nome']
        nova_variacao = form['variacao']
        database.editar_personagem(novo_nome,nova_variacao, id)
        return redirect(url_for('home'))
    
    
@app.route('/personagens/excluir/<int:id>', methods=["GET"])
def excluir_personagem(id):

    email = session['usuario']

    if database.excluir_personagem(id, email):
        return redirect(url_for('home'))
    else:
        return "Ocorreu um erro ao excluir a personagem!"


@app.route('/excluir_usuario')
def excluir_usuario():
    email = session['usuario']
    if database.excluir_usuario(email):
        return redirect(url_for('cadastro'))
    else:
        return "Ocorreu um erro ao excluir o usuário"
    
    
@app.route('/loggout')
def loggout():
    session.pop('usuario')
    return redirect(url_for('login'))
    
    
if __name__ == '__main__':
    app.run(debug=True)