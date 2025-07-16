import customtkinter as ctk
from tkinter import messagebox
from configuracao import carregar_bases, salvar_nova_base, excluir_base
from seguranca import criptografar_senha

def abrir_gerenciador_de_bases(root, combo=None, status=None):
    janela = ctk.CTkToplevel(root)
    janela.title("Gerenciador de Bases")
    janela.geometry("460x400")
    janela.grab_set()

    lista_bases = ctk.CTkComboBox(janela, values=[], width=400)
    lista_bases.pack(pady=10)

    def atualizar_lista():
        bases = carregar_bases()
        nomes = [b["nome"] for b in bases]
        lista_bases.configure(values=nomes)
        lista_bases.set("") if nomes else lista_bases.set("Nenhuma base")

    atualizar_lista()

    # Campos
    campo_nome = ctk.CTkEntry(janela, placeholder_text="Nome da base", width=400)
    campo_host = ctk.CTkEntry(janela, placeholder_text="Host/IP", width=400)
    campo_usuario = ctk.CTkEntry(janela, placeholder_text="Usuário", width=400)
    campo_senha = ctk.CTkEntry(janela, placeholder_text="Senha", show="*", width=400)
    campo_database = ctk.CTkEntry(janela, placeholder_text="Database", width=400)

    for campo in [campo_nome, campo_host, campo_usuario, campo_senha, campo_database]:
        campo.pack(pady=3)

    def salvar_base():
        if not campo_nome.get():
            messagebox.showwarning("Atenção", "O nome da base é obrigatório.")
            return
        nova = {
            "nome": campo_nome.get(),
            "host": campo_host.get(),
            "usuario": campo_usuario.get(),
            "senha": criptografar_senha(campo_senha.get()),
            "database": campo_database.get()
        }
        salvar_nova_base(nova)
        messagebox.showinfo("Base salva", f"Base '{nova['nome']}' cadastrada com sucesso!")
        atualizar_lista()
        
        # Atualiza combo_base no main.py após salvar nova base
        if combo:
            novas_bases = carregar_bases()
            nomes = [b["nome"] for b in novas_bases]
            combo.configure(values=nomes)
            combo.set(nova["nome"])
        if status:
            status.set("✅ Nova base cadastrada e carregada com sucesso.")

    ctk.CTkButton(janela, text="Salvar Base", command=salvar_base).pack(pady=10)

    def carregar_base_selecionada():
        nome = lista_bases.get()
        bases = carregar_bases()
        base = next((b for b in bases if b["nome"] == nome), None)
        if base:
            campo_nome.delete(0, "end")
            campo_nome.insert(0, base["nome"])
            campo_host.delete(0, "end")
            campo_host.insert(0, base["host"])
            campo_usuario.delete(0, "end")
            campo_usuario.insert(0, base["usuario"])
            campo_senha.delete(0, "end")
            campo_database.delete(0, "end")
            campo_database.insert(0, base["database"])
            
    ctk.CTkButton(janela, text="Carregar Base Selecionada", command=carregar_base_selecionada).pack(pady=5)
            
    def remover_base():
        nome = lista_bases.get()
        if not nome:
            messagebox.showwarning("Atenção", "Selecione uma base para excluir.")
            return
        resposta = messagebox.askyesno("Confirmação", f"Excluir a base '{nome}'?")
        if resposta:
            excluir_base(nome)
            messagebox.showinfo("Removido", f"Base '{nome}' excluída com sucesso.")
            atualizar_lista()
            campo_nome.delete(0, "end")
            campo_host.delete(0, "end")
            campo_usuario.delete(0, "end")
            campo_senha.delete(0, "end")
            campo_database.delete(0, "end")
    
    ctk.CTkButton(janela, text="Excluir Base", fg_color="#cc3333", hover_color="#a30000", command=remover_base).pack(pady=5)