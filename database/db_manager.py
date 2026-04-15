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
                    linkedin_url TEXT NOT NULL,
                    name TEXT NOT NULL,
                    title TEXT,
                    company TEXT,
                    country TEXT,
                    industry TEXT,
                    notes TEXT,
                    follow_up_status TEXT,
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
                    linkedin_url, name, title, company, country,
                    industry, notes, follow_up_status
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    lead.get("linkedin_url", ""),
                    lead.get("name", ""),
                    lead.get("title", ""),
                    lead.get("company", ""),
                    lead.get("country", ""),
                    lead.get("industry", ""),
                    lead.get("notes", ""),
                    lead.get("follow_up_status", ""),
                ),
            )
            conn.commit()
            return int(cursor.lastrowid)

    def update_lead(self, lead_id: int, lead: Dict[str, Any]) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE leads
                SET linkedin_url = ?,
                    name = ?,
                    title = ?,
                    company = ?,
                    country = ?,
                    industry = ?,
                    notes = ?,
                    follow_up_status = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
                """,
                (
                    lead.get("linkedin_url", ""),
                    lead.get("name", ""),
                    lead.get("title", ""),
                    lead.get("company", ""),
                    lead.get("country", ""),
                    lead.get("industry", ""),
                    lead.get("notes", ""),
                    lead.get("follow_up_status", ""),
                    lead_id,
                ),
            )
            conn.commit()

    def delete_lead(self, lead_id: int) -> None:
        with self._connect() as conn:
            conn.execute("DELETE FROM leads WHERE id = ?", (lead_id,))
            conn.commit()

    def get_leads(
        self,
        keyword: str = "",
        country: str = "",
        industry: str = "",
        follow_up_status: str = "",
    ) -> List[Dict[str, Any]]:
        query = "SELECT * FROM leads WHERE 1=1"
        params: List[Any] = []

        if keyword.strip():
            like_keyword = f"%{keyword.strip()}%"
            query += (
                " AND (name LIKE ? OR title LIKE ? OR company LIKE ? "
                "OR notes LIKE ? OR linkedin_url LIKE ?)"
            )
            params.extend([like_keyword] * 5)

        if country.strip():
            query += " AND country = ?"
            params.append(country.strip())

        if industry.strip():
            query += " AND industry = ?"
            params.append(industry.strip())

        if follow_up_status.strip():
            query += " AND follow_up_status = ?"
            params.append(follow_up_status.strip())

        query += " ORDER BY updated_at DESC, id DESC"

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
            return [dict(row) for row in rows]

    def get_lead_by_id(self, lead_id: int) -> Optional[Dict[str, Any]]:
        with self._connect() as conn:
            row = conn.execute("SELECT * FROM leads WHERE id = ?", (lead_id,)).fetchone()
            return dict(row) if row else None

    def get_distinct_values(self, field_name: str) -> List[str]:
        allowed_fields = {"country", "industry", "follow_up_status"}
        if field_name not in allowed_fields:
            return []

        with self._connect() as conn:
            rows = conn.execute(
                f"SELECT DISTINCT {field_name} FROM leads WHERE {field_name} IS NOT NULL AND {field_name} != '' ORDER BY {field_name}"
            ).fetchall()
            return [row[0] for row in rows if row[0]]
