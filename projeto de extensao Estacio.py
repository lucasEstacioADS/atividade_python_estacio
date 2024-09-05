import pyodbc
import pandas as pd
from getpass import getpass

def conectar_bd():
    conexao = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=DESKTOP-5H0Q5EJ\\SQLEXPRESS;"
        "DATABASE=projeto;"
    )
    return conexao

def validar_entrada(tipo, msg):
    while True:
        try:
            return tipo(input(msg))
        except (ValueError, TypeError):
            print(f"ERRO: Entrada inválida. Tente novamente.")

def cadastrar_usuario(cursor):
    usuario = validar_entrada(str, "Insira um nome de usuário: ")
    senha = validar_entrada(str, "Insira sua senha: ")
    confirmar_senha = validar_entrada(str, "Confirme sua senha: ")

    if senha == confirmar_senha:
        cursor.execute(f"INSERT INTO usuario (nome, senha) VALUES ('{usuario}', '{senha}')")
        cursor.commit()
        print("Usuário cadastrado com sucesso!")
    else:
        print("As senhas não coincidem.")

def autenticar_usuario(cursor, usuario, senha):
    cursor.execute("SELECT * FROM usuario WHERE nome=? AND senha=?", (usuario, senha))
    return cursor.fetchone() is not None

def exibir_menu():
    return validar_entrada(int, """
    O que deseja consultar?
    1-CLIENTES
    2-ESTOQUE
    3-FORNECEDORES
    4-PRODUTOS
    5-VENDAS
    6-FINALIZAR E SAIR
    """)

def gerenciar_clientes(conexao):
    opcao = validar_entrada(int, "1. Novo cliente\n2. Consultar clientes cadastrados\n")
    if opcao == 2:
        clientes = pd.read_sql("SELECT * FROM cliente", conexao)
        print(clientes)
    else:
        id_cliente = validar_entrada(int, "Digite o código do cliente: ")
        nome = validar_entrada(str, "Nome: ")
        telefone = validar_entrada(str, "Telefone: ")
        cpf = validar_entrada(str, "CPF (apenas números): ")

        cursor = conexao.cursor()
        cursor.execute(f"INSERT INTO cliente (id_cliente, nome_cliente, telefone, cpf) VALUES (?, ?, ?, ?)",
                       (id_cliente, nome, telefone, cpf))
        conexao.commit()
        print("Cliente cadastrado com sucesso!")

def main():
    conexao = conectar_bd()
    cursor = conexao.cursor()

    acesso = validar_entrada(int, "1-Acessar conta existente\n2-Cadastrar nova conta\n")

    if acesso == 2:
        cadastrar_usuario(cursor)
    else:
        usuario = validar_entrada(str, "Usuário: ")
        senha = getpass("Senha: ")

        while not autenticar_usuario(cursor, usuario, senha):
            print("Usuário ou senha incorretos.")
            usuario = validar_entrada(str, "Usuário: ")
            senha = getpass("Senha: ")

    while True:
        menu = exibir_menu()

        if menu == 1:
            gerenciar_clientes(conexao)
        elif menu == 6:
            print("Saindo...")
            cursor.close()
            conexao.close()
            break

if __name__ == "__main__":
    main()
