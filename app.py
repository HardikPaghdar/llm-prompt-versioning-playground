"""SQLite-backed prompt version registry and deterministic fixture comparison."""
import hashlib, sqlite3

class PromptRegistry:
    def __init__(self, db_path: str = "prompts.db"):
        self.db_path = db_path
        with self._connect() as db:
            db.execute("""CREATE TABLE IF NOT EXISTS prompts (
                name TEXT NOT NULL, version INTEGER NOT NULL, body TEXT NOT NULL,
                sha256 TEXT NOT NULL, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(name, version))""")
    def _connect(self): return sqlite3.connect(self.db_path)
    def save(self, name: str, body: str) -> dict:
        name, body = name.strip(), body.strip()
        if not name or not body: raise ValueError("prompt name and body are required")
        digest = hashlib.sha256(body.encode()).hexdigest()
        with self._connect() as db:
            version = db.execute("SELECT COALESCE(MAX(version),0)+1 FROM prompts WHERE name=?", (name,)).fetchone()[0]
            db.execute("INSERT INTO prompts(name,version,body,sha256) VALUES(?,?,?,?)", (name,version,body,digest))
        return {"name":name,"version":version,"sha256":digest}
    def get(self, name: str, version: int | None = None) -> dict | None:
        with self._connect() as db:
            row = db.execute("SELECT name,version,body,sha256,created_at FROM prompts WHERE name=? AND version IS ? ORDER BY version DESC LIMIT 1", (name, version)).fetchone() if version is None else db.execute("SELECT name,version,body,sha256,created_at FROM prompts WHERE name=? AND version=?", (name, version)).fetchone()
        return dict(zip(("name","version","body","sha256","created_at"),row)) if row else None
    def history(self, name: str) -> list[dict]:
        with self._connect() as db: rows = db.execute("SELECT name,version,body,sha256,created_at FROM prompts WHERE name=? ORDER BY version", (name,)).fetchall()
        return [dict(zip(("name","version","body","sha256","created_at"),row)) for row in rows]

def compare_fixtures(before: list[dict], after: list[dict]) -> dict:
    old, new = {row["id"]:row for row in before}, {row["id"]:row for row in after}
    changed = [{"id":key,"before":old.get(key),"after":new.get(key)} for key in sorted(old.keys() | new.keys()) if old.get(key) != new.get(key)]
    regressions = sum(1 for item in changed if item["id"] in old and item["id"] in new and old[item["id"]].get("expected") != new[item["id"]].get("expected"))
    return {"before_count":len(old),"after_count":len(new),"changed_cases":changed,"regression_count":regressions}
