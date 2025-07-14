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