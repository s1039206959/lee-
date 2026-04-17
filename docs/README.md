# 广州有喜传媒有限公司 静态企业官网

## 1. 项目简介
这是一个可直接上线到 GitHub Pages 的纯静态企业官网项目，品牌定位为“企业出海跨境咨询与品牌营销服务商”，面向有出海需求的中国工厂、制造企业、品牌方和跨境卖家。

核心展示内容：
- 企业出海跨境咨询
- 品牌出海营销与国际化定位
- TikTok 增长与获客指导
- 成功案例（五金收纳 / 美妆产品 / 家电3C / 服装）
- 联系咨询入口

技术栈：
- HTML + CSS + JavaScript（无后端、无数据库、无 Node 运行依赖）

---

## 2. 如何本地预览
### 方式 A：直接双击打开
直接打开 `index.html` 即可预览。

### 方式 B：本地静态服务器（推荐）
在仓库根目录执行：

```bash
python -m http.server 8080 --directory docs
```

浏览器访问：
`http://localhost:8080`

---

## 3. 如何部署到 GitHub Pages
### 方式一（推荐）
1. 推送代码到 GitHub 仓库。
2. 打开仓库：`Settings -> Pages`。
3. 在 `Build and deployment` 中设置：
   - Source: `Deploy from a branch`
   - Branch: `main`
   - Folder: `/docs`
4. 保存后等待 1~3 分钟。

### 方式二
将 `docs/` 目录内容发布到 `gh-pages` 分支根目录。
本项目案例图使用 **项目内自制 SVG 占位图**（无外部下载图片、无第三方版权依赖），用于上线前展示版：
- `assets/images/hardware-storage.svg`
- `assets/images/beauty-product.svg`
- `assets/images/home-appliance-3c.svg`
- `assets/images/fashion-apparel.svg`
> 说明：这些占位图可商用风险极低，适合作为初版上线素材。

如需替换为真实照片，建议优先选择以下低版权风险方向（请在下载前再次核对授权条款）：
- 推荐素材平台方向：Unsplash、Pexels、Pixabay（优先选择可商用、可修改、无需署名或按要求署名的素材）。
- 建议搜索关键词（中英组合）：
  - 五金收纳：`warehouse metal storage`, `industrial organizer`, `factory hardware shelf`
  - 美妆产品：`cosmetic product flat lay`, `beauty packaging studio`, `skincare product display`
  - 家电 / 3C：`consumer electronics showcase`, `smart home appliance`, `electronics manufacturing`
  - 服装：`apparel manufacturing`, `fashion production line`, `clothing export showroom`
- 素材风格建议：深色背景、工作室布光、简洁构图、偏商务展示感，保持四张案例图视觉统一。
---
### 替换公司文案
- 编辑 `index.html` 中各区块文字（Hero / About / Services / Cases / Why Us / Contact）。

### 替换案例图
1. 将正式图片放入 `docs/assets/images/`。
2. 建议文件命名：
   - `hardware-storage.jpg`
   - `beauty-product.jpg`
   - `home-appliance-3c.jpg`
   - `fashion-apparel.jpg`
3. 在 `index.html` 中修改 `<img src="...">` 路径。
### 替换品牌色与视觉风格
- 编辑 `style.css` 顶部 `:root` 颜色变量（如 `--primary`、`--metal`、`--bg`）。

### 修改动画节奏
- 编辑 `script.js` 中数字动画和滚动 reveal 逻辑。

---

## 后续可替换项（建议）
- 真实客户名称与更详细指标（需确认可公开范围）
- 企业 LOGO、办公场景图、团队照片
- 公司邮箱和微信（当前为演示占位，可替换成正式商务联系方式）
