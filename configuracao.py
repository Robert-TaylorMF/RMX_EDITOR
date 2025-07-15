import sys
import os
import json
from tkinter import messagebox

def obter_caminho(imagem_relativa):
    if getattr(sys, 'frozen', False):
        caminho_base = sys._MEIPASS
    else:
        caminho_base = os.path.dirname(__file__)
    return os.path.join(caminho_base, imagem_relativa)

def carregar_bases_json(caminho_arquivo="bases.json"):
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config["bases"]
    except Exception as e:
        print(f"Erro ao carregar bases JSON: {e}")
        return []

def conectar_base(bases_disponiveis, nome_selecionado, status_var):
    for b in bases_disponiveis:
        if b["nome"] == nome_selecionado:
            status_var.set(f"Base selecionada: {nome_selecionado}")
            return b
    messagebox.showerror("Erro", "Base não encontrada.")
    return None