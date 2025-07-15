import os
import tkinter as tk
from tkinter import messagebox, scrolledtext
import difflib
from utilitarios import realcar_sintaxe_xml

def abrir_backup(root, text_xml, status_var):
    pasta = "backups_xml"
    if not os.path.exists(pasta):
        messagebox.showinfo("Backup", "Ainda não há backups salvos.")
        return

    janela = tk.Toplevel(root)
    janela.title("Comparar XML com Backup")
    janela.geometry("1000x600")

    tk.Label(janela, text="Selecione um arquivo de backup:").pack(pady=5)

    lista = tk.Listbox(janela, width=80, height=10)
    lista.pack(pady=5)

    arquivos = sorted([f for f in os.listdir(pasta) if f.endswith(".xml")], reverse=True)
    for arq in arquivos:
        lista.insert(tk.END, arq)

    def exibir_comparacao():
        sel = lista.curselection()
        if not sel:
            messagebox.showwarning("Seleção", "Escolha um backup.")
            return

        nome = arquivos[sel[0]]
        caminho = os.path.join(pasta, nome)
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo_backup = f.read().splitlines()
        conteudo_atual = text_xml.get("1.0", tk.END).strip().splitlines()

        comp = tk.Toplevel(janela)
        comp.title("Comparativo Lado a Lado")
        comp.geometry("1200x800")

        frame_legenda = tk.Frame(comp, bg="#f0f0f0")
        frame_legenda.pack(pady=5)
        tk.Label(frame_legenda, text="🟩 Adicionado", bg="#eaffea", padx=8).grid(row=0, column=0, padx=5)
        tk.Label(frame_legenda, text="🟥 Removido", bg="#ffeaea", padx=8).grid(row=0, column=1, padx=5)
        tk.Label(frame_legenda, text="🟨 Modificado", bg="#fff7c0", padx=8).grid(row=0, column=2, padx=5)

        frame_titles = tk.Frame(comp)
        frame_titles.pack()
        tk.Label(frame_titles, text="📝 Atual", fg="blue", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=20)
        tk.Label(frame_titles, text=f"📦 Backup: {nome}", fg="green", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, padx=20)

        frame_texts = tk.Frame(comp)
        frame_texts.pack()

        scroll = tk.Scrollbar(frame_texts, orient=tk.VERTICAL)
        scroll.grid(row=0, column=2, sticky="ns")

        txt_atual = scrolledtext.ScrolledText(frame_texts, wrap=tk.NONE, width=70, height=35, font=("Courier New", 9), yscrollcommand=scroll.set)
        txt_backup = scrolledtext.ScrolledText(frame_texts, wrap=tk.NONE, width=70, height=35, font=("Courier New", 9), yscrollcommand=scroll.set)

        txt_atual.grid(row=0, column=0, padx=(10, 5))
        txt_backup.grid(row=0, column=1, padx=(5, 10))
        scroll.config(command=lambda *args: (txt_atual.yview(*args), txt_backup.yview(*args)))

        def on_scroll(*args):
            txt_atual.yview_moveto(args[0])
            txt_backup.yview_moveto(args[0])

        txt_atual.configure(yscrollcommand=on_scroll)
        txt_backup.configure(yscrollcommand=on_scroll)

        txt_atual.tag_config("modificado", background="#fff7c0")
        txt_atual.tag_config("adicao", background="#eaffea")
        txt_backup.tag_config("modificado", background="#fff7c0")
        txt_backup.tag_config("remocao", background="#ffeaea")

        max_linhas = max(len(conteudo_backup), len(conteudo_atual))
        for i in range(max_linhas):
            linha_atual = conteudo_atual[i] if i < len(conteudo_atual) else ""
            linha_backup = conteudo_backup[i] if i < len(conteudo_backup) else ""

            if linha_atual == linha_backup:
                txt_atual.insert(tk.END, linha_atual + "\n")
                txt_backup.insert(tk.END, linha_backup + "\n")
            elif linha_atual.strip() == "" and linha_backup.strip():
                txt_backup.insert(tk.END, linha_backup + "\n", "remocao")
                txt_atual.insert(tk.END, "\n")
            elif linha_backup.strip() == "" and linha_atual.strip():
                txt_atual.insert(tk.END, linha_atual + "\n", "adicao")
                txt_backup.insert(tk.END, "\n")
            else:
                txt_atual.insert(tk.END, linha_atual + "\n", "modificado")
                txt_backup.insert(tk.END, linha_backup + "\n", "modificado")

        txt_atual.config(state=tk.DISABLED)
        txt_backup.config(state=tk.DISABLED)

        def restaurar_backup():
            confirm = messagebox.askyesno("Restaurar Backup", "Deseja carregar este backup no editor?\n(É necessário clicar em SALVAR depois para aplicar no banco)")
            if confirm:
                text_xml.delete("1.0", tk.END)
                text_xml.insert(tk.END, "\n".join(conteudo_backup))
                realcar_sintaxe_xml(text_xml)
                status_var.set(f"Backup {nome} carregado no editor.")

        tk.Button(comp, text="⏪ Restaurar este backup", fg="white", bg="green", command=restaurar_backup).pack(pady=10)

    tk.Button(janela, text="Comparar com Backup Selecionado", command=exibir_comparacao).pack(pady=10)