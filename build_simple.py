#!/usr/bin/env python3
"""Build simples para criar executável único"""

import subprocess
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent

# Limpar
print("[1/3] Limpando...")
subprocess.run(["powershell", "-Command", "Remove-Item -Recurse -Force dist, build -ErrorAction SilentlyContinue"], cwd=PROJECT_ROOT)

# Build
print("[2/3] Compilando...")
cmd = [
    sys.executable, "-m", "PyInstaller",
    "--onefile",  # EXECUTÁVEL ÚNICO
    "--name", "JumpandHit",
    "--distpath", str(PROJECT_ROOT / "dist"),
    "--workpath", str(PROJECT_ROOT / "build"),
    "--specpath", str(PROJECT_ROOT / "build"),
    "--console",
    "--add-data", f"{PROJECT_ROOT / 'imagens'};imagens",
    "--add-data", f"{PROJECT_ROOT / 'musicas'};musicas",
    "--add-data", f"{PROJECT_ROOT / 'sounds'};sounds",
    "--add-data", f"{PROJECT_ROOT / 'videos'};videos",
    "--icon", str(PROJECT_ROOT / "imagens/icones/icon_desktop_new.ico"),
    # Hidden imports para MoviePy e video
    "--hidden-import", "moviepy",
    "--hidden-import", "moviepy.video.io.VideoFileClip",
    "--hidden-import", "moviepy.audio.io.AudioFileClip",
    "--hidden-import", "imageio",
    "--hidden-import", "imageio_ffmpeg",
    "--collect-all", "moviepy",
    "--collect-all", "imageio_ffmpeg",
    "--copy-metadata", "imageio",
    "--copy-metadata", "imageio_ffmpeg",
    str(PROJECT_ROOT / "bootstrap.py")
]

result = subprocess.run(cmd, cwd=PROJECT_ROOT)

if result.returncode == 0:
    exe = PROJECT_ROOT / "dist" / "JumpandHit.exe"  # Arquivo único na pasta dist
    if exe.exists():
        size_mb = exe.stat().st_size / (1024 * 1024)
        print(f"\n[3/3] OK! Executavel criado: {exe.name} ({size_mb:.1f} MB)")
        print(f"Localizacao: {exe}")
    else:
        print(f"\nErro: Executavel nao encontrado em {exe}")
        sys.exit(1)
else:
    print(f"\nErro na compilacao")
    sys.exit(1)
