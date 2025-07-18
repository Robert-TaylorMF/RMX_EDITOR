import customtkinter as ctk
import win32print
import win32api
import tempfile
import subprocess
import time
import os

def abrir_janela_impressao(editor_texto):
    conteudo = editor_texto.get("1.0", "end").strip()
    if not conteudo:
        return

    impressoras = [printer[2] for printer in win32print.EnumPrinters(2)]
    padrao = win32print.GetDefaultPrinter()

    janela = ctk.CTkToplevel()
    janela.title("Selecionar Impressora")
    janela.geometry("480x350")
    janela.grab_set()
    janela.resizable(False, False)

    ctk.CTkLabel(janela, text="🖨️ Impressoras disponíveis", font=("Segoe UI", 16)).pack(pady=(20, 10))
    lista_frame = ctk.CTkScrollableFrame(janela, height=220)
    lista_frame.pack(padx=15, fill="both")

    def imprimir_para(printer_name):
        try:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp:
                temp.write(conteudo)
                caminho = temp.name

            win32print.SetDefaultPrinter(printer_name)

            # Usa ShellExecute apenas se impressora estiver operacional
            resultado = win32api.ShellExecute(0, "print", caminho, None, ".", 0)

            # Espera um pouco antes de fechar a janela
            janela.after(800, janela.destroy)

        except Exception as e:
            print(f"❌ Erro ao imprimir com {printer_name}:", e)

    for nome in impressoras:
        cor_hover = "#3399ff" if nome == padrao else "#444444"
        texto_btn = f"{nome} 🟢 (padrão)" if nome == padrao else nome
        botao = ctk.CTkButton(
            lista_frame,
            text=texto_btn,
            command=lambda n=nome: imprimir_para(n),
            width=420,
            corner_radius=6,
            fg_color="#333333",
            hover_color=cor_hover
        )
        botao.pack(pady=6, padx=10)