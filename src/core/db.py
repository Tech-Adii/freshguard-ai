import sqlite3
import json
import uuid
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

DB_PATH = Path(__file__).resolve().parent.parent.parent / "freshguard.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                email TEXT UNIQUE,
                name TEXT,
                password_hash TEXT,
                picture TEXT,
                provider TEXT,
                created_at REAL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS history (
                id TEXT PRIMARY KEY,
                user_id TEXT,
                input_text TEXT,
                summary TEXT,
                overall_freshness_score REAL,
                stale_count INTEGER,
                fresh_count INTEGER,
                report_json TEXT,
                is_archived INTEGER DEFAULT 0,
                is_starred INTEGER DEFAULT 0,
                created_at REAL
            )
        """)
        # Ensure new columns exist
        for col in ["picture TEXT", "provider TEXT"]:
            try:
                conn.execute(f"ALTER TABLE users ADD COLUMN {col}")
            except Exception:
                pass
        for col in ["is_archived INTEGER DEFAULT 0", "is_starred INTEGER DEFAULT 0"]:
            try:
                conn.execute(f"ALTER TABLE history ADD COLUMN {col}")
            except Exception:
                pass
        conn.commit()

init_db()

def get_or_create_google_user(email: str, name: str, picture: str = "") -> Dict[str, Any]:
    with get_db() as conn:
        row = conn.execute("SELECT id, email, name, picture, provider FROM users WHERE email = ?", (email,)).fetchone()
        if row:
            conn.execute("UPDATE users SET name = ?, picture = ?, provider = 'google' WHERE email = ?", (name, picture, email))
            conn.commit()
            return {"id": row["id"], "email": email, "name": name, "picture": picture, "provider": "google"}
        
        user_id = f"goog_{uuid.uuid4().hex[:10]}"
        conn.execute("""
            INSERT INTO users (id, email, name, password_hash, picture, provider, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, email, name, "", picture, "google", time.time()))
        conn.commit()
        return {"id": user_id, "email": email, "name": name, "picture": picture, "provider": "google"}

def save_history_item(user_id: str, report_dict: Dict[str, Any]) -> str:
    item_id = f"audit_{uuid.uuid4().hex[:10]}"
    with get_db() as conn:
        conn.execute("""
            INSERT INTO history (id, user_id, input_text, summary, overall_freshness_score, stale_count, fresh_count, report_json, is_archived, is_starred, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, 0, 0, ?)
        """, (
            item_id,
            user_id,
            report_dict.get("input_text", ""),
            report_dict.get("summary", ""),
            float(report_dict.get("overall_freshness_score", 0.0)),
            int(report_dict.get("stale_count", 0)),
            int(report_dict.get("fresh_count", 0)),
            json.dumps(report_dict),
            time.time()
        ))
        conn.commit()
    return item_id

def get_user_history(user_id: str, include_archived: bool = True, limit: int = 50) -> List[Dict[str, Any]]:
    with get_db() as conn:
        query = """
            SELECT id, user_id, input_text, summary, overall_freshness_score, stale_count, fresh_count, is_archived, is_starred, created_at
            FROM history
            WHERE user_id = ?
        """
        if not include_archived:
            query += " AND is_archived = 0"
        query += " ORDER BY created_at DESC LIMIT ?"
        rows = conn.execute(query, (user_id, limit)).fetchall()
        return [dict(r) for r in rows]

def get_history_detail(history_id: str) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        row = conn.execute("SELECT report_json, is_archived, is_starred FROM history WHERE id = ?", (history_id,)).fetchone()
        if row:
            data = json.loads(row["report_json"])
            data["is_archived"] = bool(row["is_archived"])
            data["is_starred"] = bool(row["is_starred"])
            return data
        return None

def toggle_archive_history(history_id: str, user_id: str) -> bool:
    with get_db() as conn:
        row = conn.execute("SELECT is_archived FROM history WHERE id = ? AND user_id = ?", (history_id, user_id)).fetchone()
        if not row:
            return False
        new_state = 0 if row["is_archived"] else 1
        conn.execute("UPDATE history SET is_archived = ? WHERE id = ? AND user_id = ?", (new_state, history_id, user_id))
        conn.commit()
        return bool(new_state)

def toggle_star_history(history_id: str, user_id: str) -> bool:
    with get_db() as conn:
        row = conn.execute("SELECT is_starred FROM history WHERE id = ? AND user_id = ?", (history_id, user_id)).fetchone()
        if not row:
            return False
        new_state = 0 if row["is_starred"] else 1
        conn.execute("UPDATE history SET is_starred = ? WHERE id = ? AND user_id = ?", (new_state, history_id, user_id))
        conn.commit()
        return bool(new_state)

def delete_history_item(history_id: str, user_id: str) -> bool:
    with get_db() as conn:
        cur = conn.execute("DELETE FROM history WHERE id = ? AND user_id = ?", (history_id, user_id))
        conn.commit()
        return cur.rowcount > 0

def clear_user_history(user_id: str) -> bool:
    with get_db() as conn:
        conn.execute("DELETE FROM history WHERE user_id = ?", (user_id,))
        conn.commit()
        return True
