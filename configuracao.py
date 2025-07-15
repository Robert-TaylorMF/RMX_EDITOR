import sys
import os
import json
from tkinter import messagebox
from seguranca import criptografar_senha

def obter_caminho(imagem_relativa):
    if getattr(sys, 'frozen', False):
        caminho_base = sys._MEIPASS
    else:
        caminho_base = os.path.dirname(__file__)
    return os.path.join(caminho_base, imagem_relativa)

import json
import os

def carregar_bases(caminho_arquivo="conexoes.json"):
    if not os.path.exists(caminho_arquivo):
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump({"bases": []}, f, indent=2, ensure_ascii=False)
    try:
        with open(caminho_arquivo, "r", encoding="utf-8") as f:
            config = json.load(f)
        return config["bases"]
    except Exception as e:
        print(f"Erro ao carregar conexões: {e}")
        return []

def salvar_nova_base(nova_base, caminho="conexoes.json"):
    bases = carregar_bases(caminho)
    bases = [b for b in bases if b["nome"] != nova_base["nome"]]
    bases.append(nova_base)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump({"bases": bases}, f, indent=2, ensure_ascii=False)

def excluir_base(nome, caminho="conexoes.json"):
    bases = carregar_bases(caminho)
    bases = [b for b in bases if b["nome"] != nome]
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump({"bases": bases}, f, indent=2, ensure_ascii=False)
        
def conectar_base(bases_disponiveis, nome_selecionado, status_var=None):
    for base in bases_disponiveis:
        if base["nome"] == nome_selecionado:
            if status_var:
                status_var.set(f"Base selecionada: {nome_selecionado}")
            return base
    messagebox.showerror("Erro", f"Base '{nome_selecionado}' não encontrada.")
    return None

