# app/infrastructure/auth/sqlite_api_key_repository.py
 
import sqlite3
from app.application.config import settings
from app.application.errors.semantic_error import ApplicationError

class SqliteApiKeyRepository:

    def create(self, owner: str, key_hash: str):
        try:
            with sqlite3.connect(settings.DB_PATH) as conn:
                conn.execute(
                    "INSERT INTO api_keys (key_hash, owner) VALUES (?, ?)",
                    (key_hash, owner),
                )
        except:
            raise ApplicationError("ERR_CREATING_API_KEY")  

    def list_by_owner(self, owner: str):
        try:
            with sqlite3.connect(settings.DB_PATH) as conn:
                conn.row_factory = sqlite3.Row
                rows = conn.execute(
                    "SELECT id, owner, active, created_at FROM api_keys WHERE owner = ?",
                    (owner,),
                ).fetchall()
            
            if not rows:
                raise ApplicationError("NO_API_KEYS")
            
            return [
                {
                    "id": r["id"],
                    "owner": r["owner"],
                    "status": "Ativa" if r["active"] == 1 else "Inativa",
                    "create": r["created_at"],
                }
                for r in rows
            ]
        
        except ApplicationError:
            raise

    def set_active(self, key_id: int, active: bool) -> bool:
        try:
            with sqlite3.connect(settings.DB_PATH) as conn:
                cursor = conn.execute(
                    "UPDATE api_keys SET active = ? WHERE id = ?",
                    (1 if active else 0, key_id),
                )
        except:
            raise ApplicationError("ERR_UPDATING_API_KEY")
        
        return cursor.rowcount > 0
