import tkinter as tk
import customtkinter as ctk
from comparador import abrir_backup
from utilitarios import abrir_localizador

# 🧠 Funções globais de edição
def desfazer(text_widget):
    try:
        text_widget.edit_undo()
    except tk.TclError:
        pass

def refazer(text_widget):
    try:
        text_widget.edit_redo()
    except tk.TclError:
        pass

# 🧩 Configuração de atalhos globais
def configurar_atalhos(root, text_xml, status_var, base_config, entry_id, botao_salvar):
    root.bind_all("<Control-s>", lambda e: botao_salvar.invoke())
    root.bind("<Control-f>", lambda e: abrir_localizador(text_xml, root))
    root.bind_all("<Control-b>", lambda e: abrir_backup(root, text_xml, status_var))
    root.bind("<Control-z>", lambda e: desfazer(text_xml))
    root.bind("<Control-y>", lambda e: refazer(text_xml))
    root.bind("<Control-c>", lambda e: root.clipboard_clear() or root.clipboard_append(text_xml.get("sel.first", "sel.last")))