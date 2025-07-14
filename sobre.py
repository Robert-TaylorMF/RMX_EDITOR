import tkinter as tk
import webbrowser

def abrir_github():
    webbrowser.open_new("https://github.com/Robert-TaylorMF")

def mostrar_sobre(root, versao):
    sobre = tk.Toplevel(root)
    sobre.title("Sobre o XMLEditor RM")
    sobre.geometry("400x270")
    sobre.resizable(False, False)
    sobre.configure(bg="#1e1e1e")

    tk.Label(sobre, text="XMLEditor RM", font=("Segoe UI", 16, "bold"), fg="#4fc3f7", bg="#1e1e1e").pack(pady=(20, 5))
    tk.Label(sobre, text="Editor de eventos eSocial com backup inteligente", fg="#dddddd", bg="#1e1e1e").pack(pady=2)
    tk.Label(sobre, text=f"Versão: {versao}", fg="#bbbbbb", bg="#1e1e1e").pack(pady=2)
    tk.Label(sobre, text="Desenvolvido por: Robert Taylor de M. Ferreira", fg="#81c784", bg="#1e1e1e").pack(pady=10)
    tk.Label(sobre, text="© 2025", font=("Segoe UI", 8), fg="#888888", bg="#1e1e1e").pack(pady=0)

    tk.Button(sobre, text="Ver no GitHub", command=abrir_github, bg="#2e2e2e", fg="#00afff").pack(pady=(15, 5))
    tk.Button(sobre, text="Fechar", command=sobre.destroy, bg="#2e2e2e", fg="white").pack()