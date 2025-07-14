import os
import re
from datetime import datetime
import xml.dom.minidom
import tkinter as tk

def formatar_xml(xml_str):
    try:
        dom = xml.dom.minidom.parseString(xml_str.strip())
        return '\n'.join([line for line in dom.toprettyxml(indent="  ").split('\n') if line.strip()])
    except Exception as e:
        print("Erro ao formatar XML:", e)
        return xml_str

def salvar_backup(xml_antigo, evento_id):
    try:
        pasta = "backups_xml"
        os.makedirs(pasta, exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        nome_arquivo = f"{pasta}/evento_{evento_id}_{timestamp}.xml"
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write(xml_antigo)
        print(f"Backup salvo em: {nome_arquivo}")
    except Exception as e:
        print("Erro ao salvar backup:", e)

def realcar_sintaxe_xml(text_widget):
    text_widget.tag_remove("tag", "1.0", tk.END)
    text_widget.tag_remove("atributo", "1.0", tk.END)
    text_widget.tag_remove("valor", "1.0", tk.END)

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

    text_widget.tag_config("tag", foreground="#003399")
    text_widget.tag_config("atributo", foreground="#cc0000")
    text_widget.tag_config("valor", foreground="#007a00")

def buscar_texto(entry_busca, text_widget):
    termo = entry_busca.get()
    text_widget.tag_remove("destacado", "1.0", tk.END)
    if not termo:
        return

    inicio = "1.0"
    primeira_pos = None
    while True:
        pos = text_widget.search(termo, inicio, stopindex=tk.END)
        if not pos:
            break
        fim = f"{pos}+{len(termo)}c"
        text_widget.tag_add("destacado", pos, fim)
        if not primeira_pos:
            primeira_pos = pos
        inicio = fim

    text_widget.tag_config("destacado", background="yellow")
    if primeira_pos:
        text_widget.mark_set("insert", primeira_pos)
        text_widget.see(primeira_pos)

def substituir_proxima(entry_busca, entry_substituir, text_widget, posicao_substituicao):
    termo = entry_busca.get()
    novo = entry_substituir.get()
    if not termo:
        return "1.0"

    start = text_widget.search(termo, posicao_substituicao, tk.END)
    if not start:
        return "1.0"  # reinicia para próxima busca futura

    end = f"{start}+{len(termo)}c"
    text_widget.delete(start, end)
    text_widget.insert(start, novo)

    nova_pos = f"{start}+{len(novo)}c"
    text_widget.mark_set(tk.INSERT, nova_pos)
    text_widget.see(nova_pos)
    return nova_pos

def substituir_todos(entry_busca, entry_substituir, text_widget):
    termo = entry_busca.get()
    novo = entry_substituir.get()
    if termo:
        conteudo = text_widget.get("1.0", tk.END)
        atualizado = conteudo.replace(termo, novo)
        text_widget.delete("1.0", tk.END)
        text_widget.insert(tk.END, atualizado)
        buscar_texto(entry_busca, text_widget)
        realcar_sintaxe_xml(text_widget)