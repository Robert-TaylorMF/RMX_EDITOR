import customtkinter as ctk
import webbrowser

def abrir_github():
    webbrowser.open_new("https://github.com/Robert-TaylorMF")

def mostrar_sobre(root, versao):
    sobre = ctk.CTkToplevel(root)
    sobre.title("Sobre o XMLEditor RM")
    sobre.geometry("400x300")
    sobre.resizable(False, False)

    # === Garantir que a janela venha à frente ===
    sobre.transient(root)
    sobre.grab_set()
    sobre.focus_force()
    sobre.lift()

    ctk.CTkLabel(sobre, text="XMLEditor RM", font=("Segoe UI", 18, "bold")).pack(pady=(20, 5))
    ctk.CTkLabel(sobre, text="Editor de eventos eSocial com backup inteligente").pack(pady=2)
    ctk.CTkLabel(sobre, text=f"Versão: {versao}", text_color="#aaaaaa").pack(pady=2)
    ctk.CTkLabel(sobre, text="Desenvolvido por: Robert Taylor de M. Ferreira", text_color="#90ee90").pack(pady=10)
    ctk.CTkLabel(sobre, text="© 2025", font=("Segoe UI", 8), text_color="#888888").pack(pady=0)

    ctk.CTkButton(sobre, text="Ver no GitHub", command=abrir_github).pack(pady=(15, 5))
    ctk.CTkButton(sobre, text="Fechar", command=sobre.destroy).pack()