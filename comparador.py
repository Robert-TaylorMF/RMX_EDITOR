import os
import re
import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from PIL import Image
from utilitarios import realcar_sintaxe_xml, formatar_xml
from modulos.regua_visual import destacar_linhas_editadas
from tooltip import Tooltip
from difflib import SequenceMatcher
from tkinter import messagebox

# === Importação dos Icones ===
icone_lixeira = ctk.CTkImage(light_image=Image.open("recursos/lixeira.ico"), size=(20, 20))
icone_restaurar = ctk.CTkImage(light_image=Image.open("recursos/restaurar.ico"), size=(38, 38))

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
    
        xml_backup = formatar_xml(raw_backup)
        xml_atual = formatar_xml(raw_atual)
    
        comp = ctk.CTkToplevel(janela)
        comp.title("Comparativo XML")
        comp.geometry("1600x900")
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
    
        frame_comparativo = ctk.CTkFrame(comp)
        frame_comparativo.pack(expand=True, fill="both", padx=10, pady=10)

    
        def criar_editor_com_linhas(container):
            frame = tk.Frame(container)
            frame.pack(side="left", expand=True, fill="both", padx=10)

            canvas_linhas = tk.Canvas(frame, width=40, bg="#2b2b2b", highlightthickness=0)
            canvas_linhas.pack(side="left", fill="y")

            text_area = tk.Text(frame, wrap="none", font=("Consolas", 11), bg="#1e1e1e", fg="white",
                                insertbackground="white", padx=5, pady=5, undo=True)
            text_area.pack(side="left", expand=True, fill="both")

            # === Scrollbar da area de comparação ===
            scroll_y = ctk.CTkScrollbar(frame, orientation="vertical", command=text_area.yview)
            scroll_y.pack(side="right", fill="y")
            text_area.configure(yscrollcommand=scroll_y.set)
            canvas_linhas.configure(yscrollcommand=scroll_y.set)

            # Estilo de seleção visível
            text_area.configure(selectbackground="#3399ff", selectforeground="white")

            def sincronizar_scroll(*args):
                text_area.yview(*args)
                canvas_linhas.yview(*args)

            def atualizar_linhas():
                canvas_linhas.delete("all")
                i = text_area.index("@0,0")
                while True:
                    dline = text_area.dlineinfo(i)
                    if dline is None:
                        break
                    y = dline[1]
                    linha_num = str(i).split(".")[0]
                    canvas_linhas.create_text(35, y, anchor="ne", text=linha_num, fill="#aaaaaa", font=("Consolas", 10))
                    i = text_area.index(f"{i}+1line")

            text_area.bind("<KeyRelease>", lambda e: atualizar_linhas())
            text_area.bind("<MouseWheel>", lambda e: atualizar_linhas())
            text_area.bind("<ButtonRelease-1>", lambda e: atualizar_linhas())
            text_area.after(100, atualizar_linhas)

            return text_area

        txt_atual = criar_editor_com_linhas(frame_comparativo)
        txt_backup = criar_editor_com_linhas(frame_comparativo)  
        txt_atual.insert("1.0", xml_atual)
        txt_backup.insert("1.0", xml_backup)

        # Aplicar tags visuais
        txt_atual.tag_config("modificado", background="#fff7c0", foreground="#111111")
        txt_backup.tag_config("modificado", background="#fff7c0", foreground="#111111")

        txt_atual.tag_config("adicao", background="#eaffea", foreground="#0a7300")
        txt_backup.tag_config("remocao", background="#ffeaea", foreground="#a00000")

        # Comparar tags
        tags_b = dividir_por_tags(xml_backup)
        tags_a = dividir_por_tags(xml_atual)
        matcher = SequenceMatcher(None, tags_b, tags_a)
        for opcode, i1, i2, j1, j2 in matcher.get_opcodes():
            if opcode == "equal":
                continue
            elif opcode == "replace":
                for idx in range(i1, i2):
                    txt_backup.tag_add("modificado", f"{idx+1}.0", f"{idx+1}.end")
                for idx in range(j1, j2):
                    txt_atual.tag_add("modificado", f"{idx+1}.0", f"{idx+1}.end")
            elif opcode == "delete":
                for idx in range(i1, i2):
                    txt_backup.tag_add("remocao", f"{idx+1}.0", f"{idx+1}.end")
            elif opcode == "insert":
                for idx in range(j1, j2):
                    txt_atual.tag_add("adicao", f"{idx+1}.0", f"{idx+1}.end")

        # Botão restaurar
        def restaurar_backup():
            if messagebox.askyesno("Restaurar Backup", "Deseja carregar este backup no editor?\n(É necessário clicar em SALVAR depois para aplicar no banco)"):
                text_widget.delete("1.0", "end")
                text_widget.insert("end", xml_backup)
                realcar_sintaxe_xml(text_widget)
                status_var.set(f"✅ Backup restaurado: {nome_arquivo}")

                # Marcar linhas modificadas
                linhas_modificadas = []
                backup_linhas = xml_backup.strip().splitlines()
                atual_linhas = text_widget.get("1.0", "end").strip().splitlines()

                for i, (linha_b, linha_a) in enumerate(zip(backup_linhas, atual_linhas), start=1):
                    if linha_b.strip() != linha_a.strip():
                        linhas_modificadas.append(i)

                destacar_linhas_editadas(text_widget, linhas_modificadas)
        
        # === Realçar XML ===
        realcar_sintaxe_xml(txt_atual)
        realcar_sintaxe_xml(txt_backup)
        
        # Frame para centralizar o botão
        frame_btn_central = ctk.CTkFrame(comp, fg_color="transparent")
        frame_btn_central.pack(pady=10)

        # Botão restaurar com espaço garantido e texto invisível
        btn_restaurar = ctk.CTkButton(
            frame_btn_central,
            text="Restaurar XML",
            font=("Segoe UI", 10, "normal"),
            anchor="center",
            image=icone_restaurar,
            width=48,
            height=48,
            fg_color="transparent",
            command=restaurar_backup,
            compound="top"
        )
        btn_restaurar.pack(pady=5)

        # Efeito de hover (se sua função estiver definida)
        efeito_hover(btn_restaurar, "#d1e4ff")

        # Tooltip com delay para garantir ativação
        comp.after(300, lambda: Tooltip(btn_restaurar, "Restaurar XML"))
