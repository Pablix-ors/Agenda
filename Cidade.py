import sqlite3

class Cidade:
    def __init__(self, idcidade=None, nome=None, estado=None):
        self.idcidade = idcidade
        self.nome = nome
        self.estado = estado

    def insert_cidade(self):
        try:
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            cursor.execute("""
            INSERT INTO tbl_cidades (nome, estado)
            VALUES (?, ?)
            """, (self.nome, self.estado))
            conn.commit()
            conn.close()
            return "Cidade inserida com sucesso!"
        except sqlite3.Error as e:
            return f"Erro ao inserir cidade: {e}"

    def update_cidade(self):
        try:
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            cursor.execute("""
            UPDATE tbl_cidades
            SET nome = ?, estado = ?
            WHERE idcidade = ?
            """, (self.nome, self.estado, self.idcidade))
            conn.commit()
            conn.close()
            return "Cidade atualizada com sucesso!"
        except sqlite3.Error as e:
            return f"Erro ao atualizar cidade: {e}"

    def delete_cidade(self):
        if self.has_clientes():
            return "Não é possível excluir a cidade porque há clientes associados a ela."
        try:
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            cursor.execute("""
            DELETE FROM tbl_cidades WHERE idcidade = ?
            """, (self.idcidade,))
            conn.commit()
            conn.close()
            return "Cidade excluída com sucesso!"
        except sqlite3.Error as e:
            return f"Erro ao excluir cidade: {e}"

    def has_clientes(self):
        try:
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            cursor.execute("""
            SELECT COUNT(*) FROM tbl_clientes WHERE idcidade = ?
            """, (self.idcidade,))
            count = cursor.fetchone()[0]
            conn.close()
            return count > 0
        except sqlite3.Error as e:
            print(f"Erro ao verificar clientes associados: {e}")
            return False

    def select_cidade(self, idcidade):
        try:
            conn = sqlite3.connect('banco.db')
            cursor = conn.cursor()
            cursor.execute("""
            SELECT nome, estado FROM tbl_cidades WHERE idcidade = ?
            """, (idcidade,))
            result = cursor.fetchone()
            conn.close()
            if result:
                self.nome, self.estado = result
                return True
            return False
        except sqlite3.Error as e:
            print(f"Erro ao selecionar cidade: {e}")
            return False
