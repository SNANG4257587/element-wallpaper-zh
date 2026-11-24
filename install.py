# -*- coding: utf-8 -*-
"""元素周期表 + 日语五十音 动态壁纸 一键安装脚本。
把本文件夹复制进 Lively Wallpaper 壁纸库，并设为桌面壁纸。
可重复运行；也可直接把整个文件夹拖进 Lively Wallpaper 窗口。
"""
import os
import sys
import shutil
import subprocess

SRC = os.path.dirname(os.path.abspath(__file__))
WALL_NAME = "periodic_table_cn_voice"          # 库内固定目录名，避免中文路径
LOCAL = os.environ.get("LOCALAPPDATA", os.path.expanduser("~\\AppData\\Local"))
LIB = os.path.join(LOCAL, "Lively Wallpaper", "Library", "wallpapers")
DEST = os.path.join(LIB, WALL_NAME)

# 不要复制进壁纸库的安装辅助文件
SKIP = {"install.py", "安装.bat", "一键安装.bat"}
SKIP_EXT = {".zip"}


def find_lively():
    candidates = [
        os.path.join(os.environ.get("ProgramFiles", "C:\\Program Files"), "Lively Wallpaper", "Lively.exe"),
        os.path.join(os.environ.get("ProgramFiles(x86)", "C:\\Program Files (x86)"), "Lively Wallpaper", "Lively.exe"),
        os.path.join(LOCAL, "Programs", "Lively Wallpaper", "Lively.exe"),
        os.path.join(LOCAL, "Lively Wallpaper", "Lively.exe"),
    ]
    for p in candidates:
        if os.path.isfile(p):
            return p
    return None


def copy_wallpaper():
    os.makedirs(DEST, exist_ok=True)
    count = 0
    for root, dirs, files in os.walk(SRC):
        dirs[:] = [d for d in dirs if d != "__pycache__"]
        rel = os.path.relpath(root, SRC)
        tgt = DEST if rel == "." else os.path.join(DEST, rel)
        os.makedirs(tgt, exist_ok=True)
        for f in files:
            if f in SKIP or os.path.splitext(f)[1].lower() in SKIP_EXT:
                continue
            shutil.copy2(os.path.join(root, f), os.path.join(tgt, f))
            count += 1
    return count


def main():
    print("=" * 46)
    print("  元素周期表 + 日语五十音 动态壁纸 · 一键安装")
    print("=" * 46)

    lively = find_lively()
    if not lively:
        print("\n[提示] 没有检测到 Lively Wallpaper（免费壁纸软件）。")
        print("请先安装 Lively Wallpaper，再运行本脚本。")
        print("或者：打开 Lively 后，把本文件夹整个拖进它的窗口即可手动安装。")
        return 1

    if not os.path.isfile(os.path.join(SRC, "index.html")):
        print("\n[错误] 本文件夹缺少 index.html，壁纸文件不完整。")
        return 1

    print("\n[1/2] 正在复制壁纸文件到 Lively 壁纸库 ...")
    n = copy_wallpaper()
    print("      已复制 %d 个文件" % n)

    print("[2/2] 正在设置为桌面壁纸 ...")
    try:
        r = subprocess.run(
            [lively, "setwp", "--file", DEST],
            capture_output=True, text=True, timeout=30
        )
        print("      设置命令已发送（返回码 %d）" % r.returncode)
    except Exception as e:
        print("      设置命令调用异常：%s" % e)
        print("      壁纸已入库存好，请在 Lively 里点一下缩略图即可。")
        return 0

    print("\n完成。桌面壁纸已更新（若未立刻变化，稍等 1-2 秒）。")
    print("用法：单击元素/假名看详情，双击听标准发音朗读。")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print("\n[发生错误] %s" % e)
        import traceback
        traceback.print_exc()
        sys.exit(1)
