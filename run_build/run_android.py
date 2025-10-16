#!/usr/bin/env python3
"""
Script para execução direta do jogo Android via F5
Usa Docker dentro do WSL2 para build e execução completa
"""

import os
import sys
import subprocess
import time
import json
from pathlib import Path

# Definir codificação UTF-8 para evitar erros de charset
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    # No Windows, usar codepage UTF-8
    os.system("chcp 65001 > nul 2>&1")


def check_wsl_docker():
    """Verifica se WSL2 e Docker estão disponíveis"""
    try:
        # Verifica WSL2
        result = subprocess.run(
            ["wsl", "--list", "--verbose"], capture_output=True, text=True
        )
        if result.returncode != 0:
            return False, "WSL2 não disponível"

        # Verifica Docker no WSL2
        result = subprocess.run(
            ["wsl", "docker", "--version"], capture_output=True, text=True
        )
        if result.returncode != 0:
            return False, "Docker não disponível no WSL2"

        # Verifica ADB no WSL2
        result = subprocess.run(["wsl", "which", "adb"], capture_output=True, text=True)
        if result.returncode != 0:
            # Instala ADB se não estiver disponível
            print("📱 Instalando ADB no WSL2...")
            subprocess.run(["wsl", "sudo", "apt", "update", "-y"], check=False)
            subprocess.run(
                ["wsl", "sudo", "apt", "install", "android-tools-adb", "-y"],
                check=False,
            )

        return True, "WSL2 + Docker + ADB disponíveis"
    except Exception as e:
        return False, f"Erro: {e}"


def get_package_name():
    """Obtém o nome do pacote do buildozer.spec"""
    try:
        buildozer_path = os.path.join("run_build", "config", "buildozer.spec")
        with open(buildozer_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("package.name"):
                    return line.split("=")[1].strip()
        return "jumpandhit"  # fallback
    except:
        return "jumpandhit"  # fallback


def get_package_domain():
    """Obtém o domínio do pacote do buildozer.spec"""
    try:
        buildozer_path = os.path.join("run_build", "config", "buildozer.spec")
        with open(buildozer_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip().startswith("package.domain"):
                    return line.split("=")[1].strip()
        return "org.example"  # fallback
    except:
        return "org.example"  # fallback


def build_apk_docker():
    """Constrói APK usando Docker no WSL2"""
    try:
        print("🐳 Iniciando build Docker...")
        
        # Verificar se buildozer.spec existe
        buildozer_path = os.path.join("run_build", "config", "buildozer.spec")
        if not os.path.exists(buildozer_path):
            print("❌ Arquivo buildozer.spec não encontrado!")
            print("💡 Criando buildozer.spec padrão...")
            # Criar buildozer.spec básico se não existir
            os.makedirs(os.path.dirname(buildozer_path), exist_ok=True)
            return False
        
        # Criar link simbólico temporário na raiz
        temp_spec = "buildozer.spec"
        if os.path.exists(temp_spec):
            os.remove(temp_spec)
        
        # No Windows, copiar ao invés de link simbólico
        import shutil
        shutil.copy2(buildozer_path, temp_spec)
        
        try:
            # Verificar se a imagem Docker existe
            check_image = subprocess.run(
                ["wsl", "docker", "images", "-q", "android-builder"],
                capture_output=True, text=True
            )
            
            if not check_image.stdout.strip():
                print("🏗️  Construindo imagem Docker Android...")
                build_cmd = [
                    "wsl", "docker", "build",
                    "-t", "android-builder",
                    "-f", ".docker/Dockerfile.android",
                    "."
                ]
                
                build_result = subprocess.run(build_cmd, cwd=os.getcwd())
                if build_result.returncode != 0:
                    print("❌ Erro ao construir imagem Docker")
                    return False
            
            # Build usando Docker
            cmd = [
                "wsl",
                "docker", "run", "--rm",
                "-v", f"{os.getcwd()}:/home/builduser/app",
                "-w", "/home/builduser/app",
                "--platform", "linux/amd64",
                "android-builder",
                "/home/builduser/build_android.sh"
            ]
            
            print(f"🔧 Executando build Docker...")
            
            result = subprocess.run(cmd, cwd=os.getcwd(), text=True)
            
            if result.returncode == 0:
                print("✅ Build Docker concluído com sucesso")
                return True
            else:
                print(f"❌ Erro no build Docker (código: {result.returncode})")
                return False
                
        finally:
            # Remover arquivo temporário
            if os.path.exists(temp_spec):
                os.remove(temp_spec)
                
    except KeyboardInterrupt:
        print("\n🛑 Build cancelado pelo usuário")
        return False
    except Exception as e:
        print(f"❌ Erro no build Docker: {e}")
        return False


def find_apk_path():
    """Encontra o caminho do APK gerado"""
    bin_dir = Path("bin")
    if not bin_dir.exists():
        return None

    # Procura por arquivos APK
    apk_files = list(bin_dir.glob("*.apk"))
    if not apk_files:
        return None

    # Retorna o APK mais recente
    return max(apk_files, key=lambda p: p.stat().st_mtime)


def install_apk_wsl(apk_path):
    """Instala o APK no dispositivo via WSL2"""
    print(f"\n📱 Instalando APK via WSL2: {apk_path}")

    try:
        # Converte caminho Windows para WSL
        wsl_path = str(apk_path).replace("\\", "/").replace("B:", "/mnt/b")

        result = subprocess.run(
            ["wsl", "adb", "install", "-r", wsl_path],
            capture_output=True,
            text=True,
            timeout=60,
        )

        if result.returncode == 0:
            print("✅ APK instalado com sucesso!")
            return True
        else:
            print(f"❌ Erro na instalação: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Timeout na instalação")
        return False
    except Exception as e:
        print(f"❌ Erro ao instalar APK: {e}")
        return False


def launch_app_wsl():
    """Executa o aplicativo no dispositivo via WSL2"""
    package_name = get_package_name()
    package_domain = get_package_domain()
    full_package = f"{package_domain}.{package_name}"

    print(f"\n🚀 Executando aplicativo via WSL2: {full_package}")

    try:
        # Para o app se estiver rodando
        subprocess.run(
            ["wsl", "adb", "shell", "am", "force-stop", full_package],
            capture_output=True,
            timeout=10,
        )

        # Inicia o app
        result = subprocess.run(
            [
                "wsl",
                "adb",
                "shell",
                "am",
                "start",
                "-n",
                f"{full_package}/org.kivy.android.PythonActivity",
            ],
            capture_output=True,
            text=True,
            timeout=15,
        )

        if result.returncode == 0:
            print("✅ Aplicativo iniciado com sucesso!")
            return True
        else:
            print(f"❌ Erro ao iniciar aplicativo: {result.stderr}")
            return False

    except subprocess.TimeoutExpired:
        print("❌ Timeout ao iniciar aplicativo")
        return False
    except Exception as e:
        print(f"❌ Erro ao executar aplicativo: {e}")
        return False


def monitor_logs_wsl():
    """Monitora os logs do aplicativo via WSL2"""
    package_name = get_package_name()
    package_domain = get_package_domain()
    full_package = f"{package_domain}.{package_name}"

    print(f"\n📋 Monitorando logs via WSL2...")
    print("💡 Pressione Ctrl+C para parar o monitoramento")
    print("-" * 50)

    try:
        # Limpa logs antigos
        subprocess.run(["wsl", "adb", "logcat", "-c"], capture_output=True)

        # Monitora logs em tempo real
        process = subprocess.Popen(
            ["wsl", "adb", "logcat", "-s", "python", "SDL", "pygame"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )

        for line in process.stdout:
            print(line.rstrip())

    except KeyboardInterrupt:
        print("\n🛑 Monitoramento de logs interrompido")
        if "process" in locals():
            process.terminate()
    except Exception as e:
        print(f"❌ Erro no monitoramento: {e}")


def main():
    """Função principal"""
    print("🤖 EXECUÇÃO DIRETA ANDROID VIA WSL2/DOCKER")
    print("=" * 50)
    print("Este script irá:")
    print("1. 🔨 Build via Docker no WSL2")
    print("2. 📱 Instalar via ADB no WSL2")
    print("3. 🚀 Executar o jogo")
    print("4. 📋 Monitorar logs")
    print()

    # Verifica WSL2 e Docker
    wsl_ok, wsl_msg = check_wsl_docker()
    if not wsl_ok:
        print(f"❌ {wsl_msg}")
        print("\n📋 REQUISITOS NECESSÁRIOS:")
        print("1. WSL2 instalado e configurado")
        print("2. Docker instalado no WSL2")
        print("3. Dispositivo Android conectado via USB")
        print("4. Depuração USB ativada no dispositivo")
        return False

    print(f"✅ {wsl_msg}")

    # Build do APK via Docker
    if not build_apk_docker():
        return False

    # Encontra o APK
    apk_path = find_apk_path()
    if not apk_path:
        print("❌ APK não encontrado após o build")
        return False

    # Instala o APK via WSL2
    if not install_apk_wsl(apk_path):
        return False

    # Executa o aplicativo via WSL2
    if not launch_app_wsl():
        return False

    # Monitora logs via WSL2
    time.sleep(2)  # Aguarda o app inicializar
    monitor_logs_wsl()

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
