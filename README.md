# LinkedIn 关键词找客助手（Python + CustomTkinter）

一个 **Windows 本地可运行** 的最小可用工具：
- 你输入 1-3 个关键词；
- 程序生成并打开 LinkedIn 搜索链接；
- 你在浏览器里手动浏览结果并手动录入客户；
- 工具可访问公司官网公开页面，提取公开联系方式并保存。

> 合规边界：
> - 不做 LinkedIn 爬虫
> - 不绕过登录
> - 不自动翻页
> - 不自动提取 LinkedIn 私人联系方式
> - 仅处理用户手动确认的客户和公司官网公开信息

---

## 功能

1. GUI 输入 1-3 个关键词并打开 LinkedIn 搜索页（默认浏览器）
2. 手动录入客户字段：
   - `name`
   - `title`
   - `company_name`
   - `linkedin_url`
   - `country`
   - `notes`
   - `company_website`
3. 从 `company_website` 的公开页面提取：
   - `public_email`
   - `phone_number`
   - `contact_page_url`
4. 保存到本地 SQLite
5. 导出 CSV 和 Excel（xlsx）

---

## 项目结构

```text
.
├─ main.py
├─ requirements.txt
├─ README.md
├─ ui/
│  └─ app.py
├─ database/
│  └─ db_manager.py
├─ export/
│  └─ exporter.py
└─ website/
   └─ contact_extractor.py
```

---

## 安装与运行（Windows）

### 1) 创建虚拟环境（可选）

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 2) 安装依赖

```bash
pip install -r requirements.txt
```

### 3) 启动

```bash
python main.py
```

---

## 使用流程

1. 在顶部输入 1-3 个关键词，点击 **“打开LinkedIn搜索”**。
2. 在浏览器中手动查看 LinkedIn 搜索结果（你自己登录、自己浏览）。
3. 把你手动确认的客户信息填入右侧表单并保存。
4. 若有 `company_website`，点击 **“从公司官网提取公开联系方式”**。
5. 最后可导出 CSV / Excel。

---

## 说明（MVP）

- 联系方式提取只尝试官网首页和可能的联系页链接（如 contact/about/support）。
- 因网站结构差异，提取结果可能为空，建议人工复核。
- 数据库默认路径：`database/leads.db`。

