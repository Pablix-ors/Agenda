import tkinter as tk
from tkinter import ttk
import sqlite3
import subprocess

class Banco:
    def __init__(self):
        self.conexao = sqlite3.connect('banco.db')

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
            return row
        else:
            return None

def fetch_data():
    try:
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbl_usuarios")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return []

def populate_treeview(treeview, data):
    for item in treeview.get_children():
        treeview.delete(item)
    for row in data:
        treeview.insert("", "end", values=row)

def mostrar_mensagem(mensagem, cor="green"):
    mensagem_label.config(text=mensagem, fg=cor)

def buscar():
    idusuario = idusuario_entry.get()
    if not idusuario:
        mostrar_mensagem("ID Usuário não pode estar vazio!", "red")
        return

    usuario = Usuarios()
    resultado = usuario.selectUser(idusuario)
    if resultado:
        nome_entry.delete(0, tk.END)
        nome_entry.insert(0, resultado[1])
        telefone_entry.delete(0, tk.END)
        telefone_entry.insert(0, resultado[2])
        email_entry.delete(0, tk.END)
        email_entry.insert(0, resultado[3])
        usuario_entry.delete(0, tk.END)
        usuario_entry.insert(0, resultado[4])
        senha_entry.delete(0, tk.END)
        senha_entry.insert(0, resultado[5])
        mostrar_mensagem("Usuário encontrado!")
    else:
        limpar_campos()
        mostrar_mensagem("Usuário não encontrado", "red")

def inserir():
    nome = nome_entry.get()
    telefone = telefone_entry.get()
    email = email_entry.get()
    usuario = usuario_entry.get()
    senha = senha_entry.get()

    if not (nome and telefone and email and usuario and senha):
        mostrar_mensagem("Todos os campos devem ser preenchidos!", "red")
        return

    user = Usuarios(nome=nome, telefone=telefone, email=email, usuario=usuario, senha=senha)
    user.insertUser()
    limpar_campos()
    mostrar_mensagem("Usuário inserido com sucesso!")
    atualizar_treeview()

def alterar():
    idusuario = idusuario_entry.get()
    nome = nome_entry.get()
    telefone = telefone_entry.get()
    email = email_entry.get()
    usuario = usuario_entry.get()
    senha = senha_entry.get()

    if not idusuario:
        mostrar_mensagem("ID Usuário é obrigatório para alterar!", "red")
        return

    user = Usuarios(idusuario=idusuario, nome=nome, telefone=telefone, email=email, usuario=usuario, senha=senha)
    user.updateUser()
    limpar_campos()
    mostrar_mensagem("Usuário atualizado com sucesso!")
    atualizar_treeview()

def excluir():
    idusuario = idusuario_entry.get()

    if not idusuario:
        mostrar_mensagem("ID Usuário é obrigatório para excluir!", "red")
        return

    user = Usuarios(idusuario=idusuario)
    user.deleteUser()
    limpar_campos()
    mostrar_mensagem("Usuário excluído com sucesso!")
    atualizar_treeview()

def limpar_campos():
    idusuario_entry.delete(0, tk.END)
    nome_entry.delete(0, tk.END)
    telefone_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    usuario_entry.delete(0, tk.END)
    senha_entry.delete(0, tk.END)
    mostrar_mensagem("")

def atualizar_treeview():
    data = fetch_data()
    populate_treeview(treeview, data)
    inserir_button.config(state=tk.NORMAL)
    alterar_button.config(state=tk.DISABLED)
    excluir_button.config(state=tk.DISABLED)

def selecionar_item(event):
    item = treeview.selection()[0]
    valores = treeview.item(item, "values")

    idusuario_entry.delete(0, tk.END)
    idusuario_entry.insert(0, valores[0])

    nome_entry.delete(0, tk.END)
    nome_entry.insert(0, valores[1])

    telefone_entry.delete(0, tk.END)
    telefone_entry.insert(0, valores[2])

    email_entry.delete(0, tk.END)
    email_entry.insert(0, valores[3])

    usuario_entry.delete(0, tk.END)
    usuario_entry.insert(0, valores[4])

    senha_entry.delete(0, tk.END)
    senha_entry.insert(0, valores[5])

    inserir_button.config(state=tk.DISABLED)
    alterar_button.config(state=tk.NORMAL)
    excluir_button.config(state=tk.NORMAL)

# Funções para abrir outros módulos
def abrir_cadusuarios():
    subprocess.Popen(['python', 'cadusuarios.py'])

def abrir_cidades():
    subprocess.Popen(['python', 'cidades.py'])

def abrir_clientes():
    subprocess.Popen(['python', 'clientes.py'])

# Configurando a interface principal
root = tk.Tk()
root.title("Cadastro de Usuários")

# Maximizar a janela
root.state('zoomed')

# Adicionando o Menu
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

menu_gerenciamento = tk.Menu(menu_bar, tearoff=0)
menu_gerenciamento.add_command(label="Usuários", command=abrir_cadusuarios)
menu_gerenciamento.add_command(label="Cidades", command=abrir_cidades)
menu_gerenciamento.add_command(label="Clientes", command=abrir_clientes)
menu_bar.add_cascade(label="Gerenciamento", menu=menu_gerenciamento)
menu_bar.add_command(label="Sair", command=root.quit)

# Frame centralizado
frame_central = tk.Frame(root)
frame_central.grid(row=0, column=0, padx=20, pady=20)

# ID Usuário
idusuario_label = tk.Label(frame_central, text="ID Usuário:")
idusuario_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
idusuario_entry = tk.Entry(frame_central)
idusuario_entry.grid(row=0, column=1, padx=10, pady=10)
buscar_button = tk.Button(frame_central, text="Buscar", command=buscar)
buscar_button.grid(row=0, column=2, padx=10, pady=10)

# Nome
nome_label = tk.Label(frame_central, text="Nome:")
nome_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
nome_entry = tk.Entry(frame_central)
nome_entry.grid(row=1, column=1, padx=10, pady=10)

# Telefone
telefone_label = tk.Label(frame_central, text="Telefone:")
telefone_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
telefone_entry = tk.Entry(frame_central)
telefone_entry.grid(row=2, column=1, padx=10, pady=10)

# E-mail
email_label = tk.Label(frame_central, text="E-mail:")
email_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
email_entry = tk.Entry(frame_central)
email_entry.grid(row=3, column=1, padx=10, pady=10)

# Usuário
usuario_label = tk.Label(frame_central, text="Usuário:")
usuario_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
usuario_entry = tk.Entry(frame_central)
usuario_entry.grid(row=4, column=1, padx=10, pady=10)

# Senha
senha_label = tk.Label(frame_central, text="Senha:")
senha_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
senha_entry = tk.Entry(frame_central, show="*")
senha_entry.grid(row=5, column=1, padx=10, pady=10)

# Botões de ação
inserir_button = tk.Button(frame_central, text="Inserir", command=inserir)
inserir_button.grid(row=6, column=0, padx=10, pady=10)

alterar_button = tk.Button(frame_central, text="Alterar", command=alterar)
alterar_button.grid(row=6, column=1, padx=10, pady=10)
alterar_button.config(state=tk.DISABLED)

excluir_button = tk.Button(frame_central, text="Excluir", command=excluir)
excluir_button.grid(row=6, column=2, padx=10, pady=10)
excluir_button.config(state=tk.DISABLED)

# Treeview
treeview = ttk.Treeview(frame_central, columns=("idusuario", "nome", "telefone", "email", "usuario", "senha"), show="headings")
treeview.heading("idusuario", text="ID Usuário")
treeview.heading("nome", text="Nome")
treeview.heading("telefone", text="Telefone")
treeview.heading("email", text="E-mail")
treeview.heading("usuario", text="Usuário")
treeview.heading("senha", text="Senha")
treeview.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

# Configurar o evento de clique no Treeview
treeview.bind("<ButtonRelease-1>", selecionar_item)

# Mensagem
mensagem_label = tk.Label(root, text="", fg="green")
mensagem_label.grid(row=1, column=0, padx=10, pady=10)

# Carregar dados iniciais no Treeview
atualizar_treeview()

root.mainloop()
