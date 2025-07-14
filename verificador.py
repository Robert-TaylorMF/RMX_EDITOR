import pyodbc
import urllib.request
from tkinter import messagebox
import tkinter as tk
import webbrowser

# === Verifica se possui o driver odbc necessário e se não existe redireciona para pagina de download ===

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
    root.withdraw()
    resposta = messagebox.askyesno(
        "Driver ODBC ausente",
        f"O driver '{driver_faltante}' não está instalado nesta máquina.\n\nDeseja abrir o site oficial para baixar?"
    )
    if resposta:
        abrir_link()

def driver_disponivel(nome_driver):
    return nome_driver in pyodbc.drivers()
    
# Verifica se tem atualizações disponíveis para o sistema   
def verificar_atualizacao(versao_local):
    try:
        url = "https://raw.githubusercontent.com/Robert-TaylorMF/RMX_EDITOR/main/versao.txt"
        resposta = urllib.request.urlopen(url, timeout=3)
        versao_online = resposta.read().decode().strip()
        if versao_online > versao_local:
            messagebox.showinfo("Atualização disponível",
                f"Nova versão: {versao_online}\n\nAcesse:\nhttps://github.com/Robert-TaylorMF/RMX_EDITOR/releases")
        else:
            messagebox.showinfo("XMLEditor RM", "Você está usando a versão mais recente.")
    except:
        pass  # silencioso em caso de erro offline