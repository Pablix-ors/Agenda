import tkinter as tk
import subprocess
import sys
import os

# Ajustar o caminho para o módulo Banco
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def open_cadusuarios():
    subprocess.Popen([sys.executable, 'cadusuarios.py'])

def open_cidades():
    subprocess.Popen([sys.executable, 'cidades.py'])

def open_clientes():
    subprocess.Popen([sys.executable, 'clientes.py'])

def exit_app():
    root.quit()

root = tk.Tk()
root.title("Sistema Agenda")

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

root.mainloop()
