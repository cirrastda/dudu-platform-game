#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para debug do jogo Android via ADB
Conecta ao dispositivo Android e monitora logs em tempo real
"""

import os
import sys
import subprocess
import time
import threading
from pathlib import Path

# Configurar codificação UTF-8
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    os.system("chcp 65001 > nul 2>&1")


def find_adb():
    """Encontra o executável ADB"""
    # Tentar encontrar ADB no PATH
    try:
        result = subprocess.run(["adb", "version"], capture_output=True, text=True)
        if result.returncode == 0:
            return "adb"
    except FileNotFoundError:
        pass
    
    # Tentar encontrar no Android SDK
    possible_paths = [
        os.path.expanduser("~/AppData/Local/Android/Sdk/platform-tools/adb.exe"),
        "C:/Android/Sdk/platform-tools/adb.exe",
        os.path.expanduser("~/Android/Sdk/platform-tools/adb"),
        "/usr/bin/adb",
        "/usr/local/bin/adb"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # Verificar variáveis de ambiente
    android_home = os.getenv('ANDROID_HOME')
    if android_home:
        adb_path = os.path.join(android_home, "platform-tools", "adb.exe" if sys.platform == "win32" else "adb")
        if os.path.exists(adb_path):
            return adb_path
    
    return None


def check_devices(adb_path):
    """Verifica dispositivos conectados"""
    try:
        result = subprocess.run([adb_path, "devices"], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return []
        
        devices = []
        lines = result.stdout.strip().split('\n')[1:]  # Pular cabeçalho
        for line in lines:
            if '\t' in line and 'device' in line:
                device_id = line.split('\t')[0]
                devices.append(device_id)
        
        return devices
    except Exception as e:
        print(f"❌ Erro ao verificar dispositivos: {e}")
        return []


def get_package_name():
    """Obtém o nome do pacote do buildozer.spec"""
    buildozer_path = os.path.join("run_build", "config", "buildozer.spec")
    if os.path.exists(buildozer_path):
        with open(buildozer_path, 'r') as f:
            for line in f:
                if line.startswith('package.domain'):
                    domain = line.split('=')[1].strip()
                elif line.startswith('package.name'):
                    name = line.split('=')[1].strip()
                    return f"{domain}.{name}" if 'domain' in locals() else name
    return "com.cirrastec.platformgame.platformgame"


def start_app(adb_path, device_id, package_name):
    """Inicia o aplicativo no dispositivo"""
    try:
        print(f"🚀 Iniciando aplicativo {package_name}...")
        result = subprocess.run([
            adb_path, "-s", device_id, 
            "shell", "monkey", "-p", package_name, "-c", "android.intent.category.LAUNCHER", "1"
        ], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            print("✅ Aplicativo iniciado com sucesso")
            return True
        else:
            print(f"❌ Erro ao iniciar aplicativo: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Erro ao iniciar aplicativo: {e}")
        return False


def monitor_logs(adb_path, device_id, package_name):
    """Monitora logs do aplicativo em tempo real"""
    try:
        print(f"📱 Monitorando logs para {package_name}...")
        print("💡 Pressione Ctrl+C para parar o monitoramento\n")
        
        # Limpar logs anteriores
        subprocess.run([adb_path, "-s", device_id, "logcat", "-c"], 
                      capture_output=True, timeout=5)
        
        # Iniciar monitoramento
        process = subprocess.Popen([
            adb_path, "-s", device_id, "logcat", 
            "-s", "python:*", "PythonActivity:*", "SDL:*", "Kivy:*"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
           text=True, bufsize=1, universal_newlines=True)
        
        for line in process.stdout:
            if line.strip():
                print(f"📱 {line.strip()}")
        
    except KeyboardInterrupt:
        print("\n🛑 Monitoramento interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro no monitoramento: {e}")


def check_app_installed(adb_path, device_id, package_name):
    """Verifica se o aplicativo está instalado"""
    try:
        result = subprocess.run([
            adb_path, "-s", device_id, 
            "shell", "pm", "list", "packages", package_name
        ], capture_output=True, text=True, timeout=10)
        
        return package_name in result.stdout
    except Exception:
        return False


def main():
    """Função principal"""
    print("🔧 === DEBUG ANDROID VIA ADB ===")
    
    # Encontrar ADB
    adb_path = find_adb()
    if not adb_path:
        print("❌ ADB não encontrado!")
        print("💡 Instale o Android SDK ou adicione ADB ao PATH")
        return False
    
    print(f"✅ ADB encontrado: {adb_path}")
    
    # Verificar dispositivos
    devices = check_devices(adb_path)
    if not devices:
        print("❌ Nenhum dispositivo Android conectado!")
        print("💡 Conecte um dispositivo via USB ou inicie um emulador")
        return False
    
    device_id = devices[0]
    print(f"✅ Dispositivo encontrado: {device_id}")
    
    # Obter nome do pacote
    package_name = get_package_name()
    print(f"📦 Pacote: {package_name}")
    
    # Verificar se app está instalado
    if not check_app_installed(adb_path, device_id, package_name):
        print("❌ Aplicativo não está instalado no dispositivo!")
        print("💡 Execute primeiro o build e instalação do APK")
        return False
    
    print("✅ Aplicativo encontrado no dispositivo")
    
    # Iniciar aplicativo
    if start_app(adb_path, device_id, package_name):
        # Aguardar um pouco para o app inicializar
        time.sleep(2)
        
        # Monitorar logs
        monitor_logs(adb_path, device_id, package_name)
    
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