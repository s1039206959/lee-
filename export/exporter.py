import csv
from pathlib import Path
from typing import Dict, List

from openpyxl import Workbook


EXPORT_FIELDS = [
    "id",
    "name",
    "title",
    "company_name",
    "linkedin_url",
    "country",
    "notes",
    "company_website",
    "public_email",
    "phone_number",
    "contact_page_url",
    "created_at",
    "updated_at",
]


class Exporter:
    @staticmethod
    def export_to_csv(file_path: str, data: List[Dict[str, str]]) -> None:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        with path.open("w", newline="", encoding="utf-8-sig") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=EXPORT_FIELDS)
            writer.writeheader()
            for row in data:
                writer.writerow({field: row.get(field, "") for field in EXPORT_FIELDS})

    @staticmethod
    def export_to_xlsx(file_path: str, data: List[Dict[str, str]]) -> None:
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)

        wb = Workbook()
        ws = wb.active
        ws.title = "Leads"

        ws.append(EXPORT_FIELDS)
        for row in data:
            ws.append([row.get(field, "") for field in EXPORT_FIELDS])

        wb.save(path)
