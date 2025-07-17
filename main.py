# === Importações ===
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
    compactar_xml, extrair_conteudo_esocial, abrir_localizador
)
from gerenciador_bases import abrir_gerenciador_de_bases
from modulos.editor_com_linhas import criar_editor_com_linhas

# === Inicialização de variáveis globais ===
bases_disponiveis = carregar_bases()
versao = "1.3"

# === Splash screen ===
mostrar_splash()

# === Janela principal com customtkinter ===
root = CTk()

# === Importação dos Ícones ===
icone_base         = ctk.CTkImage(light_image=Image.open("recursos/bancos-de-dados.ico"), size=(36, 36))
icone_att          = ctk.CTkImage(light_image=Image.open("recursos/atualizar.ico"), size=(36, 36))
icone_sobre        = ctk.CTkImage(light_image=Image.open("recursos/sobre-nos.ico"), size=(36, 36))
icone_conectar     = ctk.CTkImage(light_image=Image.open("recursos/link.ico"), size=(36, 36))
icone_ver_backup   = ctk.CTkImage(light_image=Image.open("recursos/restaurar-backup.ico"), size=(36, 36))
icone_localizar    = ctk.CTkImage(light_image=Image.open("recursos/lupa.ico"), size=(24, 24))
icone_salvar       = ctk.CTkImage(light_image=Image.open("recursos/salvar.ico"), size=(24, 24))

# === Menu lateral à esquerda ===
menu_lateral = ctk.CTkFrame(root, width=160, corner_radius=0)
menu_lateral.pack(side="left", fill="y")

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

# Botão: Sobre
btn_sobre = ctk.CTkButton(menu_lateral, text="", image=icone_sobre, width=48, height=48,
                          fg_color="transparent", hover_color="#e0e0e0",
                          command=lambda: mostrar_sobre(root, versao))
btn_sobre.pack(pady=8)
Tooltip(btn_sobre, "Sobre o Sistema")

# === Configurações iniciais ===
status_var = ctk.StringVar()
base_selecionada = ctk.StringVar(master=root, value="Selecione a base")
root.iconbitmap("recursos/xmleditor.ico")
root.title(f"XMLEditor RM – Editor de XML eSocial v{versao}")
root.state("zoomed")
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
    root.after(1000, lambda: abrir_gerenciador_de_bases(root, combo_base, status_var))

# Botão: Conectar
btn_conectar = ctk.CTkButton(frame1, text="", image=icone_conectar, width=48, height=48,
                             fg_color="transparent", hover_color="#e0e0e0",
                             command=lambda: conectar_base(bases_disponiveis, combo_base.get(), status_var))
btn_conectar.grid(row=0, column=2, padx=5)
Tooltip(btn_conectar, "Conectar à Base")

CTkLabel(frame1, text="ID do Evento:").grid(row=0, column=3, padx=5)
entry_id = CTkEntry(frame1, width=350)
entry_id.grid(row=0, column=4, padx=5)

CTkButton(frame1, text="Carregar", command=lambda: carregar_xml(
    base_selecionada, entry_id.get(), text_xml, status_var
)).grid(row=0, column=5, padx=5)

# === Barra de ferramentas com ícones ===
frame_toolbar = ctk.CTkFrame(root, height=44)
frame_toolbar.pack(pady=5, anchor="w", fill="x", padx=10)

# Ícone lupa (abre tela de busca/substituição)
btn_lupa = ctk.CTkButton(frame_toolbar, text="", image=icone_localizar, width=48, height=48,
                         fg_color="transparent", hover_color="#e0e0e0",
                         command=lambda: abrir_localizador(text_xml, root)
)
btn_lupa.pack(side="left", padx=5)
Tooltip(btn_lupa, "Localizar e Substituir (Ctrl+F)")

botao_salvar = ctk.CTkButton(frame_toolbar, text="", image=icone_salvar, width=48, height=48,
                             fg_color="transparent", hover_color="#e0e0e0",
                             command=lambda: salvar_xml(
                                 base_selecionada,
                                 entry_id.get(),
                                 extrair_conteudo_esocial(compactar_xml(text_xml.get("1.0", "end"))),
                                 text_xml
                             ))
botao_salvar.pack(side="left", padx=5)
Tooltip(botao_salvar, "Salvar XML no Banco")

# === Editor XML com numeração ===
text_xml = criar_editor_com_linhas(root)

# === Barra de status ===
CTkLabel(root, textvariable=status_var, text_color="skyblue").pack(pady=5)

# === Inicialização final ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
verificar_driver_sql()
configurar_atalhos(root, text_xml, status_var, base_selecionada, entry_id, botao_salvar)

root.mainloop()