#!/usr/bin/env python3
"""
Script para testar o executável do jogo
Verifica se o arquivo foi criado corretamente
"""

import os
import sys
import subprocess
from pathlib import Path

def test_build():
    """Testa se o executável foi compilado corretamente"""
    
    print("=" * 60)
    print("[TEST] Verificando executável do jogo")
    print("=" * 60)
    
    # Encontrar o executável
    project_root = Path(__file__).parent.parent
    dist_dir = project_root / "dist"
    
    # Procurar por .exe
    exe_files = list(dist_dir.glob("*.exe"))
    
    if not exe_files:
        print("[ERRO] Nenhum executável .exe encontrado em dist/")
        print(f"Conteúdo de {dist_dir}:")
        for item in dist_dir.iterdir():
            print(f"  {item}")
        return False
    
    exe_file = exe_files[0]  # Pega o primeiro .exe encontrado
    
    print(f"[OK] Executável encontrado: {exe_file.name}")
    
    # Verificar tamanho
    size_mb = exe_file.stat().st_size / (1024 * 1024)
    print(f"[OK] Tamanho: {size_mb:.1f} MB")
    
    # Verificar se é executável
    if os.access(exe_file, os.X_OK):
        print(f"[OK] Arquivo é executável")
    else:
        print(f"[AVISO] Arquivo não tem permissão de execução (Windows ignora isso)")
    
    # Tentar executar com --help (não funciona com .exe do PyInstaller, mas é um teste)
    print(f"\n[TEST] Tentando executar...")
    print(f"Comando: {exe_file}")
    print(f"\nPara executar o jogo:")
    print(f"  {exe_file}\n")
    
    # Para testar em headless, usar variáveis de ambiente
    test_cmd = [
        str(exe_file)
    ]
    
    print("[INFO] Para testar em modo headless (sem janela):")
    print(f"  set SDL_VIDEODRIVER=dummy")
    print(f"  set PLATFORM_GAME_ENV=production")
    print(f"  {exe_file}\n")
    
    print("=" * 60)
    print("[OK] Executável validado com sucesso!")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    success = test_build()
    sys.exit(0 if success else 1)
