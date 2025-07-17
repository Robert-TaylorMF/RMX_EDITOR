import tkinter as tk
from modulos.scroll_canvas import ScrollCanvas

def criar_editor_com_linhas(pai, fonte=("Consolas", 12), bg="#1e1e1e", fg="white"):
    # Frame que agrupa régua e editor
    frame_editor = tk.Frame(pai)
    frame_editor.pack(fill="both", expand=True, padx=10, pady=10)

    # Régua de numeração de linha
    linha_numero = tk.Text(frame_editor, width=4, padx=4, bg="#2b2b2b", fg="gray",
                           font=fonte, state="disabled", relief="flat")
    linha_numero.pack(side="left", fill="y")
    linha_numero.configure(cursor="arrow", takefocus=0)

    # Bloqueia interação com régua
    for evento in ["<MouseWheel>", "<Button-4>", "<Button-5>", "<Key>", "<ButtonPress-1>", "<B1-Motion>"]:
        linha_numero.bind(evento, lambda e: "break")

    # Editor principal de texto
    text_xml = tk.Text(frame_editor, wrap="none", font=fonte,
                       bg=bg, fg=fg, insertbackground=fg)
    text_xml.pack(side="left", fill="both", expand=True)

    # Scrollbar personalizada com Canvas
    scrollbar = ScrollCanvas(frame_editor)
    scrollbar.pack(side="right", fill="y")
    scrollbar.connect(text_xml)

    def atualizar_linhas(event=None):
        linha_numero.config(state="normal")
        linha_numero.delete("1.0", "end")

        try:
            total = int(text_xml.index("end-1c").split(".")[0])
        except:
            total = 1

        linhas = "\n".join(str(i) for i in range(1, total + 1))
        linha_numero.insert("1.0", linhas)
        linha_numero.config(state="disabled")

        # Sincroniza a view da régua com o texto
        linha_numero.yview_moveto(text_xml.yview()[0])

    # Eventos que disparam a atualização
    for evento in ["<KeyRelease>", "<ButtonRelease-1>", "<MouseWheel>", "<Configure>"]:
        text_xml.bind(evento, atualizar_linhas)

    atualizar_linhas()
    return text_xml