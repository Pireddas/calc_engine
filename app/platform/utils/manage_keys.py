# app\platform\utils\manage_keys.py
# python -m app.platform.utils.manage_keys

import sqlite3, secrets, hashlib, os
from app.application.config import settings

DB_DIR = settings.DB_DIR
DB_PATH = settings.DB_PATH

def init_db():
    # 2. Garante a criação da pasta 'database' dentro de 'src'
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
        print(f"📁 Pasta de governança criada em: {DB_DIR}")

    if settings.DB_TYPE == "sqlite":
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                key_hash TEXT UNIQUE NOT NULL,
                owner TEXT NOT NULL,
                active INTEGER DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    elif settings.DB_TYPE == "postgresql":
        # Implementar criação de tabela para PostgreSQL se necessário
        pass

def create_key():
    owner = input("\n👤 Nome do Proprietário (Owner): ").strip()
    if not owner: return print("❌ Erro: Nome é obrigatório.")
    
    raw_key = f"vibe_{secrets.token_hex(16)}"
    key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
    
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("INSERT INTO api_keys (key_hash, owner) VALUES (?, ?)", (key_hash, owner))
    
    print(f"\n✅ Chave criada para: {owner}")
    print(f"🔑 API KEY: {raw_key}")
    print("⚠️  AVISO: Guarde esta chave! Ela não pode ser recuperada.\n")

def list_keys():
    print("\n--- CHAVES CADASTRADAS ---")
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.execute("SELECT id, owner, active, created_at FROM api_keys")
        rows = cursor.fetchall()
        
        if not rows:
            print("Nenhuma chave encontrada.")
            return

        print(f"{'ID':<4} | {'OWNER':<30} | {'STATUS':<11} | {'DATA CRIAÇÃO'}")
        print("-" * 75)
        for row in rows:
            status = "✅ ATIVA" if row['active'] == 1 else "❌ INATIVA"
            print(f"{row['id']:<4} | {row['owner']:<30} | {status:<10} | {row['created_at']}")
    print("-" * 75)

def toggle_key_status(status: int):
    action = "Ativar" if status == 1 else "Cancelar/Inativar"
    key_id = input(f"\nDigite o ID da chave que deseja {action}: ").strip()
    
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.execute("UPDATE api_keys SET active = ? WHERE id = ?", (status, key_id))
        if cursor.rowcount > 0:
            print(f"✅ Sucesso: Chave {key_id} atualizada.")
        else:
            print(f"❌ Erro: ID {key_id} não encontrado.")

def main_menu():
    init_db() 
    while True:
        print("\n=== 🛡️ GESTAO DE CHAVES API ===")
        print("1. Gerar Nova Chave")
        print("2. Listar Todas as Chaves")
        print("3. Inativar/Cancelar Chave")
        print("4. Reativar Chave")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1": create_key()
        elif opcao == "2": list_keys()
        elif opcao == "3": toggle_key_status(0)
        elif opcao == "4": toggle_key_status(1)
        elif opcao == "0": break
        else: print("Opção inválida.")

if __name__ == "__main__":
    main_menu()
