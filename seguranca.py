from cryptography.fernet import Fernet
import os

# Caminho seguro da chave
CAMINHO_CHAVE = "chave.key"

# 🔑 Gera o arquivo chave.key se não existir
def gerar_chave():
    if not os.path.exists(CAMINHO_CHAVE):
        chave = Fernet.generate_key()
        with open(CAMINHO_CHAVE, "wb") as f:
            f.write(chave)
        print("🔐 Chave criada com sucesso!")
    else:
        print("✅ Chave já existente.")

# Recupera a instância Fernet usando a chave armazenada
def obter_fernet():
    if not os.path.exists(CAMINHO_CHAVE):
        gerar_chave()
    with open(CAMINHO_CHAVE, "rb") as f:
        chave = f.read()
    return Fernet(chave)

# Criptografa a senha antes de salvar
def criptografar_senha(senha):
    return obter_fernet().encrypt(senha.encode()).decode()

# Descriptografa a senha para conectar
def descriptografar_senha(senha_criptografada):
    return obter_fernet().decrypt(senha_criptografada.encode()).decode()