import customtkinter as ctk

def configurar_atalhos(root, text_xml, status_var, base_selecionada, entry_id, botao_salvar):
    
    from comparador import abrir_backup
    from utilitarios import realcar_sintaxe_xml

    # 🔍 CTRL + F — abrir janela de busca/substituição
    def abrir_localizador():
        janela = ctk.CTkToplevel(root)
        janela.title("Localizar e Substituir")
        janela.geometry("400x300")
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
                realcar_sintaxe_xml(text_xml)
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
                realcar_sintaxe_xml(text_xml)
                resultado_var.set(f"{total} substituição(ões) feita(s)")
                
        def substituir_tudo():
            termo = campo_busca.get()
            novo = campo_substituir.get()
            if termo and novo:
                conteudo = text_xml.get("1.0", "end")
                atualizado = conteudo.replace(termo, novo)
                text_xml.delete("1.0", "end")
                text_xml.insert("end", atualizado)
                realcar_sintaxe_xml(text_xml)
                ocorrencias = atualizado.count(novo)
                resultado_var.set(f"{ocorrencias} substituição(ões) feita(s)")

        ctk.CTkButton(janela, text="Localizar", command=localizar).pack(pady=(10, 2))
        ctk.CTkButton(janela, text="Substituir", command=substituir).pack(pady=2)
        ctk.CTkButton(janela, text="Substituir Todas", command=substituir_tudo).pack(pady=2)

    # 🧩 Binds de atalhos globais
    root.bind_all("<Control-s>", lambda e: botao_salvar.invoke())
    root.bind_all("<Control-f>", lambda e: abrir_localizador())
    root.bind_all("<Control-b>", lambda e: abrir_backup(root, text_xml, status_var))