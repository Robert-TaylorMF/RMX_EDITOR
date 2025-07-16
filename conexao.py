import pyodbc
from seguranca import descriptografar_senha  # 👈 importa para descriptografar

def obter_conexao(base_config):
    drivers = [
        "ODBC Driver 17 for SQL Server",
        "SQL Server Native Client 11.0"
    ]
    
    # Ajuste de campos conforme base_config JSON
    server = base_config.get("host") or base_config.get("server")
    database = base_config.get("database")
    usuario = base_config.get("usuario") or base_config.get("user")
    senha_criptografada = base_config.get("senha") or base_config.get("password")

    try:
        senha_real = descriptografar_senha(senha_criptografada)
    except Exception as e:
        print(f"Erro ao descriptografar senha: {e}")
        return None

    for driver in drivers:
        try:
            conn = pyodbc.connect(
                f"DRIVER={{{driver}}};"
                f"SERVER={server};"
                f"DATABASE={database};"
                f"UID={usuario};"
                f"PWD={senha_real}"
            )
            print(f"Conectado com driver: {driver}")
            return conn
        except Exception as e:
            print(f"Erro com driver {driver}: {e}")
    
    print("⚠️ Nenhuma conexão foi possível.")
    return None