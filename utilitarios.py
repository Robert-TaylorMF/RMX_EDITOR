import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import os
import re
from datetime import datetime
import xml.dom.minidom

# 📋 Copiar texto selecionado do editor
def copiar_texto(text_widget):
    try:
        texto = text_widget.get("sel.first", "sel.last")
        text_widget.clipboard_clear()
        text_widget.clipboard_append(texto)
    except tk.TclError:
        pass  # nada selecionado

# 📥 Colar conteúdo do clipboard na posição atual do cursor
def colar_texto(text_widget):
    try:
        texto = text_widget.clipboard_get()
        text_widget.insert("insert", texto)
    except Exception:
        pass

# 🧹 Formata XML com identação elegante
def formatar_xml(xml_str):
    try:
        dom = xml.dom.minidom.parseString(xml_str.strip())
        return '\n'.join([line for line in dom.toprettyxml(indent="  ").split('\n') if line.strip()])
    except Exception as e:
        messagebox.showerror("Erro ao formatar XML", str(e))
        return xml_str

# 📦 Salva uma cópia do XML antigo como backup com timestamp
def salvar_backup(xml_antigo, evento_id):
    try:
        pasta = "backups_xml"
        os.makedirs(pasta, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_arquivo = f"{pasta}/evento_{evento_id}_{timestamp}.xml"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(xml_antigo)
        return nome_arquivo  # retorna o caminho para uso futuro
    except Exception as e:
        messagebox.showerror("Erro ao salvar backup", str(e))

# 🎨 Realça tags, atributos e valores no XML
def realcar_sintaxe_xml(text_widget):
    # Remove tags existentes
    text_widget.tag_delete("tag", "atributo", "valor")

    xml = text_widget.get("1.0", tk.END)
    padrao_tag = re.compile(r"<[^!?][^>]*?>")
    padrao_atributo = re.compile(r"\b([\w:.-]+)\s*=")
    padrao_valor = re.compile(r"\"(.*?)\"")

    for match in padrao_tag.finditer(xml):
        start = f"1.0 + {match.start()} chars"
        end = f"1.0 + {match.end()} chars"
        text_widget.tag_add("tag", start, end)

        tag_conteudo = match.group(0)
        offset = match.start()

        for a in padrao_atributo.finditer(tag_conteudo):
            a_ini = offset + a.start(1)
            a_fim = offset + a.end(1)
            text_widget.tag_add("atributo", f"1.0 + {a_ini} chars", f"1.0 + {a_fim} chars")

        for v in padrao_valor.finditer(tag_conteudo):
            v_ini = offset + v.start(0)
            v_fim = offset + v.end(0)
            text_widget.tag_add("valor", f"1.0 + {v_ini} chars", f"1.0 + {v_fim} chars")

    # 🎨 Visual refinado com contraste para tema escuro
    text_widget.tag_config("tag", foreground="#00ccff")
    text_widget.tag_config("atributo", foreground="#ff7700")
    text_widget.tag_config("valor", foreground="#00ff99")

# 🔍 Destaca todas as ocorrências do termo de busca
def buscar_texto(entry_busca, text_widget):
    termo = entry_busca.get()
    text_widget.tag_remove("destacado", "1.0", "end")
    if not termo:
        return 0

    inicio = "1.0"
    primeira_pos = None
    total = 0
    while True:
        pos = text_widget.search(termo, inicio, stopindex="end")
        if not pos:
            break
        fim = f"{pos}+{len(termo)}c"
        text_widget.tag_add("destacado", pos, fim)
        if not primeira_pos:
            primeira_pos = pos
        inicio = fim
        total += 1

    text_widget.tag_config("destacado", foreground="black", background="#fff700")
    if primeira_pos:
        text_widget.mark_set("insert", primeira_pos)
        text_widget.see(primeira_pos)

    return total  # retorna total de ocorrências

# 🔁 Substitui próxima ocorrência e retorna nova posição
def substituir_proxima(entry_busca, entry_substituir, text_widget, posicao_substituicao):
    termo = entry_busca.get()
    novo = entry_substituir.get()
    if not termo:
        return "1.0"

    start = text_widget.search(termo, posicao_substituicao, "end")
    if not start:
        return "1.0"

    end = f"{start}+{len(termo)}c"
    text_widget.delete(start, end)
    text_widget.insert(start, novo)

    nova_pos = f"{start}+{len(novo)}c"
    text_widget.mark_set("insert", nova_pos)
    text_widget.see(nova_pos)
    return nova_pos

# 🔁 Substitui todas ocorrências e realça resultado
def substituir_todos(entry_busca, entry_substituir, text_widget):
    termo = entry_busca.get()
    novo = entry_substituir.get()
    if termo:
        conteudo = text_widget.get("1.0", "end")
        atualizado = conteudo.replace(termo, novo)
        text_widget.delete("1.0", "end")
        text_widget.insert("end", atualizado)
        ocorrencias = buscar_texto(entry_busca, text_widget)
        realcar_sintaxe_xml(text_widget)
        return ocorrencias
    return 0

def abrir_localizador(text_xml, root):
    janela = ctk.CTkToplevel(root)
    janela.title("Localizar e Substituir")
    janela.geometry("400x250")
    janela.transient(root)
    janela.grab_set()
    janela.focus_force()

    ctk.CTkLabel(janela, text="Localizar:").pack(pady=(10, 2))
    campo_busca = ctk.CTkEntry(janela, width=350)
    campo_busca.pack()

    ctk.CTkLabel(janela, text="Substituir por:").pack(pady=(10, 2))
    campo_substituir = ctk.CTkEntry(janela, width=350)
    campo_substituir.pack()

    resultado_var = ctk.StringVar()
    ctk.CTkLabel(janela, textvariable=resultado_var, text_color="gray").pack(pady=6)

    def localizar():
        termo = campo_busca.get()
        text_xml.tag_remove("destacado", "1.0", "end")
        total = 0
        if termo:
            pos = "1.0"
            while True:
                pos = text_xml.search(termo, pos, stopindex="end")
                if not pos:
                    break
                fim = f"{pos}+{len(termo)}c"
                text_xml.tag_add("destacado", pos, fim)
                pos = fim
                total += 1
        text_xml.tag_config("destacado", foreground="black", background="#fff700")
        resultado_var.set(f"{total} ocorrência(s) encontrada(s)")

    def substituir():
        termo = campo_busca.get()
        novo = campo_substituir.get()
        if termo and novo:
            conteudo = text_xml.get("1.0", "end")
            novo_conteudo = conteudo.replace(termo, novo)
            text_xml.delete("1.0", "end")
            text_xml.insert("end", novo_conteudo)
            realcar_sintaxe_xml(text_xml)
            resultado_var.set("Substituição realizada")

    def substituir_tudo():
        termo = campo_busca.get()
        novo = campo_substituir.get()
        if termo and novo:
            total = 0
            pos = "1.0"
            while True:
                pos = text_xml.search(termo, pos, stopindex="end")
                if not pos:
                    break
                fim = f"{pos}+{len(termo)}c"
                text_xml.delete(pos, fim)
                text_xml.insert(pos, novo)
                pos = f"{pos}+{len(novo)}c"
                total += 1
            realcar_sintaxe_xml(text_xml)
            resultado_var.set(f"{total} substituição(ões) feita(s)")

    ctk.CTkButton(janela, text="🔍 Localizar", command=localizar).pack(pady=(10, 2))
    ctk.CTkButton(janela, text="↺ Substituir", command=substituir).pack(pady=2)
    ctk.CTkButton(janela, text="🔁 Substituir Todas", command=substituir_tudo).pack(pady=2)
    
def compactar_xml(xml_str):
    # Remove quebras de linha e espaços entre as tags
    xml_compacto = re.sub(r">\s+<", "><", xml_str.strip())
    return xml_compacto

def extrair_conteudo_esocial(xml_str):
    """
    Remove cabeçalho e retorna apenas o conteúdo a partir da tag <eSocial>
    """
    xml_str = xml_str.strip()
    inicio = xml_str.find("<eSocial")
    if inicio != -1:
        return xml_str[inicio:]
    return xml_str  # caso não encontre, retorna como está

def atualizar_fonte_em_editor(text_widget, nova_fonte):
    """
    Aplica a nova fonte no editor principal e na régua de linhas.
    """
    try:
        text_widget.config(font=nova_fonte)
        for child in text_widget.master.children.values():
            if isinstance(child, tk.Text) and child["state"] == "disabled":
                child.config(font=nova_fonte)
    except Exception:
        pass

def aumentar_fonte(editor, fonte_editor):
    fonte_editor[1] = min(36, fonte_editor[1] + 1)
    atualizar_fonte_em_editor(editor, tuple(fonte_editor))

def diminuir_fonte(editor, fonte_editor):
    fonte_editor[1] = max(8, fonte_editor[1] - 1)
    atualizar_fonte_em_editor(editor, tuple(fonte_editor))

def atualizar_fonte_em_editor(editor_frame, fonte):
    try:
        editor_texto = editor_frame.editor_texto
        linha_texto = editor_frame.linha_texto
        editor_texto.config(font=fonte)
        linha_texto.config(font=fonte)
    except Exception as e:
        print(f"Erro ao atualizar fonte: {e}")




