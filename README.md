# LinkedIn 客户线索整理助手（Python + CustomTkinter）

一个本地桌面工具，用于**手动整理 LinkedIn 客户线索**。  
不做批量爬虫、不绕过登录、不抓取未授权的私人联系方式。

## 功能清单

- CustomTkinter 桌面 GUI
- 手动录入字段：
  - LinkedIn 主页链接
  - 姓名
  - 职位
  - 公司
  - 国家
  - 行业
  - 备注
  - 跟进状态
- 本地 SQLite 存储
- 搜索 + 筛选（国家、行业、跟进状态）
- 导出 CSV / Excel（xlsx）
- 本地模板“生成开发信”（英文初次触达话术）

## 项目结构

```text
.
├─ main.py
├─ requirements.txt
├─ README.md
├─ database/
│  └─ db_manager.py
├─ export/
│  └─ exporter.py
├─ templates/
│  ├─ message_generator.py
│  └─ outreach_template.txt
└─ ui/
   └─ app.py
```

## 运行环境

- Windows 10/11（推荐）
- Python 3.10+

## 安装步骤

1. 进入项目目录：

```bash
cd /path/to/project
```

2. 创建虚拟环境（可选但推荐）：

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. 安装依赖：

```bash
pip install -r requirements.txt
```

## 启动程序

```bash
python main.py
```

## 数据与导出说明

- SQLite 数据库默认保存到：`database/leads.db`
- 点击界面“导出 CSV”可导出 `.csv`
- 点击界面“导出 Excel”可导出 `.xlsx`

## 使用建议

- 建议保持“LinkedIn 主页链接 + 姓名”真实准确，便于后续跟进。
- “生成开发信”使用本地模板，内容可在 `templates/outreach_template.txt` 自行修改。

