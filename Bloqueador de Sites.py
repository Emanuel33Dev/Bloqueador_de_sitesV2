import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import csv

# Cores
co0 = "#fof3f5"  # Preta
co1 = "#feffff"  # Branca
co2 = "#3fb5a3"  # Verde
co3 = "#fc766d"  # Vermelho
co4 = "#403d3d"  # Letra
co5 = "#4a88e8"  # Azul

# Variáveis globais
e_site = None
listabox = None
iniciar = None

def center_window(window, width, height, offset_x=0, offset_y=0):
    # Calcular as coordenadas para centralizar a janela
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2)) + offset_x
    y = int((screen_height / 2) - (height / 2)) + offset_y
    window.geometry(f'{width}x{height}+{x}+{y}')

# Tela de Login
def login_window():
    global usuario_entry, senha_entry, login_win
    login_win = tk.Tk()
    login_win.title('Login')
    window_width = 300
    window_height = 150
    center_window(login_win, window_width, window_height, offset_x=0, offset_y=-100)

    tk.Label(login_win, text='Usuário:').grid(row=0, column=0, padx=10, pady=10)
    usuario_entry = tk.Entry(login_win)
    usuario_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(login_win, text='Senha:').grid(row=1, column=0, padx=10, pady=10)
    senha_entry = tk.Entry(login_win, show='*')
    senha_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(login_win, text='Login', command=verify_login).grid(row=2, column=1, padx=10, pady=10)

    login_win.mainloop()

def verify_login():
    usuario = usuario_entry.get()
    senha = senha_entry.get()
    if usuario == 'Vitor' and senha == '1234':
        messagebox.showinfo('Login Sucesso', 'Logado!')
        login_win.destroy()  # Fecha a janela de login
        criar_janela_principal()
    else:
        messagebox.showerror('Login Falhou', 'Credenciais inválidas!')

def criar_janela_principal():
    global e_site, listabox, iniciar
    janela = tk.Tk()
    janela.title("Bloqueador de Sites")
    window_width = 390
    window_height = 350
    center_window(janela, window_width, window_height)
    janela.configure(background=co1)
    janela.resizable(width=False, height=False)

    # Inicializar variável global iniciar
    iniciar = tk.BooleanVar()

    # Frames
    frame_logo = tk.Frame(janela, width=400, height=60, bg=co1, relief="flat")
    frame_logo.grid(row=0, column=0, pady=1, padx=0, sticky="nsew")

    frame_corpo = tk.Frame(janela, width=400, height=400, bg=co1, relief="flat")
    frame_corpo.grid(row=1, column=0, pady=1, padx=0, sticky="nsew")

    # Configurando frame logo
    imagem = Image.open('icone.png')
    imagem = imagem.resize((50, 50))
    imagem = ImageTk.PhotoImage(imagem)

    l_imagem = tk.Label(frame_logo, height=60, image=imagem, bg=co1)
    l_imagem.place(x=20, y=1)

    l_logo = tk.Label(frame_logo, text='Bloqueador de Sites', height=1, anchor='ne', font=('Ivy 25'), bg=co1, fg=co4)
    l_logo.place(x=70, y=10)

    l_linha = tk.Label(frame_logo, text='', width=445, height=1, anchor='nw', font=('Ivy 1'), bg=co2)
    l_linha.place(x=0, y=57)

    # Configurando frame corpo
    l_site = tk.Label(frame_corpo, text='Digite o site que deseja bloquear no campo abaixo * ', height=1, anchor='ne',
                    font=('Ivy 10 bold'), bg=co1, fg=co4)
    l_site.place(x=23, y=20)

    e_site = tk.Entry(frame_corpo, width=21, justify='left', font=(' ', 15), highlightthickness=1, relief='solid')
    e_site.place(x=23, y=50)

    tk.Button(frame_corpo, text='Adicionar', width=10, height=1, font=('Ivy 10 bold'),
                        relief='raised', overrelief='ridge', bg=co5, fg=co1, command=adicionar_site).place(x=267, y=50)

    tk.Button(frame_corpo, text='Remover', width=10, height=1, font=('Ivy 10 bold'),
                      relief='raised', overrelief='ridge', bg=co5, fg=co1, command=remover_site).place(x=267, y=100)

    tk.Button(frame_corpo, text='Desbloquear', width=10, height=1,
                           font=('Ivy 10 bold'), relief='raised', overrelief='ridge', bg=co2, fg=co1, command=desbloquear_site).place(x=267, y=150)

    tk.Button(frame_corpo, text='Bloquear', width=10, height=1, font=('Ivy 10 bold'),
                        relief='raised', overrelief='ridge', bg=co3, fg=co1, command=bloquear_site).place(x=267, y=200)

    listabox = tk.Listbox(frame_corpo, font=('Arial 9 bold'), width=33, height=10)
    listabox.place(x=23, y=100)

    # Chamar a função que lê os sites bloqueados
    ver_site(listabox)

    # Manter a janela aberta
    janela.mainloop()

def ver_site(listabox):
    listabox.delete(0, tk.END)
    try:
        with open('sites.csv', 'r') as file:
            ler_csv = csv.reader(file)
            for row in ler_csv:
                if row:
                    listabox.insert(tk.END, row[0])
    except FileNotFoundError:
        messagebox.showerror('Erro', 'Arquivo "sites.csv" não encontrado.')

def adicionar_site():
    site = e_site.get()
    if site:
        listabox.insert(tk.END, site)
        e_site.delete(0, tk.END)
        salvar_site(site)

def salvar_site(i):
    try:
        with open('sites.csv', 'a+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([i])
        messagebox.showinfo('Site', 'O site foi adicionado')
        ver_site(listabox)
    except Exception as e:
        messagebox.showerror('Erro', f'Erro ao salvar o site: {e}')

def remover_site():
    site = listabox.get(tk.ACTIVE)
    if site:
        deletar_site(site)

def deletar_site(i):
    nova_lista = []
    try:
        with open('sites.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] != i:
                    nova_lista.append(row)

        with open('sites.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(nova_lista)
        messagebox.showinfo('Site', 'O site foi removido')
        ver_site(listabox)
    except Exception as e:
        messagebox.showerror('Erro', f'Erro ao remover o site: {e}')

def desbloquear_site():
    iniciar.set(False)
    messagebox.showinfo('Site', 'Os sites na lista foram Desbloqueados')
    bloqueador_site()

def bloquear_site():
    iniciar.set(True)
    messagebox.showinfo('Site', 'Os sites na lista foram Bloqueados')
    bloqueador_site()

def bloqueador_site():
    local_do_host = r"C:\\Windows\\System32\\drivers\\etc\\hosts"
    redicionar = '127.0.0.1'
    websites = []

    try:
        with open('sites.csv', 'r') as file:
            ler_csv = csv.reader(file)
            for row in ler_csv:
                if row:
                    websites.append(row[0])

        if iniciar.get():
            with open(local_do_host, 'r+') as arquivo:
                conteudo = arquivo.read()
                for site in websites:
                    if site not in conteudo:
                        arquivo.write(f'\n{redicionar} {site}')
        else:
            with open(local_do_host, 'r+') as arquivo:
                conteudo = arquivo.readlines()
                arquivo.seek(0)
                for linha in conteudo:
                    if not any(site in linha for site in websites):
                        arquivo.write(linha)
                arquivo.truncate()
    except Exception as e:
        messagebox.showerror('Erro', f'Erro ao bloquear/desbloquear sites: {e}')

if __name__ == "__main__":
    login_window()
