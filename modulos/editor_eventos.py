import customtkinter as ctk
from tkinter import messagebox
from conexao import obter_conexao
from PIL import Image
from tkinter import Toplevel
from tkcalendar import Calendar
from datetime import datetime
from utilitarios import extrair_conteudo_esocial

def cor_por_tipo(tipo):
    cores = {
        "S-1200": "#64dd17", "S-1210": "#2196f3", "S-2205": "#ab47bc", "S-2299": "#ff7043"
    }
    return cores.get(tipo, "#90a4ae")

status_opcoes = {
    "0": "0 - Pendente", "1": "1 - Gerado", "2": "2 - Erro na geração",
    "3": "3 - Enviado", "4": "4 - Aceito TAF", "5": "5 - Erro na integração TAF",
    "6": "6 - Rejeitado TAF", "9": "9 - Rejeitado RET",
    "10": "10 - Aceito RET", "11": "11 - Excluído RET"
}

tipo_eventos = [
    "S-1000", "S-1005", "S-1010", "S-1020", "S-1030", "S-1035", "S-1040", "S-1050",
    "S-1060", "S-1070", "S-1080", "S-1100", "S-1200", "S-1202", "S-1207", "S-1210", "S-1250",
    "S-1295", "S-1298", "S-1299", "S-1300", "S-2200", "S-2205", "S-2210", "S-2220", "S-2230",
    "S-2240", "S-2299", "S-2300", "S-2306", "S-2399", "S-3000"
]

def aplicar_hover(widget, cor_normal="#2b2b2b", cor_hover="#383838"):
    widget.bind("<Enter>", lambda e: widget.configure(fg_color=cor_hover))
    widget.bind("<Leave>", lambda e: widget.configure(fg_color=cor_normal))

def abrir_calendario(callback):
    def selecionar_data():
        data = cal.selection_get()
        janela_cal.destroy()
        callback(data)

    janela_cal = Toplevel()
    janela_cal.title("Selecionar Data")
    janela_cal.configure(bg="gray15")
    cal = Calendar(janela_cal, selectmode='day', year=2025, month=7, day=1,
                   background="gray20", foreground="white", headersbackground="gray25",
                   selectbackground="#3949ab")
    cal.pack(pady=10)
    ctk.CTkButton(janela_cal, text="Selecionar", command=selecionar_data).pack(pady=10)

def abrir_seletor_eventos(base_selecionada_dict):
    if not base_selecionada_dict or not base_selecionada_dict.get("database"):
        messagebox.showwarning("Base não conectada", "Conecte-se a uma base antes de usar o editor de eventos.")
        return

    conexao = obter_conexao(base_selecionada_dict)
    if not conexao:
        messagebox.showerror("Erro", "Não foi possível conectar à base selecionada.")
        return

    janela = ctk.CTkToplevel()
    janela.title("Filtro de Eventos XML")
    janela.geometry("1000x720")
    janela.configure(fg_color="#1e1e1e")
    janela.grab_set()

    ctk.CTkLabel(janela, text="Filtro de Eventos XML", font=("Segoe UI", 17, "bold"), text_color="#ffffff").pack(pady=12)

    frame_filtros = ctk.CTkFrame(janela, fg_color="#2b2b2b", corner_radius=10)
    frame_filtros.pack(padx=10, pady=10, fill="x")

    campo_id        = ctk.CTkEntry(frame_filtros, placeholder_text="ID Evento", width=160)
    campo_chapa     = ctk.CTkEntry(frame_filtros, placeholder_text="CHAPA", width=100)
    campo_codpessoa = ctk.CTkEntry(frame_filtros, placeholder_text="Pessoa", width=120)
    campo_tipo      = ctk.CTkComboBox(frame_filtros, width=120, values=tipo_eventos)
    campo_tipo.set("Selecione o tipo")
    campo_status    = ctk.CTkComboBox(frame_filtros, width=180, values=list(status_opcoes.values()))
    campo_status.set("Selecione o status")
    campo_anocomp   = ctk.CTkEntry(frame_filtros, placeholder_text="Ano", width=80)
    campo_mescomp   = ctk.CTkEntry(frame_filtros, placeholder_text="Mês", width=80)

    def preencher_data(data):
        campo_anocomp.delete(0, 'end')
        campo_mescomp.delete(0, 'end')
        campo_anocomp.insert(0, str(data.year))
        campo_mescomp.insert(0, f"{data.month:02}")

    btn_data = ctk.CTkButton(
        frame_filtros, text="📅", width=40,
        command=lambda: [janela.grab_release(), abrir_calendario(preencher_data)],
        fg_color="#424242", hover_color="#616161"
    )

    try:
        lupa_image = Image.open("lupa.ico")
        lupa_icon = ctk.CTkImage(dark_image=lupa_image, size=(22, 22))
    except:
        lupa_icon = None

    botao_buscar = ctk.CTkButton(
        frame_filtros, text="", image=lupa_icon, width=40, height=40,
        command=None, fg_color="transparent", hover_color="#303030"
    )

    campo_id.grid(row=0, column=0, padx=6, pady=6)
    campo_chapa.grid(row=0, column=1, padx=6, pady=6)
    campo_codpessoa.grid(row=0, column=2, padx=6, pady=6)
    campo_tipo.grid(row=0, column=3, padx=6, pady=6)
    campo_status.grid(row=0, column=4, padx=6, pady=6)
    campo_anocomp.grid(row=0, column=5, padx=6, pady=6)
    campo_mescomp.grid(row=0, column=6, padx=6, pady=6)
    btn_data.grid(row=0, column=7, padx=4, pady=6)
    botao_buscar.grid(row=0, column=8, padx=6, pady=6)

    frame_resultados = ctk.CTkScrollableFrame(janela, height=460, corner_radius=12, fg_color="#1e1e1e")
    frame_resultados.pack(fill="both", expand=True, padx=10, pady=12)
    
    def buscar_eventos():
        tipo_valor = campo_tipo.get()
        status_valor = campo_status.get()

        filtros = {
            "ID": campo_id.get().strip(),
            "CHAPA": campo_chapa.get().strip(),
            "TIPOEVENTO": tipo_valor if tipo_valor and "Selecione" not in tipo_valor else "",
            "STATUS": status_valor.split(" ")[0] if status_valor and "Selecione" not in status_valor else "",
            "ANOCOMP": campo_anocomp.get().strip(),
            "MESCOMP": campo_mescomp.get().strip(),
            "CODPESSOA": campo_codpessoa.get().strip()
        }

        clausulas = [f"{campo} LIKE '%{valor}%'" for campo, valor in filtros.items() if valor]
        where = " AND ".join(clausulas) if clausulas else "1=1"

        query = f"""
            SELECT TOP 50 ID, CHAPA, TIPOEVENTO, DATAEVENTO, STATUS,
                           CODPESSOA, ANOCOMP, MESCOMP
            FROM PESOCIALEVENTOS
            WHERE {where}
            ORDER BY TIPOEVENTO ASC, DATAEVENTO DESC
        """

        try:
            cursor = conexao.cursor()
            cursor.execute(query)
            eventos = cursor.fetchall()
        except Exception as e:
            messagebox.showerror("Erro SQL", f"Erro ao buscar eventos:\n{e}")
            return

        for widget in frame_resultados.winfo_children():
            widget.destroy()

        if not eventos:
            ctk.CTkLabel(frame_resultados, text="Nenhum evento encontrado.",
                         font=("Segoe UI", 13), text_color="#ffffff").pack(pady=12)
            return

        for evento in eventos:
            id_evt, chapa, tipo, data, status, codpessoa, ano, mes = evento
            cor = cor_por_tipo(tipo)
            status_str = status_opcoes.get(str(status), "Desconhecido")

            card = ctk.CTkFrame(frame_resultados, corner_radius=12, fg_color="#2b2b2b")
            card.pack(fill="x", padx=10, pady=8)
            aplicar_hover(card)

            ctk.CTkLabel(card, text=f"Evento ID: {id_evt}",
                         font=("Segoe UI", 16, "bold"), text_color="#42a5f5").pack(anchor="w", padx=12, pady=2)

            ctk.CTkLabel(card, text=f"{tipo} • Status: {status_str}",
                         font=("Segoe UI", 13, "bold"), text_color=cor).pack(anchor="w", padx=12, pady=2)

            ctk.CTkLabel(card, text=f"CHAPA: {chapa} • Pessoa: {codpessoa} • Competência: {mes}/{ano}",
                         font=("Segoe UI", 12), text_color="#d3d3d3").pack(anchor="w", padx=12, pady=2)

            ctk.CTkButton(
                card,
                text="Editar XML",
                font=("Segoe UI", 12, "bold"),
                width=130,
                fg_color="#424242",
                text_color="#ffffff",
                hover_color="#616161",
                corner_radius=8,
                command=lambda eid=id_evt: abrir_editor_xml(eid)
            ).pack(anchor="e", padx=10, pady=10)

    botao_buscar.configure(command=buscar_eventos)

    # 🧾 Editor de XML
    def abrir_editor_xml(evt_id):
        try:
            cursor = conexao.cursor()
            cursor.execute("SELECT mensagem FROM PESOCIALEVENTOS WHERE ID = ?", evt_id)
            resultado = cursor.fetchone()

            if not resultado or not resultado[0]:
                messagebox.showwarning("XML ausente", "Este evento não possui XML para exibir.")
                return

            xml_original = resultado[0]
            xml_tratado = extrair_conteudo_esocial(xml_original)

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao buscar XML:\n{e}")
            return

        janela_editor = ctk.CTkToplevel()
        janela_editor.title(f"Editor XML - Evento {evt_id}")
        janela_editor.geometry("800x600")
        janela_editor.configure(fg_color="#1e1e1e")

        janela_editor.transient(janela)
        janela_editor.focus_force()
        janela_editor.lift()
        janela_editor.attributes("-topmost", True)
        janela_editor.grab_set()
        
        modo_edicao = [False]

        campo_texto = ctk.CTkTextbox(janela_editor, wrap="word", font=("Consolas", 12))
        campo_texto.insert("1.0", xml_tratado)
        campo_texto.configure(state="disabled")
        campo_texto.pack(expand=True, fill="both", padx=12, pady=12)

        def alternar_modo():
            if modo_edicao[0]:
                campo_texto.configure(state="disabled")
                botao_salvar.pack_forget()
                botao_editar.configure(text="Editar XML")
                modo_edicao[0] = False
            else:
                campo_texto.configure(state="normal")
                botao_salvar.pack(pady=10)
                botao_editar.configure(text="Cancelar edição")
                modo_edicao[0] = True

        def salvar_alteracoes():
            conteudo_editado = campo_texto.get("1.0", "end").strip()
            xml_compactado = " ".join(conteudo_editado.split())

            try:
                cursor.execute("UPDATE PESOCIALEVENTOS SET mensagem = ? WHERE ID = ?", xml_compactado, evt_id)
                conexao.commit()
                messagebox.showinfo("Sucesso", "XML atualizado com sucesso!")
                janela_editor.destroy()
            except Exception as e:
                messagebox.showerror("Erro ao salvar", f"{e}")

        botao_editar = ctk.CTkButton(janela_editor, text="Editar XML", command=alternar_modo,
                                     fg_color="#3949ab", hover_color="#5c6bc0")
        botao_editar.pack(pady=8)

        botao_salvar = ctk.CTkButton(janela_editor, text="Salvar alterações", command=salvar_alteracoes,
                                     fg_color="#2e7d32", hover_color="#388e3c")