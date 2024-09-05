import tkinter as tk
from tkinter import ttk, messagebox
from Cidade import Cidade
import sqlite3
import subprocess

def fetch_cidades():
    try:
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM tbl_cidades")
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

def populate_treeview_cidades(treeview, data):
    for item in treeview.get_children():
        treeview.delete(item)
    for row in data:
        treeview.insert("", "end", values=row)

def mostrar_mensagem_cidade(mensagem, cor="green"):
    mensagem_label.config(text=mensagem, fg=cor)

def buscar_cidade():
    idcidade = idcidade_entry.get()
    if not idcidade:
        mostrar_mensagem_cidade("ID Cidade não pode estar vazio!", "red")
        return

    cidade = Cidade(idcidade=idcidade)
    resultado = cidade.select_cidade(idcidade)
    if resultado:
        nome_entry.delete(0, tk.END)
        nome_entry.insert(0, cidade.nome)
        estado_entry.delete(0, tk.END)
        estado_entry.insert(0, cidade.estado)
        mostrar_mensagem_cidade("Cidade encontrada!")
    else:
        limpar_campos_cidade()
        mostrar_mensagem_cidade("Cidade não encontrada", "red")

def inserir_cidade():
    nome = nome_entry.get()
    estado = estado_entry.get()

    if not (nome and estado):
        mostrar_mensagem_cidade("Todos os campos devem ser preenchidos!", "red")
        return

    cidade = Cidade(nome=nome, estado=estado)
    resultado = cidade.insert_cidade()
    mostrar_mensagem_cidade(resultado)
    limpar_campos_cidade()
    atualizar_treeview_cidades()

def alterar_cidade():
    idcidade = idcidade_entry.get()
    nome = nome_entry.get()
    estado = estado_entry.get()

    if not idcidade:
        mostrar_mensagem_cidade("ID Cidade é obrigatório para alterar!", "red")
        return

    cidade = Cidade(idcidade=idcidade, nome=nome, estado=estado)
    resultado = cidade.update_cidade()
    mostrar_mensagem_cidade(resultado)
    limpar_campos_cidade()
    atualizar_treeview_cidades()

def excluir_cidade():
    idcidade = idcidade_entry.get()

    if not idcidade:
        mostrar_mensagem_cidade("ID Cidade é obrigatório para excluir!", "red")
        return

    cidade = Cidade(idcidade=idcidade)

    # Verifica se a cidade está associada a algum cliente
    if cidade_associada_a_cliente(idcidade):
        messagebox.showerror("Erro", "Erro, Cidade cadastrada a um cliente")
        return

    resultado = cidade.delete_cidade()
    mostrar_mensagem_cidade(resultado)
    limpar_campos_cidade()
    atualizar_treeview_cidades()

def cidade_associada_a_cliente(idcidade):
    try:
        conn = sqlite3.connect('banco.db')
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM tbl_clientes WHERE idcidade = ?", (idcidade,))
        count = cursor.fetchone()[0]
        conn.close()
        return count > 0
    except sqlite3.Error as e:
        print(f"Erro ao verificar associação da cidade com clientes: {e}")
        return False

def limpar_campos_cidade():
    idcidade_entry.delete(0, tk.END)
    nome_entry.delete(0, tk.END)
    estado_entry.delete(0, tk.END)
    mostrar_mensagem_cidade("")

def atualizar_treeview_cidades():
    data = fetch_cidades()
    populate_treeview_cidades(treeview, data)

def selecionar_item_cidade(event):
    selected_item = treeview.selection()
    if not selected_item:
        return

    item = selected_item[0]
    valores = treeview.item(item, "values")

    idcidade_entry.delete(0, tk.END)
    idcidade_entry.insert(0, valores[0])

    nome_entry.delete(0, tk.END)
    nome_entry.insert(0, valores[1])

    estado_entry.delete(0, tk.END)
    estado_entry.insert(0, valores[2])

def abrir_cadusuarios():
    subprocess.Popen(['python', 'cadusuarios.py'])

def abrir_cidades():
    subprocess.Popen(['python', 'cidades.py'])

def abrir_clientes():
    subprocess.Popen(['python', 'clientes.py'])

def sair():
    root.quit()

# Configurando a interface principal para cidades
root = tk.Tk()
root.title("Cadastro de Cidades")

# Maximizar a janela
root.state('zoomed')

# Menu de navegação
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)

menu_gerenciar = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Gerenciar", menu=menu_gerenciar)
menu_gerenciar.add_command(label="Gerenciar Cidades", command=abrir_cidades)
menu_gerenciar.add_command(label="Gerenciar Usuários", command=abrir_cadusuarios)
menu_gerenciar.add_command(label="Gerenciar Clientes", command=abrir_clientes)
menu_gerenciar.add_separator()
menu_gerenciar.add_command(label="Sair", command=sair)

# Frame centralizado
frame_central = tk.Frame(root)
frame_central.grid(row=0, column=0, padx=20, pady=20)

# ID Cidade
idcidade_label = tk.Label(frame_central, text="ID Cidade:")
idcidade_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")
idcidade_entry = tk.Entry(frame_central)
idcidade_entry.grid(row=0, column=1, padx=10, pady=10)
buscar_button_cidade = tk.Button(frame_central, text="Buscar", command=buscar_cidade)
buscar_button_cidade.grid(row=0, column=2, padx=10, pady=10)

# Nome
nome_label = tk.Label(frame_central, text="Nome:")
nome_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")
nome_entry = tk.Entry(frame_central)
nome_entry.grid(row=1, column=1, padx=10, pady=10)

# Estado
estado_label = tk.Label(frame_central, text="Estado:")
estado_label.grid(row=2, column=0, padx=10, pady=10, sticky="e")
estado_entry = tk.Entry(frame_central)
estado_entry.grid(row=2, column=1, padx=10, pady=10)

# Botões
inserir_button_cidade = tk.Button(frame_central, text="Inserir", command=inserir_cidade)
inserir_button_cidade.grid(row=4, column=0, padx=10, pady=10)
alterar_button_cidade = tk.Button(frame_central, text="Alterar", command=alterar_cidade)
alterar_button_cidade.grid(row=4, column=1, padx=10, pady=10)
excluir_button_cidade = tk.Button(frame_central, text="Excluir", command=excluir_cidade)
excluir_button_cidade.grid(row=4, column=2, padx=10, pady=10)

# Treeview
treeview = ttk.Treeview(frame_central, columns=("ID", "Nome", "Estado"), show="headings")
treeview.grid(row=5, column=0, columnspan=3, padx=10, pady=10)

treeview.heading("ID", text="ID")
treeview.heading("Nome", text="Nome")
treeview.heading("Estado", text="Estado")

treeview.column("ID", width=50)
treeview.column("Nome", width=150)
treeview.column("Estado", width=100)

# Mensagem
mensagem_label = tk.Label(root, text="")
mensagem_label.grid(row=1, column=0)

# Populando o Treeview
atualizar_treeview_cidades()

# Adicionando evento de seleção ao Treeview
treeview.bind("<<TreeviewSelect>>", selecionar_item_cidade)

root.mainloop()
