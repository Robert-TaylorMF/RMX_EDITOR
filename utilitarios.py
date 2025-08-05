import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import tempfile
import win32print
import win32api
import os
import re
from datetime import datetime
import xml.dom.minidom

# Caminho da pasta recurso
def caminho_recurso(nome_arquivo):
    import sys, os
    base = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "recursos", nome_arquivo)

# 📋 Copiar texto selecionado do editor
def copiar_texto(editor_frame):
    text_widget = editor_frame.editor_texto if hasattr(editor_frame, "editor_texto") else editor_frame
    try:
        texto = text_widget.get("sel.first", "sel.last")
        text_widget.clipboard_clear()
        text_widget.clipboard_append(texto)
    except tk.TclError:
        pass

# 📥 Colar conteúdo do clipboard na posição atual do cursor
def colar_texto(editor_frame):
    text_widget = editor_frame.editor_texto if hasattr(editor_frame, "editor_texto") else editor_frame
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
        return nome_arquivo
    except Exception as e:
        messagebox.showerror("Erro ao salvar backup", str(e))

# 🎨 Realça tags, atributos e valores no XML
def realcar_sintaxe_xml(editor_frame):
    text_widget = editor_frame.editor_texto if hasattr(editor_frame, "editor_texto") else editor_frame
    text_widget.tag_delete("tag", "atributo", "valor")

    xml = text_widget.get("1.0", tk.END)
    padrao_tag = re.compile(r"<[^!?][^>]*?>")
    padrao_atributo = re.compile(r"\b([\w:.-]+)\s*=")
    padrao_valor = re.compile(r'"(.*?)"')

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

    text_widget.tag_config("tag", foreground="#00ccff")
    text_widget.tag_config("atributo", foreground="#ff7700")
    text_widget.tag_config("valor", foreground="#00ff99")

# 🔧 Compacta XML removendo quebras e espaços entre tags
def compactar_xml(xml_str):
    return re.sub(r">\s+<", "><", xml_str.strip()).replace("\n", "").strip()

# 🧾 Extrai apenas o conteúdo do <eSocial>
def extrair_conteudo_esocial(xml_str):
    xml_str = xml_str.strip()
    match = re.search(r"(<eSocial[\s\S]*</eSocial>)", xml_str)
    return match.group(1).strip() if match else xml_str

# 🔠 Atualiza fonte no editor e régua lateral
def atualizar_fonte_em_editor(editor_frame, fonte):
    try:
        editor_texto = editor_frame.editor_texto
        linha_texto = editor_frame.linha_texto
        editor_texto.config(font=fonte)
        linha_texto.config(font=fonte)
    except Exception as e:
        print(f"Erro ao atualizar fonte: {e}")

def aumentar_fonte(editor_frame, fonte_editor):
    fonte_editor[1] = min(36, fonte_editor[1] + 1)
    atualizar_fonte_em_editor(editor_frame, tuple(fonte_editor))

def diminuir_fonte(editor_frame, fonte_editor):
    fonte_editor[1] = max(8, fonte_editor[1] - 1)
    atualizar_fonte_em_editor(editor_frame, tuple(fonte_editor))

# 📤 Exporta o XML para um arquivo
def exportar_xml(editor_frame):
    editor = editor_frame.editor_texto if hasattr(editor_frame, "editor_texto") else editor_frame
    conteudo = editor.get("1.0", "end").strip()
    if not conteudo:
        return

    caminho = filedialog.asksaveasfilename(
        defaultextension=".xml",
        filetypes=[("Arquivos XML", "*.xml")],
        title="Exportar XML"
    )
    if caminho:
        with open(caminho, "w", encoding="utf-8") as f:
            f.write(conteudo)

# 🖨️ Imprime o XML com seleção de impressora
def imprimir_xml(editor_frame):
    editor = editor_frame.editor_texto if hasattr(editor_frame, "editor_texto") else editor_frame
    conteudo = editor.get("1.0", "end").strip()
    if not conteudo:
        return

    with tempfile.NamedTemporaryFile(delete=False, suffix=".txt", mode="w", encoding="utf-8") as temp:
        temp.write(conteudo)
        caminho_temp = temp.name

    impressora_padrao = win32print.GetDefaultPrinter()
    lista = [printer[2] for printer in win32print.EnumPrinters(2)]

    escolha = tk.Toplevel()
    escolha.title("Escolher impressora")
    escolha.geometry("400x120")
    escolha.grab_set()

    var_impressora = tk.StringVar(value=impressora_padrao)

    tk.Label(escolha, text="Escolha a impressora:", font=("Arial", 12)).pack(pady=10)
    box = tk.OptionMenu(escolha, var_impressora, *lista)
    box.pack(pady=5)

    def enviar():
        nome = var_impressora.get()
        escolha.destroy()
        try:
            win32print.SetDefaultPrinter(nome)
            win32api.ShellExecute(0, "print", caminho_temp, None, ".", 0)
        except Exception as e:
            print("Erro ao imprimir:", e)

    tk.Button(escolha, text="Imprimir", command=enviar).pack(pady=10)

# 📄 Gera PDF estilizado com ReportLab
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Preformatted
from reportlab.lib.units import mm

def gerar_e_abrir_pdf_xml(editor_frame):
    editor = editor_frame.editor_texto if hasattr(editor_frame, "editor_texto") else editor_frame
    conteudo = editor.get("1.0", "end").strip()
    if not conteudo:
        print("Nenhum conteúdo para gerar PDF.")
        return

    try:
        caminho_pdf = os.path.join(tempfile.gettempdir(), "xml_gerado.pdf")
        doc = SimpleDocTemplate(caminho_pdf, pagesize=A4, rightMargin=20, leftMargin=20, topMargin=20, bottomMargin=20)

        estilo = getSampleStyleSheet()["Code"]
        estilo.fontName = "Courier"
        estilo.fontSize = 10
        estilo.leading = 12
        estilo.leftIndent = 0

        elemento = Preformatted(conteudo, estilo)
        doc.build([elemento])

        os.startfile(caminho_pdf)
    except Exception as e:
        print("Erro ao gerar PDF do XML:", e)
        
# 📥 Prepara XML para gravação no banco

def preparar_xml_para_salvar(xml_bruto):
    return compactar_xml(extrair_conteudo_esocial(xml_bruto))

import customtkinter as ctk
from tkinter import ttk

def abrir_localizador_substituir(text_widget, root):
    janela = ctk.CTkToplevel(root)
    janela.title("🔍 Localizar e Substituir")
    janela.geometry("460x300")
    janela.resizable(False, False)
    janela.grab_set()

    estilo_entry = {"font": ("Consolas", 12), "width": 320}
    estilo_btn = {"height": 32, "corner_radius": 6}

    aba_control = ctk.CTkTabview(janela, width=440, height=240)
    aba_control.pack(padx=10, pady=10)
    aba_control.add("Localizar")
    aba_control.add("Substituir")

    # ========================= ABA LOCALIZAR =========================
    aba_localizar = aba_control.tab("Localizar")

    entry_termo = ctk.CTkEntry(aba_localizar, placeholder_text="Texto para localizar", **estilo_entry)
    entry_termo.pack(pady=(15, 5))

    def buscar_ocorrencias():
        termo = entry_termo.get()
        if not termo:
            return
        text_widget.tag_remove("busca", "1.0", "end")
        primeira = None
        pos = "1.0"
        while True:
            pos = text_widget.search(termo, pos, nocase=1, stopindex="end")
            if not pos:
                break
            fim = f"{pos}+{len(termo)}c"
            text_widget.tag_add("busca", pos, fim)
            if not primeira:
                primeira = pos
            pos = fim
        text_widget.tag_config("busca", background="#3b82f6")
        if primeira:
            text_widget.see(primeira)
            text_widget.mark_set("insert", primeira)
            text_widget.focus_set()

    def proxima_ocorrencia():
        termo = entry_termo.get()
        if not termo:
            return
        atual = text_widget.index("insert")
        pos = text_widget.search(termo, atual, nocase=1, stopindex="end")
        if pos:
            fim = f"{pos}+{len(termo)}c"
            text_widget.tag_remove("selecionado", "1.0", "end")
            text_widget.tag_add("selecionado", pos, fim)
            text_widget.tag_config("selecionado", background="#2dd4bf")
            text_widget.mark_set("insert", fim)
            text_widget.see(pos)

    btn_buscar = ctk.CTkButton(aba_localizar, text="Localizar", command=buscar_ocorrencias, **estilo_btn)
    btn_proxima = ctk.CTkButton(aba_localizar, text="Próxima ocorrência", command=proxima_ocorrencia, **estilo_btn)

    btn_buscar.pack(pady=5)
    btn_proxima.pack(pady=5)

    # ========================= ABA SUBSTITUIR =========================
    aba_substituir = aba_control.tab("Substituir")

    entry_de = ctk.CTkEntry(aba_substituir, placeholder_text="Texto a localizar", **estilo_entry)
    entry_para = ctk.CTkEntry(aba_substituir, placeholder_text="Substituir por", **estilo_entry)
    entry_de.pack(pady=(15, 5))
    entry_para.pack(pady=(0, 10))

    def substituir_atual():
        termo = entry_de.get()
        novo = entry_para.get()
        if not termo:
            return
        atual = text_widget.search(termo, "insert", nocase=1, stopindex="end")
        if atual:
            fim = f"{atual}+{len(termo)}c"
            text_widget.delete(atual, fim)
            text_widget.insert(atual, novo)
            text_widget.mark_set("insert", f"{atual}+{len(novo)}c")
            text_widget.see(atual)

    def substituir_todos():
        termo = entry_de.get()
        novo = entry_para.get()
        if not termo:
            return
        pos = "1.0"
        while True:
            pos = text_widget.search(termo, pos, nocase=1, stopindex="end")
            if not pos:
                break
            fim = f"{pos}+{len(termo)}c"
            text_widget.delete(pos, fim)
            text_widget.insert(pos, novo)
            pos = f"{pos}+{len(novo)}c"

    btn_substituir = ctk.CTkButton(aba_substituir, text="Substituir atual", command=substituir_atual, **estilo_btn)
    btn_tudo = ctk.CTkButton(aba_substituir, text="Substituir todos", command=substituir_todos, **estilo_btn)

    btn_substituir.pack(pady=5)
    btn_tudo.pack(pady=5)

    janela.bind("<Return>", lambda e: buscar_ocorrencias())