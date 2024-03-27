'''
CREATE SCHEMA IF NOT EXISTS ac;

USE ac;

CREATE TABLE IF NOT EXISTS tbl_cadastro
(
Nome VARCHAR(20) NOT NULL
, Telefone VARCHAR(30) NOT NULL
, Endereco VARCHAR(50)
,CONSTRAINT nome_pk PRIMARY KEY(Nome)
);

SELECT * FROM tbl_cadastro;

'''
import os
from flask import Flask, render_template, json, request, jsonify
from flaskext.mysql import MySQL
#from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Impacta2024'
app.config['MYSQL_DATABASE_DB'] = 'ac'
app.config['MYSQL_DATABASE_HOST'] = 'db'
#app.config['MYSQL_DATABASE_HOST'] = '172.17.0.7'
mysql.init_app(app)

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/cadastrar')
def cadastrar_tutores():
    return render_template('form.html')


@app.route('/cadastro',methods=['POST','GET'])
def cadastro_tutores():
    try:
        nome_cadastro = request.form['inputNome']
        telefone_cadastro = request.form['inputTelefone']
        endereco_cadastro = request.form['inputEndereco']
    

        print(nome_cadastro)
        print(telefone_cadastro)
        print(endereco_cadastro)

        
        cur = mysql.connection.cursor()
        cur.execute("SELECT Nome FROM tbl_tutor WHERE Nome = %s", (nome_cadastro,))
        #EXIJO ESPLICACOES DO PQ PRECISA DE UMA VIRGULA NO FINAL DESSA MERDA
        resultado = cur.fetchone()
        print(resultado)
            
        if resultado:
            msg = "Nome ja cadastrado no banco de dados"
            return render_template('form.html', mensagem = msg)
        else:
            conn = mysql.connection()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO tbl_cadastro (Nome,Telefone,Endereco) VALUES (%s, %s, %s)", ( nome_cadastro,telefone_cadastro,endereco_cadastro ))
            #Alt  + Z para quebra linhas grandes
            conn.commit()
            msg = "Cadastrado com sucesso"

            return render_template('form.html', mensagem = msg)
        
    except Exception as e:
        return json.dumps({'error': str(e)})
    
@app.route('/lista',methods=['GET']) 
def listar():
    try:
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM tbl_cadastro')
        lista = cursor.fetchall()
        print(lista[0])

        return render_template('lista.html', Lista = lista)

    except Exception as e:
        return json.dumps({'error': str(e)})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port) 