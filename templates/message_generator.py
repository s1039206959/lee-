from pathlib import Path


def generate_outreach_message(name: str, title: str, company: str) -> str:
    template_path = Path(__file__).resolve().parent / "outreach_template.txt"
    template = template_path.read_text(encoding="utf-8")

    safe_name = name.strip() or "there"
    safe_title = title.strip() or "your role"
    safe_company = company.strip() or "your company"

    return template.format(name=safe_name, title=safe_title, company=safe_company)
