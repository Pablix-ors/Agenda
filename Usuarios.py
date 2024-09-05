from Banco import Banco

class Usuarios:
    def __init__(self, idusuario=None, nome=None, telefone=None, email=None, usuario=None, senha=None):
        self.idusuario = idusuario
        self.nome = nome
        self.telefone = telefone
        self.email = email
        self.usuario = usuario
        self.senha = senha
        self.conexao = Banco().conexao

    def insertUser(self):
        c = self.conexao.cursor()
        c.execute("""
        INSERT INTO tbl_usuarios (nome, telefone, email, usuario, senha)
        VALUES (?, ?, ?, ?, ?)""", (self.nome, self.telefone, self.email, self.usuario, self.senha))
        self.conexao.commit()
        c.close()
        return "Usuário inserido com sucesso!"

    def updateUser(self):
        c = self.conexao.cursor()
        c.execute("""
        UPDATE tbl_usuarios SET nome=?, telefone=?, email=?, usuario=?, senha=? WHERE idusuario=?""",
                  (self.nome, self.telefone, self.email, self.usuario, self.senha, self.idusuario))
        self.conexao.commit()
        c.close()
        return "Usuário atualizado com sucesso!"

    def deleteUser(self):
        c = self.conexao.cursor()
        c.execute("DELETE FROM tbl_usuarios WHERE idusuario=?", (self.idusuario,))
        self.conexao.commit()
        c.close()
        return "Usuário excluído com sucesso!"

    def selectUser(self, idusuario):
        c = self.conexao.cursor()
        c.execute("SELECT * FROM tbl_usuarios WHERE idusuario=?", (idusuario,))
        row = c.fetchone()
        c.close()
        if row:
            self.idusuario, self.nome, self.telefone, self.email, self.usuario, self.senha = row
            return "Usuário encontrado!"
        else:
            return "Usuário não encontrado."
