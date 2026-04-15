import re
import subprocess
import threading
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# 匹配 TikTok 链接（支持 m/vm/www）
TIKTOK_URL_REGEX = re.compile(r"(https?://(?:www\.|m\.|vm\.)?tiktok\.com/[^\s]+)", re.IGNORECASE)


def extract_tiktok_url(text: str) -> str | None:
    """从用户粘贴的文本中提取 TikTok 链接。"""
    match = TIKTOK_URL_REGEX.search(text.strip())
    return match.group(1).rstrip(').,!?\"\'') if match else None


class TikTokDownloaderUI:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("TikTok 视频下载器")
        self.root.geometry("700x420")

        self.download_dir = tk.StringVar(value=str(Path.cwd() / "downloads"))
        self.status = tk.StringVar(value="准备就绪")

        self._build_ui()

    def _build_ui(self):
        main = ttk.Frame(self.root, padding=16)
        main.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main, text="把 TikTok 文本链接粘贴到这里：").pack(anchor=tk.W)

        self.input_text = tk.Text(main, height=8, wrap=tk.WORD)
        self.input_text.pack(fill=tk.BOTH, expand=False, pady=(6, 12))

        quick_actions = ttk.Frame(main)
        quick_actions.pack(fill=tk.X, pady=(0, 12))
        ttk.Button(quick_actions, text="从剪贴板粘贴", command=self.paste_clipboard).pack(side=tk.LEFT)
        ttk.Button(quick_actions, text="清空", command=self.clear_input).pack(side=tk.LEFT, padx=8)

        dir_frame = ttk.LabelFrame(main, text="下载目录", padding=10)
        dir_frame.pack(fill=tk.X, pady=(0, 12))

        ttk.Entry(dir_frame, textvariable=self.download_dir).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(dir_frame, text="选择目录", command=self.choose_directory).pack(side=tk.LEFT, padx=(8, 0))

        download_btn = ttk.Button(main, text="下载视频", command=self.start_download)
        download_btn.pack(fill=tk.X)

        self.progress = ttk.Progressbar(main, mode="indeterminate")
        self.progress.pack(fill=tk.X, pady=(12, 8))

        self.log_box = tk.Text(main, height=8, wrap=tk.WORD, state=tk.DISABLED)
        self.log_box.pack(fill=tk.BOTH, expand=True)

        status_frame = ttk.Frame(main)
        status_frame.pack(fill=tk.X, pady=(8, 0))
        ttk.Label(status_frame, text="状态：").pack(side=tk.LEFT)
        ttk.Label(status_frame, textvariable=self.status).pack(side=tk.LEFT)

    def append_log(self, message: str):
        self.log_box.config(state=tk.NORMAL)
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state=tk.DISABLED)

    def paste_clipboard(self):
        try:
            content = self.root.clipboard_get()
            self.input_text.delete("1.0", tk.END)
            self.input_text.insert(tk.END, content)
            self.status.set("已粘贴剪贴板内容")
        except tk.TclError:
            messagebox.showwarning("提示", "剪贴板为空或无法读取")

    def clear_input(self):
        self.input_text.delete("1.0", tk.END)
        self.status.set("已清空输入")

    def choose_directory(self):
        selected = filedialog.askdirectory(initialdir=self.download_dir.get())
        if selected:
            self.download_dir.set(selected)

    def start_download(self):
        raw_text = self.input_text.get("1.0", tk.END)
        video_url = extract_tiktok_url(raw_text)

        if not video_url:
            messagebox.showerror("错误", "未检测到有效的 TikTok 链接，请检查输入")
            return

        download_path = Path(self.download_dir.get()).expanduser().resolve()
        download_path.mkdir(parents=True, exist_ok=True)

        self.progress.start(8)
        self.status.set("下载中...")
        self.append_log(f"开始下载：{video_url}")

        thread = threading.Thread(
            target=self._download_worker,
            args=(video_url, download_path),
            daemon=True,
        )
        thread.start()

    def _download_worker(self, video_url: str, download_path: Path):
        # 文件名模板：上传者_视频ID
        output_template = str(download_path / "%(uploader)s_%(id)s.%(ext)s")

        cmd = [
            "yt-dlp",
            "-o",
            output_template,
            "--restrict-filenames",
            "--no-playlist",
            video_url,
        ]

        try:
            process = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                check=False,
            )

            self.root.after(0, self._on_download_complete, process.returncode, process.stdout, str(download_path))
        except FileNotFoundError:
            self.root.after(
                0,
                self._on_download_complete,
                127,
                "未找到 yt-dlp。请先安装：pip install yt-dlp",
                str(download_path),
            )

    def _on_download_complete(self, return_code: int, output: str, download_path: str):
        self.progress.stop()

        if output:
            self.append_log(output.strip())

        if return_code == 0:
            self.status.set("下载完成")
            messagebox.showinfo("完成", f"视频已下载到：{download_path}")
        else:
            self.status.set("下载失败")
            messagebox.showerror("失败", "下载失败，请查看日志信息")


def main():
    root = tk.Tk()
    app = TikTokDownloaderUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
