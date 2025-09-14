#!/usr/bin/env python3
"""
Script para build release do Android

Este script automatiza o processo de build release:
1. Verifica configurações de release
2. Executa build release com Buildozer
3. Assina o APK (se configurado)
4. Cria pacote distribuível
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path
from datetime import datetime


def check_buildozer():
    """Verifica se o Buildozer está instalado"""
    try:
        result = subprocess.run(
            ["buildozer", "--version"], capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ):
        return False


def install_buildozer():
    """Instala o Buildozer"""
    print("📦 Instalando Buildozer...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "buildozer"], check=True
        )
        print("✅ Buildozer instalado com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar Buildozer: {e}")
        return False


def check_release_config():
    """Verifica configurações de release no buildozer.spec"""
    print("🔍 Verificando configurações de release...")

    spec_file = Path("run_build") / "config" / "buildozer.spec"
    if not spec_file.exists():
        print("❌ Arquivo buildozer.spec não encontrado")
        return False

    try:
        with open(spec_file, "r", encoding="utf-8") as f:
            content = f.read()

        # Verifica configurações importantes
        checks = {
            "package.name": "Nome do pacote",
            "package.domain": "Domínio do pacote",
            "title": "Título do aplicativo",
            "version": "Versão",
            "android.permissions": "Permissões Android",
        }

        missing = []
        for key, desc in checks.items():
            if f"{key} =" not in content:
                missing.append(f"{desc} ({key})")

        if missing:
            print("⚠️  Configurações ausentes ou incompletas:")
            for item in missing:
                print(f"   - {item}")
        else:
            print("✅ Configurações básicas encontradas")

        # Verifica configurações de release específicas
        release_checks = {
            "android.release_artifact": "Tipo de artefato de release",
            "android.debug": "Modo debug (deve ser 0 para release)",
        }

        for key, desc in release_checks.items():
            if f"{key} =" in content:
                print(f"✅ {desc} configurado")
            else:
                print(f"💡 {desc} não configurado (usando padrão)")

        return True

    except Exception as e:
        print(f"❌ Erro ao verificar configurações: {e}")
        return False


def setup_android_environment():
    """Configura o ambiente Android"""
    print("🤖 Configurando ambiente Android...")

    # Verifica Buildozer
    if not check_buildozer():
        print("Buildozer não encontrado. Instalando...")
        if not install_buildozer():
            return False

    print("✅ Buildozer disponível")

    # Verifica configurações
    if not check_release_config():
        return False

    return True


def clean_build_cache():
    """Limpa cache de build anterior"""
    print("🧹 Limpando cache de build...")

    dirs_to_clean = [".buildozer", "bin"]

    for dir_name in dirs_to_clean:
        dir_path = Path(dir_name)
        if dir_path.exists():
            try:
                shutil.rmtree(dir_path)
                print(f"✅ Removido: {dir_name}")
            except Exception as e:
                print(f"⚠️  Erro ao remover {dir_name}: {e}")
        else:
            print(f"💡 {dir_name} não existe (ok)")

    print("✅ Limpeza concluída")


def build_android_release():
    """Executa o build release do Android"""
    print("\n🔨 Iniciando build release do Android...")
    print("⏳ Este processo pode demorar 10-30 minutos...")
    print("💡 Primeira execução demora mais (download de dependências)")

    try:
        # Executa o build release com verbose
        process = subprocess.Popen(
            ["buildozer", "-v", "android", "release"],
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
            print("\n✅ Build release concluído com sucesso!")

            # Mover APKs para dist/android/
            bin_dir = Path("bin")
            android_dist_dir = Path("dist") / "android"
            android_dist_dir.mkdir(parents=True, exist_ok=True)

            apk_files = list(bin_dir.glob("*.apk"))
            if apk_files:
                for apk_file in apk_files:
                    dest_path = android_dist_dir / apk_file.name
                    shutil.copy2(apk_file, dest_path)
                    print(f"📱 APK copiado para: {dest_path}")

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


def find_release_apk():
    """Encontra o APK de release gerado"""
    bin_dir = Path("bin")
    if not bin_dir.exists():
        return None

    # Procura por arquivos APK de release
    apk_files = list(bin_dir.glob("*-release*.apk"))
    if not apk_files:
        # Fallback para qualquer APK
        apk_files = list(bin_dir.glob("*.apk"))

    if not apk_files:
        return None

    # Retorna o APK mais recente
    return max(apk_files, key=lambda p: p.stat().st_mtime)


def create_release_package():
    """Cria pacote de release"""
    print("\n📦 Criando pacote de release...")

    # Encontra o APK
    apk_path = find_release_apk()
    if not apk_path:
        print("❌ APK de release não encontrado")
        return False

    print(f"📱 APK encontrado: {apk_path}")

    # Cria diretório de releases
    releases_dir = Path("releases")
    releases_dir.mkdir(exist_ok=True)

    # Nome do pacote com timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    package_name = f"jumpandhit_android_release_{timestamp}"
    package_dir = releases_dir / package_name
    package_dir.mkdir(exist_ok=True)

    try:
        # Copia o APK
        release_apk = package_dir / f"jumpandhit_release_{timestamp}.apk"
        shutil.copy2(apk_path, release_apk)

        # Cria README
        readme = package_dir / "README.txt"
        with open(readme, "w", encoding="utf-8") as f:
            f.write("Jump and Hit - Android Release\n")
            f.write("==============================\n\n")
            f.write("Instalação:\n")
            f.write("1. Ative 'Fontes desconhecidas' no Android\n")
            f.write("2. Transfira o APK para o dispositivo\n")
            f.write("3. Toque no APK para instalar\n\n")
            f.write("Via ADB:\n")
            f.write(f"adb install -r {release_apk.name}\n\n")
            f.write("Requisitos:\n")
            f.write("- Android 5.0+ (API 21+)\n")
            f.write("- 100MB de espaço livre\n")
            f.write("- Acelerômetro (opcional)\n\n")
            f.write(
                f"Build criado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
            )

        # Cria informações técnicas
        info_file = package_dir / "build_info.txt"
        with open(info_file, "w", encoding="utf-8") as f:
            f.write("Informações do Build\n")
            f.write("===================\n\n")
            f.write(f"APK Original: {apk_path}\n")
            f.write(f"Tamanho: {apk_path.stat().st_size / 1024 / 1024:.2f} MB\n")
            f.write(f"Data do Build: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Plataforma: {platform.system()} {platform.release()}\n")

        # Cria arquivo ZIP
        zip_path = releases_dir / f"{package_name}.zip"
        shutil.make_archive(str(zip_path.with_suffix("")), "zip", package_dir)

        print(f"✅ Pacote de release criado: {zip_path}")
        print(f"📁 Pasta: {package_dir}")
        print(f"📱 APK: {release_apk}")

        return True

    except Exception as e:
        print(f"❌ Erro ao criar pacote: {e}")
        return False


def show_release_info():
    """Mostra informações sobre o processo de release"""
    print("\n📋 INFORMAÇÕES SOBRE RELEASE ANDROID:")
    print("\n🔨 Processo de Build:")
    print("- Build release otimizado para produção")
    print("- APK menor e mais rápido que debug")
    print("- Sem símbolos de debug")
    print("- Pronto para distribuição")

    print("\n📱 Distribuição:")
    print("- Google Play Store (requer assinatura)")
    print("- Instalação direta (APK)")
    print("- Lojas alternativas")

    print("\n🔐 Assinatura:")
    print("- Para Play Store: configure keystore no buildozer.spec")
    print("- Para distribuição direta: APK atual funciona")

    print("\n⚠️  IMPORTANTE:")
    print("- Teste sempre antes de distribuir")
    print("- Verifique permissões necessárias")
    print("- Considere diferentes tamanhos de tela")


def main():
    """Função principal"""
    print("📱 BUILD RELEASE ANDROID")
    print("=" * 30)
    print("Este script irá:")
    print("1. 🔍 Verificar configurações")
    print("2. 🧹 Limpar cache anterior")
    print("3. 🔨 Fazer build release")
    print("4. 📦 Criar pacote distribuível")
    print()

    # Pergunta se deve limpar cache
    try:
        response = input("🧹 Limpar cache de build anterior? (s/N): ").strip().lower()
        if response in ["s", "sim", "y", "yes"]:
            clean_build_cache()
    except KeyboardInterrupt:
        print("\n🛑 Operação cancelada")
        return False

    # Configura ambiente
    if not setup_android_environment():
        print("❌ Falha na configuração do ambiente")
        show_release_info()
        return False

    # Executa build
    if not build_android_release():
        print("❌ Falha no build release")
        return False

    # Cria pacote
    if not create_release_package():
        print("❌ Falha na criação do pacote")
        return False

    print("\n🎉 Build release Android concluído com sucesso!")
    print("📁 Verifique a pasta 'releases' para os arquivos gerados")

    show_release_info()

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
