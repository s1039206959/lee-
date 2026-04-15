# B2B 线索发现助手（合规版）

这是一个 Streamlit UI 示例：

- 输入 1~3 个行业关键词
- 返回公司名称 + 联系邮箱（示例数据）
- 支持导出 CSV

> ⚠️ 注意：本项目**不提供**对 LinkedIn 的自动化抓取功能。推荐使用公开网页与已授权 API 数据源进行线索收集。

## 运行方式

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 可扩展方向

- 接入合规数据源 API（如公司目录 API）
- 邮箱验证服务（ZeroBounce / NeverBounce）
- CRM 同步（HubSpot / Salesforce）
