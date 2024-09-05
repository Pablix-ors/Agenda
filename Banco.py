import sqlite3

# Funções para a tabela de clientes
def criar_tabela_clientes():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Criar a tabela de clientes
        c.execute("""
        CREATE TABLE IF NOT EXISTS tbl_clientes (
            idcliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT NOT NULL,
            bairro TEXT NOT NULL,
            telefone TEXT NOT NULL
        )
        """)

        # Confirmar as alterações e fechar a conexão
        conn.commit()
        conn.close()
        print("Tabela de clientes criada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabela de clientes: {e}")

def inserir_cliente(nome, endereco, bairro, telefone):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Inserir um novo cliente
        c.execute("""
        INSERT INTO tbl_clientes (nome, endereco, bairro, telefone)
        VALUES (?, ?, ?, ?)
        """, (nome, endereco, bairro, telefone))

        # Confirmar as alterações e fechar a conexão
        conn.commit()
        conn.close()
        print("Cliente inserido com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao inserir cliente: {e}")

def atualizar_cliente(idcliente, nome, endereco, bairro, telefone):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Atualizar os dados do cliente
        c.execute("""
        UPDATE tbl_clientes
        SET nome = ?, endereco = ?, bairro = ?, telefone = ?
        WHERE idcliente = ?
        """, (nome, endereco, bairro, telefone, idcliente))

        # Confirmar as alterações e fechar a conexão
        conn.commit()
        conn.close()
        print("Cliente atualizado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar cliente: {e}")

def excluir_cliente(idcliente):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Excluir o cliente
        c.execute("DELETE FROM tbl_clientes WHERE idcliente = ?", (idcliente,))

        # Confirmar as alterações e fechar a conexão
        conn.commit()
        conn.close()
        print("Cliente excluído com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao excluir cliente: {e}")

def buscar_cliente(idcliente):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Buscar o cliente
        c.execute("SELECT * FROM tbl_clientes WHERE idcliente = ?", (idcliente,))
        cliente = c.fetchone()

        # Fechar a conexão
        conn.close()

        return cliente
    except sqlite3.Error as e:
        print(f"Erro ao buscar cliente: {e}")
        return None

def listar_clientes():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Listar todos os clientes
        c.execute("SELECT * FROM tbl_clientes")
        clientes = c.fetchall()

        # Fechar a conexão
        conn.close()

        return clientes
    except sqlite3.Error as e:
        print(f"Erro ao listar clientes: {e}")
        return []

# Funções para a tabela de cidades
def criar_tabela_cidades():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Criar a tabela de cidades
        c.execute("""
        CREATE TABLE IF NOT EXISTS tbl_cidades (
            idcidade INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            estado TEXT NOT NULL
        )
        """)

        # Confirmar as alterações e fechar a conexão
        conn.commit()
        conn.close()
        print("Tabela de cidades criada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabela de cidades: {e}")

def inserir_cidade(nome, estado):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Inserir uma nova cidade
        c.execute("""
        INSERT INTO tbl_cidades (nome, estado)
        VALUES (?, ?)
        """, (nome, estado))

        # Confirmar as alterações e fechar a conexão
        conn.commit()
        conn.close()
        print("Cidade inserida com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao inserir cidade: {e}")

def atualizar_cidade(idcidade, nome, estado):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Atualizar os dados da cidade
        c.execute("""
        UPDATE tbl_cidades
        SET nome = ?, estado = ?
        WHERE idcidade = ?
        """, (nome, estado, idcidade))

        # Confirmar as alterações e fechar a conexão
        conn.commit()
        conn.close()
        print("Cidade atualizada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar cidade: {e}")

def excluir_cidade(idcidade):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Excluir a cidade
        c.execute("DELETE FROM tbl_cidades WHERE idcidade = ?", (idcidade,))

        # Confirmar as alterações e fechar a conexão
        conn.commit()
        conn.close()
        print("Cidade excluída com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao excluir cidade: {e}")

def buscar_cidade(idcidade):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Buscar a cidade
        c.execute("SELECT * FROM tbl_cidades WHERE idcidade = ?", (idcidade,))
        cidade = c.fetchone()

        # Fechar a conexão
        conn.close()

        return cidade
    except sqlite3.Error as e:
        print(f"Erro ao buscar cidade: {e}")
        return None

def listar_cidades():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Listar todas as cidades
        c.execute("SELECT * FROM tbl_cidades")
        cidades = c.fetchall()

        # Fechar a conexão
        conn.close()

        return cidades
    except sqlite3.Error as e:
        print(f"Erro ao listar cidades: {e}")
        return []

# Funções para a tabela de usuários
def criar_tabela_usuarios():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Criar a tabela de usuários
        c.execute("""
        CREATE TABLE IF NOT EXISTS tbl_usuarios (
            idusuario INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            senha TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
        """)

        # Confirmar as alterações e fechar a conexão
        conn.commit()
        conn.close()
        print("Tabela de usuários criada com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabela de usuários: {e}")

def inserir_usuario(username, senha, email):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Inserir um novo usuário
        c.execute("""
        INSERT INTO tbl_usuarios (username, senha, email)
        VALUES (?, ?, ?)
        """, (username, senha, email))

        # Confirmar as alterações e fechar a conexão
        conn.commit()
        conn.close()
        print("Usuário inserido com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao inserir usuário: {e}")

def atualizar_usuario(idusuario, username, senha, email):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Atualizar os dados do usuário
        c.execute("""
        UPDATE tbl_usuarios
        SET username = ?, senha = ?, email = ?
        WHERE idusuario = ?
        """, (username, senha, email, idusuario))

        # Confirmar as alterações e fechar a conexão
        conn.commit()
        conn.close()
        print("Usuário atualizado com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao atualizar usuário: {e}")

def excluir_usuario(idusuario):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Excluir o usuário
        c.execute("DELETE FROM tbl_usuarios WHERE idusuario = ?", (idusuario,))

        # Confirmar as alterações e fechar a conexão
        conn.commit()
        conn.close()
        print("Usuário excluído com sucesso!")
    except sqlite3.Error as e:
        print(f"Erro ao excluir usuário: {e}")

def buscar_usuario(idusuario):
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Buscar o usuário
        c.execute("SELECT * FROM tbl_usuarios WHERE idusuario = ?", (idusuario,))
        usuario = c.fetchone()

        # Fechar a conexão
        conn.close()

        return usuario
    except sqlite3.Error as e:
        print(f"Erro ao buscar usuário: {e}")
        return None

def listar_usuarios():
    try:
        # Conectar ao banco de dados
        conn = sqlite3.connect('banco.db')
        c = conn.cursor()

        # Listar todos os usuários
        c.execute("SELECT * FROM tbl_usuarios")
        usuarios = c.fetchall()

        # Fechar a conexão
        conn.close()

        return usuarios
    except sqlite3.Error as e:
        print(f"Erro ao listar usuários: {e}")
        return []
