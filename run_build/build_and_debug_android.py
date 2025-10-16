#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para build completo e debug do jogo Android
Faz o build do APK, instala no dispositivo e inicia o debug via ADB
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Configurar codificação UTF-8
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    os.system("chcp 65001 > nul 2>&1")


def run_script(script_path, description):
    """Executa um script Python e retorna o resultado"""
    print(f"\n🔧 {description}...")
    try:
        result = subprocess.run([sys.executable, script_path], 
                              cwd=os.getcwd(), 
                              capture_output=False,
                              text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} concluído com sucesso")
            return True
        else:
            print(f"❌ Erro em {description}")
            return False
    except Exception as e:
        print(f"❌ Erro ao executar {description}: {e}")
        return False


def check_buildozer_spec():
    """Verifica se o buildozer.spec existe"""
    buildozer_path = os.path.join("run_build", "config", "buildozer.spec")
    if not os.path.exists(buildozer_path):
        print("❌ Arquivo buildozer.spec não encontrado!")
        print("💡 O arquivo foi criado automaticamente, mas pode precisar de ajustes")
        return False
    return True


def find_adb():
    """Encontra o executável ADB"""
    try:
        result = subprocess.run(["adb", "version"], capture_output=True, text=True)
        if result.returncode == 0:
            return "adb"
    except FileNotFoundError:
        pass
    
    possible_paths = [
        os.path.expanduser("~/AppData/Local/Android/Sdk/platform-tools/adb.exe"),
        "C:/Android/Sdk/platform-tools/adb.exe",
        os.path.expanduser("~/Android/Sdk/platform-tools/adb"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None


def check_android_device():
    """Verifica se há dispositivo Android conectado"""
    adb_path = find_adb()
    if not adb_path:
        return False, "ADB não encontrado"
    
    try:
        result = subprocess.run([adb_path, "devices"], capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            return False, "Erro ao executar ADB"
        
        devices = []
        lines = result.stdout.strip().split('\n')[1:]
        for line in lines:
            if '\t' in line and 'device' in line:
                devices.append(line.split('\t')[0])
        
        if not devices:
            return False, "Nenhum dispositivo conectado"
        
        return True, f"Dispositivo encontrado: {devices[0]}"
    except Exception as e:
        return False, f"Erro: {e}"


def main():
    """Função principal"""
    print("🚀 === BUILD E DEBUG ANDROID COMPLETO ===")
    
    # Verificar pré-requisitos
    print("\n🔍 Verificando pré-requisitos...")
    
    # Verificar buildozer.spec
    if not check_buildozer_spec():
        print("⚠️  Continuando mesmo assim...")
    
    # Verificar dispositivo Android
    device_ok, device_msg = check_android_device()
    if device_ok:
        print(f"✅ {device_msg}")
    else:
        print(f"⚠️  {device_msg}")
        print("💡 Conecte um dispositivo ou inicie um emulador")
    
    print("\n📋 Processo de build e debug:")
    print("1. Build do APK")
    print("2. Instalação no dispositivo")
    print("3. Início do debug via ADB")
    
    input("\n⏸️  Pressione Enter para continuar ou Ctrl+C para cancelar...")
    
    # Etapa 1: Build do APK
    build_script = os.path.join("run_build", "run_android.py")
    if not run_script(build_script, "Build do APK"):
        print("❌ Falha no build do APK")
        return False
    
    # Aguardar um pouco
    print("\n⏳ Aguardando 3 segundos...")
    time.sleep(3)
    
    # Etapa 2: Verificar se o dispositivo ainda está conectado
    if device_ok:
        device_ok, device_msg = check_android_device()
        if not device_ok:
            print(f"⚠️  {device_msg}")
            print("💡 Reconecte o dispositivo e tente novamente")
            return False
    
    # Etapa 3: Iniciar debug
    debug_script = os.path.join("run_build", "debug_android_adb.py")
    if device_ok:
        print("\n🔧 Iniciando debug via ADB...")
        print("💡 O debug será iniciado em uma nova janela")
        
        # Executar debug em processo separado para não bloquear
        try:
            subprocess.Popen([sys.executable, debug_script], 
                           cwd=os.getcwd(),
                           creationflags=subprocess.CREATE_NEW_CONSOLE if sys.platform == "win32" else 0)
            print("✅ Debug iniciado com sucesso")
        except Exception as e:
            print(f"⚠️  Erro ao iniciar debug: {e}")
            print("💡 Execute manualmente o debug_android_adb.py")
    else:
        print("\n⚠️  Debug via ADB não disponível (dispositivo não conectado)")
        print("💡 Conecte um dispositivo e execute debug_android_adb.py manualmente")
    
    print("\n🎉 Processo concluído!")
    print("\n📱 Para debug manual:")
    print("   - Conecte o dispositivo via USB")
    print("   - Execute: python run_build/debug_android_adb.py")
    
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