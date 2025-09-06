#!/usr/bin/env python3
"""
Script para criar executável do jogo de plataforma
"""

import os
import sys
import subprocess

def build_executable():
    """Criar executável usando PyInstaller"""
    print("Criando executável do jogo...")
    
    # Comando PyInstaller
    cmd = [
        "pyinstaller",
        "--onefile",  # Criar um único arquivo executável
        "--windowed",  # Não mostrar console (apenas para Windows/Mac)
        "--name=JogoPlataforma",  # Nome do executável
        "--icon=icon.ico" if os.path.exists("icon.ico") else "",  # Ícone (opcional)
        "main.py"
    ]
    
    # Remover argumentos vazios
    cmd = [arg for arg in cmd if arg]
    
    try:
        subprocess.run(cmd, check=True)
        print("\n✅ Executável criado com sucesso!")
        print("📁 Localização: dist/JogoPlataforma")
        print("\n🎮 Para executar o jogo:")
        print("   - No macOS/Linux: ./dist/JogoPlataforma")
        print("   - No Windows: dist\\JogoPlataforma.exe")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao criar executável: {e}")
        return False
    except FileNotFoundError:
        print("❌ PyInstaller não encontrado. Instale com: pip install pyinstaller")
        return False
        
    return True

def install_dependencies():
    """Instalar dependências do requirements.txt"""
    print("Instalando dependências...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def main():
    print("🎮 Build do Jogo de Plataforma")
    print("=" * 40)
    
    # Verificar se estamos no diretório correto
    if not os.path.exists("main.py"):
        print("❌ Arquivo main.py não encontrado!")
        print("   Execute este script no diretório do jogo.")
        return
    
    # Instalar dependências
    if not install_dependencies():
        return
        
    print("\n" + "=" * 40)
    
    # Criar executável
    if build_executable():
        print("\n🎉 Build concluído com sucesso!")
    else:
        print("\n❌ Falha no build.")

if __name__ == "__main__":
    main()