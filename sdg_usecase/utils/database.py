import sqlite3
import json
import os
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent.parent / "data" / "hub.db"

def get_conn():
    DB_PATH.parent.mkdir(exist_ok=True)
    conn = sqlite3.connect(str(DB_PATH), check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS usecases (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            category    TEXT,
            client      TEXT,
            client_anon INTEGER DEFAULT 0,
            team_name   TEXT,
            team_members TEXT,
            start_date  TEXT,
            end_date    TEXT,
            description TEXT,
            solution    TEXT,
            tech_stack  TEXT,
            outcome     TEXT,
            links       TEXT,
            tags        TEXT,
            status      TEXT DEFAULT 'Completed',
            source      TEXT DEFAULT 'manual',
            created_at  TEXT,
            updated_at  TEXT
        )
    """)
    conn.commit()
    conn.close()
    
def get_all_usecases():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM usecases ORDER BY created_at DESC").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_usecase(uid):
    conn = get_conn()
    row = conn.execute("SELECT * FROM usecases WHERE id=?", (uid,)).fetchone()
    conn.close()
    return dict(row) if row else None

def save_usecase(data: dict) -> int:
    conn = get_conn()
    c = conn.cursor()
    now = datetime.now().isoformat()
    if data.get("id"):
        c.execute("""
            UPDATE usecases SET title=?,category=?,client=?,client_anon=?,team_name=?,team_members=?,
            start_date=?,end_date=?,description=?,solution=?,tech_stack=?,outcome=?,links=?,tags=?,status=?,updated_at=?
            WHERE id=?
        """, (
            data["title"], data["category"], data["client"], data.get("client_anon",0),
            data["team_name"], data["team_members"], data["start_date"], data["end_date"],
            data["description"], data["solution"], data["tech_stack"], data["outcome"],
            json.dumps(data.get("links",[])), json.dumps(data.get("tags",[])),
            data["status"], now, data["id"]
        ))
        uid = data["id"]
    else:
        c.execute("""
            INSERT INTO usecases (title,category,client,client_anon,team_name,team_members,
            start_date,end_date,description,solution,tech_stack,outcome,links,tags,status,source,created_at,updated_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            data["title"], data["category"], data["client"], data.get("client_anon",0),
            data["team_name"], data["team_members"], data["start_date"], data["end_date"],
            data["description"], data["solution"], data["tech_stack"], data["outcome"],
            json.dumps(data.get("links",[])), json.dumps(data.get("tags",[])),
            data["status"], "manual", now, now
        ))
        uid = c.lastrowid
    conn.commit()
    conn.close()
    return uid

def delete_usecase(uid):
    conn = get_conn()
    conn.execute("DELETE FROM usecases WHERE id=?", (uid,))
    conn.commit()
    conn.close()

def search_usecases(query: str, category: str = None, status: str = None, team: str = None):
    all_uc = get_all_usecases()
    results = []
    q = query.lower().strip()
    for uc in all_uc:
        if category and uc.get("category") != category:
            continue
        if status and uc.get("status") != status:
            continue
        if team and team.lower() not in (uc.get("team_name") or "").lower():
            continue
        if q:
            # Parse tags JSON so "gdrive-import" and other tags are searchable
            tags_str = ""
            try:
                tags_list = json.loads(uc.get("tags") or "[]")
                tags_str = " ".join(tags_list)
            except Exception:
                tags_str = uc.get("tags", "")

            # Parse links JSON into plain text
            links_str = ""
            try:
                links_list = json.loads(uc.get("links") or "[]")
                links_str = " ".join(links_list)
            except Exception:
                links_str = uc.get("links", "")

            haystack = " ".join([
                uc.get("title", ""), uc.get("description", ""), uc.get("solution", ""),
                uc.get("category", ""), uc.get("tech_stack", ""), tags_str,
                uc.get("team_name", ""), uc.get("outcome", ""), uc.get("source", ""),
                uc.get("client", ""), links_str,
            ]).lower()
            if q in haystack:
                results.append(uc)
        else:
            results.append(uc)
    return results

def get_categories():
    conn = get_conn()
    rows = conn.execute("SELECT DISTINCT category FROM usecases WHERE category IS NOT NULL ORDER BY category").fetchall()
    conn.close()
    return [r[0] for r in rows]

def get_teams():
    conn = get_conn()
    rows = conn.execute("SELECT DISTINCT team_name FROM usecases WHERE team_name IS NOT NULL ORDER BY team_name").fetchall()
    conn.close()
    return [r[0] for r in rows]
