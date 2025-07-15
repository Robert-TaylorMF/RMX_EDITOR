import customtkinter as ctk
from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkTextbox, CTkComboBox
from configuracao import obter_caminho, carregar_bases, conectar_base
from conexao import obter_conexao
from verificador import verificar_driver_sql, verificar_atualizacao
from xml_operacoes import carregar_xml, salvar_xml
from splash import mostrar_splash
from sobre import mostrar_sobre
from comparador import abrir_backup
from atalhos import configurar_atalhos
from utilitarios import (
    formatar_xml, salvar_backup, realcar_sintaxe_xml,
    buscar_texto, substituir_proxima, substituir_todos
)
from gerenciador_bases import abrir_gerenciador_de_bases

# === Inicialização de variáveis globais ===
bases_disponiveis = carregar_bases()
substituir_posicao = "1.0"
versao = "1.3"
modo_escuro_ativo = True  # placeholder para controle futuro de tema

# === Funções auxiliares ===
def conectar_e_atualizar():
    global base_selecionada
    base_selecionada = conectar_base(bases_disponiveis, combo_base.get(), status_var)

def substituir_e_avancar():
    global substituir_posicao
    substituir_posicao = substituir_proxima(entry_busca, entry_substituir, text_xml, substituir_posicao)

# === Splash screen ===
mostrar_splash()

# === Janela principal com customtkinter ===
root = CTk()
status_var = ctk.StringVar()
base_selecionada = ctk.StringVar(master=root, value="Selecione a base")
root.iconbitmap("recursos/xmleditor.ico")
root.state("zoomed")
root.title(f"XMLEditor RM – Editor de XML eSocial v{versao}")
root.after(100, lambda: root.state("zoomed"))
root.minsize(width=1350, height=740)

# === Frame superior ===
frame1 = ctk.CTkFrame(root)
frame1.pack(pady=10, anchor="w", fill="x", padx=10)

CTkLabel(frame1, text="Base:").grid(row=0, column=0, padx=5, pady=5)
combo_base = CTkComboBox(frame1, values=[b["nome"] for b in bases_disponiveis], width=200)
combo_base.grid(row=0, column=1, padx=5)
if bases_disponiveis:
    combo_base.set(bases_disponiveis[0]["nome"])
else:
    combo_base.set("Nenhuma base encontrada")
    status_var.set("Nenhuma base disponível. Cadastre uma usando o botão no canto superior.")
    root.after(1000, lambda: abrir_gerenciador_de_bases(root))

CTkButton(frame1, text="Conectar", command=conectar_e_atualizar).grid(row=0, column=2, padx=5)

CTkLabel(frame1, text="ID do Evento:").grid(row=0, column=3, padx=5)
entry_id = CTkEntry(frame1, width=350)
entry_id.grid(row=0, column=4, padx=5)

CTkButton(frame1, text="Carregar", command=lambda: carregar_xml(
    base_selecionada, entry_id.get(), text_xml, status_var
)).grid(row=0, column=5, padx=5)

# Botão de salvar e referência para o atalho
botao_salvar = CTkButton(
    frame1,
    text="Salvar",
    command=lambda: salvar_xml(
        base_selecionada,
        entry_id.get(),
        text_xml.get("1.0", "end").strip(),
        text_xml
    )
)
botao_salvar.grid(row=0, column=6, padx=5)

CTkButton(frame1, text="Ver Backup", command=lambda: abrir_backup(
    root, text_xml, status_var, modo_escuro_ativo
)).grid(row=0, column=7, padx=5)

# Botão Gerenciar Bases — destacado no canto direito!
botao_gerenciar = CTkButton(
    root,
    text="🗂️ Gerenciar Bases",
    fg_color="#0077cc",
    hover_color="#005fa3",
    text_color="white",
    corner_radius=8,
    command=lambda: abrir_gerenciador_de_bases(root)
)
botao_gerenciar.place(relx=1.0, y=10, anchor="ne")

# === Frame 2: Busca e substituição ===
frame2 = ctk.CTkFrame(root)
frame2.pack(pady=5, anchor="w", fill="x", padx=10)

CTkLabel(frame2, text="Buscar:").grid(row=0, column=0, padx=5, pady=5)
entry_busca = CTkEntry(frame2, width=250)
entry_busca.grid(row=0, column=1, padx=5)

CTkLabel(frame2, text="Substituir por:").grid(row=0, column=2, padx=5)
entry_substituir = CTkEntry(frame2, width=250)
entry_substituir.grid(row=0, column=3, padx=5)

CTkButton(frame2, text="Localizar", command=lambda: buscar_texto(entry_busca, text_xml)).grid(row=0, column=4, padx=5)
CTkButton(frame2, text="Substituir", command=substituir_e_avancar).grid(row=0, column=5, padx=5)
CTkButton(frame2, text="Substituir todos", command=lambda: substituir_todos(entry_busca, entry_substituir, text_xml)).grid(row=0, column=6, padx=5)

# === Editor XML ===
text_xml = CTkTextbox(root, wrap="word", height=20)
text_xml.pack(padx=10, pady=10, fill="both", expand=True)

# === Barra de status ===
CTkLabel(root, textvariable=status_var, text_color="skyblue").pack(pady=5)

# === Botões adicionais ===
CTkButton(root, text="Verificar Atualização", command=lambda: verificar_atualizacao(versao)).pack(pady=8)
CTkButton(root, text="Sobre", command=lambda: mostrar_sobre(root, versao)).pack(pady=4)

# === Inicialização final ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
verificar_driver_sql()
configurar_atalhos(root, text_xml, status_var, base_selecionada, entry_id, botao_salvar)

root.mainloop()