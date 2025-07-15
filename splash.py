import customtkinter as ctk
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
    splash = ctk.CTk()
    splash.overrideredirect(True)

    largura, altura = 400, 250
    pos_x = splash.winfo_screenwidth() // 2 - largura // 2
    pos_y = splash.winfo_screenheight() // 2 - altura // 2
    splash.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")
    splash.configure(fg_color="#1e1e1e")

    caminho_logo = obter_caminho("recursos/logo_splash.png")
    imagem_logo = Image.open(caminho_logo).resize((100, 100))
    img_logo = ImageTk.PhotoImage(imagem_logo)

    logo_label = ctk.CTkLabel(splash, image=img_logo, text="")
    logo_label.image = img_logo
    logo_label.pack(pady=15)

    ctk.CTkLabel(splash, text="XMLEditor RM", font=("Segoe UI", 18, "bold"), text_color="#00ccff").pack()
    ctk.CTkLabel(splash, text="Inicializando ambiente XML...", font=("Segoe UI", 10), text_color="white").pack(pady=5)

    splash.update()
    time.sleep(2.5)
    splash.destroy()