from tkinter.ttk import Label, Button, Combobox, Style
from ttkthemes import ThemedTk
from tkinter import ttk, Checkbutton, IntVar, Label, messagebox, filedialog
from PIL import Image, ImageTk
import keyboard
import pyautogui
from window import hidden_client
import json
import threading
import pynput
import time
import atexit
import win32gui
import pygetwindow as gw


root = ThemedTk(theme="msc", themebg=True)
root.title("Macro")
root.resizable(False, False)
style = Style()
style.configure('TButton', font=("Roboto", 12))
style.configure('Ativado.TButton', foreground="green")
style.configure('Desativado.TButton', foreground="red")


HOTKEYS = ["Desligado", "F1", "F2", "F3", "F4", "F5", "F6", "F7", "F8", "F9", "F10", "F11", "F12"]
HUR = ["Desligado", "Utani Hur", "Utani Gran Hur", "Utani Tempo Hur"]
UTURA = ["Desligado", "Utura", "Utura gran"]
var = IntVar
settings_changed = False
loaded_filename = None
settings_saved = False

def generate_widget(widget, row, column, sticky="NSEW", columnspan= None, **kwargs):
    my_widget = widget(**kwargs)
    my_widget.grid(row=row, column=column, padx=5, pady= 5, columnspan=columnspan, sticky=sticky)
    return my_widget

def load_trash():
    load_image = Image.open('trash-icon.jpg')
    resized_image = load_image.resize((20, 20))
    return ImageTk.PhotoImage(resized_image)

def load_ssa():
    load_image_ssa = Image.open('ssa-icon.gif')
    resized_image = load_image_ssa.resize((30, 30))
    return ImageTk.PhotoImage(resized_image)

def load_might_ring():
    load_image_might_ring = Image.open('might-ring-icon.gif')
    resized_image = load_image_might_ring.resize((30, 30))
    return ImageTk.PhotoImage(resized_image)

sep1 = ttk.Separator(root, orient='horizontal')
sep1.grid(row=0, column=0, columnspan=8, sticky='ew')

sep2 = ttk.Separator(root, orient='horizontal')
sep2.grid(row=5, column=0, columnspan=8, sticky='ew')

sep3 = ttk.Separator(root, orient='horizontal')
sep3.grid(row=11, column=0, columnspan=8, sticky='ew')

sep_vertical = ttk.Separator(root, orient='vertical')
sep_vertical.grid(row=1, column=7, rowspan=10, sticky='ns')





lbl_healing = generate_widget(Label, row=0, column=0, sticky="W", text="Healing", font=("Roboto", 13, 'bold'))
lbl_utilities = generate_widget(Label, row=5, column=0, sticky="W", text="Utility", font=("Roboto", 13, 'bold'))

lbl_food = generate_widget(Label, row=6, column=0, sticky="W", text="Eatfood", font=("Roboto", 12))
cbx_food = generate_widget(Combobox, row=6, column=1, values=HOTKEYS, state="readonly", font=("Roboto", 12), width= 12)
cbx_food.current(0)

lbl_utura = generate_widget(Label, row=8, column=0, sticky="W", text="Utura/Utura Gran (F7)", font=("Roboto", 12))
cbx_utura = generate_widget(Combobox, row=8, column=1, values=UTURA, state="readonly", font=("Roboto", 12), width= 12)
cbx_utura.current(0)

lbl_hur = generate_widget(Label, row=7, column=0, sticky="W", text="Auto Hur (F4)", font=("Roboto", 12))
cbx_hur = generate_widget(Combobox, row=7, column=1, values=HUR, state="readonly", font=("Roboto", 12), width= 12)
cbx_hur.current(0)

lbl_cast = generate_widget(Label, row=2, column=0, sticky="W", text="Mana", font=("Roboto", 12))
cbx_cast = generate_widget(Combobox, row= 2, column=1, values=HOTKEYS, state="readonly", font=("Roboto", 12), width= 12)
cbx_cast.current(0)

lbl_hp_heal = generate_widget(Label, row=1, column=0, sticky="W", text="HP", font=("Roboto", 12))
cbx_hp_heal = generate_widget(Combobox, row= 1, column=1, values=HOTKEYS, state="readonly", font=("Roboto", 12), width= 12)
cbx_hp_heal.current(0)

# Adicionando as novas funções Skill 1 e Skill 2
lbl_skill1 = generate_widget(Label, row=3, column=0, sticky="W", text="Skill 1", font=("Roboto", 12))
cbx_skill1 = generate_widget(Combobox, row= 3, column=1, values=HOTKEYS, state="readonly", font=("Roboto", 12), width= 12)
cbx_skill1.current(0)

lbl_skill2 = generate_widget(Label, row=4, column=0, sticky="W", text="Skill 2", font=("Roboto", 12))
cbx_skill2 = generate_widget(Combobox, row= 4, column=1, values=HOTKEYS, state="readonly", font=("Roboto", 12), width= 12)
cbx_skill2.current(0)

rgb = ''
mana_position = ''
def get_mana_position():
    global rgb
    global mana_position
    messagebox.showinfo(title="Mana Position", message="Position the mouse over the mana bar and press the insert key")
    keyboard.wait('insert')
    x, y = pyautogui.position()
    new_rgb = pyautogui.screenshot().getpixel((x, y))
    while new_rgb != rgb:
        rgb = new_rgb
        messagebox.showinfo(title='Mana Result', message=f"X: {x} Y: {y} - RGB: {rgb}")
        lbl_mana_position.configure(text=f"({x}, {y})")
        mana_position = [x, y]
        new_rgb = pyautogui.screenshot().getpixel((x, y))

btn_mana_position = generate_widget(Button, row=2, column=2, text= "Mana Position", command=get_mana_position)
lbl_mana_position = generate_widget(Label, row=2, column=3, text="Empty", font=("Roboto", 12), sticky="W")

hp_rgb = ''
hp_position = ''
def get_hp_position():
    global hp_rgb
    global hp_position
    messagebox.showinfo(title="HP Position", message="Position the mouse over the HP bar and press the insert key")
    keyboard.wait('insert')
    x, y = pyautogui.position()
    new_rgb = pyautogui.screenshot().getpixel((x, y))
    while new_rgb != hp_rgb:
        hp_rgb = new_rgb
        messagebox.showinfo(title='HP Result', message=f"X: {x} Y: {y} - RGB: {hp_rgb}")
        lbl_hp_position.configure(text=f"({x}, {y})")
        hp_position = [x, y]
        new_rgb = pyautogui.screenshot().getpixel((x, y))

btn_hp_position = generate_widget(Button, row=1, column=2, text= "HP Position", command=get_hp_position)
lbl_hp_position = generate_widget(Label, row=1, column=3, text="Empty", font=("Roboto", 12), sticky="W")

# Adicionando as funções para obter a posição das skills
skill1_rgb = ''
skill1_position = ''
def get_skill1_position():
    global skill1_rgb
    global skill1_position
    messagebox.showinfo(title="Skill 1 Position", message="Position the mouse over the Skill 1 bar and press the insert key")
    keyboard.wait('insert')
    x, y = pyautogui.position()
    new_rgb = pyautogui.screenshot().getpixel((x, y))
    while new_rgb != skill1_rgb:
        skill1_rgb = new_rgb
        messagebox.showinfo(title='Skill 1 Result', message=f"X: {x} Y: {y} - RGB: {skill1_rgb}")
        lbl_skill1_position.configure(text=f"({x}, {y})")
        skill1_position = [x, y]
        new_rgb = pyautogui.screenshot().getpixel((x, y))

btn_skill1_position = generate_widget(Button, row=3, column=2, text= "Skill 1 Position", command=get_skill1_position)
lbl_skill1_position = generate_widget(Label, row=3, column=3, text="Empty", font=("Roboto", 12), sticky="W")

skill2_rgb = ''
skill2_position = ''
def get_skill2_position():
    global skill2_rgb
    global skill2_position
    messagebox.showinfo(title="Skill 2 Position", message="Position the mouse over the Skill 2 bar and press the insert key")
    keyboard.wait('insert')
    x, y = pyautogui.position()
    new_rgb = pyautogui.screenshot().getpixel((x, y))
    while new_rgb != skill2_rgb:
        skill2_rgb = new_rgb
        messagebox.showinfo(title='Skill 2 Result', message=f"X: {x} Y: {y} - RGB: {skill2_rgb}")
        lbl_skill2_position.configure(text=f"({x}, {y})")
        skill2_position = [x, y]
        new_rgb = pyautogui.screenshot().getpixel((x, y))

btn_skill2_position = generate_widget(Button, row=4, column=2, text= "Skill 2 Position", command=get_skill2_position)
lbl_skill2_position = generate_widget(Label, row=4, column=3, text="Empty", font=("Roboto", 12), sticky="W")

trash = load_trash()
ssa = load_ssa()
might_ring = load_might_ring()

def clear_mana():
    lbl_mana_position.configure(text="Empty")

def clear_hp():  # Função para limpar a posição do hp
    lbl_hp_position.configure(text="Empty")

def clear_skill1():  # Função para limpar a posição da skill 1
    lbl_skill1_position.configure(text="Empty")

def clear_skill2():  # Função para limpar a posição da skill 2
    lbl_skill2_position.configure(text="Empty")

btn_mana_position_trash = generate_widget(Button, row=2, column=4, image=trash, sticky="E")
btn_mana_position_trash.configure(command=clear_mana)

btn_hp_position_trash = generate_widget(Button, row=1, column=4, image=trash, sticky="E")  # Botão de limpar para hp
btn_hp_position_trash.configure(command=clear_hp)

btn_skill1_position_trash = generate_widget(Button, row=3, column=4, image=trash, sticky="E")  # Botão de limpar para skill 1
btn_skill1_position_trash.configure(command=clear_skill1)

btn_skill2_position_trash = generate_widget(Button, row=4, column=4, image=trash, sticky="E")  # Botão de limpar para skill 2
btn_skill2_position_trash.configure(command=clear_skill2)

lbl_ssa_position_image = generate_widget(Label, row=9, column=0, sticky="W", image=ssa, text="Auto SSA (insert)", compound='left', font=("Roboto", 12))
cbx_ssa = generate_widget(Checkbutton, row=9, column=1, variable=var)

lbl_might_ring_position_image = generate_widget(Label, row=10, column=0, font=("Roboto", 12), text="Auto Might Ring (end)", compound='left', sticky="W", image=might_ring)
cbx_might_ring = generate_widget(Checkbutton, row=10, column=1, variable=var)


def disable_opacity():
    # Adicione aqui o código para desativar a opacidade
    style.configure('Desativado.TButton', foreground='red')
    btn_opacity.configure(text='Opacidade desativada', style='Desativado.TButton')

def opacity():
    try:
        result = hidden_client()
        style = ttk.Style()
        if result == 1:
            style.configure('Ativado.TButton', foreground='green')
            btn_opacity.configure(text='Opacidade ativada', style='Ativado.TButton')
        else:
            disable_opacity()
    except (IndexError, ValueError):
        print("Janela do Tibia não localizada")

style = ttk.Style()
style.configure('Neutro.TButton', foreground='black')  # Cor neutra para o estado inicial
btn_opacity = generate_widget(Button, row=12, column=0, text="Ativar opacidade", columnspan=1, command=opacity)
btn_opacity.configure(style='Neutro.TButton')  # Inicia a função como neutra





def cleanup():
    try:
        btn_opacity.configure(style='Desativado.TButton')  # Desativa a função quando o programa é fechado
    except (IndexError, ValueError):
        print("Janela do Tibia não localizada")

atexit.register(cleanup)


def save():
    global settings_changed, loaded_filename, settings_saved
    settings_changed = False
    existing_data = {}
    if loaded_filename:
        with open(loaded_filename, 'r') as file:
            existing_data = json.loads(file.read())
    my_data = {
        "food": {
            "value": cbx_food.get(),
            "position": cbx_food.current()
        },
        "hur":{
            "value": cbx_hur.get(),
            "position": cbx_hur.current()
        },
        "utura":{
            "value": cbx_utura.get(),
            "position": cbx_utura.current()
        },        
        "spell": {
            "value": cbx_cast.get(),
            "position": cbx_cast.current()
        },
        "hp_heal": {
            "value": cbx_hp_heal.get(),
            "position": cbx_hp_heal.current()
        },
        "skill1": {  # Salvando a posição da skill 1
            "value": cbx_skill1.get(),
            "position": cbx_skill1.current()
        },
        "skill2": {  # Salvando a posição da skill 2
            "value": cbx_skill2.get(),
            "position": cbx_skill2.current()
        },
        "mana_pos": existing_data.get('mana_pos', {"position": mana_position, "rgb": rgb}),
        "hp_pos": {  # Salvando a posição do hp
            "position": hp_position,
            "rgb": hp_rgb
        },
        "skill1_pos": {  # Salvando a posição do hp
            "position": skill1_position,
            "rgb": skill1_rgb
        },
        "skill2_pos": {  # Salvando a posição do hp
            "position": skill2_position,
            "rgb": skill2_rgb
        }
    }
    if loaded_filename is None:
        loaded_filename = filedialog.asksaveasfilename(defaultextension=".json")
    if loaded_filename:
        with open(loaded_filename, 'w') as file:
            file.write(json.dumps(my_data))
    settings_saved = True

def load():
    global settings_changed, loaded_filename, data
    settings_changed = True
    filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if filename:
        loaded_filename = filename
        with open(filename, 'r') as file:
            data = json.loads(file.read())
        cbx_food.current(data['food']['position'])
        cbx_cast.current(data['spell']['position'])
        cbx_hur.current(data['hur']['position'])
        cbx_utura.current(data['utura']['position'])
        cbx_hp_heal.current(data['hp_heal']['position'])
        cbx_skill1.current(data['skill1']['position'])  # Carregando a posição da skill 1
        cbx_skill2.current(data['skill2']['position'])  # Carregando a posição da skill 2
        lbl_mana_position.configure(text=data['mana_pos']['position'])
        lbl_hp_position.configure(text=data['hp_pos']['position'])  # Carregando a posição do hp
        lbl_skill1_position.configure(text=data['skill1_pos']['position'])
        lbl_skill2_position.configure(text=data['skill2_pos']['position'])
        return data

opacity_on = False

def run():
    first_press_utura = True
    first_press_hur = True

    wait_to_eat_food = 60
    time_food = time.time() - wait_to_eat_food

    time_utura = time.time()
    time_hur = time.time()

    while not myEvent.is_set():
        tibia_windows = gw.getWindowsWithTitle('Tibia')
        if tibia_windows:
            try:
                tibia = tibia_windows[0]
                tibia.activate()
            except IndexError:
                print("Erro ao ativar a janela do Tibia")
                close_program()
                break
        else:
            print("Janela do Tibia não encontrada")
            global opacity_on
            if opacity_on:
                opacity_on = False
                opacity()
            close_program()
            break

        if isinstance(data['hp_pos']['position'], list):  
            x_hp = data['hp_pos']['position'][0]
            y_hp = data['hp_pos']['position'][1]
            if not pyautogui.pixelMatchesColor(x_hp, y_hp, tuple(data['hp_pos']['rgb'])):
                if data['hp_heal']['value'] != 'Desligado':
                    pyautogui.press(data['hp_heal']['value'])
                    time.sleep(0.1) 

        if isinstance(data['mana_pos']['position'], list):
            x = data['mana_pos']['position'][0]
            y = data['mana_pos']['position'][1]
            if not pyautogui.pixelMatchesColor(x, y, tuple(data['mana_pos']['rgb'])):
                if data['spell']['value'] != 'Desligado':
                    pyautogui.press(data['spell']['value'])
                    time.sleep(0.1) 


        if data['utura']['value'] != 'Desligado':
            if data['utura']['value'] == 'Utura' or data['utura']['value'] == 'Utura Gran':
                wait_to_cast_utura = 60.5
            if first_press_utura or int(time.time() - time_utura) >= wait_to_cast_utura:
                time.sleep(1)  # Pause for 1 second before casting utura
                pyautogui.press('F7')
                time_utura = time.time()
                first_press_utura = False

        if data['hur']['value'] != 'Desligado':
            if data['hur']['value'] == 'Utani Hur':
                wait_to_cast_hur = 29
            elif data['hur']['value'] == 'Utani Gran Hur':
                wait_to_cast_hur = 19
            elif data['hur']['value'] == 'Utani Tempo Hur':
                wait_to_cast_hur = 4
            if first_press_hur or int(time.time() - time_hur) >= wait_to_cast_hur:
                time.sleep(1)  # Pause for 1 second before casting hur
                pyautogui.press('f4')
                time_hur = time.time()
                first_press_hur = False

        if isinstance(data['skill1_pos']['position'], list):
            x_skill1 = data['skill1_pos']['position'][0]
            y_skill1 = data['skill1_pos']['position'][1]
            if not pyautogui.pixelMatchesColor(x_skill1, y_skill1, tuple(data['skill1_pos']['rgb'])):
                if data['skill1']['value'] != 'Desligado':
                    pyautogui.press(data['skill1']['value'])
                    time.sleep(0.1) 

        if isinstance(data['skill2_pos']['position'], list):
            x_skill2 = data['skill2_pos']['position'][0]
            y_skill2 = data['skill2_pos']['position'][1]
            if not pyautogui.pixelMatchesColor(x_skill2, y_skill2, tuple(data['skill2_pos']['rgb'])):
                if data['skill2']['value'] != 'Desligado':
                    pyautogui.press(data['skill2']['value'])
                    time.sleep(0.1) 

        if data['food']['value'] != 'Desligado':
            if int(time.time() - time_food) >= wait_to_eat_food:
                pyautogui.press(data['food']['value'])
                time_food = time.time()

def key_code(key):
    if key == pynput.keyboard.Key.f12:
        myEvent.set()
        root.deiconify()
        win32gui.SetForegroundWindow(root.winfo_id())
        return False


def listener_keyboard():
    with pynput.keyboard.Listener(on_press=key_code) as Listener:
        Listener.join()

def on_change():
    global settings_changed, settings_saved
    settings_changed = True
    settings_saved = False

def start():
    global opacity_on
    # Verifique a opacidade da janela antes de iniciar o programa
    #if hidden_client() == 1:
    #    messagebox.showwarning("Aviso", "Por favor, ative a opacidade da tela para poder iniciar a macro")
    #    return
    root.iconify()
    global data
    global settings_saved
    # Verifique se as configurações foram salvas antes de iniciar o programa
    if not settings_saved:
        messagebox.showwarning("Aviso", "Por favor, salve as configurações antes de iniciar o programa.")
        return
    if loaded_filename:
        with open(loaded_filename, 'r') as file:
            data = json.loads(file.read())
    global myEvent
    myEvent = threading.Event()
    global start_th
    start_th = threading.Thread(target=run)
    start_th.start()
    keyboard_th = threading.Thread(target=listener_keyboard)
    keyboard_th.start()


def close_program():
    global opacity_on
    tibia_windows = gw.getWindowsWithTitle('Tibia')
    if tibia_windows:
        if opacity_on:
            opacity_on = False
            disable_opacity()  # Desativa a opacidade
    else:
        try:
            if opacity_on:
                opacity_on = False
                style.configure('Desativado.TButton', foreground='red')
                btn_opacity.configure(text='Opacidade desativada', style='Desativado.TButton')  # Desativa a opacidade
                disable_opacity()  # Desativa a opacidade
        except ValueError:
            print("Janela do Tibia não localizada")
    root.destroy()
    disable_opacity()  # Garante que a opacidade seja desativada quando o programa for fechado



root.protocol("WM_DELETE_WINDOW", close_program)

btn_start = generate_widget(Button, row=12, column=3, text="Start", columnspan=2, command=start, width=10)
btn_load = generate_widget(Button, row=12, column=2, text="Load", command=load, width=10)
btn_save = generate_widget(Button, row=12, column=1, text="Save", command=save, width=10)



root.mainloop()

