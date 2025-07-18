import customtkinter as ctk
from customtkinter import CTkImage
from PIL import Image
from modulos.editor_com_linhas import criar_editor_com_linhas
from utilitarios import realcar_sintaxe_xml
from tooltip import Tooltip
import tkinter as tk  # necessário para manipular entry_id

class PainelDeGuias(ctk.CTkFrame):
    def __init__(self, master, entry_id):
        super().__init__(master)
        self.entry_id = entry_id
        self.contador = 0
        self.editores = {}  # nome → {frame, editor, base, evento_id}
        self.botoes = {}    # nome → botão guia

        self.top_bar = ctk.CTkFrame(self)
        self.top_bar.pack(fill="x", padx=10, pady=(10, 0))

        icone_nova_guia = CTkImage(light_image=Image.open("recursos/mais.ico"), size=(24, 24))

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

        self.area_guia = ctk.CTkFrame(self)
        self.area_guia.pack(expand=True, fill="both", padx=10, pady=10)

        self.criar_guia()

    def criar_guia(self):
        self.contador += 1
        nome = f"Guia {self.contador}"

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

        frame_guia = ctk.CTkFrame(self.area_guia)
        editor = criar_editor_com_linhas(frame_guia)
        editor.pack(expand=True, fill="both", padx=10, pady=10)
        realcar_sintaxe_xml(editor.editor_texto)

        self.editores[nome] = {
            "frame": frame_guia,
            "editor": editor,
            "evento_id": None,
            "base": None
        }

        self.ativar_guia(nome)

    def ativar_guia(self, nome):
        # Oculta todas as guias
        for guia in self.editores.values():
            guia["frame"].pack_forget()

        # Exibe a guia atual
        self.editores[nome]["frame"].pack(expand=True, fill="both")

        # Destaque visual nos botões
        for nome_btn, btn in self.botoes.items():
            if nome_btn == nome:
                btn.configure(fg_color="#22a6f5", text_color="white")
            else:
                btn.configure(fg_color="#333333", text_color="#cccccc")

        # 🔄 Sincroniza o campo entry_id com o evento_id da guia ativa
        evento_id = self.editores[nome].get("evento_id")
        if evento_id is not None and self.entry_id:
            self.entry_id.delete(0, tk.END)
            self.entry_id.insert(0, str(evento_id))

    def fechar_guia(self, nome, frame_btn):
        if nome in self.editores:
            self.editores[nome]["frame"].destroy()
            del self.editores[nome]

        if nome in self.botoes:
            del self.botoes[nome]

        frame_btn.destroy()

        if self.editores:
            nova = next(iter(self.editores))
            self.ativar_guia(nova)

    def obter_editor_ativo(self):
        for nome, guia in self.editores.items():
            if guia["frame"].winfo_ismapped():
                return guia["editor"]
        return None

    def obter_nome_guia_ativa(self):
        for nome, guia in self.editores.items():
            if guia["frame"].winfo_ismapped():
                return nome
        return None