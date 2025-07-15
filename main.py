import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from configuracao import obter_caminho, carregar_bases_json, conectar_base
from conexao import obter_conexao
from verificador import verificar_driver_sql, verificar_atualizacao
from xml_operacoes import carregar_xml, salvar_xml
from splash import mostrar_splash
from sobre import mostrar_sobre
from comparador import abrir_backup
from utilitarios import (
    formatar_xml, salvar_backup, realcar_sintaxe_xml,
    buscar_texto, substituir_proxima, substituir_todos
)

# === Inicialização de variáveis globais ===
bases_disponiveis = carregar_bases_json()
base_selecionada = None
substituir_posicao = "1.0"
versao = "1.2"
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

# === Janela principal ===
root = tk.Tk()
root.title(f"XMLEditor RM – Editor de XML eSocial v{versao}")
root.geometry("1080x740")

# === Frame 1: Seleção de base e ID do evento ===
frame1 = tk.Frame(root)
frame1.pack(pady=10, anchor="w")

tk.Label(frame1, text="Base:").grid(row=0, column=0)
combo_base = ttk.Combobox(frame1, values=[b["nome"] for b in bases_disponiveis], state="readonly", width=25)
combo_base.grid(row=0, column=1)
combo_base.current(0)

tk.Button(frame1, text="Conectar", command=conectar_e_atualizar).grid(row=0, column=2, padx=5)

tk.Label(frame1, text="ID do Evento:").grid(row=0, column=3)
entry_id = tk.Entry(frame1, width=45)
entry_id.grid(row=0, column=4)

tk.Button(frame1, text="Carregar", command=lambda: carregar_xml(
    base_selecionada, entry_id.get(), text_xml, status_var
)).grid(row=0, column=5, padx=5)

tk.Button(frame1, text="Salvar", command=lambda: salvar_xml(
    base_selecionada, entry_id.get(), text_xml.get("1.0", tk.END).strip(), text_xml
)).grid(row=0, column=6, padx=5)

tk.Button(frame1, text="Ver Backup", command=lambda: abrir_backup(
    root, text_xml, status_var
)).grid(row=0, column=7, padx=5)

# === Frame 2: Busca e substituição ===
frame2 = tk.Frame(root)
frame2.pack(pady=5, anchor="w")

tk.Label(frame2, text="Buscar:").grid(row=0, column=0)
entry_busca = tk.Entry(frame2, width=30)
entry_busca.grid(row=0, column=1, padx=5)

tk.Label(frame2, text="Substituir por:").grid(row=0, column=3)
entry_substituir = tk.Entry(frame2, width=30)
entry_substituir.grid(row=0, column=3, padx=5)

tk.Button(frame2, text="Localizar", command=lambda: buscar_texto(entry_busca, text_xml)).grid(row=0, column=4, padx=5)
tk.Button(frame2, text="Substituir", command=substituir_e_avancar).grid(row=0, column=5, padx=5)
tk.Button(frame2, text="Substituir todos", command=lambda: substituir_todos(entry_busca, entry_substituir, text_xml)).grid(row=0, column=6, padx=5)

# === Editor XML ===
text_xml = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_xml.pack(padx=10, pady=10, fill="both", expand=True)

# === Barra de status ===
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, fg="blue")
status_label.pack()

# === Botões adicionais ===
tk.Button(root, text="Verificar Atualização", command=lambda: verificar_atualizacao(versao)).pack(pady=10)
tk.Button(root, text="Sobre", command=lambda: mostrar_sobre(root, versao)).pack(pady=10)

# === Inicialização final ===
verificar_driver_sql()
root.mainloop()