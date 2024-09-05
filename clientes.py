import tkinter as tk
from tkinter import ttk
from Cliente import Cliente
from Cidade import Cidade
import sqlite3
import subprocess
import sys
import os

# Função para abrir outros módulos
def open_cadusuarios():
    subprocess.Popen([sys.executable, 'cadusuarios.py'])

def open_cidades():
    subprocess.Popen([sys.executable, 'cidades.py'])

def open_clientes():
    subprocess.Popen([sys.executable, 'clientes.py'])

def exit_app():
    root.quit()

# Função para criar ou atualizar a tabela de clientes
def criar_ou_atualizar_tabela_clientes():
    try:
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_clientes (
            idcliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            endereco TEXT NOT NULL,
            bairro TEXT NOT NULL,
            telefone TEXT,
            idcidade INTEGER,
            FOREIGN KEY (idcidade) REFERENCES tbl_cidades(idcidade)
        )
        """)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")

# Chama a função para garantir que a tabela esteja correta
criar_ou_atualizar_tabela_clientes()

# Definição das funções de interação com o banco de dados
def fetch_clientes():
    try:
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("""
        SELECT c.idcliente, c.nome, c.endereco, c.bairro, c.telefone, ci.nome
        FROM tbl_clientes c
        JOIN tbl_cidades ci ON c.idcidade = ci.idcidade
        """)
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return []

def fetch_cidades_para_combobox():
    try:
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT idcidade, nome FROM tbl_cidades")
        rows = cursor.fetchall()
        conn.close()
        return rows
    except sqlite3.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return []

def populate_treeview_clientes(treeview, data):
    for item in treeview.get_children():
        treeview.delete(item)
    for row in data:
        treeview.insert("", "end", values=row)

def mostrar_mensagem_cliente(mensagem, cor="green"):
    mensagem_label.config(text=mensagem, fg=cor)

def buscar_cliente():
    idcliente = idcliente_entry.get()
    if not idcliente:
        mostrar_mensagem_cliente("ID Cliente não pode estar vazio!", "red")
        return

    cliente = Cliente(idcliente=idcliente)
    resultado = cliente.select_cliente(idcliente)
    if resultado:
        nome_entry.delete(0, tk.END)
        nome_entry.insert(0, cliente.nome)
        endereco_entry.delete(0, tk.END)
        endereco_entry.insert(0, cliente.endereco)
        bairro_entry.delete(0, tk.END)
        bairro_entry.insert(0, cliente.bairro)
        telefone_entry.delete(0, tk.END)
        telefone_entry.insert(0, cliente.telefone)
        cidade_combobox.set(cliente.idcidade)
        mostrar_mensagem_cliente("Cliente encontrado!")
    else:
        limpar_campos_cliente()
        mostrar_mensagem_cliente("Cliente não encontrado", "red")

def inserir_cliente():
    nome = nome_entry.get()
    endereco = endereco_entry.get()
    bairro = bairro_entry.get()
    telefone = telefone_entry.get()
    cidade_selecionada = cidade_combobox.get()

    cidades = fetch_cidades_para_combobox()
    idcidade = None
    for cidade in cidades:
        if cidade[1] == cidade_selecionada:
            idcidade = cidade[0]
            break

    if not (nome, endereco, bairro, telefone, idcidade):
        mostrar_mensagem_cliente("Todos os campos devem ser preenchidos e a cidade deve ser válida!", "red")
        return

    cliente = Cliente(nome=nome, endereco=endereco, bairro=bairro, telefone=telefone, idcidade=idcidade)
    resultado = cliente.inserir_cliente()
    mostrar_mensagem_cliente(resultado)
    limpar_campos_cliente()
    atualizar_treeview_clientes()

def alterar_cliente():
    idcliente = idcliente_entry.get()
    nome = nome_entry.get()
    endereco = endereco_entry.get()
    bairro = bairro_entry.get()
    telefone = telefone_entry.get()
    cidade_selecionada = cidade_combobox.get()

    if not idcliente:
        mostrar_mensagem_cliente("ID Cliente é obrigatório para alterar!", "red")
        return

    cidades = fetch_cidades_para_combobox()
    idcidade = None
    for cidade in cidades:
        if cidade[1] == cidade_selecionada:
            idcidade = cidade[0]
            break

    cliente = Cliente(idcliente=idcliente, nome=nome, endereco=endereco, bairro=bairro, telefone=telefone, idcidade=idcidade)
    resultado = cliente.update_cliente()
    mostrar_mensagem_cliente(resultado)
    limpar_campos_cliente()
    atualizar_treeview_clientes()

def excluir_cliente():
    idcliente = idcliente_entry.get()

    if not idcliente:
        mostrar_mensagem_cliente("ID Cliente é obrigatório para excluir!", "red")
        return

    cliente = Cliente(idcliente=idcliente)
    resultado = cliente.delete_cliente()
    mostrar_mensagem_cliente(resultado)
    limpar_campos_cliente()
    atualizar_treeview_clientes()

def limpar_campos_cliente():
    idcliente_entry.delete(0, tk.END)
    nome_entry.delete(0, tk.END)
    endereco_entry.delete(0, tk.END)
    bairro_entry.delete(0, tk.END)
    telefone_entry.delete(0, tk.END)
    cidade_combobox.set("")
    mostrar_mensagem_cliente("")

def atualizar_treeview_clientes():
    data = fetch_clientes()
    populate_treeview_clientes(treeview, data)
    inserir_button_cliente.config(state=tk.NORMAL)
    alterar_button_cliente.config(state=tk.DISABLED)
    excluir_button_cliente.config(state=tk.DISABLED)

def selecionar_item_cliente(event):
    selected_item = treeview.selection()
    if not selected_item:
        return

    item = selected_item[0]
    valores = treeview.item(item, "values")

    idcliente_entry.delete(0, tk.END)
    idcliente_entry.insert(0, valores[0])

    nome_entry.delete(0, tk.END)
    nome_entry.insert(0, valores[1])

    endereco_entry.delete(0, tk.END)
    endereco_entry.insert(0, valores[2])

    bairro_entry.delete(0, tk.END)
    bairro_entry.insert(0, valores[3])

    telefone_entry.delete(0, tk.END)
    telefone_entry.insert(0, valores[4])

    cidade_combobox.set(valores[5])

    inserir_button_cliente.config(state=tk.DISABLED)
    alterar_button_cliente.config(state=tk.NORMAL)
    excluir_button_cliente.config(state=tk.NORMAL)

# Configurando a interface principal para clientes
root = tk.Tk()
root.title("Cadastro de Clientes")

# Maximizar a janela
root.state('zoomed')

# Criar o menu
menu = tk.Menu(root)
root.config(menu=menu)

# Adicionar itens ao menu
file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Arquivo", menu=file_menu)
file_menu.add_command(label="Usuários", command=open_cadusuarios)
file_menu.add_command(label="Cidades", command=open_cidades)
file_menu.add_command(label="Clientes", command=open_clientes)
file_menu.add_separator()
file_menu.add_command(label="Sair", command=exit_app)

# Frame centralizado
frame_central = tk.Frame(root)
frame_central.grid(row=0, column=0, padx=20, pady=20)

# ID Cliente
idcliente_label = tk.Label(frame_central, text="ID Cliente:")
idcliente_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
idcliente_entry = tk.Entry(frame_central)
idcliente_entry.grid(row=0, column=1, padx=10, pady=10)
buscar_button_cliente = tk.Button(frame_central, text="Buscar", command=buscar_cliente)
buscar_button_cliente.grid(row=0, column=2, padx=10, pady=10)

# Nome
nome_label = tk.Label(frame_central, text="Nome:")
nome_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
nome_entry = tk.Entry(frame_central)
nome_entry.grid(row=1, column=1, padx=10, pady=10)

# Endereço
endereco_label = tk.Label(frame_central, text="Endereço:")
endereco_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
endereco_entry = tk.Entry(frame_central)
endereco_entry.grid(row=2, column=1, padx=10, pady=10)

# Bairro
bairro_label = tk.Label(frame_central, text="Bairro:")
bairro_label.grid(row=3, column=0, padx=10, pady=10, sticky="e")
bairro_entry = tk.Entry(frame_central)
bairro_entry.grid(row=3, column=1, padx=10, pady=10)

# Telefone
telefone_label = tk.Label(frame_central, text="Telefone:")
telefone_label.grid(row=4, column=0, padx=10, pady=10, sticky="e")
telefone_entry = tk.Entry(frame_central)
telefone_entry.grid(row=4, column=1, padx=10, pady=10)

# Cidade
cidade_label = tk.Label(frame_central, text="Cidade:")
cidade_label.grid(row=5, column=0, padx=10, pady=10, sticky="e")
cidades = fetch_cidades_para_combobox()
cidade_combobox = ttk.Combobox(frame_central, values=[cidade[1] for cidade in cidades])
cidade_combobox.grid(row=5, column=1, padx=10, pady=10)

# Botões de ação para Clientes
inserir_button_cliente = tk.Button(frame_central, text="Inserir", command=inserir_cliente)
inserir_button_cliente.grid(row=6, column=0, padx=10, pady=10)

alterar_button_cliente = tk.Button(frame_central, text="Alterar", state=tk.DISABLED, command=alterar_cliente)
alterar_button_cliente.grid(row=6, column=1, padx=10, pady=10)

excluir_button_cliente = tk.Button(frame_central, text="Excluir", state=tk.DISABLED, command=excluir_cliente)
excluir_button_cliente.grid(row=6, column=2, padx=10, pady=10)

# Treeview para mostrar os clientes
treeview_frame = tk.Frame(frame_central)
treeview_frame.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

treeview = ttk.Treeview(treeview_frame, columns=("ID", "Nome", "Endereço", "Bairro", "Telefone", "Cidade"), show="headings")
treeview.heading("ID", text="ID")
treeview.heading("Nome", text="Nome")
treeview.heading("Endereço", text="Endereço")
treeview.heading("Bairro", text="Bairro")
treeview.heading("Telefone", text="Telefone")
treeview.heading("Cidade", text="Cidade")
treeview.pack(fill="both", expand=True)

treeview.bind("<Double-1>", selecionar_item_cliente)

# Label para exibir mensagens para o usuário
mensagem_label = tk.Label(frame_central, text="", fg="green")
mensagem_label.grid(row=8, column=0, columnspan=3)

# Preencher o Treeview com os dados dos clientes
atualizar_treeview_clientes()

root.mainloop()
