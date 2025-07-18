import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from modulos.editor_com_linhas import criar_editor_com_linhas
from utilitarios import realcar_sintaxe_xml
from tooltip import Tooltip

class PainelDeGuias(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        self.contador = 0
        self.editores = {}  # nome → (frame, editor)
        self.botoes = {}    # nome → botão guia

        # Painel superior com abas simuladas
        self.top_bar = ctk.CTkFrame(self)
        self.top_bar.pack(fill="x", padx=10, pady=(10, 0))

        # Ícone do botão Nova Guia
        icone_nova_guia = CTkImage(light_image=Image.open("recursos/mais.ico"), size=(24, 24))

        # Botão “Nova Guia” com imagem
        btn_nova = ctk.CTkButton(
            self.top_bar,
            text="",
            image=icone_nova_guia,
            width=48,
            height=48,
            fg_color="transparent",
            hover_color="#e0e0e0",
            command=self.criar_guia
        )
        btn_nova.pack(side="left", padx=6)
        Tooltip(btn_nova, "Abrir nova guia")

        # Área de conteúdo da guia
        self.area_guia = ctk.CTkFrame(self)
        self.area_guia.pack(expand=True, fill="both", padx=10, pady=10)

        # Cria a primeira guia
        self.criar_guia()

    def criar_guia(self):
        self.contador += 1
        nome = f"Guia {self.contador}"

        # Botão de guia + botão de fechar lado a lado
        frame_guia_btn = ctk.CTkFrame(self.top_bar, fg_color="transparent")
        frame_guia_btn.pack(side="left", padx=4)

        btn_guia = ctk.CTkButton(
            frame_guia_btn,
            text=nome,
            width=80,
            fg_color="#333333",
            hover_color="#22a6f5",
            text_color="white",
            command=lambda: self.ativar_guia(nome)
        )
        btn_guia.pack(side="left")

        btn_fechar = ctk.CTkButton(
            frame_guia_btn,
            text="❌",
            width=32,
            fg_color="transparent",
            hover_color="#550000",
            text_color="gray",
            command=lambda: self.fechar_guia(nome, frame_guia_btn)
        )
        btn_fechar.pack(side="left")

        self.botoes[nome] = btn_guia

        # Editor embutido
        frame_guia = ctk.CTkFrame(self.area_guia)
        editor = criar_editor_com_linhas(frame_guia)
        editor.pack(expand=True, fill="both", padx=10, pady=10)
        realcar_sintaxe_xml(editor.editor_texto)

        self.editores[nome] = (frame_guia, editor)

        self.ativar_guia(nome)

    def ativar_guia(self, nome):
        # Remove guia anterior
        for f, _ in self.editores.values():
            f.pack_forget()

        # Mostra guia atual
        frame, _ = self.editores[nome]
        frame.pack(expand=True, fill="both")

        # Destaque visual nos botões
        for nome_btn, btn in self.botoes.items():
            if nome_btn == nome:
                btn.configure(fg_color="#22a6f5", text_color="white")
            else:
                btn.configure(fg_color="#333333", text_color="#cccccc")

    def fechar_guia(self, nome, frame_btn):
        # Remover editor
        if nome in self.editores:
            frame, _ = self.editores[nome]
            frame.destroy()
            del self.editores[nome]

        # Remover botão de guia
        if nome in self.botoes:
            del self.botoes[nome]

        frame_btn.destroy()

        # Selecionar outra guia, se houver
        if self.editores:
            nova = next(iter(self.editores))
            self.ativar_guia(nova)

    def obter_editor_ativo(self):
        for nome in self.editores:
            frame, editor_frame = self.editores[nome]
            if frame.winfo_ismapped():
                return editor_frame
        return None

