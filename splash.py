import tkinter as tk
import time
from PIL import Image, ImageTk
import os
import sys

def obter_caminho(imagem_relativa):
    if getattr(sys, 'frozen', False):
        caminho_base = sys._MEIPASS
    else:
        caminho_base = os.path.dirname(__file__)
    return os.path.join(caminho_base, imagem_relativa)

def mostrar_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg="#1e1e1e")

    largura, altura = 400, 250
    pos_x = splash.winfo_screenwidth() // 2 - largura // 2
    pos_y = splash.winfo_screenheight() // 2 - altura // 2
    splash.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    caminho_logo = obter_caminho("recursos/logo_splash.png")
    imagem_logo = Image.open(caminho_logo).resize((100, 100))
    img_logo = ImageTk.PhotoImage(imagem_logo)

    tk.Label(splash, image=img_logo, bg="#1e1e1e").pack(pady=15)
    tk.Label(splash, text="XMLEditor RM", font=("Segoe UI", 18, "bold"),
             bg="#1e1e1e", fg="#00ccff").pack()
    tk.Label(splash, text="Inicializando ambiente XML...",
             font=("Segoe UI", 10), bg="#1e1e1e", fg="white").pack(pady=5)

    splash.update()
    time.sleep(2.5)
    splash.destroy()