import tkinter as tk
from modulos.scroll_canvas import ScrollCanvas

def criar_editor_com_linhas(pai, fonte=("Consolas", 12), bg="#1e1e1e", fg="white"):
    # Frame principal do editor
    frame_editor = tk.Frame(pai)
    frame_editor.pack(fill="both", expand=True, padx=10, pady=10)

    # Régua lateral com numeração de linhas
    linha_numero = tk.Text(frame_editor, width=4, padx=4, bg="#2b2b2b", fg="gray",
                           font=fonte, state="disabled", relief="flat")
    linha_numero.pack(side="left", fill="y")
    linha_numero.configure(cursor="arrow", takefocus=0)

    # Bloqueia interação com a régua
    for evento in ["<MouseWheel>", "<Button-4>", "<Button-5>", "<Key>", "<ButtonPress-1>", "<B1-Motion>"]:
        linha_numero.bind(evento, lambda e: "break")

    # Editor principal de texto XML
    text_xml = tk.Text(frame_editor, wrap="none", font=fonte,
                       bg=bg, fg=fg, insertbackground=fg, undo=True)
    text_xml.pack(side="left", fill="both", expand=True)

    # Scrollbar personalizada com Canvas
    scrollbar = ScrollCanvas(frame_editor)
    scrollbar.pack(side="right", fill="y")
    scrollbar.connect(text_xml)

    # Tag para destacar a linha atual
    text_xml.tag_configure("linha_atual", background="#2e2e2e")

    def atualizar_linhas(event=None):
        # Atualiza a numeração lateral
        linha_numero.config(state="normal")
        linha_numero.delete("1.0", "end")
        try:
            total = int(text_xml.index("end-1c").split(".")[0])
        except:
            total = 1
        linhas = "\n".join(str(i) for i in range(1, total + 1))
        linha_numero.insert("1.0", linhas)
        linha_numero.config(state="disabled")

        # Mantém visual sincronizado com conteúdo
        linha_numero.yview_moveto(text_xml.yview()[0])

    def realcar_linha_atual(event=None):
        # Remove destaque anterior
        text_xml.tag_remove("linha_atual", "1.0", "end")

        # Aplica destaque à linha atual
        linha = text_xml.index("insert").split(".")[0]
        inicio = f"{linha}.0"
        fim = f"{linha}.end"
        text_xml.tag_add("linha_atual", inicio, fim)

    # Eventos que disparam as atualizações
    eventos = ["<KeyRelease>", "<ButtonRelease-1>", "<MouseWheel>", "<Configure>"]
    for evento in eventos:
        text_xml.bind(evento, lambda e: [atualizar_linhas(), realcar_linha_atual()])

    atualizar_linhas()
    realcar_linha_atual()
    return text_xml