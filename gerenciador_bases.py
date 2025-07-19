import customtkinter as ctk
from PIL import Image
from tkinter import messagebox
from configuracao import carregar_bases, salvar_nova_base, excluir_base
from seguranca import criptografar_senha
from tooltip import Tooltip

icone_adicionar = ctk.CTkImage(light_image=Image.open("recursos/adicionar_banco.ico"), size=(32, 32))
icone_editar    = ctk.CTkImage(light_image=Image.open("recursos/editar_banco.ico"), size=(32, 32))
icone_remover   = ctk.CTkImage(light_image=Image.open("recursos/remover_banco.ico"), size=(32, 32))

def abrir_gerenciador_de_bases(root, combo=None, status=None):
    janela = ctk.CTkToplevel(root)
    janela.title("Gerenciador de Bases")
    janela.geometry("440x300")
    janela.resizable(False, False)
    janela.grab_set()

    lista_bases = ctk.CTkComboBox(janela, values=[], width=400)
    lista_bases.pack(pady=10)

    campos = {}
    for nome in ["nome", "host", "usuario", "senha", "database"]:
        campo = ctk.CTkEntry(janela, placeholder_text=nome.capitalize(), width=400)
        campo.pack(pady=3)
        campos[nome] = campo
    campos["senha"].configure(show="*")

    frame_botoes = ctk.CTkFrame(janela, fg_color="transparent")
    frame_botoes.pack(pady=10, anchor="w", padx=20)

    def efeito_hover(botao, cor_hover):
        botao.bind("<Enter>", lambda e: botao.configure(fg_color=cor_hover))
        botao.bind("<Leave>", lambda e: botao.configure(fg_color="transparent"))

    def validar_campos():
        todos_validos = True
        for chave, campo in campos.items():
            valor = campo.get().strip()
            valido = bool(valor)
            cor = "#00cc66" if valido else "#ff4444"
            campo.configure(border_color=cor)
            if not valido and chave != "senha":
                todos_validos = False
        btn_incluir.configure(state="normal" if todos_validos else "disabled")

    def atualizar_lista():
        bases = carregar_bases()
        nomes = [b["nome"] for b in bases]
        lista_bases.configure(values=nomes)
        lista_bases.set(nomes[0] if nomes else "Nenhuma base")
        atualizar_estado_botoes()

    def salvar_base():
        nova = {
            "nome": campos["nome"].get().strip(),
            "host": campos["host"].get().strip(),
            "usuario": campos["usuario"].get().strip(),
            "senha": criptografar_senha(campos["senha"].get()),
            "database": campos["database"].get().strip()
        }
        if not nova["nome"]:
            messagebox.showwarning("Atenção", "O nome da base é obrigatório.")
            return
        salvar_nova_base(nova)
        messagebox.showinfo("Base salva", f"Base '{nova['nome']}' cadastrada com sucesso!")
        atualizar_lista()
        if combo:
            novas_bases = carregar_bases()
            nomes = [b["nome"] for b in novas_bases]
            combo.configure(values=nomes)
            combo.set(nova["nome"])
        if status:
            status.set("✅ Nova base cadastrada e carregada com sucesso.")
        for campo in campos.values():
            campo.delete(0, "end")
        validar_campos()

    def carregar_base_selecionada_por_nome():
        nome = lista_bases.get()
        if not nome or nome == "Nenhuma base":
            messagebox.showwarning("Atenção", "Selecione uma base para carregar.")
            return
        bases = carregar_bases()
        base = next((b for b in bases if b["nome"] == nome), None)
        if base:
            campos["nome"].delete(0, "end")
            campos["nome"].insert(0, base["nome"])
            campos["host"].delete(0, "end")
            campos["host"].insert(0, base["host"])
            campos["usuario"].delete(0, "end")
            campos["usuario"].insert(0, base["usuario"])
            campos["senha"].delete(0, "end")
            campos["database"].delete(0, "end")
            campos["database"].insert(0, base["database"])
            validar_campos()

    def remover_base():
        nome = lista_bases.get()
        if not nome or nome == "Nenhuma base":
            messagebox.showwarning("Atenção", "Selecione uma base para excluir.")
            return
        resposta = messagebox.askyesno("Confirmação", f"Excluir a base '{nome}'?")
        if resposta:
            excluir_base(nome)
            messagebox.showinfo("Removido", f"Base '{nome}' excluída com sucesso.")
            atualizar_lista()
            for campo in campos.values():
                campo.delete(0, "end")
            validar_campos()

    def atualizar_estado_botoes():
        nome = lista_bases.get()
        estado = "normal" if nome and nome != "Nenhuma base" else "disabled"
        btn_editar.configure(state=estado)
        btn_excluir.configure(state=estado)

    btn_incluir = ctk.CTkButton(frame_botoes, text="", image=icone_adicionar, width=48, height=48,
        fg_color="transparent", command=salvar_base)
    btn_incluir.pack(side="left", padx=5)
    efeito_hover(btn_incluir, "#d1ffd1")
    Tooltip(btn_incluir, "Incluir Nova Base")

    btn_editar = ctk.CTkButton(frame_botoes, text="", image=icone_editar, width=48, height=48,
        fg_color="transparent", command=carregar_base_selecionada_por_nome)
    btn_editar.pack(side="left", padx=5)
    efeito_hover(btn_editar, "#d1e4ff")
    Tooltip(btn_editar, "Editar Base Selecionada")

    btn_excluir = ctk.CTkButton(frame_botoes, text="", image=icone_remover, width=48, height=48,
        fg_color="transparent", command=remover_base)
    btn_excluir.pack(side="left", padx=5)
    efeito_hover(btn_excluir, "#ffe1e1")
    Tooltip(btn_excluir, "Excluir Base")

    lista_bases.bind("<<ComboboxSelected>>", lambda e: atualizar_estado_botoes())
    for campo in campos.values():
        campo.bind("<KeyRelease>", lambda e: validar_campos())

    validar_campos()
    atualizar_lista()