import tkinter as tk
import customtkinter as ctk
from comparador import abrir_backup
from utilitarios import abrir_localizador

# 🧠 Funções globais de edição
def desfazer(editor_frame):
    if hasattr(editor_frame, "editor_texto"):
        text_widget = editor_frame.editor_texto
    else:
        text_widget = editor_frame
    try:
        text_widget.edit_undo()
    except tk.TclError:
        pass

def refazer(editor_frame):
    if hasattr(editor_frame, "editor_texto"):
        text_widget = editor_frame.editor_texto
    else:
        text_widget = editor_frame
    try:
        text_widget.edit_redo()
    except tk.TclError:
        pass

# 🧩 Configuração de atalhos globais
def configurar_atalhos(root, painel_guias, status_var, base_config, entry_id, botao_salvar):
    def obter_text_widget():
        editor_frame = painel_guias.obter_editor_ativo()
        if editor_frame is None:
            return None
        return editor_frame.editor_texto if hasattr(editor_frame, "editor_texto") else editor_frame

    root.bind_all("<Control-s>", lambda e: botao_salvar.invoke())

    root.bind("<Control-f>", lambda e: abrir_localizador(obter_text_widget(), root))

    root.bind_all("<Control-b>", lambda e: abrir_backup(root, obter_text_widget(), status_var))

    root.bind("<Control-z>", lambda e: desfazer(painel_guias.obter_editor_ativo()))
    root.bind("<Control-y>", lambda e: refazer(painel_guias.obter_editor_ativo()))

    root.bind("<Control-c>", lambda e: copiar_selecao(root, obter_text_widget()))

def copiar_selecao(root, text_widget):
    if text_widget is None:
        return
    try:
        texto = text_widget.get("sel.first", "sel.last")
        root.clipboard_clear()
        root.clipboard_append(texto)
    except tk.TclError:
        pass  # Nenhuma seleção ativa