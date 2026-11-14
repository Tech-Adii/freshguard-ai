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
        # Ensure new columns exist if table was already created
        try:
            conn.execute("ALTER TABLE users ADD COLUMN picture TEXT")
        except Exception:
            pass
        try:
            conn.execute("ALTER TABLE users ADD COLUMN provider TEXT")
        except Exception:
            pass

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
                created_at REAL
            )
        """)
        conn.commit()

init_db()

def get_or_create_google_user(email: str, name: str, picture: str = "") -> Dict[str, Any]:
    with get_db() as conn:
        row = conn.execute("SELECT id, email, name, picture, provider FROM users WHERE email = ?", (email,)).fetchone()
        if row:
            # Update picture or name if changed
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
    item_id = f"hist_{uuid.uuid4().hex[:10]}"
    with get_db() as conn:
        conn.execute("""
            INSERT INTO history (id, user_id, input_text, summary, overall_freshness_score, stale_count, fresh_count, report_json, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
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

def get_user_history(user_id: str, limit: int = 25) -> List[Dict[str, Any]]:
    with get_db() as conn:
        rows = conn.execute("""
            SELECT id, user_id, input_text, summary, overall_freshness_score, stale_count, fresh_count, created_at
            FROM history
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
        """, (user_id, limit)).fetchall()
        return [dict(r) for r in rows]

def get_history_detail(history_id: str) -> Optional[Dict[str, Any]]:
    with get_db() as conn:
        row = conn.execute("SELECT report_json FROM history WHERE id = ?", (history_id,)).fetchone()
        if row:
            return json.loads(row["report_json"])
        return None

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
