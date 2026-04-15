@echo off
setlocal

REM Windows 一键打包脚本（生成 dist\TikTokDownloader.exe）
if not exist .venv (
  py -m venv .venv
)

call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install pyinstaller

pyinstaller --clean --noconfirm tiktok_downloader.spec

echo.
echo Build done. EXE path: dist\TikTokDownloader.exe
endlocal
