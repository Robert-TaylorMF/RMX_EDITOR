import os
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from utilitarios import realcar_sintaxe_xml, formatar_xml
from modulos.regua_visual import destacar_linhas_editadas
import re
from difflib import SequenceMatcher

icone_lixeira = ctk.CTkImage(light_image=Image.open("recursos/lixeira.ico"), size=(20, 20))

def dividir_por_tags(xml_str):
    return re.findall(r"<[^>]+>[^<]*</[^>]+>", formatar_xml(xml_str))

def abrir_backup(root, painel_guias, nome_guia, status_var):
    import time
    pasta = "backups_xml"

    if nome_guia not in painel_guias.editores:
        messagebox.showwarning("Erro", f"A guia {nome_guia} não existe.")
        return

    guia = painel_guias.editores[nome_guia]
    editor_frame = guia["editor"]
    evento_id = guia.get("evento_id")

    if not evento_id:
        messagebox.showwarning("Atenção", "Esta guia não possui um ID de evento definido.")
        return

    if not os.path.exists(pasta):
        messagebox.showinfo("Backup", "Ainda não há backups salvos.")
        return
    
    janela = ctk.CTkToplevel(root)
    janela.title("Comparar XML com Backup")
    janela.geometry("800x360")
    janela.transient(root)
    janela.grab_set()
    janela.focus_force()
    janela.lift()

    ctk.CTkLabel(janela, text=f"Backups para o evento: {evento_id}", font=("Arial", 14, "bold")).pack(pady=(5, 0))
    frame_lista = ctk.CTkScrollableFrame(janela, width=780, height=220, corner_radius=6)
    frame_lista.pack(pady=5)

    arquivos = sorted([
        f for f in os.listdir(pasta)
        if f.endswith(".xml") and str(evento_id) in f
    ], reverse=True)

    if not arquivos:
        ctk.CTkLabel(frame_lista, text="⚠️ Nenhum backup encontrado para este ID.", text_color="orange").pack(pady=10)
        return

    def criar_botao_backup(nome_arquivo):
        caminho = os.path.join(pasta, nome_arquivo)
        data_mod = time.strftime("%d/%m/%Y %H:%M", time.localtime(os.path.getmtime(caminho)))

        grupo = ctk.CTkFrame(frame_lista, fg_color="transparent")
        grupo.pack(fill="x", padx=10, pady=2)

        botao = ctk.CTkButton(
            grupo, text=f"{nome_arquivo}  ({data_mod})",
            width=720, anchor="w",
            command=lambda: exibir_comparacao(nome_arquivo, editor_frame)
        )
        botao.pack(side="left", fill="x", expand=True)

        ctk.CTkButton(
            grupo, text="",
            image=icone_lixeira,
            width=36,
            fg_color="transparent",
            hover_color="#550000",
            command=lambda: excluir_backup(caminho, grupo)
        ).pack(side="right", padx=5)

    for nome_arquivo in arquivos:
        criar_botao_backup(nome_arquivo)
        
    def exibir_comparacao(nome_arquivo, editor_frame):
        caminho = os.path.join(pasta, nome_arquivo)
        with open(caminho, "r", encoding="utf-8") as f:
            raw_backup = f.read()

        text_widget = editor_frame.editor_texto if hasattr(editor_frame, "editor_texto") else editor_frame
        raw_atual = text_widget.get("1.0", "end")

        tags_backup = dividir_por_tags(raw_backup)
        tags_atual = dividir_por_tags(raw_atual)

        comp = ctk.CTkToplevel(janela)
        comp.title("Comparativo Visual Estilo WinMerge")
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

        titulo = ctk.CTkFrame(comp)
        titulo.pack(pady=(5, 0))
        ctk.CTkLabel(titulo, text="📂 XML Atual (Editor)", text_color="skyblue", font=("Segoe UI", 14, "bold")).grid(row=0, column=0, padx=50)
        ctk.CTkLabel(titulo, text=f"📦 Backup Selecionado: {nome_arquivo}", text_color="lightgreen", font=("Segoe UI", 14, "bold")).grid(row=0, column=1, padx=50)

        frame = ctk.CTkFrame(comp)
        frame.pack(expand=True, fill="both", padx=10, pady=10)

        txt_atual = tk.Text(frame, wrap="word", font=("Consolas", 12), bg="#1e1e1e", fg="white", insertbackground="white")
        txt_backup = tk.Text(frame, wrap="word", font=("Consolas", 12), bg="#1e1e1e", fg="white", insertbackground="white")

        txt_atual.grid(row=0, column=0, padx=(5, 3), sticky="nsew")
        txt_backup.grid(row=0, column=1, padx=(3, 5), sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)
        frame.grid_columnconfigure(1, weight=1)
        
        matcher = SequenceMatcher(None, tags_backup, tags_atual)
        linha_atual = linha_backup = 1

        for op, i1, i2, j1, j2 in matcher.get_opcodes():
            for k in range(max(i2 - i1, j2 - j1)):
                tag_b = tags_backup[i1 + k] if i1 + k < i2 else ""
                tag_a = tags_atual[j1 + k] if j1 + k < j2 else ""

                txt_backup.insert("end", tag_b + "\n" if tag_b else "\n")
                txt_atual.insert("end", tag_a + "\n" if tag_a else "\n")

                idx_b = f"{linha_backup}.0"
                idx_fb = f"{linha_backup}.end"
                idx_a = f"{linha_atual}.0"
                idx_fa = f"{linha_atual}.end"

                if op == "replace":
                    txt_backup.tag_add("modificado", idx_b, idx_fb)
                    txt_atual.tag_add("modificado", idx_a, idx_fa)
                elif op == "delete":
                    txt_backup.tag_add("remocao", idx_b, idx_fb)
                elif op == "insert":
                    txt_atual.tag_add("adicao", idx_a, idx_fa)

                linha_backup += 1
                linha_atual += 1

        for txt in [txt_atual, txt_backup]:
            txt.tag_config("modificado", foreground="#000000", background="#fff7c0")
            txt.tag_config("adicao", foreground="#000000", background="#eaffea")
            txt.tag_config("remocao", foreground="#000000", background="#ffeaea")
            txt.config(state="disabled")

        def restaurar_backup():
            if messagebox.askyesno(
                "Restaurar Backup",
                "Deseja carregar este backup no editor?\n(É necessário clicar em SALVAR depois para aplicar no banco)"
            ):
                text_widget.delete("1.0", "end")
                text_widget.insert("end", raw_backup)
                realcar_sintaxe_xml(text_widget)
                status_var.set(f"✅ Backup restaurado: {nome_arquivo}")

                linhas_modificadas = []
                backup_linhas = raw_backup.strip().splitlines()
                atual_linhas = text_widget.get("1.0", "end").strip().splitlines()

                for i, (linha_b, linha_a) in enumerate(zip(backup_linhas, atual_linhas), start=1):
                    if linha_b.strip() != linha_a.strip():
                        linhas_modificadas.append(i)

                destacar_linhas_editadas(text_widget, linhas_modificadas)

        ctk.CTkButton(comp, text="⏪ Restaurar este backup", command=restaurar_backup).pack(pady=10)