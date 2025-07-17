import customtkinter as ctk

def desfazer(text_xml):
    try:
        text_xml.edit_undo()
    except tk.TclError:
        pass  # nada para desfazer
def refazer():
    try:
        text_xml.edit_redo()
    except tk.TclError:
        pass  # nada para refazer

def configurar_atalhos(root, text_xml, status_var, base_selecionada, entry_id, botao_salvar):
    
    from comparador import abrir_backup
    from utilitarios import abrir_localizador

    # 🧩 Binds de atalhos globais
    root.bind_all("<Control-s>", lambda e: botao_salvar.invoke())
    root.bind("<Control-f>", lambda e: abrir_localizador(text_xml, root))
    root.bind_all("<Control-b>", lambda e: abrir_backup(root, text_xml, status_var))
    root.bind("<Control-z>", lambda e: desfazer())
    root.bind("<Control-y>", lambda e: refazer())