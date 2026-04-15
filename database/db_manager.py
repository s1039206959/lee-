import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional


class DatabaseManager:
    def __init__(self, db_path: str = "database/leads.db") -> None:
        self.db_path = Path(db_path)
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS leads (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    title TEXT,
                    company_name TEXT,
                    linkedin_url TEXT NOT NULL,
                    country TEXT,
                    notes TEXT,
                    company_website TEXT,
                    public_email TEXT,
                    phone_number TEXT,
                    contact_page_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            conn.commit()

    def add_lead(self, lead: Dict[str, Any]) -> int:
        with self._connect() as conn:
            cursor = conn.execute(
                """
                INSERT INTO leads (
                    name, title, company_name, linkedin_url,
                    country, notes, company_website,
                    public_email, phone_number, contact_page_url
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    lead.get("name", ""),
                    lead.get("title", ""),
                    lead.get("company_name", ""),
                    lead.get("linkedin_url", ""),
                    lead.get("country", ""),
                    lead.get("notes", ""),
                    lead.get("company_website", ""),
                    lead.get("public_email", ""),
                    lead.get("phone_number", ""),
                    lead.get("contact_page_url", ""),
                ),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def update_lead(self, lead_id: int, lead: Dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE leads
                SET name = ?,
                    title = ?,
                    company_name = ?,
                    linkedin_url = ?,
                    country = ?,
                    notes = ?,
                    company_website = ?,
                    public_email = ?,
                    phone_number = ?,
                    contact_page_url = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    lead.get("name", ""),
                    lead.get("title", ""),
                    lead.get("company_name", ""),
                    lead.get("linkedin_url", ""),
                    lead.get("country", ""),
                    lead.get("notes", ""),
                    lead.get("company_website", ""),
                    lead.get("public_email", ""),
                    lead.get("phone_number", ""),
                    lead.get("contact_page_url", ""),
                    lead_id,
                ),
            )
            conn.commit()

    def delete_lead(self, lead_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
            conn.commit()

    def get_leads(self, keyword: str = "", country: str = "") -> List[Dict[str, Any]]:
        query = "SELECT * FROM leads WHERE 1=1"
        params: List[Any] = []

        if keyword.strip():
            value = f"%{keyword.strip()}%"
            query += (
                " AND (name LIKE ? OR title LIKE ? OR company_name LIKE ? OR notes LIKE ? "
                "OR linkedin_url LIKE ? OR company_website LIKE ?)"
            )
            params.extend([value] * 6)

        if country.strip():
            query += " AND country = ?"
            params.append(country.strip())

        query += " ORDER BY updated_at DESC, id DESC"

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]

    def get_distinct_countries(self) -> List[str]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT DISTINCT country FROM leads WHERE country IS NOT NULL AND country != '' ORDER BY country"
            ).fetchall()
            return [row[0] for row in rows if row[0]]

    def get_lead_by_id(self, lead_id: int) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
            return dict(row) if row else None
