import tkinter as tk
from tkinter import filedialog, messagebox
from typing import Dict, Optional
from urllib.parse import quote_plus
import webbrowser

import customtkinter as ctk

from database.db_manager import DatabaseManager
from export.exporter import Exporter
from website.contact_extractor import PublicContactExtractor


class LeadAssistantApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("LinkedIn 关键词找客助手")
        self.geometry("1320x780")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.db = DatabaseManager()
        self.contact_extractor = PublicContactExtractor()
        self.selected_lead_id: Optional[int] = None
        self.current_rows = []

        self._build_ui()
        self.refresh_filters()
        self.load_leads()

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        top = ctk.CTkFrame(self)
        top.grid(row=0, column=0, columnspan=2, sticky="ew", padx=12, pady=12)
        self._build_top(top)

        table_frame = ctk.CTkFrame(self)
        table_frame.grid(row=1, column=0, sticky="nsew", padx=(12, 6), pady=(0, 12))
        self._build_table(table_frame)

        form_frame = ctk.CTkFrame(self)
        form_frame.grid(row=1, column=1, sticky="nsew", padx=(6, 12), pady=(0, 12))
        self._build_form(form_frame)

    def _build_top(self, parent: ctk.CTkFrame) -> None:
        parent.grid_columnconfigure(11, weight=1)

        self.keyword_vars = [tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.search_var = tk.StringVar()
        self.country_filter_var = tk.StringVar(value="All")

        ctk.CTkLabel(parent, text="LinkedIn关键词1").grid(row=0, column=0, padx=6, pady=6)
        ctk.CTkEntry(parent, textvariable=self.keyword_vars[0], width=140).grid(row=0, column=1, padx=6, pady=6)
        ctk.CTkLabel(parent, text="关键词2").grid(row=0, column=2, padx=6, pady=6)
        ctk.CTkEntry(parent, textvariable=self.keyword_vars[1], width=140).grid(row=0, column=3, padx=6, pady=6)
        ctk.CTkLabel(parent, text="关键词3").grid(row=0, column=4, padx=6, pady=6)
        ctk.CTkEntry(parent, textvariable=self.keyword_vars[2], width=140).grid(row=0, column=5, padx=6, pady=6)

        ctk.CTkButton(parent, text="打开LinkedIn搜索", command=self.open_linkedin_search).grid(row=0, column=6, padx=8, pady=6)

        ctk.CTkLabel(parent, text="本地搜索").grid(row=1, column=0, padx=6, pady=6)
        ctk.CTkEntry(parent, textvariable=self.search_var, width=260).grid(row=1, column=1, columnspan=3, padx=6, pady=6, sticky="ew")
        ctk.CTkLabel(parent, text="国家筛选").grid(row=1, column=4, padx=6, pady=6)
        self.country_filter_menu = ctk.CTkOptionMenu(parent, variable=self.country_filter_var, values=["All"])
        self.country_filter_menu.grid(row=1, column=5, padx=6, pady=6)

        ctk.CTkButton(parent, text="搜索/筛选", command=self.load_leads).grid(row=1, column=6, padx=6, pady=6)
        ctk.CTkButton(parent, text="重置", command=self.reset_filters).grid(row=1, column=7, padx=6, pady=6)
        ctk.CTkButton(parent, text="导出CSV", command=self.export_csv).grid(row=1, column=8, padx=6, pady=6)
        ctk.CTkButton(parent, text="导出Excel", command=self.export_xlsx).grid(row=1, column=9, padx=6, pady=6)

    def _build_table(self, parent: ctk.CTkFrame) -> None:
        parent.grid_rowconfigure(0, weight=1)
        parent.grid_columnconfigure(0, weight=1)

        self.lead_listbox = tk.Listbox(parent, font=("Segoe UI", 10))
        self.lead_listbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.lead_listbox.bind("<<ListboxSelect>>", self.on_select_lead)

        scrollbar = tk.Scrollbar(parent, orient="vertical", command=self.lead_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10)
        self.lead_listbox.config(yscrollcommand=scrollbar.set)

    def _build_form(self, parent: ctk.CTkFrame) -> None:
        parent.grid_columnconfigure(1, weight=1)

        fields = [
            ("name", "name"),
            ("title", "title"),
            ("company_name", "company_name"),
            ("linkedin_url", "linkedin_url"),
            ("country", "country"),
            ("company_website", "company_website"),
            ("public_email", "public_email"),
            ("phone_number", "phone_number"),
            ("contact_page_url", "contact_page_url"),
        ]

        self.entries: Dict[str, ctk.CTkEntry] = {}
        for idx, (label_text, key) in enumerate(fields):
            ctk.CTkLabel(parent, text=label_text).grid(row=idx, column=0, padx=10, pady=6, sticky="w")
            entry = ctk.CTkEntry(parent)
            entry.grid(row=idx, column=1, padx=10, pady=6, sticky="ew")
            self.entries[key] = entry

        notes_row = len(fields)
        ctk.CTkLabel(parent, text="notes").grid(row=notes_row, column=0, padx=10, pady=6, sticky="nw")
        self.notes_text = ctk.CTkTextbox(parent, height=100)
        self.notes_text.grid(row=notes_row, column=1, padx=10, pady=6, sticky="ew")

        actions = ctk.CTkFrame(parent, fg_color="transparent")
        actions.grid(row=notes_row + 1, column=0, columnspan=2, padx=10, pady=8, sticky="ew")

        ctk.CTkButton(actions, text="新增", command=self.add_lead).pack(side="left", padx=4)
        ctk.CTkButton(actions, text="更新", command=self.update_lead).pack(side="left", padx=4)
        ctk.CTkButton(actions, text="删除", command=self.delete_lead).pack(side="left", padx=4)
        ctk.CTkButton(actions, text="清空", command=self.clear_form).pack(side="left", padx=4)

        ctk.CTkButton(
            parent,
            text="从公司官网提取公开联系方式",
            command=self.fetch_public_contacts,
        ).grid(row=notes_row + 2, column=0, columnspan=2, padx=10, pady=(4, 10), sticky="ew")

        ctk.CTkLabel(
            parent,
            text="说明：仅访问 company_website 公共页面，不抓取 LinkedIn 私人联系方式。",
            text_color="gray60",
            wraplength=420,
            justify="left",
        ).grid(row=notes_row + 3, column=0, columnspan=2, padx=10, pady=(0, 10), sticky="w")

    def build_linkedin_search_url(self, keywords: list[str]) -> str:
        joined_query = " ".join(keywords)
        return f"https://www.linkedin.com/search/results/people/?keywords={quote_plus(joined_query)}"

    def open_linkedin_search(self) -> None:
        keywords = [v.get().strip() for v in self.keyword_vars if v.get().strip()]
        if not keywords:
            messagebox.showwarning("提示", "请至少输入 1 个关键词。")
            return
        if len(keywords) > 3:
            messagebox.showwarning("提示", "最多支持 3 个关键词。")
            return

        search_url = self.build_linkedin_search_url(keywords)
        webbrowser.open(search_url)
        messagebox.showinfo("已打开", "已在默认浏览器打开 LinkedIn 搜索页面。")

    def _collect_form_data(self) -> Dict[str, str]:
        return {
            "name": self.entries["name"].get().strip(),
            "title": self.entries["title"].get().strip(),
            "company_name": self.entries["company_name"].get().strip(),
            "linkedin_url": self.entries["linkedin_url"].get().strip(),
            "country": self.entries["country"].get().strip(),
            "notes": self.notes_text.get("1.0", "end").strip(),
            "company_website": self.entries["company_website"].get().strip(),
            "public_email": self.entries["public_email"].get().strip(),
            "phone_number": self.entries["phone_number"].get().strip(),
            "contact_page_url": self.entries["contact_page_url"].get().strip(),
        }

    def _validate_required(self, lead: Dict[str, str]) -> bool:
        if not lead["name"]:
            messagebox.showerror("缺少字段", "name 不能为空。")
            return False
        if not lead["linkedin_url"]:
            messagebox.showerror("缺少字段", "linkedin_url 不能为空。")
            return False
        return True

    def add_lead(self) -> None:
        lead = self._collect_form_data()
        if not self._validate_required(lead):
            return
        self.db.add_lead(lead)
        self.clear_form()
        self.refresh_filters()
        self.load_leads()

    def update_lead(self) -> None:
        if not self.selected_lead_id:
            messagebox.showwarning("提示", "请先选择一条记录。")
            return
        lead = self._collect_form_data()
        if not self._validate_required(lead):
            return
        self.db.update_lead(self.selected_lead_id, lead)
        self.refresh_filters()
        self.load_leads()

    def delete_lead(self) -> None:
        if not self.selected_lead_id:
            messagebox.showwarning("提示", "请先选择一条记录。")
            return
        if not messagebox.askyesno("确认", "确定删除这条记录吗？"):
            return
        self.db.delete_lead(self.selected_lead_id)
        self.clear_form()
        self.refresh_filters()
        self.load_leads()

    def fetch_public_contacts(self) -> None:
        company_website = self.entries["company_website"].get().strip()
        if not company_website:
            messagebox.showwarning("提示", "请先填写 company_website。")
            return

        data = self.contact_extractor.extract(company_website)
        self.entries["public_email"].delete(0, "end")
        self.entries["public_email"].insert(0, data.get("public_email", ""))
        self.entries["phone_number"].delete(0, "end")
        self.entries["phone_number"].insert(0, data.get("phone_number", ""))
        self.entries["contact_page_url"].delete(0, "end")
        self.entries["contact_page_url"].insert(0, data.get("contact_page_url", ""))
        messagebox.showinfo("完成", "已尝试从公司官网公共页面提取公开联系方式。")

    def clear_form(self) -> None:
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.notes_text.delete("1.0", "end")
        self.selected_lead_id = None

    def on_select_lead(self, _event: tk.Event) -> None:
        selected = self.lead_listbox.curselection()
        if not selected:
            return
        idx = selected[0]
        if idx >= len(self.current_rows):
            return

        lead = self.current_rows[idx]
        self.selected_lead_id = int(lead["id"])
        for key, entry in self.entries.items():
            entry.delete(0, "end")
            entry.insert(0, lead.get(key, ""))
        self.notes_text.delete("1.0", "end")
        self.notes_text.insert("1.0", lead.get("notes", ""))

    def load_leads(self) -> None:
        keyword = self.search_var.get().strip()
        country = "" if self.country_filter_var.get() in ("", "All") else self.country_filter_var.get().strip()
        rows = self.db.get_leads(keyword=keyword, country=country)
        self.current_rows = rows

        self.lead_listbox.delete(0, "end")
        for row in rows:
            display = f"[{row['id']}] {row.get('name', '')} | {row.get('title', '')} | {row.get('company_name', '')} | {row.get('country', '')}"
            self.lead_listbox.insert("end", display)

    def refresh_filters(self) -> None:
        countries = ["All"] + self.db.get_distinct_countries()
        self.country_filter_menu.configure(values=countries)
        if self.country_filter_var.get() not in countries:
            self.country_filter_var.set("All")

    def reset_filters(self) -> None:
        self.search_var.set("")
        self.country_filter_var.set("All")
        self.load_leads()

    def export_csv(self) -> None:
        if not self.current_rows:
            messagebox.showwarning("提示", "没有可导出的记录。")
            return
        path = filedialog.asksaveasfilename(
            title="导出 CSV",
            defaultextension=".csv",
            filetypes=[("CSV", "*.csv")],
            initialfile="linkedin_keyword_leads.csv",
        )
        if not path:
            return
        Exporter.export_to_csv(path, self.current_rows)
        messagebox.showinfo("成功", f"CSV 已导出到:\n{path}")

    def export_xlsx(self) -> None:
        if not self.current_rows:
            messagebox.showwarning("提示", "没有可导出的记录。")
            return
        path = filedialog.asksaveasfilename(
            title="导出 Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel", "*.xlsx")],
            initialfile="linkedin_keyword_leads.xlsx",
        )
        if not path:
            return
        Exporter.export_to_xlsx(path, self.current_rows)
        messagebox.showinfo("成功", f"Excel 已导出到:\n{path}")
