# === Importações ===
import tkinter as tk
import pyperclip
import customtkinter as ctk
from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkTextbox, CTkComboBox, CTkFrame
from PIL import Image
from tooltip import Tooltip
from splash import mostrar_splash
from sobre import mostrar_sobre
from verificador import verificar_atualizacao
from configuracao import carregar_bases, obter_base_selecionada
from gerenciador_bases import abrir_gerenciador_de_bases
from xml_operacoes import carregar_xml, salvar_xml, salvar_xml_por_guia
from comparador import abrir_backup
from atalhos import configurar_atalhos, desfazer, refazer
from modulos.editor_com_linhas import criar_editor_com_linhas
from modulos.painel_de_guias import PainelDeGuias
from modulos.seletor_impressora import abrir_janela_impressao
from modulos.regua_visual import destacar_ocorrencias, destacar_linhas_erro, destacar_linhas_editadas
from utilitarios import (
    formatar_xml, salvar_backup, realcar_sintaxe_xml,
    compactar_xml, extrair_conteudo_esocial, abrir_localizador,
    copiar_texto, colar_texto, atualizar_fonte_em_editor,
    aumentar_fonte, diminuir_fonte, exportar_xml, imprimir_xml,
    gerar_e_abrir_pdf_xml
)

# === Variáveis Globais ===
bases_disponiveis = carregar_bases()
base_selecionada_dict = None
versao = "2.0"
fonte_editor = ["Consolas", 12]
contagem_janelas_xml = [0] 

# === Função para ajustar a fonte do editor de texto ===
def ajustar_fonte(delta):
    fonte_editor[1] = max(8, min(36, fonte_editor[1] + delta))
    editor_ativo = painel_guias.obter_editor_ativo().editor_texto
    if editor_ativo:
        atualizar_fonte_em_editor(editor_ativo, tuple(fonte_editor))

# === Splash screen ===
mostrar_splash()

# === Janela principal ===
root = CTk()
root.iconbitmap("recursos/xmleditor.ico")
root.title(f"XMLEditor RM – Editor de XML eSocial v{versao}")
root.state("zoomed")
root.after(100, lambda: root.state("zoomed"))
root.minsize(width=1350, height=740)

# === Ícones ===
icone_base         = ctk.CTkImage(light_image=Image.open("recursos/bancos-de-dados.ico"), size=(36, 36))
icone_att          = ctk.CTkImage(light_image=Image.open("recursos/atualizar.ico"), size=(36, 36))
icone_sobre        = ctk.CTkImage(light_image=Image.open("recursos/sobre-nos.ico"), size=(36, 36))
icone_conectar     = ctk.CTkImage(light_image=Image.open("recursos/link.ico"), size=(28, 28))
icone_ver_backup   = ctk.CTkImage(light_image=Image.open("recursos/restaurar-backup.ico"), size=(36, 36))
icone_localizar    = ctk.CTkImage(light_image=Image.open("recursos/lupa.ico"), size=(24, 24))
icone_salvar       = ctk.CTkImage(light_image=Image.open("recursos/salvar.ico"), size=(24, 24))
icone_desfazer     = ctk.CTkImage(light_image=Image.open("recursos/desfazer.ico"), size=(24, 24))
icone_refazer      = ctk.CTkImage(light_image=Image.open("recursos/refazer.ico"), size=(24, 24))
icone_copiar       = ctk.CTkImage(light_image=Image.open("recursos/copiar.ico"), size=(24, 24))
icone_colar        = ctk.CTkImage(light_image=Image.open("recursos/colar.ico"), size=(24, 24))
icone_aumentar_t   = ctk.CTkImage(light_image=Image.open("recursos/aumentar_texto.ico"), size=(24, 24))
icone_diminuir_t   = ctk.CTkImage(light_image=Image.open("recursos/diminuir_texto.ico"), size=(24, 24))
icone_exportar     = ctk.CTkImage(light_image=Image.open("recursos/exportar.ico"), size=(24, 24))
icone_imprimir     = ctk.CTkImage(light_image=Image.open("recursos/imprimir.ico"), size=(24, 24))

# === Menu lateral ===
menu_lateral = CTkFrame(root, width=160, corner_radius=0)
menu_lateral.pack(side="left", fill="y")

btn_base = CTkButton(menu_lateral, text="", image=icone_base, width=48, height=48,
                     fg_color="transparent", hover_color="#e0e0e0",
                     command=lambda: abrir_gerenciador_de_bases(root, combo_base, status_var))
btn_base.pack(pady=(10, 8))
Tooltip(btn_base, "Gerenciar Bases")

btn_backup = CTkButton(menu_lateral, text="", image=icone_ver_backup, width=48, height=48,
                       fg_color="transparent", hover_color="#e0e0e0",
                       command=lambda: abrir_backup(root, painel_guias, painel_guias.obter_nome_guia_ativa(), status_var))
btn_backup.pack(pady=8)
Tooltip(btn_backup, "Ver Backups e Comparar")

btn_att = CTkButton(menu_lateral, text="", image=icone_att, width=48, height=48,
                    fg_color="transparent", hover_color="#e0e0e0",
                    command=lambda: verificar_atualizacao(versao))
btn_att.pack(pady=8)
Tooltip(btn_att, "Verificar Atualização")

btn_sobre = CTkButton(menu_lateral, text="", image=icone_sobre, width=48, height=48,
                      fg_color="transparent", hover_color="#e0e0e0",
                      command=lambda: mostrar_sobre(root, versao))
btn_sobre.pack(pady=8)
Tooltip(btn_sobre, "Sobre o Sistema")

# === Frame superior ===
status_var = ctk.StringVar()
frame1 = CTkFrame(root)
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

def conectar_base_e_atualizar():
    global base_selecionada_dict
    base_selecionada_dict = obter_base_selecionada(combo_base.get(), status_var)

btn_conectar = CTkButton(frame1, text="", image=icone_conectar, width=48, height=48,
                         fg_color="transparent", hover_color="#e0e0e0",
                         command=conectar_base_e_atualizar)
btn_conectar.grid(row=0, column=2, padx=5)
Tooltip(btn_conectar, "Conectar à Base")

CTkLabel(frame1, text="ID do Evento:").grid(row=0, column=3, padx=5)
entry_id = CTkEntry(frame1, width=350)
entry_id.grid(row=0, column=4, padx=5)

CTkButton(frame1, text="Carregar", command=lambda: carregar_xml(
    base_selecionada_dict,
    entry_id.get(),
    painel_guias.obter_editor_ativo(),
    status_var,
    painel_guias,
    painel_guias.obter_nome_guia_ativa()
)).grid(row=0, column=5, padx=5)


# === Barra de ferramentas ===
frame_toolbar = CTkFrame(root, height=44)
frame_toolbar.pack(pady=5, anchor="w", fill="x", padx=10)

btn_lupa = CTkButton(frame_toolbar, text="", image=icone_localizar, width=48, height=48,
                     fg_color="transparent", hover_color="#e0e0e0",
                     command=lambda: abrir_localizador(painel_guias.obter_editor_ativo(), root))
btn_lupa.pack(side="left", padx=5)
Tooltip(btn_lupa, "Localizar e Substituir (Ctrl+F)")

botao_salvar = CTkButton(
    frame_toolbar, text="", image=icone_salvar, width=48, height=48,
    fg_color="transparent", hover_color="#e0e0e0",
    command=lambda: salvar_xml_por_guia(painel_guias, painel_guias.obter_nome_guia_ativa())
)
botao_salvar.pack(side="left", padx=5)
Tooltip(botao_salvar, "Salvar XML no Banco")


btn_copiar = CTkButton(frame_toolbar, text="", image=icone_copiar, width=38, height=38,
                       fg_color="transparent", hover_color="#e0e0e0",
                       command=lambda: copiar_texto(painel_guias.obter_editor_ativo()))
btn_copiar.pack(side="left", padx=5)
Tooltip(btn_copiar, "Copiar texto selecionado (Ctrl+C)")

btn_colar = CTkButton(frame_toolbar, text="", image=icone_colar, width=38, height=38,
                      fg_color="transparent", hover_color="#e0e0e0",
                      command=lambda: colar_texto(painel_guias.obter_editor_ativo()))
btn_colar.pack(side="left", padx=5)
Tooltip(btn_colar, "Colar conteúdo (Ctrl+V)")

btn_exportar = CTkButton(frame_toolbar, text="", image=icone_exportar, width=38, height=38,
                         fg_color="transparent", hover_color="#e0e0e0",
                         command=lambda: exportar_xml(painel_guias.obter_editor_ativo()))
btn_exportar.pack(side="left", padx=5)
Tooltip(btn_exportar, "Exportar para arquivo XML")

btn_pdf = CTkButton(
    frame_toolbar, text="", image=icone_imprimir, width=38, height=38,
    fg_color="transparent", hover_color="#e0e0e0",
    command=lambda: gerar_e_abrir_pdf_xml(painel_guias.obter_editor_ativo())
)
btn_pdf.pack(side="left", padx=5)
Tooltip(btn_pdf, "Imprimir")

btn_desfazer = CTkButton(frame_toolbar, text="", image=icone_desfazer, width=38, height=38,
                         fg_color="transparent", hover_color="#e0e0e0",
                         command=lambda: desfazer(painel_guias.obter_editor_ativo()))
btn_desfazer.pack(side="left", padx=5)
Tooltip(btn_desfazer, "Desfazer (Ctrl+Z)")

btn_refazer = CTkButton(frame_toolbar, text="", image=icone_refazer, width=38, height=38,
                        fg_color="transparent", hover_color="#e0e0e0",
                        command=lambda: refazer(painel_guias.obter_editor_ativo()))
btn_refazer.pack(side="left", padx=5)
Tooltip(btn_refazer, "Refazer (Ctrl+Y)")

btn_aumentar = CTkButton(frame_toolbar, text="", image=icone_aumentar_t, width=38, height=38,
                         fg_color="transparent", hover_color="#e0e0e0",
                         command=lambda: aumentar_fonte(painel_guias.obter_editor_ativo(), fonte_editor))
btn_aumentar.pack(side="left", padx=5)
Tooltip(btn_aumentar, "Aumentar Fonte")

btn_diminuir = CTkButton(frame_toolbar, text="", image=icone_diminuir_t, width=38, height=38,
                         fg_color="transparent", hover_color="#e0e0e0",
                         command=lambda: diminuir_fonte(painel_guias.obter_editor_ativo(), fonte_editor))
btn_diminuir.pack(side="left", padx=5)
Tooltip(btn_diminuir, "Diminuir Fonte")

# === Editor XML com Guias ===
painel_guias = PainelDeGuias(root, entry_id)
painel_guias.pack(expand=True, fill="both", padx=10, pady=10)

# === Barra de status ===
CTkLabel(root, textvariable=status_var, text_color="skyblue").pack(pady=5)

# === Inicialização final ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

configurar_atalhos(root, painel_guias, status_var, base_selecionada_dict, entry_id, botao_salvar)

# === Aplicar marcador na inicialização (ou após carregamento)
#destacar_linhas_editadas(text_xml, [1])

# === Loop principal ===
root.mainloop()