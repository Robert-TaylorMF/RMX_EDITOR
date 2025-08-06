import tkinter as tk
import customtkinter as ctk
from comparador import abrir_backup
from utilitarios import abrir_localizador_substituir, restaurar_formatacao, formatar_xml_editor

# 🧠 Funções globais de edição
def desfazer(editor_frame):
    if hasattr(editor_frame, "editor_texto"):
        text_widget = editor_frame.editor_texto
    else:
        text_widget = editor_frame
    try:
        text_widget.edit_undo()
        # NÃO chama restaurar_formatacao aqui para manter undo granular
        # restaurar_formatacao(text_widget)
    except tk.TclError:
        pass

def refazer(editor_frame):
    if hasattr(editor_frame, "editor_texto"):
        text_widget = editor_frame.editor_texto
    else:
        text_widget = editor_frame
    try:
        text_widget.edit_redo()
        # NÃO chama restaurar_formatacao aqui
        # restaurar_formatacao(text_widget)
    except tk.TclError:
        pass

# Chamar restaurar_formatacao no evento <KeyRelease> para aplicar formatação após digitação:
def aplicar_formatacao_com_undo(text_widget):
    def on_key_release(event):
        # Adiciona separator antes de formatar para marcar um ponto para undo
        text_widget.edit_separator()
        restaurar_formatacao(text_widget)
        text_widget.edit_separator()
    text_widget.bind("<KeyRelease>", on_key_release)

# 🧩 Configuração de atalhos globais
def configurar_atalhos(root, painel_guias, status_var, base_config, entry_id, botao_salvar):
    def obter_text_widget():
        editor_frame = painel_guias.obter_editor_ativo()
        if editor_frame and hasattr(editor_frame, "editor_texto"):
            return editor_frame.editor_texto
        return None

    root.bind_all("<Control-s>", lambda e: (botao_salvar.invoke(), "break"))
    root.bind_all("<Control-f>", lambda e: (abrir_localizador_substituir(obter_text_widget(), root), "break"))
    root.bind_all("<Control-b>", lambda e: (abrir_backup(root, painel_guias, painel_guias.obter_nome_guia_ativa(), status_var), "break"))
    root.bind_all("<Control-z>", lambda e: desfazer(painel_guias.obter_editor_ativo()))
    root.bind_all("<Control-y>", lambda e: refazer(painel_guias.obter_editor_ativo()))
    root.bind_all("<Control-c>", lambda e: (copiar_selecao(root, obter_text_widget()), "break"))
    root.bind_all("<Control-Shift-F>", lambda e: formatar_xml_editor(painel_guias.obter_editor_ativo()))

def copiar_selecao(root, text_widget):
    if text_widget is None:
        return
    try:
        texto = text_widget.get("sel.first", "sel.last")
        root.clipboard_clear()
        root.clipboard_append(texto)
    except tk.TclError:
        pass  # Nenhuma seleção ativa
