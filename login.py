import tkinter as tk
from tkinter import ttk, messagebox
from main import main_program
import psycopg2
from datetime import datetime
import os


def check_credentials(event=None):
    if not email.get() or not password.get():
        messagebox.showerror("Erro", "Por favor, insira seu e-mail e senha.")
        return False

    try:
        conn = psycopg2.connect(
            dbname="assistbot_db",
            user="postgre",
            password="53491810",
            host="assistbotdb.c7cuy0gu2y5w.us-east-1.rds.amazonaws.com",
            port=5432
        )
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=%s", (email.get(),))
        row = c.fetchone()

        if row is not None:
            print("Usuário recuperado do banco de dados!")
            db_email, db_password, db_expiry_key = row
            db_expiry_date = db_expiry_key
            if password.get() == db_password and db_expiry_date > datetime.today().date():
                days_left = (db_expiry_date - datetime.today().date()).days
                if root is not None:
                    messagebox.showinfo("Login info", "Bem-vindo, " + db_email + "! Você tem " + str(days_left) + " dias restantes.")
                root.destroy()
                main_program()
            else:
                if root is not None:
                    messagebox.showerror("Login info", "Credenciais incorretas ou chave de expiração expirada")
        else:
            if root is not None:
                messagebox.showerror("Login info", "Usuário não encontrado")
        conn.close()
    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        if email.get() and password.get() and root is not None:
            messagebox.showerror("Erro", "Senha ou e-mail inválido!")
    return True

root = tk.Tk()
root.title("AssistBOT")  # Nome na barra superior

# Adicionando um pouco de padding ao redor de cada widget
frame = ttk.Frame(root, padding="50 50 50 50")
frame.pack()


email_label = ttk.Label(frame, text="Email:")  # Alterado de "Usuário" para "Email"
email_label.pack(pady=(0,10))  # Adicionando um pouco de espaço vertical
email = tk.StringVar()  # Alterado de "username" para "email"
email_entry = ttk.Entry(frame, textvariable=email)  # Alterado de "username_entry" para "email_entry"
email_entry.pack(pady=(0,10))  # Adicionando um pouco de espaço vertical

password_label = ttk.Label(frame, text="Senha:")
password_label.pack(pady=(0,10))  # Adicionando um pouco de espaço vertical
password = tk.StringVar()
password_entry = ttk.Entry(frame, textvariable=password, show="*")
password_entry.pack(pady=(0,10))  # Adicionando um pouco de espaço vertical

login_button = ttk.Button(frame, text="Login", command=check_credentials)
login_button.pack(pady=(0,10))  # Adicionando um pouco de espaço vertical

# Permitindo que o usuário pressione Enter para fazer login
root.bind('<Return>', check_credentials)

icon_path = os.path.join(os.getcwd(), "AssistBOT.ico")
root.iconbitmap(icon_path)

def center(win):
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

center(root)

root.mainloop()
