import customtkinter as ctk
from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkTextbox, CTkComboBox
import tkinter as tk
from tooltip import Tooltip
from PIL import Image
from configuracao import carregar_bases, conectar_base
from conexao import obter_conexao
from verificador import verificar_driver_sql, verificar_atualizacao
from xml_operacoes import carregar_xml, salvar_xml
from splash import mostrar_splash
from sobre import mostrar_sobre
from comparador import abrir_backup
from atalhos import configurar_atalhos
from utilitarios import (
    formatar_xml, salvar_backup, realcar_sintaxe_xml,
    buscar_texto, substituir_proxima, substituir_todos,
    compactar_xml, extrair_conteudo_esocial
)
from gerenciador_bases import abrir_gerenciador_de_bases

# === Inicialização de variáveis globais ===
bases_disponiveis = carregar_bases()
substituir_posicao = "1.0"
versao = "1.3"

# === Funções auxiliares ===
def conectar_e_atualizar():
    global base_selecionada
    bases_atualizadas = carregar_bases()
    base_selecionada = conectar_base(bases_atualizadas, combo_base.get(), status_var)

def substituir_e_avancar():
    global substituir_posicao
    substituir_posicao = substituir_proxima(entry_busca, entry_substituir, text_xml, substituir_posicao)

# === Splash screen ===
mostrar_splash()

# === Janela principal com customtkinter ===
root = CTk()

# === Importação dos Icones ===

icone_base  = ctk.CTkImage(light_image=Image.open("recursos/bancos-de-dados.ico"), size=(36, 36))
icone_att   = ctk.CTkImage(light_image=Image.open("recursos/atualizar.ico"), size=(36, 36))
icone_sobre = ctk.CTkImage(light_image=Image.open("recursos/sobre-nos.ico"), size=(36, 36))
icone_conectar = ctk.CTkImage(light_image=Image.open("recursos/link.ico"), size=(36, 36))
icone_ver_backup = ctk.CTkImage(light_image=Image.open("recursos/restaurar-backup.ico"), size=(36, 36))
icone_localizar = ctk.CTkImage(light_image=Image.open("recursos/lupa.ico"), size=(30, 30))
icone_salvar = ctk.CTkImage(light_image=Image.open("recursos/salvar.ico"), size=(36, 36))

# === Menu lateral à esquerda ===
menu_lateral = ctk.CTkFrame(root, width=160, corner_radius=0)
menu_lateral.pack(side="left", fill="y")

# Título do sistema
#ctk.CTkLabel(menu_lateral, text="XMLEditor RM", font=("Arial", 18, "bold")).pack(pady=20)

# Botão: Gerenciar Bases
btn_base = ctk.CTkButton(menu_lateral, text="", image=icone_base, width=48, height=48,
                         fg_color="transparent", hover_color="#e0e0e0",
                         command=lambda: abrir_gerenciador_de_bases(root, combo_base, status_var))
btn_base.pack(pady=(10, 8))
Tooltip(btn_base, "Gerenciar Bases")

# Botão: Ver Backups
btn_backup = ctk.CTkButton(menu_lateral, text="", image=icone_ver_backup, width=48, height=48,
                           fg_color="transparent", hover_color="#e0e0e0",
                           command=lambda: abrir_backup(root, text_xml, status_var, entry_id))
btn_backup.pack(pady=8)
Tooltip(btn_backup, "Ver Backups e Comparar")

# Botão: Verificar Atualização
btn_att = ctk.CTkButton(menu_lateral, text="", image=icone_att, width=48, height=48,
                        fg_color="transparent", hover_color="#e0e0e0",
                        command=lambda: verificar_atualizacao(versao))
btn_att.pack(pady=8)
Tooltip(btn_att, "Verificar Atualização")

# Botão: Sobre — fixado no rodapé
btn_sobre = ctk.CTkButton(menu_lateral, text="", image=icone_sobre, width=48, height=48,
                          fg_color="transparent", hover_color="#e0e0e0",
                          command=lambda: mostrar_sobre(root, versao))
btn_sobre.pack(pady=8)
Tooltip(btn_sobre, "Sobre o Sistema")

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
global combo_base
combo_base = CTkComboBox(frame1, values=[b["nome"] for b in bases_disponiveis], width=200)
combo_base.grid(row=0, column=1, padx=5)
if bases_disponiveis:
    combo_base.set(bases_disponiveis[0]["nome"])
else:
    combo_base.set("Nenhuma base encontrada")
    status_var.set("Nenhuma base disponível. Cadastre uma usando o botão no canto superior.")
    root.after(1000, lambda: abrir_gerenciador_de_bases(root, combo_base, status_var))

# === Botão Conectar ===
btn_conectar = ctk.CTkButton(frame1, text="", image=icone_conectar, width=48, height=48,
                             fg_color="transparent", hover_color="#e0e0e0",
                             command=conectar_e_atualizar)
btn_conectar.grid(row=0, column=2, padx=5)
Tooltip(btn_conectar, "Conectar à Base")

CTkLabel(frame1, text="ID do Evento:").grid(row=0, column=3, padx=5)
entry_id = CTkEntry(frame1, width=350)
entry_id.grid(row=0, column=4, padx=5)

CTkButton(frame1, text="Carregar", command=lambda: carregar_xml(
    base_selecionada, entry_id.get(), text_xml, status_var
)).grid(row=0, column=5, padx=5)

# === Frame 2: Busca e substituição ===
frame2 = ctk.CTkFrame(root)
frame2.pack(pady=5, anchor="w", fill="x", padx=10)

CTkLabel(frame2, text="Buscar:").grid(row=0, column=0, padx=5, pady=5)
entry_busca = CTkEntry(frame2, width=250)
entry_busca.grid(row=0, column=1, padx=5)

# === Botão Localizar ===
btn_localizar = ctk.CTkButton(frame2, text="", image=icone_localizar, width=48, height=48,
                               fg_color="transparent", hover_color="#e0e0e0",
                               command=lambda: buscar_texto(entry_busca, text_xml))
btn_localizar.grid(row=0, column=2, padx=5)
Tooltip(btn_localizar, "Localizar")

CTkLabel(frame2, text="Substituir por:").grid(row=0, column=3, padx=5)
entry_substituir = CTkEntry(frame2, width=250)
entry_substituir.grid(row=0, column=4, padx=5)

CTkButton(frame2, text="Substituir", command=substituir_e_avancar).grid(row=0, column=5, padx=5)
CTkButton(frame2, text="Substituir todos", command=lambda: substituir_todos(entry_busca, entry_substituir, text_xml)).grid(row=0, column=6, padx=5)

# === Editor XML ===
text_xml = CTkTextbox(root, wrap="word", height=20)
text_xml.pack(padx=10, pady=10, fill="both", expand=True)

# == Rodapé ===
frame_rodape = ctk.CTkFrame(root)
frame_rodape.pack(anchor="sw", padx=10, pady=5)

# === Botão de salvar e referência para o atalho ===
botao_salvar = ctk.CTkButton(frame_rodape, text="", image=icone_salvar, width=48, height=48,
                           fg_color="transparent", hover_color="#e0e0e0",
                           command=lambda: salvar_xml(
                               base_selecionada,
                               entry_id.get(),
                               extrair_conteudo_esocial(compactar_xml(text_xml.get("1.0", "end"))),
                               text_xml
                           ))
botao_salvar.pack(side="left", padx=5)
Tooltip(botao_salvar, "Salvar XML no Banco")

# === Barra de status ===
CTkLabel(root, textvariable=status_var, text_color="skyblue").pack(pady=5)

# === Inicialização final ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
verificar_driver_sql()
configurar_atalhos(root, text_xml, status_var, base_selecionada, entry_id, botao_salvar)

root.mainloop()