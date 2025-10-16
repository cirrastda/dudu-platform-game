#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para testar configurações Android
Verifica se o ambiente está configurado corretamente para build e debug
"""

import os
import sys
import subprocess
from pathlib import Path

# Configurar codificação UTF-8
os.environ["PYTHONIOENCODING"] = "utf-8"
if sys.platform == "win32":
    os.system("chcp 65001 > nul 2>&1")


def test_buildozer_spec():
    """Testa se buildozer.spec existe e está válido"""
    print("\n🔍 Testando buildozer.spec...")
    
    buildozer_path = os.path.join("run_build", "config", "buildozer.spec")
    if not os.path.exists(buildozer_path):
        print("❌ buildozer.spec não encontrado")
        return False
    
    try:
        with open(buildozer_path, 'r') as f:
            content = f.read()
            
        # Verificar campos essenciais
        required_fields = ['title', 'package.name', 'package.domain', 'requirements']
        missing_fields = []
        
        for field in required_fields:
            if field not in content:
                missing_fields.append(field)
        
        if missing_fields:
            print(f"❌ Campos obrigatórios ausentes: {', '.join(missing_fields)}")
            return False
        
        print("✅ buildozer.spec válido")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao ler buildozer.spec: {e}")
        return False


def test_adb():
    """Testa se ADB está disponível"""
    print("\n🔍 Testando ADB...")
    
    # Tentar encontrar ADB
    adb_paths = [
        "adb",
        os.path.expanduser("~/AppData/Local/Android/Sdk/platform-tools/adb.exe"),
        "C:/Android/Sdk/platform-tools/adb.exe",
    ]
    
    for adb_path in adb_paths:
        try:
            result = subprocess.run([adb_path, "version"], 
                                  capture_output=True, text=True, timeout=10)
            if result.returncode == 0:
                print(f"✅ ADB encontrado: {adb_path}")
                print(f"   Versão: {result.stdout.strip().split()[4]}")
                return adb_path
        except (FileNotFoundError, subprocess.TimeoutExpired):
            continue
    
    print("❌ ADB não encontrado")
    return None


def test_android_devices(adb_path):
    """Testa dispositivos Android conectados"""
    print("\n🔍 Testando dispositivos Android...")
    
    if not adb_path:
        print("❌ ADB não disponível")
        return False
    
    try:
        result = subprocess.run([adb_path, "devices"], 
                              capture_output=True, text=True, timeout=15)
        
        if result.returncode != 0:
            print(f"❌ Erro ao executar ADB: {result.stderr}")
            return False
        
        devices = []
        lines = result.stdout.strip().split('\n')[1:]  # Pular cabeçalho
        for line in lines:
            if '\t' in line and 'device' in line:
                device_id = line.split('\t')[0]
                devices.append(device_id)
        
        if devices:
            print(f"✅ {len(devices)} dispositivo(s) conectado(s):")
            for device in devices:
                print(f"   - {device}")
            return True
        else:
            print("⚠️  Nenhum dispositivo conectado")
            print("💡 Conecte um dispositivo via USB ou inicie um emulador")
            return False
            
    except Exception as e:
        print(f"❌ Erro ao verificar dispositivos: {e}")
        return False


def test_wsl_docker():
    """Testa WSL2 e Docker"""
    print("\n🔍 Testando WSL2 e Docker...")
    
    # Testar WSL2
    try:
        result = subprocess.run(["wsl", "--list", "--verbose"], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode != 0:
            print("❌ WSL2 não disponível")
            return False
        
        print("✅ WSL2 disponível")
    except Exception as e:
        print(f"❌ Erro ao testar WSL2: {e}")
        return False
    
    # Testar Docker no WSL2
    try:
        result = subprocess.run(["wsl", "docker", "--version"], 
                              capture_output=True, text=True, timeout=15)
        if result.returncode == 0:
            print(f"✅ Docker disponível: {result.stdout.strip()}")
            return True
        else:
            print("❌ Docker não disponível no WSL2")
            return False
    except Exception as e:
        print(f"❌ Erro ao testar Docker: {e}")
        return False


def test_python_dependencies():
    """Testa dependências Python"""
    print("\n🔍 Testando dependências Python...")
    
    required_packages = {
        'pygame': 'pygame',
        'pillow': 'PIL'  # pillow é importado como PIL
    }
    optional_packages = {
        'buildozer': 'buildozer',
        'kivy': 'kivy'
    }
    
    missing_required = []
    missing_optional = []
    
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name} instalado")
        except ImportError:
            missing_required.append(package_name)
            print(f"❌ {package_name} não encontrado")
    
    for package_name, import_name in optional_packages.items():
        try:
            __import__(import_name)
            print(f"✅ {package_name} instalado")
        except ImportError:
            missing_optional.append(package_name)
            print(f"⚠️  {package_name} não encontrado (opcional)")
    
    if missing_required:
        print(f"\n❌ Dependências obrigatórias ausentes: {', '.join(missing_required)}")
        print("💡 Execute: pip install -r requirements.txt")
        return False
    
    if missing_optional:
        print(f"\n⚠️  Dependências opcionais ausentes: {', '.join(missing_optional)}")
        print("💡 Para build Android: pip install buildozer")
    
    return True


def test_launch_configurations():
    """Testa configurações do VS Code"""
    print("\n🔍 Testando configurações do VS Code...")
    
    launch_json = Path(".vscode") / "launch.json"
    if not launch_json.exists():
        print("❌ .vscode/launch.json não encontrado")
        return False
    
    try:
        import json
        with open(launch_json, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # Verificar se as novas configurações Android existem
        android_configs = [
            "📱 Debug Android via ADB",
            "📱 Build e Debug Android Completo"
        ]
        
        existing_configs = [c['name'] for c in config.get('configurations', [])]
        
        for android_config in android_configs:
            if android_config in existing_configs:
                print(f"✅ Configuração encontrada: {android_config}")
            else:
                print(f"❌ Configuração ausente: {android_config}")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ Erro ao verificar launch.json: {e}")
        return False


def main():
    """Função principal"""
    print("🧪 === TESTE DE CONFIGURAÇÃO ANDROID ===")
    print("Verificando se o ambiente está configurado para build e debug Android\n")
    
    tests = [
        ("Buildozer Spec", test_buildozer_spec),
        ("Dependências Python", test_python_dependencies),
        ("Configurações VS Code", test_launch_configurations),
        ("WSL2 e Docker", test_wsl_docker),
    ]
    
    results = {}
    
    # Executar testes básicos
    for test_name, test_func in tests:
        results[test_name] = test_func()
    
    # Testar ADB e dispositivos
    adb_path = test_adb()
    results["ADB"] = adb_path is not None
    
    if adb_path:
        results["Dispositivos Android"] = test_android_devices(adb_path)
    else:
        results["Dispositivos Android"] = False
    
    # Resumo dos resultados
    print("\n" + "="*50)
    print("📊 RESUMO DOS TESTES")
    print("="*50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name:<25} {status}")
        if result:
            passed += 1
    
    print(f"\n📈 Resultado: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Ambiente configurado corretamente!")
        print("💡 Você pode usar as configurações de debug Android")
    else:
        print("\n⚠️  Alguns testes falharam")
        print("💡 Verifique as mensagens acima para corrigir os problemas")
    
    print("\n📱 Para usar o debug Android:")
    print("   1. Conecte um dispositivo Android via USB")
    print("   2. Ative a depuração USB no dispositivo")
    print("   3. Use F5 > '📱 Build e Debug Android Completo'")
    print("   4. Ou use Ctrl+Shift+P > Tasks > 'debug-android-adb'")
    
    return passed == total


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Teste cancelado pelo usuário")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        sys.exit(1)