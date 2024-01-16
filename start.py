import login
import main  # Importa o módulo main aqui



def start_program():
    if login.check_credentials():
        main.main_program()  # Chama a função main_program() aqui

if __name__ == "__main__":
    start_program()
