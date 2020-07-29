#Projeto apenas para teste e descoberta sobre a criação de um gerenciador de senhas

import sqlite3

MASTER_PASSWORD = '123'
conn = sqlite3.connect('passwords.db')

cursor = conn.cursor()

senha = input("Digite sua senha master: ")
if senha != MASTER_PASSWORD:
    print("Senha inválida! Encerrando...")
    exit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    service TEXT NOT NULL,
    username TEXT NOT NULL,
    password TEXT NOT NULL
);
''')

def menu():
    print("******************************")
    print("* i : Inserir nova senha     *")
    print("* l : Listar serviços salvos *")
    print("* r : Recuperar senha        *")
    print("* s : Sair                   *")
    print("******************************")

def get_password(service):
    cursor.execute(f'''
        SELECT username, password FROM users
        WHERE service = '{service}'
    ''')

    if cursor.rowcount == 0:
        print('Serviço não cadastrado (use "l" para verificar os serviços). ')
    else:
        for user in cursor.fetchall():
            print(user)


def insert_password(service, username, password):
    cursor.execute(f'''
        INSERT INTO users (service, username, password) 
        VALUES ('{service}', '{username}', '{password}')
    ''')
    conn.commit()

def show_services():
    cursor.execute('''
        SELECT service FROM users;
    ''')
    for service in cursor.fetchall():
        print(service)

    while True:
        menu()
        op = input("O que deseja fazer? ")
        if op not in ['i', 'l', 'r', 's']:
            print("Opção inválida! ")
            continue

        if op == 's':
            break

        if op == 'i':
            service = input('Qual o nome do serviço? ')
            username = input('Qual o nome de usuario? ')
            password = input('Qual a senha? ')
            insert_password(service, username, password)

        if op == 'l':
            show_services()

        if op == 'r':
            service = input('Redefinir senha')
            get_password(service)


conn.close()