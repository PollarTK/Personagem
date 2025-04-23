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

    cursor.execute('''create table if not exists personagens (id integer primary key, nome text, variacao integer, email_usuario text,
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
        

def criar_personagem(nome,variacao,email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute(''' INSERT INTO personagens (nome,variacao, email_usuario)
                   VALUES (?,?,?)''', 
                   (nome,variacao, email))
    conexao.commit()
    return True


def editar_personagem(novo_nome,nova_variacao, id):
    # Conecta com o banco
    conexao = conectar_banco()
    cursor = conexao.cursor()
    #Executa o comando
    cursor.execute('''UPDATE personagens SET nome=?, variacao=? WHERE id=?''', (novo_nome,nova_variacao, id))
    conexao.commit()
    return True

        
def buscar_personagens(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT id, nome, variacao
                   FROM personagens WHERE email_usuario=?''', 
                   (email,))
    conexao.commit()
    personagens = cursor.fetchall() # Busca todos os resultados do select e guarda em "personagens"
    return personagens


def buscar_conteudo_personagem(id):
    # Conecta com o banco
    conexao = conectar_banco()
    cursor = conexao.cursor()
    #Executa a query do conteúdo
    cursor.execute('''SELECT nome,variacao FROM personagens WHERE id=?''', (id,))
    conexao.commit()
    conteudo = cursor.fetchone()
    #Retorna o conteudo
    return(conteudo)


def excluir_personagem(id, email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('''SELECT email_usuario FROM personagens WHERE id=?''', (id,))
    conexao.commit()
    email_banco = cursor.fetchone()
    print(email, email_banco)
    if (email_banco[0] !=email):
        
        return False
    else:
        cursor.execute(''' DELETE FROM personagens WHERE id=?''', (id,))
        conexao.commit()
        cursor.close()
        return True


def excluir_usuario(email):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM personagens WHERE email_usuario=?',(email,))
    cursor.execute('DELETE FROM usuarios WHERE email=?',(email,))
    conexao.commit()
    return True
    
if __name__ == '__main__':
    criar_tabelas()