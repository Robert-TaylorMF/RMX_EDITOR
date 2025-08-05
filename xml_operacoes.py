import tkinter as tk
from tkinter import messagebox
from conexao import obter_conexao
from utilitarios import formatar_xml, salvar_backup, realcar_sintaxe_xml, compactar_xml, extrair_conteudo_esocial, preparar_xml_para_salvar
import re

def carregar_xml(base_selecionada, evento_id, editor_frame, status_var, painel_guias=None, nome_guia=None):
    if not base_selecionada:
        messagebox.showwarning("Base", "Selecione uma base.")
        return
    if not evento_id:
        messagebox.showwarning("ID", "Informe o ID do evento.")
        return

    conn = obter_conexao(base_selecionada)
    if not conn:
        messagebox.showerror("Erro de conexão", "Não foi possível conectar ao banco.")
        return

    text_widget = editor_frame.editor_texto if hasattr(editor_frame, "editor_texto") else editor_frame

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT mensagem FROM PESOCIALEVENTOS WHERE id = ?", evento_id)
        row = cursor.fetchone()
        conn.close()

        if row:
            xml = formatar_xml(row[0])
            text_widget.delete("1.0", tk.END)
            text_widget.insert(tk.END, xml)
            realcar_sintaxe_xml(text_widget)
            status_var.set(f"✅ XML do evento {evento_id} carregado.")

            # ✅ Armazena metadados da guia
            if painel_guias and nome_guia:
                if nome_guia in painel_guias.editores:
                    painel_guias.editores[nome_guia]["evento_id"] = evento_id
                    painel_guias.editores[nome_guia]["base"] = base_selecionada
        else:
            messagebox.showinfo("Não encontrado", f"Nenhum evento com ID {evento_id}.")
    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao carregar XML: {e}")

    text_widget.edit_modified(True)
    text_widget.event_generate("<<Modified>>")

def salvar_xml(base_selecionada, evento_id, novo_xml, text_widget):
    if not base_selecionada:
        messagebox.showwarning("Base", "Selecione uma base.")
        return
    if not evento_id or not novo_xml:
        messagebox.showwarning("Atenção", "ID e XML são obrigatórios.")
        return

    conn = obter_conexao(base_selecionada)
    if not conn:
        messagebox.showerror("Erro de conexão", "Não foi possível conectar ao banco.")
        return

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT mensagem FROM PESOCIALEVENTOS WHERE id = ?", evento_id)
        row = cursor.fetchone()
        if row:
            xml_antigo = row[0]
            salvar_backup(xml_antigo, evento_id)

        xml_para_salvar = preparar_xml_para_salvar(novo_xml)

        cursor.execute(
            "UPDATE PESOCIALEVENTOS SET mensagem = ? WHERE id = ?",
            xml_para_salvar, evento_id
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", f"💾 XML do evento {evento_id} atualizado com sucesso.")
        realcar_sintaxe_xml(text_widget)
    except Exception as e:
        messagebox.showerror("Erro ao salvar", str(e))
        
def salvar_xml_por_guia(painel_guias, nome_guia):
    if nome_guia not in painel_guias.editores:
        messagebox.showwarning("Erro", f"A guia {nome_guia} não existe.")
        return

    guia = painel_guias.editores[nome_guia]
    base = guia.get("base")
    evento_id = guia.get("evento_id")
    editor_frame = guia.get("editor")

    if not base or not evento_id:
        messagebox.showwarning("Atenção", "Esta guia não possui base ou ID definidos.")
        return

    text_widget = editor_frame.editor_texto if hasattr(editor_frame, "editor_texto") else editor_frame
    novo_xml = text_widget.get("1.0", tk.END).strip()

    if not novo_xml:
        messagebox.showwarning("Atenção", "O XML está vazio. Nada foi salvo.")
        return

    salvar_xml(base, evento_id, novo_xml, text_widget)

def dividir_por_tags(xml_str):
    return re.findall(r"<[^>]+>[^<]*</[^>]+>", formatar_xml(xml_str))