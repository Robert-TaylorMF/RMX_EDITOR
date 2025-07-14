import pyodbc

def obter_conexao(base_config):
    drivers = [
        "ODBC Driver 17 for SQL Server",
        "SQL Server Native Client 11.0"
    ]
    for driver in drivers:
        try:
            conn = pyodbc.connect(
                f"DRIVER={{{driver}}};"
                f"SERVER={base_config['server']};"
                f"DATABASE={base_config['database']};"
                f"UID={base_config['user']};"
                f"PWD={base_config['password']}"
            )
            print(f"Conectado com {driver}")
            return conn
        except Exception as e:
            print(f"Erro com driver {driver}: {e}")
    return None

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