# Cliente.py

import sqlite3

class Cliente:
    def __init__(self, idcliente=None, nome=None, endereco=None, bairro=None, telefone=None, idcidade=None):
        self.idcliente = idcliente
        self.nome = nome
        self.endereco = endereco
        self.bairro = bairro
        self.telefone = telefone
        self.idcidade = idcidade

    def inserir_cliente(self):
        try:
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO tbl_clientes (nome, endereco, bairro, telefone, idcidade)
            VALUES (?, ?, ?, ?, ?)
            """, (self.nome, self.endereco, self.bairro, self.telefone, self.idcidade))
            conn.commit()
            conn.close()
            return "Cliente inserido com sucesso!"
        except sqlite3.Error as e:
            return f"Erro ao inserir cliente: {e}"

    def update_cliente(self):
        try:
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE tbl_clientes
            SET nome = ?, endereco = ?, bairro = ?, telefone = ?, idcidade = ?
            WHERE idcliente = ?
            """, (self.nome, self.endereco, self.bairro, self.telefone, self.idcidade, self.idcliente))
            conn.commit()
            conn.close()
            return "Cliente atualizado com sucesso!"
        except sqlite3.Error as e:
            return f"Erro ao atualizar cliente: {e}"

    def delete_cliente(self):
        try:
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            cursor.execute("""
            DELETE FROM tbl_clientes WHERE idcliente = ?
            """, (self.idcliente,))
            conn.commit()
            conn.close()
            return "Cliente excluído com sucesso!"
        except sqlite3.Error as e:
            return f"Erro ao excluir cliente: {e}"

    def select_cliente(self, idcliente):
        try:
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            cursor.execute("""
            SELECT nome, endereco, bairro, telefone, idcidade FROM tbl_clientes WHERE idcliente = ?
            """, (idcliente,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self.nome, self.endereco, self.bairro, self.telefone, self.idcidade = result
                return True
            return False
        except sqlite3.Error as e:
            print(f"Erro ao selecionar cliente: {e}")
            return False
