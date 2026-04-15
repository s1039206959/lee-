import re
from dataclasses import dataclass, asdict
from typing import List, Optional

import pandas as pd
import streamlit as st


@dataclass
class CompanyLead:
    keyword: str
    company_name: str
    website: str
    contact_email: Optional[str]
    source: str


# 示例数据：用于演示 UI 与流程（避免违反平台条款的抓取）
DEMO_COMPANIES = [
    {"name": "CloudNova", "industry": "cloud security", "website": "https://cloudnova.example"},
    {"name": "DataForge Labs", "industry": "data platform", "website": "https://dataforge.example"},
    {"name": "GreenVolt AI", "industry": "energy ai", "website": "https://greenvolt.example"},
    {"name": "MediPulse Tech", "industry": "digital health", "website": "https://medipulse.example"},
    {"name": "RetailFlow", "industry": "ecommerce automation", "website": "https://retailflow.example"},
]


def _extract_domain(url: str) -> str:
    return re.sub(r"^https?://", "", url).strip("/")


def _guess_generic_email(website: str) -> str:
    """
    演示用途：根据域名生成通用邮箱。
    生产环境建议接入邮箱验证服务（如 ZeroBounce / NeverBounce）并检查合规性。
    """
    domain = _extract_domain(website)
    return f"info@{domain}"


def discover_companies(keywords: List[str]) -> List[CompanyLead]:
    results: List[CompanyLead] = []
    lowered = [k.lower().strip() for k in keywords if k.strip()]

    for kw in lowered:
        for item in DEMO_COMPANIES:
            if kw in item["industry"].lower() or kw in item["name"].lower():
                results.append(
                    CompanyLead(
                        keyword=kw,
                        company_name=item["name"],
                        website=item["website"],
                        contact_email=_guess_generic_email(item["website"]),
                        source="公开网站（演示数据）",
                    )
                )

    # 去重
    dedup = {}
    for r in results:
        dedup[(r.keyword, r.company_name)] = r
    return list(dedup.values())


def render_header() -> None:
    st.set_page_config(page_title="B2B 线索发现助手", page_icon="🔎", layout="wide")
    st.markdown(
        """
        <style>
            .hero {
                padding: 1rem 1.2rem;
                border-radius: 16px;
                background: linear-gradient(120deg, #0f172a, #1d4ed8);
                color: white;
                margin-bottom: 1rem;
            }
            .hint {
                padding: 0.8rem;
                border-radius: 12px;
                background: #ecfeff;
                border: 1px solid #a5f3fc;
                color: #155e75;
                margin-bottom: 0.8rem;
            }
        </style>
        <div class="hero">
            <h2>🔎 B2B 公司线索发现助手</h2>
            <p>输入 1-3 个行业关键词，获取公司名称与公开联系方式（合规版流程）。</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar() -> tuple[list[str], bool]:
    with st.sidebar:
        st.header("⚙️ 参数设置")
        raw = st.text_input("行业关键词（英文逗号分隔，最多 3 个）", "cloud security,data platform")
        run = st.button("开始检索", type="primary", use_container_width=True)

        st.markdown("---")
        st.caption("说明：本示例不包含对 LinkedIn 的自动化抓取，以避免违反平台条款。")

    keywords = [k.strip() for k in raw.split(",") if k.strip()][:3]
    return keywords, run


def render_results(leads: List[CompanyLead]) -> None:
    if not leads:
        st.warning("未找到匹配公司，请尝试更通用的关键词。")
        return

    df = pd.DataFrame([asdict(l) for l in leads])
    st.success(f"检索完成，共发现 {len(df)} 条记录")
    st.dataframe(df, use_container_width=True)

    csv = df.to_csv(index=False).encode("utf-8-sig")
    st.download_button(
        "⬇️ 下载 CSV",
        data=csv,
        file_name="company_leads.csv",
        mime="text/csv",
        use_container_width=False,
    )


def main() -> None:
    render_header()
    st.markdown(
        "<div class='hint'>✅ 推荐方案：从公开网页、企业官网联系方式页、以及已授权的数据源获取线索，再做邮箱有效性验证。</div>",
        unsafe_allow_html=True,
    )

    keywords, run = render_sidebar()

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("🧠 工作流")
        st.markdown(
            """
            1. 输入关键词（最多 3 个）  
            2. 根据关键词匹配相关公司  
            3. 输出公司名 + 联系邮箱（演示/公开来源）  
            4. 导出 CSV 进入销售流程
            """
        )

    with col2:
        st.subheader("🛡️ 合规提醒")
        st.info(
            "请遵守目标网站的 robots.txt、服务条款和适用的数据隐私法规（例如 GDPR/CCPA）。"
        )

    if run:
        if not (1 <= len(keywords) <= 3):
            st.error("请提供 1~3 个关键词。")
            return

        leads = discover_companies(keywords)
        render_results(leads)


if __name__ == "__main__":
    main()
