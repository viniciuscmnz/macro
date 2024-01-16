import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2
from datetime import datetime, timedelta
import bcrypt

def add_user():
    conn = psycopg2.connect(
        dbname="your_database_name",
        user="your_username",
        password="your_password",
        host="your_host",
        port="your_port"
    )
    c = conn.cursor()

    # Verifica se o email já existe
    c.execute("SELECT * FROM users WHERE email=%s", (email.get(),))
    row = c.fetchone()

    expiry_date = datetime.today().date() + timedelta(days=int(expiry_key.get()))
    password_hash = bcrypt.hashpw(password.get().encode('utf-8'), bcrypt.gensalt())

    if row is not None:
        # Se o usuário já existir, atualiza a chave de expiração
        db_email, db_password, db_expiry_key = row
        db_expiry_date = datetime.strptime(db_expiry_key, '%Y-%m-%d').date()
        if db_expiry_date < expiry_date:
            db_expiry_date = expiry_date
        c.execute("UPDATE users SET password = %s, expiry_key = %s WHERE email = %s", 
                  (password_hash, db_expiry_date.strftime('%Y-%m-%d'), email.get()))
        messagebox.showinfo("Info", "Usuário atualizado com sucesso!")
    else:
        # Se o usuário não existir, insere um novo usuário
        c.execute("INSERT INTO users VALUES (%s, %s, %s)", 
                  (email.get(), password_hash, expiry_date.strftime('%Y-%m-%d')))
        messagebox.showinfo("Info", "Usuário adicionado com sucesso!")

    conn.commit()
    conn.close()

root = tk.Tk()
root.title("Gerenciador de Usuários")

frame = ttk.Frame(root)
frame.pack(padx=10, pady=10)

email_label = ttk.Label(frame, text="Email:")  # Alterado de "Usuário" para "Email"
email_label.pack(fill='x', expand=True)
email = tk.StringVar()  # Alterado de "username" para "email"
email_entry = ttk.Entry(frame, textvariable=email)  # Alterado de "username_entry" para "email_entry"
email_entry.pack(fill='x', expand=True)

password_label = ttk.Label(frame, text="Senha:")
password_label.pack(fill='x', expand=True)
password = tk.StringVar()
password_entry = ttk.Entry(frame, textvariable=password)
password_entry.pack(fill='x', expand=True)

expiry_key_label = ttk.Label(frame, text="Chave de Expiração:")
expiry_key_label.pack(fill='x', expand=True)
expiry_key = tk.StringVar()
expiry_key_entry = ttk.Entry(frame, textvariable=expiry_key)
expiry_key_entry.pack(fill='x', expand=True)

add_button = ttk.Button(frame, text="Adicionar Usuário", command=add_user)
add_button.pack(fill='x', expand=True)

root.mainloop()
