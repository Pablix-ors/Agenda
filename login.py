import tkinter as tk
from tkinter import messagebox
from Banco import Banco


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Tela de Login")
        self.banco = Banco()
        self.create_widgets()

    def create_widgets(self):
        # Carregar as imagens
        self.load_images()

        # Frame para login
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack(pady=20)

        # Adicionar a imagem ao frame de login
        self.image_label_login = tk.Label(self.login_frame, image=self.img_login)
        self.image_label_login.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.login_frame, text="Usuário").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.login_frame, text="Senha").grid(row=2, column=0, padx=10, pady=5)

        self.usuario_entry = tk.Entry(self.login_frame)
        self.senha_entry = tk.Entry(self.login_frame, show="*")

        self.usuario_entry.grid(row=1, column=1, padx=10, pady=5)
        self.senha_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Button(self.login_frame, text="Login", command=self.authenticate).grid(row=3, column=0, columnspan=2,
                                                                                  pady=10)

        # Botão para novo cadastro
        self.new_user_button = tk.Button(self.root, text="Não é cadastrado? Clique aqui!",
                                         command=self.show_registration)
        self.new_user_button.pack(pady=10)

        # Frame para cadastro, inicialmente oculto
        self.registration_frame = tk.Frame(self.root)
        self.create_registration_widgets()

    def load_images(self):
        # Defina o caminho completo para as imagens
        img_path_login = r'C:\Python\exercicios\Agenda\imagens\login_image.gif'
        img_path_registration = r'C:\Python\exercicios\Agenda\imagens\registration_image.gif'

        # Carregar a imagem para o login
        self.img_login = tk.PhotoImage(file=img_path_login)

        # Carregar a imagem para o cadastro
        self.img_registration = tk.PhotoImage(file=img_path_registration)

    def create_registration_widgets(self):
        # Adicionar a imagem ao frame de cadastro
        self.image_label_registration = tk.Label(self.registration_frame, image=self.img_registration)
        self.image_label_registration.grid(row=0, column=0, columnspan=2, pady=10)

        tk.Label(self.registration_frame, text="Nome").grid(row=1, column=0, padx=10, pady=5)
        tk.Label(self.registration_frame, text="Telefone").grid(row=2, column=0, padx=10, pady=5)
        tk.Label(self.registration_frame, text="Email").grid(row=3, column=0, padx=10, pady=5)
        tk.Label(self.registration_frame, text="Usuário").grid(row=4, column=0, padx=10, pady=5)
        tk.Label(self.registration_frame, text="Senha").grid(row=5, column=0, padx=10, pady=5)

        self.nome_entry = tk.Entry(self.registration_frame)
        self.telefone_entry = tk.Entry(self.registration_frame)
        self.email_entry = tk.Entry(self.registration_frame)
        self.usuario_entry_reg = tk.Entry(self.registration_frame)
        self.senha_entry_reg = tk.Entry(self.registration_frame, show="*")

        self.nome_entry.grid(row=1, column=1, padx=10, pady=5)
        self.telefone_entry.grid(row=2, column=1, padx=10, pady=5)
        self.email_entry.grid(row=3, column=1, padx=10, pady=5)
        self.usuario_entry_reg.grid(row=4, column=1, padx=10, pady=5)
        self.senha_entry_reg.grid(row=5, column=1, padx=10, pady=5)

        tk.Button(self.registration_frame, text="Cadastrar", command=self.register).grid(row=6, column=0, columnspan=2,
                                                                                         pady=10)

    def show_registration(self):
        self.login_frame.pack_forget()
        self.new_user_button.pack_forget()
        self.registration_frame.pack(pady=20)

    def show_login(self):
        self.registration_frame.pack_forget()
        self.login_frame.pack(pady=20)
        self.new_user_button.pack(pady=10)

    def authenticate(self):
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()

        if not (usuario and senha):
            messagebox.showwarning("Aviso", "Usuário e senha devem ser preenchidos")
            return

        if self.banco.check_user(usuario, senha):
            messagebox.showinfo("Sucesso", "Login realizado com sucesso")
            self.root.quit()
            # Importa o aplicativo principal
            import principal
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos")

    def register(self):
        nome = self.nome_entry.get()
        telefone = self.telefone_entry.get()
        email = self.email_entry.get()
        usuario = self.usuario_entry_reg.get()
        senha = self.senha_entry_reg.get()

        if not (nome and telefone and email and usuario and senha):
            messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos")
            return

        self.banco.add_user(nome, telefone, email, usuario, senha)
        messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso")
        self.show_login()


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)

    # Maximizar a janela
    root.state('zoomed')

    root.mainloop()
