@echo off
chcp 65001 >nul
title 元素周期表壁纸 - 一键安装
cd /d "%~dp0"

echo ============================================
echo   元素周期表 + 日语五十音 动态壁纸
echo   一键安装（需要已安装 Lively Wallpaper）
echo ============================================
echo.

where python >nul 2>nul
if errorlevel 1 (
  echo [错误] 没找到 Python，无法自动安装。
  echo 请手动：打开 Lively Wallpaper，把本文件夹整个拖进去。
  pause
  exit /b 1
)

python "%~dp0install.py"
pause
