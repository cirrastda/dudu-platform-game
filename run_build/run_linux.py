#!/usr/bin/env python3
"""
Script para executar o jogo no Linux via WSL2

Este script facilita a execução do jogo em ambiente Linux através do WSL2,
configuração automática do ambiente e execução do jogo.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def check_wsl():
    """Verifica se o WSL2 está disponível"""
    try:
        result = subprocess.run(
            ["wsl", "--status"], capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ):
        return False


def setup_linux_environment():
    """Configura o ambiente Linux no WSL2"""
    print("🐧 Configurando ambiente Linux via WSL2...")

    # Converte o caminho do Windows para WSL
    current_dir = os.getcwd()
    wsl_path = (
        current_dir.replace("\\", "/")
        .replace(":", "")
        .replace("C", "/mnt/c")
        .replace("B", "/mnt/b")
    )

    commands = [
        f"cd '{wsl_path}'",
        "echo 'Diretório atual:' && pwd",
        "echo 'Verificando Python...'",
        "python3 --version || (echo 'Instalando Python3...' && sudo apt update && sudo apt install -y python3 python3-pip python3-venv)",
        "echo 'Verificando ambiente virtual...'",
        "if [ ! -d 'venv' ]; then echo 'Criando ambiente virtual...' && python3 -m venv venv; fi",
        "echo 'Ativando ambiente virtual...'",
        "source venv/bin/activate",
        "echo 'Instalando dependências...'",
        "pip install --upgrade pip",
        "pip install -r requirements.txt",
        "echo 'Verificando display...'",
        "export DISPLAY=:0",
        "echo 'Ambiente configurado com sucesso!'",
    ]

    full_command = " && ".join(commands)

    try:
        result = subprocess.run(
            ["wsl", "--", "bash", "-c", full_command],
            check=False,
            text=True,
            timeout=300,  # 5 minutos timeout
        )

        if result.returncode == 0:
            print("✅ Ambiente Linux configurado com sucesso!")
            return True
        else:
            print(f"❌ Erro na configuração do ambiente (código: {result.returncode})")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Timeout na configuração do ambiente")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False


def run_game_linux():
    """Executa o jogo no Linux via WSL2"""
    print("🎮 Executando jogo no Linux...")

    # Converte o caminho do Windows para WSL
    current_dir = os.getcwd()
    wsl_path = (
        current_dir.replace("\\", "/")
        .replace(":", "")
        .replace("C", "/mnt/c")
        .replace("B", "/mnt/b")
    )

    commands = [
        f"cd '{wsl_path}'",
        "source venv/bin/activate",
        "export DISPLAY=:0",
        "export SDL_AUDIODRIVER=pulse",
        "export PULSE_RUNTIME_PATH=/mnt/wslg/runtime",
        'python3 -c "import pygame; pygame.mixer.pre_init(frequency=22050, size=-16, channels=2, buffer=512); pygame.mixer.init()" 2>/dev/null || export SDL_AUDIODRIVER=dummy',
        "python3 main.py",
    ]

    full_command = " && ".join(commands)

    try:
        # Executa o jogo de forma interativa
        subprocess.run(["wsl", "--", "bash", "-c", full_command], check=False)

    except KeyboardInterrupt:
        print("\n🛑 Jogo interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar o jogo: {e}")


def show_linux_requirements():
    """Mostra os requisitos para executar no Linux"""
    print("\n📋 REQUISITOS PARA LINUX:")
    print("1. WSL2 instalado e configurado")
    print("2. Distribuição Linux no WSL2 (Ubuntu recomendado)")
    print("3. WSLg (Windows Subsystem for Linux GUI) ou X Server")
    print("4. Python 3.8+ na distribuição Linux")
    print("5. Pygame e dependências instaladas")
    print("\n💡 DICAS:")
    print("- Execute 'setup_wsl2.ps1' para configuração automática")
    print("- WSLg (incluído no Windows 11) oferece melhor suporte gráfico")
    print("- Para Windows 10, use X Server (VcXsrv, Xming)")
    print("- Problemas de áudio são comuns no WSL2")
    print("- Para melhor experiência, considere VM Linux dedicada")
    print("\n🔧 SOLUÇÃO DE PROBLEMAS:")
    print("- Áudio: O jogo tentará usar áudio dummy se necessário")
    print("- Display: Certifique-se de que DISPLAY=:0 está configurado")
    print("- Performance: WSL2 pode ter limitações gráficas")


def main():
    """Função principal"""
    print("🐧 EXECUTAR JOGO NO LINUX VIA WSL2")
    print("=" * 40)

    # Verifica se está no Windows
    if platform.system() != "Windows":
        print("❌ Este script deve ser executado no Windows com WSL2")
        return False

    # Verifica se o WSL está disponível
    if not check_wsl():
        print("❌ WSL2 não encontrado ou não configurado")
        show_linux_requirements()
        return False

    print("✅ WSL2 detectado")

    # Configura o ambiente
    if not setup_linux_environment():
        print("❌ Falha na configuração do ambiente Linux")
        return False

    # Executa o jogo
    run_game_linux()

    return True


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Operação cancelada pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)
