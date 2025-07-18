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

    text_widget.tag_config("tag", foreground="#00ccff")
    text_widget.tag_config("atributo", foreground="#ff7700")
    text_widget.tag_config("valor", foreground="#00ff99")
    
def abrir_localizador(editor_frame, root):
    text_xml = editor_frame.editor_texto if hasattr(editor_frame, "editor_texto") else editor_frame

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
            realcar_sintaxe_xml(editor_frame)
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
            realcar_sintaxe_xml(editor_frame)
            resultado_var.set(f"{total} substituição(ões) feita(s)")

    ctk.CTkButton(janela, text="🔍 Localizar", command=localizar).pack(pady=(10, 2))
    ctk.CTkButton(janela, text="↺ Substituir", command=substituir).pack(pady=2)
    ctk.CTkButton(janela, text="🔁 Substituir Todas", command=substituir_tudo).pack(pady=2)
    
# 🔧 Compacta XML removendo quebras e espaços entre tags
def compactar_xml(xml_str):
    return re.sub(r">\s+<", "><", xml_str.strip())

# 🧾 Extrai apenas o conteúdo do <eSocial>
def extrair_conteudo_esocial(xml_str):
    xml_str = xml_str.strip()
    inicio = xml_str.find("<eSocial")
    return xml_str[inicio:] if inicio != -1 else xml_str

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
        print("⚠️ Nenhum conteúdo para gerar PDF.")
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
        print("❌ Erro ao gerar PDF do XML:", e)