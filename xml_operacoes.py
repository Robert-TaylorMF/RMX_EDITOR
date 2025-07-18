import tkinter as tk
from tkinter import messagebox
from conexao import obter_conexao
from utilitarios import formatar_xml, salvar_backup, realcar_sintaxe_xml

def carregar_xml(base_selecionada, evento_id, text_widget, status_var):
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
            status_var.set(f"XML do evento {evento_id} carregado.")
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

        cursor.execute(
            "UPDATE PESOCIALEVENTOS SET mensagem = ? WHERE id = ?",
            novo_xml, evento_id
        )
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "XML atualizado com sucesso.")
        realcar_sintaxe_xml(text_widget)
    except Exception as e:
        messagebox.showerror("Erro ao salvar", str(e))