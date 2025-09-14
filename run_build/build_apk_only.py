#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PLATFORM GAME - BUILD APK ONLY
Gera apenas o APK sem tentar instalar no emulador
"""

import os
import sys
import shutil
import subprocess
import zipfile
from pathlib import Path

def find_android_sdk():
    """Encontra o Android SDK"""
    possible_paths = [
        os.path.expanduser("~/Android/Sdk"),
        os.path.expanduser("~/AppData/Local/Android/Sdk"),
        "C:/Android/Sdk",
        "C:/Users/" + os.getenv('USERNAME', '') + "/AppData/Local/Android/Sdk"
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    # Tenta encontrar via variáveis de ambiente
    android_home = os.getenv('ANDROID_HOME')
    if android_home and os.path.exists(android_home):
        return android_home
    
    android_sdk_root = os.getenv('ANDROID_SDK_ROOT')
    if android_sdk_root and os.path.exists(android_sdk_root):
        return android_sdk_root
    
    return None

def setup_android_tools():
    """Configura as ferramentas Android no PATH"""
    sdk_path = find_android_sdk()
    if not sdk_path:
        print("❌ Android SDK não encontrado!")
        return False
    
    print(f"✅ Android SDK encontrado: {sdk_path}")
    
    # Adiciona ferramentas ao PATH
    tools_paths = [
        os.path.join(sdk_path, "platform-tools"),
        os.path.join(sdk_path, "build-tools"),
        os.path.join(sdk_path, "tools"),
        os.path.join(sdk_path, "tools", "bin")
    ]
    
    # Encontra a versão mais recente do build-tools
    build_tools_dir = os.path.join(sdk_path, "build-tools")
    if os.path.exists(build_tools_dir):
        versions = [d for d in os.listdir(build_tools_dir) if os.path.isdir(os.path.join(build_tools_dir, d))]
        if versions:
            latest_version = sorted(versions)[-1]
            tools_paths.append(os.path.join(build_tools_dir, latest_version))
    
    for tool_path in tools_paths:
        if os.path.exists(tool_path) and tool_path not in os.environ.get('PATH', ''):
            os.environ['PATH'] = tool_path + os.pathsep + os.environ.get('PATH', '')
    
    print("✅ PATH atualizado com ferramentas Android")
    return True

def create_apk_structure():
    """Cria a estrutura básica do APK"""
    apk_dir = "apk_build"
    
    # Remove diretório existente
    if os.path.exists(apk_dir):
        shutil.rmtree(apk_dir)
    
    # Cria estrutura
    os.makedirs(apk_dir, exist_ok=True)
    os.makedirs(os.path.join(apk_dir, "assets"), exist_ok=True)
    os.makedirs(os.path.join(apk_dir, "res"), exist_ok=True)
    
    # Copia arquivos do jogo
    game_files = [
        "main_android.py",
        "version.py"
    ]
    
    for file in game_files:
        if os.path.exists(file):
            shutil.copy2(file, os.path.join(apk_dir, "assets"))
    
    # Copia recursos
    if os.path.exists("imagens"):
        shutil.copytree("imagens", os.path.join(apk_dir, "assets", "imagens"), dirs_exist_ok=True)
    
    if os.path.exists("sounds"):
        shutil.copytree("sounds", os.path.join(apk_dir, "assets", "sounds"), dirs_exist_ok=True)
    
    if os.path.exists("musicas"):
        shutil.copytree("musicas", os.path.join(apk_dir, "assets", "musicas"), dirs_exist_ok=True)
    
    # Cria AndroidManifest.xml
    manifest_content = '''<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    package="com.cirrastec.platformgame"
    android:versionCode="1"
    android:versionName="1.0">
    
    <uses-sdk android:minSdkVersion="21" android:targetSdkVersion="33" />
    
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE" />
    <uses-permission android:name="android.permission.INTERNET" />
    
    <application
        android:label="Platform Game"
        android:theme="@android:style/Theme.NoTitleBar.Fullscreen"
        android:hardwareAccelerated="true">
        
        <activity
            android:name="org.kivy.android.PythonActivity"
            android:label="Platform Game"
            android:screenOrientation="landscape"
            android:configChanges="keyboardHidden|orientation|screenSize">
            
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>
    </application>
</manifest>'''
    
    with open(os.path.join(apk_dir, "AndroidManifest.xml"), "w", encoding="utf-8") as f:
        f.write(manifest_content)
    
    return apk_dir

def package_apk(apk_dir):
    """Empacota o APK usando ferramentas Android"""
    print("📱 Empacotando APK...")
    
    try:
        # Cria APK não assinado
        # Cria diretório de saída se não existir
        dist_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dist", "android")
        os.makedirs(dist_dir, exist_ok=True)
        apk_path = os.path.join(dist_dir, "platform_game_unsigned.apk")
        
        # Usa aapt para criar APK
        sdk_path = find_android_sdk()
        build_tools_dir = os.path.join(sdk_path, "build-tools")
        versions = [d for d in os.listdir(build_tools_dir) if os.path.isdir(os.path.join(build_tools_dir, d))]
        latest_version = sorted(versions)[-1]
        aapt_path = os.path.join(build_tools_dir, latest_version, "aapt.exe")
        
        if not os.path.exists(aapt_path):
            print(f"❌ aapt não encontrado: {aapt_path}")
            return None
        
        # Encontra a plataforma Android disponível
        platforms_dir = os.path.join(sdk_path, "platforms")
        platforms = [d for d in os.listdir(platforms_dir) if os.path.isdir(os.path.join(platforms_dir, d))]
        latest_platform = sorted(platforms)[-1]
        android_jar = os.path.join(platforms_dir, latest_platform, "android.jar")
        
        if not os.path.exists(android_jar):
            print(f"❌ android.jar não encontrado: {android_jar}")
            return None
        
        print(f"📱 Usando plataforma: {latest_platform}")
        
        # Comando aapt para criar APK
        cmd = [
            aapt_path, "package", "-f", "-M", os.path.join(apk_dir, "AndroidManifest.xml"),
            "-S", os.path.join(apk_dir, "res"),
            "-A", os.path.join(apk_dir, "assets"),
            "-I", android_jar,
            "-F", apk_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ APK criado: {apk_path}")
            return apk_path
        else:
            print(f"❌ Erro no aapt: {result.stderr}")
            return None
            
    except Exception as e:
        print(f"❌ Erro: {e}")
        return None

def build_apk():
    """Constrói o APK"""
    print("📦 Criando APK...")
    
    apk_dir = create_apk_structure()
    print("✅ Estrutura APK criada")
    
    # Empacota o APK usando aapt
    apk_name = package_apk(apk_dir)
    if not apk_name:
        return None
    
    # Tenta assinar o APK se possível
    try:
        sign_apk(apk_name)
    except Exception as e:
        print(f"⚠️ Não foi possível assinar o APK: {e}")
        print("⚠️ Usando APK não assinado (mais compatível)...")
    
    return apk_name

def sign_apk(apk_name):
    """Tenta assinar o APK"""
    print("🔐 Tentando assinar APK...")
    
    # Procura por keytool e jarsigner
    try:
        # Cria keystore se não existir
        keystore_name = "platform_game.keystore"
        if not os.path.exists(keystore_name):
            subprocess.run([
                "keytool", "-genkey", "-v", "-keystore", keystore_name,
                "-alias", "platformgame", "-keyalg", "RSA", "-keysize", "2048",
                "-validity", "10000", "-storepass", "platformgame",
                "-keypass", "platformgame", "-dname", "CN=Platform Game"
            ], check=True, capture_output=True)
        
        # Assina o APK
        subprocess.run([
            "jarsigner", "-verbose", "-sigalg", "SHA1withRSA",
            "-digestalg", "SHA1", "-keystore", keystore_name,
            "-storepass", "platformgame", "-keypass", "platformgame",
            apk_name, "platformgame"
        ], check=True, capture_output=True)
        
        print("✅ APK assinado com sucesso")
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("🔐 Pulando assinatura (usando APK não assinado)...")
        raise

def main():
    """Função principal"""
    print("🎮 PLATFORM GAME - BUILD APK ONLY")
    print("====================================")
    
    # Configura ferramentas Android
    if not setup_android_tools():
        sys.exit(1)
    
    # Constrói o APK
    try:
        apk_name = build_apk()
        
        print("\n🎮 Build APK concluído!")
        print(f"📱 APK gerado: {apk_name}")
        print("\n📋 Para instalar manualmente:")
        print(f"   adb install {apk_name}")
        print("\n📋 Para executar:")
        print("   adb shell am start -n com.cirrastec.platformgame/.PythonActivity")
        
    except Exception as e:
        print(f"❌ Erro durante o build: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()