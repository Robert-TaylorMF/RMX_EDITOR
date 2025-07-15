import os
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from utilitarios import realcar_sintaxe_xml

def abrir_backup(root, text_xml, status_var, modo_escuro_ativo):
    pasta = "backups_xml"
    if not os.path.exists(pasta):
        messagebox.showinfo("Backup", "Ainda não há backups salvos.")
        return

    janela = ctk.CTkToplevel(root)
    janela.title("Comparar XML com Backup")
    janela.geometry("700x300")
    janela.transient(root)
    janela.grab_set()
    janela.focus_force()
    janela.lift()

    ctk.CTkLabel(janela, text="Selecione um arquivo de backup:").pack(pady=(5, 0))
    frame_lista = ctk.CTkScrollableFrame(janela, width=700, height=200, corner_radius=6)
    frame_lista.pack(pady=5)

    arquivos = sorted([f for f in os.listdir(pasta) if f.endswith(".xml")], reverse=True)
    for nome_arquivo in arquivos:
        ctk.CTkButton(frame_lista, text=nome_arquivo, width=680, anchor="w",
                      command=lambda n=nome_arquivo: exibir_comparacao(n)).pack(pady=2)

    def exibir_comparacao(nome):
        caminho = os.path.join(pasta, nome)
        with open(caminho, "r", encoding="utf-8") as f:
            conteudo_backup = f.read().splitlines()
        conteudo_atual = text_xml.get("1.0", "end").strip().splitlines()

        comp = ctk.CTkToplevel(janela)
        comp.title("Comparativo Lado a Lado")
        comp.geometry("1350x800")
        comp.transient(janela)
        comp.grab_set()
        comp.focus_force()
        comp.lift()

        legenda = ctk.CTkFrame(comp)
        legenda.pack(pady=5)
        ctk.CTkLabel(legenda, text="🟩 Adicionado", fg_color="#eaffea", text_color="#0a7300", corner_radius=4).grid(row=0, column=0, padx=5)
        ctk.CTkLabel(legenda, text="🟥 Removido", fg_color="#ffeaea", text_color="#a00000", corner_radius=4).grid(row=0, column=1, padx=5)
        ctk.CTkLabel(legenda, text="🟨 Modificado", fg_color="#fff7c0", text_color="#c27c00", corner_radius=4).grid(row=0, column=2, padx=5)

        # 🎯 Títulos acima das caixas de texto
        titulo_campos = ctk.CTkFrame(comp)
        titulo_campos.pack(pady=(5, 0))
        ctk.CTkLabel(titulo_campos, text="📂 XML Atual (Editor)", text_color="skyblue", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, padx=50)
        ctk.CTkLabel(titulo_campos, text=f"📦 Backup Selecionado: {nome}", text_color="lightgreen", font=("Segoe UI", 14, "bold")).grid(row=0, column=1, padx=50)

        frame = ctk.CTkFrame(comp)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        # Usando tk.Text para compatibilidade total com tags
        txt_atual = tk.Text(frame, wrap="none", font=("Consolas", 12))
        txt_backup = tk.Text(frame, wrap="none", font=("Consolas", 12))

        # 🌑 Estilo escuro com fonte branca e cursor visível
        for txt in [txt_atual, txt_backup]:
            txt.configure(bg="#1e1e1e", fg="white", insertbackground="white")

        txt_atual.grid(row=0, column=0, padx=(5, 3), sticky="nsew")
        txt_backup.grid(row=0, column=1, padx=(3, 5), sticky="nsew")

        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)

        max_linhas = max(len(conteudo_backup), len(conteudo_atual))
        for i in range(max_linhas):
            linha_atual = conteudo_atual[i] if i < len(conteudo_atual) else ""
            linha_backup = conteudo_backup[i] if i < len(conteudo_backup) else ""

            txt_atual.insert("end", linha_atual + "\n")
            txt_backup.insert("end", linha_backup + "\n")

            idx_atual = f"{i+1}.0"
            idx_fim_atual = f"{i+1}.end"
            idx_backup = f"{i+1}.0"
            idx_fim_backup = f"{i+1}.end"

            if linha_atual.strip() == "" and linha_backup.strip():
                txt_backup.tag_add("remocao", idx_backup, idx_fim_backup)
            elif linha_backup.strip() == "" and linha_atual.strip():
                txt_atual.tag_add("adicao", idx_atual, idx_fim_atual)
            elif linha_atual != linha_backup:
                txt_atual.tag_add("modificado", idx_atual, idx_fim_atual)
                txt_backup.tag_add("modificado", idx_backup, idx_fim_backup)

        # 🎨 Tags com texto preto e fundo destacado
        for txt in [txt_atual, txt_backup]:
            txt.tag_config("modificado", foreground="#000000", background="#fff7c0")
            txt.tag_config("adicao", foreground="#000000", background="#eaffea")
            txt.tag_config("remocao", foreground="#000000", background="#ffeaea")
            txt.config(state="disabled")

        def restaurar_backup():
            confirm = messagebox.askyesno("Restaurar Backup", "Deseja carregar este backup no editor?\n(É necessário clicar em SALVAR depois para aplicar no banco)")
            if confirm:
                text_xml.delete("1.0", "end")
                text_xml.insert("end", "\n".join(conteudo_backup))
                realcar_sintaxe_xml(text_xml)
                status_var.set(f"Backup {nome} carregado no editor.")

        ctk.CTkButton(comp, text="⏪ Restaurar este backup", command=restaurar_backup).pack(pady=10)