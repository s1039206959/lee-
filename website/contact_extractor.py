import re
from typing import Dict, List, Optional
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup

EMAIL_RE = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE)
PHONE_RE = re.compile(r"(?:\+?\d[\d\s().-]{7,}\d)")


class PublicContactExtractor:
    def __init__(self, timeout: int = 10) -> None:
        self.timeout = timeout
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        }

    def extract(self, company_website: str) -> Dict[str, str]:
        url = self._normalize_url(company_website)
        if not url:
            return {"public_email": "", "phone_number": "", "contact_page_url": ""}

        page_texts: List[str] = []
        contact_page_url = ""

        home_html = self._fetch_html(url)
        if home_html:
            page_texts.append(self._get_visible_text(home_html))
            contact_page_url = self._find_contact_page(url, home_html) or ""

        if contact_page_url:
            contact_html = self._fetch_html(contact_page_url)
            if contact_html:
                page_texts.append(self._get_visible_text(contact_html))

        combined = "\n".join(page_texts)
        public_email = self._first_email(combined)
        phone_number = self._first_phone(combined)

        return {
            "public_email": public_email,
            "phone_number": phone_number,
            "contact_page_url": contact_page_url,
        }

    def _normalize_url(self, raw_url: str) -> str:
        value = (raw_url or "").strip()
        if not value:
            return ""
        if not value.startswith(("http://", "https://")):
            value = f"https://{value}"
        parsed = urlparse(value)
        if not parsed.netloc:
            return ""
        return value

    def _fetch_html(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=self.timeout, headers=self.headers)
            if response.status_code >= 400:
                return ""
            return response.text
        except requests.RequestException:
            return ""

    def _find_contact_page(self, base_url: str, html: str) -> Optional[str]:
        soup = BeautifulSoup(html, "html.parser")
        keywords = ["contact", "联系我们", "about", "support"]

        for link in soup.find_all("a", href=True):
            href = (link.get("href") or "").strip()
            anchor_text = link.get_text(" ", strip=True).lower()
            target = href.lower()
            if any(k in anchor_text or k in target for k in keywords):
                joined = urljoin(base_url, href)
                if self._same_domain(base_url, joined):
                    return joined
        return None

    def _same_domain(self, url1: str, url2: str) -> bool:
        return urlparse(url1).netloc == urlparse(url2).netloc

    def _get_visible_text(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "noscript"]):
            tag.extract()
        return soup.get_text(" ", strip=True)

    def _first_email(self, text: str) -> str:
        for email in EMAIL_RE.findall(text):
            if "@example." in email.lower():
                continue
            return email
        return ""

    def _first_phone(self, text: str) -> str:
        for phone in PHONE_RE.findall(text):
            digits = re.sub(r"\D", "", phone)
            if len(digits) >= 8:
                return phone.strip()
        return ""
