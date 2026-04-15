# TikTok 视频下载脚本（带 UI）

这是一个基于 Python + Tkinter 的 TikTok 视频下载工具。

## 功能

- 支持用户直接粘贴 TikTok 文本链接（会自动提取 URL）
- 一键下载视频到指定目录
- 带有图形界面（UI）和日志输出
- 可直接从剪贴板粘贴内容

## 环境要求

- Python 3.10+
- 依赖：`yt-dlp`

## 安装

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## 运行

```bash
python app.py
```

## 使用说明

1. 打开程序后，把 TikTok 分享文本（或纯链接）粘贴到输入框。
2. 点击“下载视频”。
3. 下载完成后会弹窗提示，并在日志框看到详细输出。

## 注意

- TikTok 可能会调整反爬机制，导致下载失败。可以尝试升级 `yt-dlp`：

```bash
pip install -U yt-dlp
```

- 请遵守当地法律法规以及 TikTok 的服务条款，仅下载你有权使用的内容。
