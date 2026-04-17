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

---

## 4. 表单服务接入（静态站可用）
本项目已集成 **Formspree** 前端提交方案（不需要后端，不暴露密码/API Key）。

### 你需要做什么
1. 注册 Formspree：<https://formspree.io/>
2. 创建一个新表单（目标收件邮箱填写：`ss1039206959@gmail.com`）。
3. 获取 Form Endpoint（格式类似：`https://formspree.io/f/xxxxabcd`）。
4. 打开 `docs/index.html`，找到联系表单 `action` 这一行并替换：
   - 当前占位：`https://formspree.io/f/REPLACE_WITH_YOUR_FORM_ID`
   - 替换为你的真实 endpoint。

### 表单成功/失败反馈
- 提交成功：页面会提示“提交成功！我们已收到您的咨询信息...”
- 提交失败：页面会提示失败原因并建议直接发邮件到 `ss1039206959@gmail.com`

### 如何测试是否成功发到邮箱
1. 完成 endpoint 替换后，本地运行：
   ```bash
   python -m http.server 8080 --directory docs
   ```
2. 访问 `http://localhost:8080`，填写表单并提交。
3. 页面出现“提交成功”提示后，检查 `ss1039206959@gmail.com` 收件箱（含垃圾邮件箱）。
4. 再尝试断网或伪造错误 endpoint，确认失败提示正常显示。

---

## 5. 图片来源说明
本项目案例图使用 **项目内自制 SVG 占位图**（无外部下载图片、无第三方版权依赖），用于上线前展示版：
- `assets/images/hardware-storage.svg`
- `assets/images/beauty-product.svg`
- `assets/images/home-appliance-3c.svg`
- `assets/images/fashion-apparel.svg`
- `assets/images/wechat-qr-placeholder.svg`（微信二维码占位图）

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

## 6. 后续如何替换文案和案例
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

### 替换微信二维码图片
1. 将你的真实二维码图片放到：`docs/assets/images/wechat-qr.png`（建议路径）。
2. 在 `docs/index.html` 中把 `wechat-qr-placeholder.svg` 改为 `wechat-qr.png`。
3. 建议尺寸：`720x720` 或 `1024x1024`，保证扫码清晰。

### 替换品牌色与视觉风格
- 编辑 `style.css` 顶部 `:root` 颜色变量（如 `--primary`、`--metal`、`--bg`）。

### 修改动画节奏
- 编辑 `script.js` 中数字动画和滚动 reveal 逻辑。

---

## 后续可替换项（建议）
- 真实客户名称与更详细指标（需确认可公开范围）
- 企业 LOGO、办公场景图、团队照片
- 表单 endpoint（当前是 Formspree 占位地址，需替换为你自己的 endpoint）
- 公司邮箱和微信（当前为演示占位，可替换成正式商务联系方式）
