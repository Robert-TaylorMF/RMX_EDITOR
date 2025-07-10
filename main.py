import urllib.request
from tkinter import messagebox
import json
import pyodbc
import os
import sys
import re
import difflib
from datetime import datetime
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import xml.dom.minidom
import time
import webbrowser

# === Verifica se possui o driver odbc necessário e se não existe redireciona para pagina de download ===

def driver_disponivel(nome_driver):
    return nome_driver in pyodbc.drivers()

def verificar_driver_sql():
    driver_necessario = "ODBC Driver 17 for SQL Server"
    drivers_disponiveis = pyodbc.drivers()

    if driver_necessario in drivers_disponiveis:
        print(f"Driver encontrado: {driver_necessario}")
        return True
    else:
        print(f"Driver ausente: {driver_necessario}")
        mostrar_aviso_driver(driver_necessario)
        return False

def mostrar_aviso_driver(driver_faltante):
    def abrir_link():
        webbrowser.open("https://learn.microsoft.com/sql/connect/odbc/download-odbc-driver-for-sql-server")

    root = tk.Tk()
    root.withdraw()  # Esconde janela principal

    resposta = messagebox.askyesno(
        "Driver ODBC ausente",
        f"O driver '{driver_faltante}' não está instalado nesta máquina, é recomendado a sua instalação.\n\nDeseja abrir o site oficial para baixar?"
    )

    if resposta:
        abrir_link()

# === verifica se há uma nova versão disponível ===
def verificar_atualizacao(versao_local="1.0"):
    try:
        url = "https://raw.githubusercontent.com/Robert-TaylorMF/RMX_EDITOR/main/versao.txt"
        resposta = urllib.request.urlopen(url, timeout=3)
        versao_online = resposta.read().decode().strip()
        if versao_online > versao_local:
            messagebox.showinfo("Atualização disponível",
                                f"Uma nova versão está disponível: {versao_online}\n\nAcesse:\nhttps://github.com/Robert-TaylorMF/RMX_EDITOR/releases")
        else:
            messagebox.showinfo("XMLEditor RM", "Você está usando a versão mais recente.")
    except:
        pass  # Silencioso em caso de erro offline

modo_escuro_ativo = False;
posicao_substituicao = "1.0"

# === Trabalhar com caminho relativo das imagens ===
def obter_caminho(imagem_relativa):
    if getattr(sys, 'frozen', False):
        # Executável .exe via PyInstaller
        caminho_base = sys._MEIPASS
    else:
        # Execução via script .py
        caminho_base = os.path.dirname(__file__)
    return os.path.join(caminho_base, imagem_relativa)

# === Carregar bases de dados do arquivo JSON ===
with open("bases.json", "r", encoding="utf-8") as f:
    config = json.load(f)
bases_disponiveis = config["bases"]
base_selecionada = None

# === Formatar XML de forma legível ===
def formatar_xml(xml_str):
    try:
        dom = xml.dom.minidom.parseString(xml_str.strip())
        return '\n'.join([line for line in dom.toprettyxml(indent="  ").split('\n') if line.strip()])
    except Exception as e:
        print("Erro ao formatar XML:", e)
        return xml_str

# === Salvar backup do XML anterior ===
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

# === Conectar à base selecionada no dropdown ===
def conectar_base():
    global base_selecionada
    nome = combo_base.get()
    for b in bases_disponiveis:
        if b["nome"] == nome:
            base_selecionada = b
            status_var.set(f"Base selecionada: {nome}")
            return
    messagebox.showerror("Erro", "Base não encontrada.")

# === Carregar XML de um evento específico pelo ID ===
def carregar_xml():
    if not base_selecionada:
        messagebox.showwarning("Base", "Selecione uma base.")
        return

    evento_id = entry_id.get()
    if not evento_id:
        messagebox.showwarning("ID", "Informe o ID do evento.")
        return

    # Drivers que podem funcionar (ordem de preferência)
    drivers_preferidos = [
        "ODBC Driver 17 for SQL Server",
        "SQL Server Native Client 11.0"
    ]

    # Tenta conexão com fallback entre os drivers
    for driver in drivers_preferidos:
        try:
            conn = pyodbc.connect(
                f"DRIVER={{{driver}}};"
                f"SERVER={base_selecionada['server']};"
                f"DATABASE={base_selecionada['database']};"
                f"UID={base_selecionada['user']};"
                f"PWD={base_selecionada['password']}"
            )
            cursor = conn.cursor()
            cursor.execute("SELECT mensagem FROM PESOCIALEVENTOS WHERE id = ?", evento_id)
            row = cursor.fetchone()
            conn.close()

            if row:
                xml = formatar_xml(row[0])
                text_xml.delete("1.0", tk.END)
                text_xml.insert(tk.END, xml)
                realcar_sintaxe_xml()
                status_var.set(f"XML do evento {evento_id} carregado.")
            else:
                messagebox.showinfo("Não encontrado", f"Nenhum evento com ID {evento_id}.")
            return  # sucesso, sai da função

        except Exception as e:
            print(f"⚠️ Falha com {driver}: {e}")

    # Se nenhum driver funcionou
    messagebox.showerror("Erro de conexão", "Não foi possível conectar ao banco.\nVerifique os drivers ODBC disponíveis.")

# === Salvar alterações no XML e aplicar realce ===
def salvar_xml():
    if not base_selecionada:
        messagebox.showwarning("Base", "Selecione uma base.")
        return

    evento_id = entry_id.get()
    novo_xml = text_xml.get("1.0", tk.END).strip()
    if not evento_id or not novo_xml:
        messagebox.showwarning("Atenção", "ID e XML são obrigatórios.")
        return

    drivers_preferidos = [
        "ODBC Driver 17 for SQL Server",
        "SQL Server Native Client 11.0"
    ]

    for driver in drivers_preferidos:
        try:
            conn = pyodbc.connect(
                f"DRIVER={{{driver}}};"
                f"SERVER={base_selecionada['server']};"
                f"DATABASE={base_selecionada['database']};"
                f"UID={base_selecionada['user']};"
                f"PWD={base_selecionada['password']}"
            )
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
            realcar_sintaxe_xml()
            return  # sucesso, sai da função

        except Exception as e:
            print(f"Falha com driver {driver}: {e}")

    messagebox.showerror("Erro de conexão", "Não foi possível salvar o XML.\nVerifique os drivers ODBC disponíveis.")

# === Realce de sintaxe XML com cores ===
def realcar_sintaxe_xml():
    text_xml.tag_remove("tag", "1.0", tk.END)
    text_xml.tag_remove("atributo", "1.0", tk.END)
    text_xml.tag_remove("valor", "1.0", tk.END)

    xml = text_xml.get("1.0", tk.END)
    padrao_tag = re.compile(r"<[^!?][^>]*?>")
    padrao_atributo = re.compile(r"\b([\w:.-]+)\s*=")
    padrao_valor = re.compile(r"\"(.*?)\"")

    for match in padrao_tag.finditer(xml):
        start = f"1.0 + {match.start()} chars"
        end = f"1.0 + {match.end()} chars"
        text_xml.tag_add("tag", start, end)

        tag_conteudo = match.group(0)
        offset = match.start()

        for a in padrao_atributo.finditer(tag_conteudo):
            a_ini = offset + a.start(1)
            a_fim = offset + a.end(1)
            text_xml.tag_add("atributo", f"1.0 + {a_ini} chars", f"1.0 + {a_fim} chars")

        for v in padrao_valor.finditer(tag_conteudo):
            v_ini = offset + v.start(0)
            v_fim = offset + v.end(0)
            text_xml.tag_add("valor", f"1.0 + {v_ini} chars", f"1.0 + {v_fim} chars")

    text_xml.tag_config("tag", foreground="#003399")
    text_xml.tag_config("atributo", foreground="#cc0000")
    text_xml.tag_config("valor", foreground="#007a00")

# === Buscar termo e destacar no texto ===
def buscar_texto():
    text_xml.tag_remove("destacado", "1.0", tk.END)
    termo = entry_busca.get()
    if not termo:
        return
    inicio = "1.0"
    primeira_pos = None
    while True:
        pos = text_xml.search(termo, inicio, stopindex=tk.END)
        if not pos:
            break
        fim = f"{pos}+{len(termo)}c"
        text_xml.tag_add("destacado", pos, fim)
        if not primeira_pos:
            primeira_pos = pos
        inicio = fim
    text_xml.tag_config("destacado", background="yellow")
    if primeira_pos:
        text_xml.mark_set("insert", primeira_pos)
        text_xml.see(primeira_pos)

# === Substituir uma ocorrência ===
def substituir_proxima():
    global posicao_substituicao

    termo = entry_busca.get()
    novo = entry_substituir.get()
    if not termo:
        messagebox.showinfo("Busca", "Digite um termo para buscar.")
        return

    start = text_xml.search(termo, posicao_substituicao, tk.END)
    if not start:
        messagebox.showinfo("Busca", "Nenhuma outra ocorrência encontrada.")
        posicao_substituicao = "1.0"
        return

    end = f"{start}+{len(termo)}c"
    text_xml.delete(start, end)
    text_xml.insert(start, novo)

    posicao_substituicao = f"{start}+{len(novo)}c"
    text_xml.mark_set(tk.INSERT, posicao_substituicao)
    text_xml.see(posicao_substituicao)

# === Substituir todas as ocorrências ===
def substituir_todos():
    termo = entry_busca.get()
    novo = entry_substituir.get()
    if termo:
        conteudo = text_xml.get("1.0", tk.END)
        atualizado = conteudo.replace(termo, novo)
        text_xml.delete("1.0", tk.END)
        text_xml.insert(tk.END, atualizado)
        buscar_texto()
        realcar_sintaxe_xml()
 
# === Aplicar Dark Mode ===
def aplicar_tema(escuro=True):
    fundo = "#1e1e1e" if escuro else "#ffffff"
    texto = "#e0e0e0" if escuro else "#000000"
    input_bg = "#2e2e2e" if escuro else "#ffffff"
    destaque = "#264f78" if escuro else "yellow"
    barra_status = "#1e1e1e" if escuro else "#f0f0f0"
    fonte_status = "#aaaaaa" if escuro else "#0000aa"

    root.configure(bg=fundo)
    for frame in [frame1, frame2]:
        frame.configure(bg=fundo)
        for child in frame.winfo_children():
            try:
                child.configure(bg=input_bg, fg=texto, insertbackground=texto)
            except:
                pass

    text_xml.configure(
        bg=fundo,
        fg=texto,
        insertbackground=texto,
        selectbackground=destaque
    )
    status_label.configure(bg=barra_status, fg=fonte_status)

    # Realce de sintaxe
    text_xml.tag_config("tag", foreground="#569cd6")
    text_xml.tag_config("atributo", foreground="#d19a66")
    text_xml.tag_config("valor", foreground="#98c379")
    text_xml.tag_config("destacado", background=destaque) 

# === Splash Screen ===
def mostrar_splash():
    splash = tk.Tk()
    splash.overrideredirect(True)
    splash.configure(bg="#1e1e1e")

    largura, altura = 400, 250
    pos_x = splash.winfo_screenwidth() // 2 - largura // 2
    pos_y = splash.winfo_screenheight() // 2 - altura // 2
    splash.geometry(f"{largura}x{altura}+{pos_x}+{pos_y}")

    # Carrega o logo PNG do app
    caminho_logo = obter_caminho("recursos/logo_splash.png")
    imagem_logo = Image.open(caminho_logo).resize((100, 100))
    img_logo = ImageTk.PhotoImage(imagem_logo)

    label_logo = tk.Label(splash, image=img_logo, bg="#1e1e1e")
    label_logo.image = img_logo
    label_logo.pack(pady=15)

    # Título e mensagem
    tk.Label(splash, text="XMLEditor RM", font=("Segoe UI", 18, "bold"),
             bg="#1e1e1e", fg="#00ccff").pack()
    
    tk.Label(splash, text="Inicializando ambiente XML...",
             font=("Segoe UI", 10), bg="#1e1e1e", fg="white").pack(pady=5)

    splash.update()
    time.sleep(2.5)
    splash.destroy()


# === Janela principal ===
mostrar_splash()

# === Carrega interface principal ===
root = tk.Tk()

# === Resolve caminho mesmo quando empacotado com PyInstaller ===
if not getattr(sys, 'frozen', False):
    caminho_icone = os.path.join(os.path.dirname(__file__), "xmleditor.ico")
    root.iconbitmap(caminho_icone)

root.title("XMLEditor RM – Editor de XML eSocial")
root.geometry("1080x740")

# === Barra superior: seleção de base, ID e botões principais ===
frame1 = tk.Frame(root)
frame1.pack(pady=10, anchor="w")

# === Dark Mode ===
def alternar_tema():
    global modo_escuro_ativo
    modo_escuro_ativo = not modo_escuro_ativo
    aplicar_tema(escuro=modo_escuro_ativo)

# btn_tema = tk.Button(frame1, text="🌓 Alternar Tema", command=alternar_tema)
# btn_tema.grid(row=0, column=8, padx=5)

# =================

tk.Label(frame1, text="Base:" ).grid(row=0, column=0)
combo_base = ttk.Combobox(frame1, values=[b["nome"] for b in bases_disponiveis], state="readonly", width=25)
combo_base.grid(row=0, column=1)
combo_base.current(0)
tk.Button(frame1, text="Conectar", command=conectar_base).grid(row=0, column=2, padx=5)

tk.Label(frame1, text="ID do Evento:").grid(row=0, column=3)
entry_id = tk.Entry(frame1, width=45)
entry_id.grid(row=0, column=4)
tk.Button(frame1, text="Carregar", command=carregar_xml).grid(row=0, column=5, padx=5)
tk.Button(frame1, text="Salvar", command=salvar_xml).grid(row=0, column=6, padx=5)

def abrir_backup():
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

        # Legenda de cores
        frame_legenda = tk.Frame(comp, bg="#f0f0f0")
        frame_legenda.pack(pady=5)

        tk.Label(frame_legenda, text="🟩 Adicionado", bg="#eaffea", fg="black", padx=8).grid(row=0, column=0, padx=5)
        tk.Label(frame_legenda, text="🟥 Removido", bg="#ffeaea", fg="black", padx=8).grid(row=0, column=1, padx=5)
        tk.Label(frame_legenda, text="🟨 Modificado", bg="#fff7c0", fg="black", padx=8).grid(row=0, column=2, padx=5)

        # Cabeçalhos
        frame_titles = tk.Frame(comp)
        frame_titles.pack()
        tk.Label(frame_titles, text="📝 Atual", fg="blue", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, padx=20)
        tk.Label(frame_titles, text=f"📦 Backup: {nome}", fg="green", font=("Segoe UI", 10, "bold")).grid(row=0, column=1, padx=20)

        # Área de texto lado a lado com rolagens sincronizadas
        frame_texts = tk.Frame(comp)
        frame_texts.pack()

        scroll = tk.Scrollbar(frame_texts, orient=tk.VERTICAL)
        scroll.grid(row=0, column=2, sticky="ns")

        txt_atual = scrolledtext.ScrolledText(frame_texts, wrap=tk.NONE, width=70, height=35, font=("Courier New", 9), yscrollcommand=scroll.set)
        txt_atual.grid(row=0, column=0, padx=(10, 5))
        txt_backup = scrolledtext.ScrolledText(frame_texts, wrap=tk.NONE, width=70, height=35, font=("Courier New", 9), yscrollcommand=scroll.set)
        txt_backup.grid(row=0, column=1, padx=(5, 10))
        scroll.config(command=lambda *args: (txt_atual.yview(*args), txt_backup.yview(*args)))

        def on_scroll(*args):
            txt_atual.yview_moveto(args[0])
            txt_backup.yview_moveto(args[0])

        txt_atual.configure(yscrollcommand=on_scroll)
        txt_backup.configure(yscrollcommand=on_scroll)

        # Tags de destaque
        txt_atual.tag_config("modificado", background="#fff7c0")
        txt_atual.tag_config("adicao", background="#eaffea")
        txt_backup.tag_config("modificado", background="#fff7c0")
        txt_backup.tag_config("remocao", background="#ffeaea")

        # Comparar linha a linha
        max_linhas = max(len(conteudo_backup), len(conteudo_atual))
        for i in range(max_linhas):
            linha_atual = conteudo_atual[i] if i < len(conteudo_atual) else ""
            linha_backup = conteudo_backup[i] if i < len(conteudo_backup) else ""

            if linha_atual == linha_backup:
                txt_atual.insert(tk.END, linha_atual + "\n")
                txt_backup.insert(tk.END, linha_backup + "\n")
            elif linha_atual.strip() == "" and linha_backup.strip():
                pos = txt_backup.index(tk.END)
                txt_backup.insert(tk.END, linha_backup + "\n", "remocao")
                txt_atual.insert(tk.END, "\n")
            elif linha_backup.strip() == "" and linha_atual.strip():
                pos = txt_atual.index(tk.END)
                txt_atual.insert(tk.END, linha_atual + "\n", "adicao")
                txt_backup.insert(tk.END, "\n")
            else:
                pos_a = txt_atual.index(tk.END)
                txt_atual.insert(tk.END, linha_atual + "\n", "modificado")
                pos_b = txt_backup.index(tk.END)
                txt_backup.insert(tk.END, linha_backup + "\n", "modificado")

        if modo_escuro_ativo:
            for widget in [comp, frame_legenda, frame_titles, frame_texts, txt_atual, txt_backup]:
                try:
                    widget.configure(bg="#1e1e1e")
                except:
                    pass
                
            for text in [txt_atual, txt_backup]:
                text.configure(
                    bg="#1e1e1e",
                    fg="#e0e0e0",
                    insertbackground="white",
                    selectbackground="#264f78"
                )

        txt_atual.config(state=tk.DISABLED)
        txt_backup.config(state=tk.DISABLED)

        # Botão para restaurar
        def restaurar_backup_no_editor():
            confirm = messagebox.askyesno("Restaurar Backup", "Deseja carregar este backup no editor?\n(É necessário clicar em SALVAR depois para aplicar no banco)")
            if confirm:
                text_xml.delete("1.0", tk.END)
                text_xml.insert(tk.END, "\n".join(conteudo_backup))
                realcar_sintaxe_xml()
                status_var.set(f"Backup {nome} carregado no editor.")

        tk.Button(comp, text="⏪ Restaurar este backup", fg="white", bg="green", command=restaurar_backup_no_editor).pack(pady=10)

    tk.Button(janela, text="Comparar com Backup Selecionado", command=exibir_comparacao).pack(pady=10)

tk.Button(frame1, text="Ver Backup", command=abrir_backup).grid(row=0, column=7, padx=5)

# === Barra de busca e substituição ===
frame2 = tk.Frame(root)
frame2.pack(pady=5, anchor="w")

tk.Label(frame2, text="Buscar:").grid(row=0, column=0)
entry_busca = tk.Entry(frame2, width=30)
entry_busca.grid(row=0, column=1, padx=5)

tk.Label(frame2, text="Substituir por:").grid(row=0, column=3)
entry_substituir = tk.Entry(frame2, width=30)
entry_substituir.grid(row=0, column=3, padx=5)

tk.Button(frame2, text="Localizar", command=buscar_texto).grid(row=0, column=4, padx=5)
tk.Button(frame2, text="Substituir", command=substituir_proxima).grid(row=0, column=5, padx=5)
tk.Button(frame2, text="Substituir todos", command=substituir_todos).grid(row=0, column=6, padx=5)

# === Editor XML ===
text_xml = text_xml = scrolledtext.ScrolledText(root, wrap=tk.WORD)
text_xml.pack(padx=10, pady=10, fill="both", expand=True)

# === Barra de status ===
status_var = tk.StringVar()
status_label = tk.Label(root, textvariable=status_var, fg="blue")
status_label.pack()

# === Sobre ===

import webbrowser

def abrir_github():
    webbrowser.open_new("https://github.com/Robert-TaylorMF")

def mostrar_sobre():
    sobre = tk.Toplevel(root)
    sobre.title("Sobre o XMLEditor RM")
    sobre.geometry("400x270")
    sobre.resizable(False, False)
    sobre.configure(bg="#1e1e1e")

    tk.Label(sobre, text="XMLEditor RM", font=("Segoe UI", 16, "bold"), fg="#4fc3f7", bg="#1e1e1e").pack(pady=(20, 5))
    tk.Label(sobre, text="Editor de eventos eSocial com backup inteligente", fg="#dddddd", bg="#1e1e1e").pack(pady=2)
    tk.Label(sobre, text="Versão: 1.1", fg="#bbbbbb", bg="#1e1e1e").pack(pady=2)
    tk.Label(sobre, text="Desenvolvido por: Robert Taylor de M. Ferreira", fg="#81c784", bg="#1e1e1e").pack(pady=10)
    tk.Label(sobre, text="© 2025", font=("Segoe UI", 8), fg="#888888", bg="#1e1e1e").pack(pady=0)

    tk.Button(sobre, text="Ver no GitHub", command=abrir_github, bg="#2e2e2e", fg="#00afff").pack(pady=(15, 5))
    tk.Button(sobre, text="Fechar", command=sobre.destroy, bg="#2e2e2e", fg="white").pack()

# === Botão verificar atualizações ===
tk.Button(root, text="Verificar Atualização", command=verificar_atualizacao).pack(pady=10)

# === Botão sobre ===
tk.Button(root, text="Sobre", command=mostrar_sobre).pack(pady=10)

# === Iniciar no modo claro ===
def aplicar_tema(escuro=True):
    fundo = "#1e1e1e" if escuro else "#ffffff"
    texto = "#e0e0e0" if escuro else "#000000"
    input_bg = "#2e2e2e" if escuro else "#ffffff"
    destaque = "#264f78" if escuro else "yellow"
    barra_status = "#1e1e1e" if escuro else "#f0f0f0"
    fonte_status = "#aaaaaa" if escuro else "#0000aa"

    root.configure(bg=fundo)
    for frame in [frame1, frame2]:
        frame.configure(bg=fundo)
        for child in frame.winfo_children():
            try:
                if isinstance(child, tk.Label):
                    child.configure(bg=frame.cget("bg"), fg=texto)
                else:
                    child.configure(bg=input_bg, fg=texto, insertbackground=texto)
            except:
                pass

    text_xml.configure(
        bg=fundo,
        fg=texto,
        insertbackground=texto,
        selectbackground=destaque
    )
    status_label.configure(bg=barra_status, fg=fonte_status)

    # Realce de sintaxe
    text_xml.tag_config("tag", foreground="#569cd6")
    text_xml.tag_config("atributo", foreground="#d19a66")
    text_xml.tag_config("valor", foreground="#98c379")
    text_xml.tag_config("destacado", background=destaque)

# === Iniciar aplicação ===
verificar_driver_sql()
root.mainloop()