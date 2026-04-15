import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
from typing import Dict, Optional

import customtkinter as ctk

from database.db_manager import DatabaseManager
from export.exporter import Exporter
from templates.message_generator import generate_outreach_message


class LeadAssistantApp(ctk.CTk):
    STATUS_OPTIONS = ["", "Not Contacted", "Contacted", "Replied", "In Discussion", "Closed"]

    def __init__(self) -> None:
        super().__init__()
        self.title("LinkedIn 客户线索整理助手")
        self.geometry("1280x760")
        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("blue")

        self.db = DatabaseManager()
        self.selected_lead_id: Optional[int] = None

        self._build_ui()
        self.refresh_filters()
        self.load_leads()

    def _build_ui(self) -> None:
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=2)
        self.grid_rowconfigure(1, weight=1)

        self.top_bar = ctk.CTkFrame(self)
        self.top_bar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=12, pady=12)
        self._build_top_bar()

        self.table_frame = ctk.CTkFrame(self)
        self.table_frame.grid(row=1, column=0, sticky="nsew", padx=(12, 6), pady=(0, 12))
        self._build_table()

        self.form_frame = ctk.CTkFrame(self)
        self.form_frame.grid(row=1, column=1, sticky="nsew", padx=(6, 12), pady=(0, 12))
        self._build_form()

    def _build_top_bar(self) -> None:
        self.top_bar.grid_columnconfigure(7, weight=1)

        self.search_var = tk.StringVar()
        self.country_filter_var = tk.StringVar()
        self.industry_filter_var = tk.StringVar()
        self.status_filter_var = tk.StringVar()

        ctk.CTkLabel(self.top_bar, text="搜索").grid(row=0, column=0, padx=6, pady=6)
        ctk.CTkEntry(self.top_bar, textvariable=self.search_var, width=180).grid(row=0, column=1, padx=6, pady=6)

        ctk.CTkLabel(self.top_bar, text="国家").grid(row=0, column=2, padx=6, pady=6)
        self.country_filter_menu = ctk.CTkOptionMenu(self.top_bar, variable=self.country_filter_var, values=["All"])
        self.country_filter_menu.grid(row=0, column=3, padx=6, pady=6)

        ctk.CTkLabel(self.top_bar, text="行业").grid(row=0, column=4, padx=6, pady=6)
        self.industry_filter_menu = ctk.CTkOptionMenu(self.top_bar, variable=self.industry_filter_var, values=["All"])
        self.industry_filter_menu.grid(row=0, column=5, padx=6, pady=6)

        ctk.CTkLabel(self.top_bar, text="跟进状态").grid(row=0, column=6, padx=6, pady=6)
        self.status_filter_menu = ctk.CTkOptionMenu(self.top_bar, variable=self.status_filter_var, values=["All"])
        self.status_filter_menu.grid(row=0, column=7, padx=6, pady=6, sticky="w")

        ctk.CTkButton(self.top_bar, text="搜索/筛选", command=self.load_leads).grid(row=0, column=8, padx=6, pady=6)
        ctk.CTkButton(self.top_bar, text="重置", command=self.reset_filters).grid(row=0, column=9, padx=6, pady=6)
        ctk.CTkButton(self.top_bar, text="导出 CSV", command=self.export_csv).grid(row=0, column=10, padx=6, pady=6)
        ctk.CTkButton(self.top_bar, text="导出 Excel", command=self.export_xlsx).grid(row=0, column=11, padx=6, pady=6)

    def _build_table(self) -> None:
        self.table_frame.grid_rowconfigure(0, weight=1)
        self.table_frame.grid_columnconfigure(0, weight=1)

        self.lead_listbox = tk.Listbox(self.table_frame, font=("Segoe UI", 10))
        self.lead_listbox.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.lead_listbox.bind("<<ListboxSelect>>", self.on_select_lead)

        scrollbar = tk.Scrollbar(self.table_frame, orient="vertical", command=self.lead_listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=10)
        self.lead_listbox.config(yscrollcommand=scrollbar.set)

        self.current_rows = []

    def _build_form(self) -> None:
        self.form_frame.grid_columnconfigure(1, weight=1)

        fields = [
            ("LinkedIn 主页链接", "linkedin_url"),
            ("姓名", "name"),
            ("职位", "title"),
            ("公司", "company"),
            ("国家", "country"),
            ("行业", "industry"),
            ("跟进状态", "follow_up_status"),
        ]

        self.entries: Dict[str, ctk.CTkEntry] = {}
        for idx, (label_text, key) in enumerate(fields):
            ctk.CTkLabel(self.form_frame, text=label_text).grid(row=idx, column=0, padx=10, pady=8, sticky="w")
            if key == "follow_up_status":
                self.status_var = tk.StringVar(value=self.STATUS_OPTIONS[0])
                self.status_option = ctk.CTkOptionMenu(
                    self.form_frame,
                    variable=self.status_var,
                    values=self.STATUS_OPTIONS,
                )
                self.status_option.grid(row=idx, column=1, padx=10, pady=8, sticky="ew")
            else:
                entry = ctk.CTkEntry(self.form_frame)
                entry.grid(row=idx, column=1, padx=10, pady=8, sticky="ew")
                self.entries[key] = entry

        notes_row = len(fields)
        ctk.CTkLabel(self.form_frame, text="备注").grid(row=notes_row, column=0, padx=10, pady=8, sticky="nw")
        self.notes_text = ctk.CTkTextbox(self.form_frame, height=110)
        self.notes_text.grid(row=notes_row, column=1, padx=10, pady=8, sticky="ew")

        button_row = notes_row + 1
        button_frame = ctk.CTkFrame(self.form_frame, fg_color="transparent")
        button_frame.grid(row=button_row, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        ctk.CTkButton(button_frame, text="新增", command=self.add_lead).pack(side="left", padx=4)
        ctk.CTkButton(button_frame, text="更新", command=self.update_lead).pack(side="left", padx=4)
        ctk.CTkButton(button_frame, text="删除", command=self.delete_lead).pack(side="left", padx=4)
        ctk.CTkButton(button_frame, text="清空表单", command=self.clear_form).pack(side="left", padx=4)

        message_row = button_row + 1
        ctk.CTkButton(
            self.form_frame,
            text="生成开发信",
            command=self.generate_message,
        ).grid(row=message_row, column=0, columnspan=2, padx=10, pady=(5, 8), sticky="ew")

        ctk.CTkLabel(self.form_frame, text="英文开发信预览").grid(row=message_row + 1, column=0, columnspan=2, padx=10, sticky="w")
        self.message_text = ctk.CTkTextbox(self.form_frame, height=180)
        self.message_text.grid(row=message_row + 2, column=0, columnspan=2, padx=10, pady=8, sticky="nsew")

    def _collect_form_data(self) -> Dict[str, str]:
        return {
            "linkedin_url": self.entries["linkedin_url"].get().strip(),
            "name": self.entries["name"].get().strip(),
            "title": self.entries["title"].get().strip(),
            "company": self.entries["company"].get().strip(),
            "country": self.entries["country"].get().strip(),
            "industry": self.entries["industry"].get().strip(),
            "notes": self.notes_text.get("1.0", "end").strip(),
            "follow_up_status": self.status_var.get().strip(),
        }

    def _validate_required(self, lead: Dict[str, str]) -> bool:
        if not lead["linkedin_url"]:
            messagebox.showerror("缺少字段", "LinkedIn 主页链接不能为空。")
            return False
        if not lead["name"]:
            messagebox.showerror("缺少字段", "姓名不能为空。")
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
        messagebox.showinfo("成功", "客户线索已新增。")

    def update_lead(self) -> None:
        if not self.selected_lead_id:
            messagebox.showwarning("提示", "请先在左侧选择一条记录。")
            return

        lead = self._collect_form_data()
        if not self._validate_required(lead):
            return

        self.db.update_lead(self.selected_lead_id, lead)
        self.refresh_filters()
        self.load_leads()
        messagebox.showinfo("成功", "客户线索已更新。")

    def delete_lead(self) -> None:
        if not self.selected_lead_id:
            messagebox.showwarning("提示", "请先在左侧选择一条记录。")
            return

        confirm = messagebox.askyesno("确认删除", "确定要删除这条客户线索吗？")
        if not confirm:
            return

        self.db.delete_lead(self.selected_lead_id)
        self.clear_form()
        self.refresh_filters()
        self.load_leads()
        messagebox.showinfo("成功", "客户线索已删除。")

    def clear_form(self) -> None:
        for entry in self.entries.values():
            entry.delete(0, "end")
        self.notes_text.delete("1.0", "end")
        self.message_text.delete("1.0", "end")
        self.status_var.set(self.STATUS_OPTIONS[0])
        self.selected_lead_id = None

    def on_select_lead(self, event: tk.Event) -> None:
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

        self.status_var.set(lead.get("follow_up_status", ""))

    def reset_filters(self) -> None:
        self.search_var.set("")
        self.country_filter_var.set("All")
        self.industry_filter_var.set("All")
        self.status_filter_var.set("All")
        self.load_leads()

    def load_leads(self) -> None:
        keyword = self.search_var.get().strip()
        country = "" if self.country_filter_var.get() in ("", "All") else self.country_filter_var.get().strip()
        industry = "" if self.industry_filter_var.get() in ("", "All") else self.industry_filter_var.get().strip()
        status = "" if self.status_filter_var.get() in ("", "All") else self.status_filter_var.get().strip()

        rows = self.db.get_leads(keyword=keyword, country=country, industry=industry, follow_up_status=status)
        self.current_rows = rows

        self.lead_listbox.delete(0, "end")
        for row in rows:
            display = (
                f"[{row['id']}] {row.get('name', '')} | {row.get('title', '')} | "
                f"{row.get('company', '')} | {row.get('country', '')} | {row.get('follow_up_status', '')}"
            )
            self.lead_listbox.insert("end", display)

    def refresh_filters(self) -> None:
        countries = ["All"] + self.db.get_distinct_values("country")
        industries = ["All"] + self.db.get_distinct_values("industry")
        statuses = ["All"] + self.db.get_distinct_values("follow_up_status")

        self.country_filter_menu.configure(values=countries)
        self.industry_filter_menu.configure(values=industries)
        self.status_filter_menu.configure(values=statuses)

        if self.country_filter_var.get() not in countries:
            self.country_filter_var.set("All")
        if self.industry_filter_var.get() not in industries:
            self.industry_filter_var.set("All")
        if self.status_filter_var.get() not in statuses:
            self.status_filter_var.set("All")

    def generate_message(self) -> None:
        name = self.entries["name"].get().strip()
        title = self.entries["title"].get().strip()
        company = self.entries["company"].get().strip()

        message = generate_outreach_message(name=name, title=title, company=company)
        self.message_text.delete("1.0", "end")
        self.message_text.insert("1.0", message)

    def export_csv(self) -> None:
        rows = self.current_rows
        if not rows:
            messagebox.showwarning("提示", "没有可导出的数据。")
            return

        file_path = filedialog.asksaveasfilename(
            title="导出 CSV",
            defaultextension=".csv",
            filetypes=[("CSV 文件", "*.csv")],
            initialfile="linkedin_leads.csv",
        )
        if not file_path:
            return

        Exporter.export_to_csv(file_path, rows)
        messagebox.showinfo("成功", f"已导出到:\n{file_path}")

    def export_xlsx(self) -> None:
        rows = self.current_rows
        if not rows:
            messagebox.showwarning("提示", "没有可导出的数据。")
            return

        file_path = filedialog.asksaveasfilename(
            title="导出 Excel",
            defaultextension=".xlsx",
            filetypes=[("Excel 文件", "*.xlsx")],
            initialfile="linkedin_leads.xlsx",
        )
        if not file_path:
            return

        Exporter.export_to_xlsx(file_path, rows)
        messagebox.showinfo("成功", f"已导出到:\n{file_path}")
