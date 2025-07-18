import tkinter as tk

# 🟨 Destacar linhas com resultados de busca
def destacar_ocorrencias(text_widget, termo, cor="#3c3c3c"):
    text_widget.tag_remove("busca_ocorrencia", "1.0", "end")
    if not termo:
        return

    text_widget.tag_configure("busca_ocorrencia", background=cor)
    idx = "1.0"
    while True:
        idx = text_widget.search(termo, idx, nocase=1, stopindex="end")
        if not idx:
            break
        fim = f"{idx}+{len(termo)}c"
        text_widget.tag_add("busca_ocorrencia", idx, fim)
        idx = fim

# ❌ Destacar linhas com erro (tag faltando ou inválida)
def destacar_linhas_erro(text_widget, linhas_com_erro, cor="#ff2b2b"):
    text_widget.tag_remove("erro_linha", "1.0", "end")
    text_widget.tag_configure("erro_linha", background=cor)

    for linha in linhas_com_erro:
        inicio = f"{linha}.0"
        fim = f"{linha}.end"
        text_widget.tag_add("erro_linha", inicio, fim)

# ✅ Destacar linhas modificadas (desde o último carregamento)
def destacar_linhas_editadas(text_widget, linhas_editadas, cor="#2b5bff"):
    text_widget.tag_remove("linha_editada", "1.0", "end")
    text_widget.tag_configure("linha_editada", background=cor)

    for linha in linhas_editadas:
        inicio = f"{linha}.0"
        fim = f"{linha}.end"
        text_widget.tag_add("linha_editada", inicio, fim)