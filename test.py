# Importação dos módulos
from flask import Flask, request, jsonify
import sqlite3

# Inicializa o banco de dados
def init_db():
    conn = sqlite3.connect('banco.db')
    return conn

# Interface Cliente
class Cliente:
    def __init__(self, saldo):
        self.saldo = saldo

    def sacar_dinheiro(self, valor):
        pass

    def realizar_extrato(self):
        return self.saldo

# Modelos
class PessoaFisica(Cliente):
    def __init__(self, id, nome, renda_mensal, saldo):
        super().__init__(saldo)
        self.id = id
        self.nome = nome
        self.renda_mensal = renda_mensal

    def sacar_dinheiro(self, valor):
        if valor > 1000:
            raise ValueError("Limite de saque excedido para Pessoa Física")
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente")
        self.saldo -= valor

class PessoaJuridica(Cliente):
    def __init__(self, id, nome, faturamento, saldo):
        super().__init__(saldo)
        self.id = id
        self.nome = nome
        self.faturamento = faturamento

    def sacar_dinheiro(self, valor):
        if valor > 5000:
            raise ValueError("Limite de saque excedido para Pessoa Jurídica")
        if valor > self.saldo:
            raise ValueError("Saldo insuficiente")
        self.saldo -= valor

# Inicializa o servidor Flask
app = Flask(__name__)

# Rota para criar usuários
@app.route('/clientes', methods=['POST'])
def criar_cliente():
    data = request.json
    tipo = data.get("tipo")
    nome = data.get("nome")
    saldo = data.get("saldo")
    renda_mensal = data.get("renda_mensal")
    faturamento = data.get("faturamento")

    conn = init_db()
    cursor = conn.cursor()
    
    if tipo == 'pf':
        cursor.execute("INSERT INTO pessoa_fisica (nome_completo, renda_mensal, saldo) VALUES (?, ?, ?)", (nome, renda_mensal, saldo))
    elif tipo == 'pj':
        cursor.execute("INSERT INTO pessoa_juridica (nome_fantasia, faturamento, saldo) VALUES (?, ?, ?)", (nome, faturamento, saldo))
    
    conn.commit()
    conn.close()
    return jsonify({"message": "Cliente criado com sucesso!"})

# Rota para listar usuários
@app.route('/clientes', methods=['GET'])
def listar_clientes():
    conn = init_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM pessoa_fisica")
    pessoas_fisicas = cursor.fetchall()
    
    cursor.execute("SELECT * FROM pessoa_juridica")
    pessoas_juridicas = cursor.fetchall()
    
    conn.close()
    return jsonify({"pessoas_fisicas": pessoas_fisicas, "pessoas_juridicas": pessoas_juridicas})

# Inicia o servidor
if __name__ == '__main__':
    app.run(debug=True)
