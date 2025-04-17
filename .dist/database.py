import sqlite3
from werkzeug.security import generate_password_hash,check_password_hash

def conectar_banco():
    conexao = sqlite3.connect("personagens.db")
    return conexao

def criar_tabelas():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''create table if not exists usuarios
                   (email text primary key, nome text, senha text)''' )

    cursor.execute('''create table if not exists personagens (id integer primary key, nome text, genero integer,variacao integer, email_usuario text,
             FOREIGN KEY(email_usuario) REFERENCES usuarios(email))''')
    
    cursor.execute('''create table if not exists olhos (id integer primary key, cor integer, email_usuario text,
             FOREIGN KEY(email_usuario) REFERENCES usuarios(email))''')
    
    cursor.execute('''create table if not exists cabelos (id integer primary key, cor integer, email_usuario text,
             FOREIGN KEY(email_usuario) REFERENCES usuarios(email))''')
    conexao.commit()

def criar_usuario(formulario):
    # Verifica se ja existe esse email no banco de dados
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT count(email) from usuarios WHERE email=?''',(formulario['email'],))
    conexao.commit()

    quantidade_de_emails = cursor.fetchone()
    if(quantidade_de_emails[0] > 0):
        print("LOG: Já existe esse email cadastrado no banco!")
        return False
    
    senha_criptografada = generate_password_hash(formulario['senha'])
    cursor.execute('''INSERT INTO usuarios (email, nome, senha)
                        VALUES (?, ?, ?)''', (formulario['email'], formulario['nome'], senha_criptografada))
    conexao.commit()
    return True

def fazer_login(formulario):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT count(email) from usuarios WHERE email=?''',(formulario['email'],))
    conexao.commit()

    quantidade_de_emails = cursor.fetchone()
    if(quantidade_de_emails[0] < 0):
        print("LOG: email não encontrado.")
        return False
    else:
        try: 
            cursor = conexao.cursor()
            cursor.execute('''SELECT (senha) from usuarios WHERE email=?''',(formulario['email'],))
            conexao.commit()
            senha_criptografada = cursor.fetchone()
            resultado_verificacao = check_password_hash(senha_criptografada[0], formulario['senha'])
            return resultado_verificacao
        except:
            return False
        

def criar_personagem(nome,genero,variacao,email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(''' INSERT INTO personagens (nome, genero,variacao, email_usuario)
                   VALUES (?,?,?)''', 
                   (nome,genero,variacao, email))
    conexao.commit()
    return True

        
def buscar_personagens(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT id, nome, genero, variacao
                   FROM personagens WHERE email_usuario=?''', 
                   (email,))
    conexao.commit()
    personagens = cursor.fetchall() # Busca todos os resultados do select e guarda em "personagens"
    return personagens

def excluir_usuario(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM personagens WHERE email_usuario=?',(email,))
    cursor.execute('DELETE FROM usuarios WHERE email=?',(email,))
    conexao.commit()
    return True
    
if __name__ == '__main__':
    criar_tabelas()