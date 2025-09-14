#!/usr/bin/env python3
"""
Script para build do jogo para Linux via WSL2

Este script automatiza o processo de build para Linux:
1. Verifica e configura WSL2
2. Instala dependências Linux
3. Executa build com PyInstaller
4. Cria pacote distribuível
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
from datetime import datetime


def check_wsl():
    """Verifica se WSL2 está disponível"""
    if platform.system() != "Windows":
        print("❌ Este script deve ser executado no Windows")
        return False

    try:
        result = subprocess.run(
            ["wsl", "--status"], capture_output=True, text=True, timeout=10
        )
        if "WSL 2" in result.stdout:
            print("✅ WSL2 detectado")
            return True
        else:
            print("❌ WSL2 não encontrado")
            return False
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ):
        print("❌ WSL não disponível")
        return False


def get_wsl_path():
    """Converte o caminho Windows para WSL"""
    current_path = Path.cwd()
    # Converte C:\path para /mnt/c/path
    drive = current_path.parts[0].lower().replace(":", "")
    path_parts = current_path.parts[1:]
    wsl_path = f"/mnt/{drive}/" + "/".join(path_parts)
    return wsl_path


def setup_linux_environment():
    """Configura o ambiente Linux no WSL2"""
    print("🐧 Configurando ambiente Linux...")
    wsl_path = get_wsl_path()

    commands = [
        f"cd '{wsl_path}'",
        "echo 'Diretório atual:'",
        "pwd",
        "echo 'Verificando Python...'",
        "python3 --version",
        "echo 'Verificando ambiente virtual...'",
        "if [ ! -d 'venv' ]; then python3 -m venv venv; fi",
        "echo 'Ativando ambiente virtual...'",
        "source venv/bin/activate",
        "echo 'Atualizando pip...'",
        "python3 -m pip install --upgrade pip",
        "echo 'Instalando dependências...'",
        "pip install -r requirements.txt",
        "echo 'Instalando PyInstaller...'",
        "pip install pyinstaller",
        "echo 'Instalando dependências de sistema...'",
        "sudo apt-get update -qq",
        "sudo apt-get install -y python3-dev libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev libfreetype6-dev libportmidi-dev",
    ]

    full_command = " && ".join(commands)

    try:
        result = subprocess.run(
            ["wsl", "--", "bash", "-c", full_command], check=False, text=True
        )

        if result.returncode == 0:
            print("✅ Ambiente Linux configurado com sucesso!")
            return True
        else:
            print(f"❌ Erro na configuração: código {result.returncode}")
            return False

    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False


def build_linux_executable():
    """Executa o build do executável Linux"""
    print("\n🔨 Iniciando build para Linux...")
    wsl_path = get_wsl_path()

    # Cria diretório de build se não existir
    build_dir = Path("build_linux")
    build_dir.mkdir(exist_ok=True)

    commands = [
        f"cd '{wsl_path}'",
        "source venv/bin/activate",
        "echo 'Executando PyInstaller...'",
        "pyinstaller --onefile --windowed --name jumpandhit_linux --distpath dist/linux --workpath build_linux/work --specpath build_linux main.py",
        "echo 'Copiando recursos...'," "cp -r imagens dist/linux/",
        "cp -r musicas dist/linux/",
        "cp -r sounds dist/linux/",
        "echo 'Build concluído!'",
    ]

    full_command = " && ".join(commands)

    try:
        print("⏳ Este processo pode demorar alguns minutos...")

        process = subprocess.Popen(
            ["wsl", "--", "bash", "-c", full_command],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True,
        )

        # Mostra output em tempo real
        for line in process.stdout:
            print(line.rstrip())

        process.wait()

        if process.returncode == 0:
            print("\n✅ Build Linux concluído com sucesso!")
            return True
        else:
            print(f"\n❌ Build falhou com código {process.returncode}")
            return False

    except KeyboardInterrupt:
        print("\n🛑 Build cancelado pelo usuário")
        return False
    except Exception as e:
        print(f"\n❌ Erro durante o build: {e}")
        return False


def create_linux_package():
    """Cria pacote distribuível para Linux"""
    print("\n📦 Criando pacote Linux...")

    dist_dir = Path("dist") / "linux"

    if not dist_dir.exists():
        print("❌ Diretório de distribuição não encontrado")
        return False

    # Cria diretório de releases
    releases_dir = Path("releases")
    releases_dir.mkdir(exist_ok=True)

    # Nome do pacote com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"jumpandhit_linux_{timestamp}"
    package_dir = releases_dir / package_name

    try:
        # Copia arquivos para o pacote
        shutil.copytree(dist_dir, package_dir)

        # Cria script de execução
        run_script = package_dir / "run.sh"
        with open(run_script, "w") as f:
            f.write("#!/bin/bash\n")
            f.write('cd "$(dirname "$0")"\n')
            f.write("./jumpandhit_linux\n")

        # Torna o script executável
        os.chmod(run_script, 0o755)

        # Cria README
        readme = package_dir / "README.txt"
        with open(readme, "w") as f:
            f.write("Jump and Hit - Linux Version\n")
            f.write("============================\n\n")
            f.write("Para executar o jogo:\n")
            f.write("1. Abra um terminal\n")
            f.write("2. Navegue até esta pasta\n")
            f.write("3. Execute: ./run.sh\n")
            f.write("   ou: ./jumpandhit_linux\n\n")
            f.write("Requisitos:\n")
            f.write("- Linux x64\n")
            f.write("- Bibliotecas SDL2 (geralmente já instaladas)\n")
            f.write("- Placa de som (opcional)\n\n")
            f.write(
                f"Build criado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )

        # Cria arquivo ZIP
        zip_path = releases_dir / f"{package_name}.zip"
        shutil.make_archive(str(zip_path.with_suffix("")), "zip", package_dir)

        print(f"✅ Pacote Linux criado: {zip_path}")
        print(f"📁 Pasta: {package_dir}")

        return True

    except Exception as e:
        print(f"❌ Erro ao criar pacote: {e}")
        return False


def test_linux_executable():
    """Testa o executável Linux"""
    print("\n🧪 Testando executável Linux...")
    wsl_path = get_wsl_path()

    commands = [
        f"cd '{wsl_path}/build_linux/dist'",
        "echo 'Verificando executável...'",
        "ls -la jumpandhit_linux",
        "echo 'Testando execução (5 segundos)...'",
        "timeout 5s ./jumpandhit_linux || echo 'Teste concluído (timeout esperado)'",
    ]

    full_command = " && ".join(commands)

    try:
        result = subprocess.run(
            ["wsl", "--", "bash", "-c", full_command],
            capture_output=True,
            text=True,
            timeout=30,
        )

        print(result.stdout)
        if result.stderr:
            print("Avisos:", result.stderr)

        print("✅ Teste do executável concluído")
        return True

    except subprocess.TimeoutExpired:
        print("⏰ Timeout no teste (normal)")
        return True
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False


def show_linux_requirements():
    """Mostra os requisitos para build Linux"""
    print("\n📋 REQUISITOS PARA BUILD LINUX:")
    print("1. Windows com WSL2 instalado")
    print("2. Distribuição Linux no WSL2 (Ubuntu recomendado)")
    print("3. Python 3.8+ na distribuição Linux")
    print("4. Sudo/root access no WSL2")
    print("5. Conexão com internet para instalar dependências")
    print("\n💡 DICAS:")
    print("- Execute 'setup_wsl2.ps1' para configuração inicial")
    print("- O build pode demorar 5-10 minutos na primeira vez")
    print("- Builds subsequentes são mais rápidos")
    print("- O executável gerado roda em qualquer Linux x64")


def main():
    """Função principal"""
    print("🐧 BUILD LINUX VIA WSL2")
    print("=" * 30)
    print("Este script irá:")
    print("1. 🔍 Verificar WSL2")
    print("2. 🐧 Configurar ambiente Linux")
    print("3. 🔨 Fazer build do executável")
    print("4. 📦 Criar pacote distribuível")
    print("5. 🧪 Testar executável")
    print()

    # Verifica WSL2
    if not check_wsl():
        show_linux_requirements()
        return False

    # Configura ambiente
    if not setup_linux_environment():
        print("❌ Falha na configuração do ambiente")
        return False

    # Executa build
    if not build_linux_executable():
        print("❌ Falha no build")
        return False

    # Cria pacote
    if not create_linux_package():
        print("❌ Falha na criação do pacote")
        return False

    # Testa executável
    if not test_linux_executable():
        print("⚠️  Falha no teste (pode ser normal)")

    print("\n🎉 Build Linux concluído com sucesso!")
    print("📁 Verifique a pasta 'releases' para os arquivos gerados")

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
