#!/usr/bin/env python3
"""
Script para criar releases multiplataforma do jogo
Automatiza o processo de build para Windows, Linux e MacOS
"""

import os
import sys
import subprocess
import platform
import shutil
import zipfile
from pathlib import Path
from datetime import datetime

# Importar informações de versão
try:
    from version import VERSION_FULL, GAME_TITLE, GAME_NAME, get_version_info
except ImportError:
    print("⚠️  Arquivo version.py não encontrado.")
    sys.exit(1)


class ReleaseBuilder:
    def __init__(self):
        self.project_root = Path.cwd()
        self.releases_dir = self.project_root / "releases"
        self.current_platform = self.detect_platform()

    def detect_platform(self):
        """Detecta a plataforma atual"""
        system = platform.system().lower()
        if system == "windows":
            return "windows"
        elif system == "darwin":
            return "macos"
        elif system == "linux":
            return "linux"
        else:
            return "unknown"

    def setup_release_directory(self):
        """Configura diretório de releases"""
        self.releases_dir.mkdir(exist_ok=True)
        print(f"Diretorio de releases: {self.releases_dir}")

    def build_for_current_platform(self):
        """Executa build para a plataforma atual"""
        print(f"Executando build para {self.current_platform}...")

        try:
            # Executar o build usando o script correto dentro de run_build
            build_script = str(Path(__file__).parent / "build.py")
            result = subprocess.run(
                [sys.executable, build_script], check=True, capture_output=True, text=True
            )

            print("Build concluido com sucesso!")
            return True

        except subprocess.CalledProcessError as e:
            print(f"Erro no build: {e}")
            print(f"Saída: {e.stdout}")
            print(f"Erro: {e.stderr}")
            return False

    def create_platform_package(self):
        """Cria pacote específico da plataforma"""
        # Procurar na estrutura dist/<platform>/
        platform_dist_dir = self.project_root / "dist" / self.current_platform
        if not platform_dist_dir.exists():
            # Fallback para o diretório dist geral
            dist_dir = self.project_root / "dist"
            if not dist_dir.exists():
                print("❌ Diretório dist não encontrado. Execute o build primeiro.")
                return None
            platform_dist_dir = dist_dir

        print(f"📁 Usando diretório: {platform_dist_dir}")

        # Nome do pacote
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        package_name = (
            f"JogoPlataforma-{VERSION_FULL}-{self.current_platform}-{timestamp}"
        )
        package_dir = self.releases_dir / package_name

        print(f"📦 Criando pacote: {package_name}")

        # Criar diretório do pacote
        package_dir.mkdir(exist_ok=True)

        # Copiar artefatos do build
        # Preferir copiar a pasta onedir do executável principal
        base_name = GAME_NAME.replace(" ", "").replace("-", "")
        if self.current_platform == "windows":
            onedir_name = f"{base_name}-{VERSION_FULL}-win64"
        elif self.current_platform == "linux":
            onedir_name = f"{base_name}-{VERSION_FULL}-linux64"
        elif self.current_platform == "macos":
            onedir_name = f"{base_name}-{VERSION_FULL}-macos"
        else:
            onedir_name = f"{base_name}-{VERSION_FULL}"

        onedir_path = platform_dist_dir / onedir_name

        if onedir_path.exists() and onedir_path.is_dir():
            # Copia a pasta do executável (onedir) com todas as dependências
            shutil.copytree(onedir_path, package_dir / onedir_name, dirs_exist_ok=True)
            print(f"   Copiado diretório do executável: {onedir_name}")
        else:
            # Fallback: copiar todos os arquivos e diretórios gerados para a plataforma
            for item in platform_dist_dir.iterdir():
                if item.is_file():
                    shutil.copy2(item, package_dir)
                    print(f"   Copiado: {item.name}")
                elif item.is_dir():
                    shutil.copytree(item, package_dir / item.name, dirs_exist_ok=True)
                    print(f"   Copiado diretório: {item.name}")

        # Copiar documentação essencial
        docs = ["README.md", "CHANGELOG.md", "LICENSE", "requirements.txt"]
        for doc in docs:
            doc_path = self.project_root / doc
            if doc_path.exists():
                shutil.copy2(doc_path, package_dir)
                print(f"   Copiado: {doc}")

        # Criar arquivo de instruções específico da plataforma
        self.create_platform_instructions(package_dir)

        return package_dir

    def create_platform_instructions(self, package_dir):
        """Cria arquivo de instruções específico da plataforma"""
        instructions_file = package_dir / "COMO_EXECUTAR.txt"

        with open(instructions_file, "w", encoding="utf-8") as f:
            f.write(f"{GAME_TITLE}\n")
            f.write(f"Versão: {VERSION_FULL}\n")
            f.write(f"Plataforma: {self.current_platform.upper()}\n")
            f.write("=" * 50 + "\n\n")

            if self.current_platform == "windows":
                f.write("🎮 COMO EXECUTAR NO WINDOWS:\n")
                f.write("1. Extraia todos os arquivos para uma pasta\n")
                f.write("2. Execute o arquivo .exe\n")
                f.write("3. Divirta-se!\n\n")
                f.write("⚠️  REQUISITOS:\n")
                f.write("- Windows 10 ou superior\n")
                f.write("- Arquitetura x64\n")

            elif self.current_platform == "linux":
                f.write("🎮 COMO EXECUTAR NO LINUX:\n")
                f.write("1. Extraia todos os arquivos para uma pasta\n")
                f.write("2. Abra o terminal na pasta\n")
                f.write("3. Execute: chmod +x JogoPlataforma*\n")
                f.write("4. Execute: ./JogoPlataforma*\n")
                f.write("5. Divirta-se!\n\n")
                f.write("⚠️  REQUISITOS:\n")
                f.write("- Linux com suporte a X11\n")
                f.write("- Arquitetura x64\n")

            elif self.current_platform == "macos":
                f.write("🎮 COMO EXECUTAR NO MACOS:\n")
                f.write("1. Extraia todos os arquivos para uma pasta\n")
                f.write("2. Abra o Terminal na pasta\n")
                f.write("3. Execute: chmod +x JogoPlataforma*\n")
                f.write("4. Execute: ./JogoPlataforma*\n")
                f.write("5. Divirta-se!\n\n")
                f.write("⚠️  REQUISITOS:\n")
                f.write("- macOS 10.14 ou superior\n")
                f.write("- Arquitetura x64 ou ARM64\n")

            f.write("\n" + "=" * 50 + "\n")
            f.write("🐛 PROBLEMAS?\n")
            f.write("- Verifique se todos os arquivos foram extraídos\n")
            f.write("- Verifique as permissões de execução\n")
            f.write("- Consulte o README.md para mais informações\n")

    def create_zip_package(self, package_dir):
        """Cria arquivo ZIP do pacote"""
        zip_name = f"{package_dir.name}.zip"
        zip_path = self.releases_dir / zip_name

        print(f"🗜️  Criando arquivo ZIP: {zip_name}")

        with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            for file_path in package_dir.rglob("*"):
                if file_path.is_file():
                    arcname = file_path.relative_to(package_dir)
                    zipf.write(file_path, arcname)

        print(f"   ✅ ZIP criado: {zip_path}")
        print(f"   📁 Tamanho: {zip_path.stat().st_size / (1024*1024):.1f} MB")

        return zip_path

    def cleanup_temp_files(self):
        """Remove arquivos temporários"""
        temp_dirs = ["build", "__pycache__"]

        for temp_dir in temp_dirs:
            temp_path = self.project_root / temp_dir
            if temp_path.exists():
                shutil.rmtree(temp_path)
                print(f"🧹 Removido: {temp_path}")

    def build_release(self):
        """Processo completo de build de release"""
        print(f"Iniciando build de release para {self.current_platform.upper()}")
        print(f"Versao: {VERSION_FULL}")
        print(f"Jogo: {GAME_TITLE}")
        print()

        # Configurar diretório
        self.setup_release_directory()

        # Executar build
        if not self.build_for_current_platform():
            print("Falha no build. Abortando release.")
            return False

        # Criar pacote
        package_dir = self.create_platform_package()
        if not package_dir:
            print("❌ Falha ao criar pacote.")
            return False

        # Criar ZIP
        zip_path = self.create_zip_package(package_dir)

        # Limpeza
        self.cleanup_temp_files()

        print(f"\n🎉 Release criado com sucesso!")
        print(f"📦 Pacote: {package_dir}")
        print(f"🗜️  ZIP: {zip_path}")
        print(f"\n📋 Resumo:")
        print(f"   Versão: {VERSION_FULL}")
        print(f"   Plataforma: {self.current_platform}")
        print(f"   Arquivos: {len(list(package_dir.iterdir()))}")

        return True


def main():
    """Função principal"""
    if len(sys.argv) > 1 and sys.argv[1] == "--help":
        print(
            f"""🎮 {GAME_TITLE} - Release Builder

Cria pacotes de release prontos para distribuição.

Uso: python build_release.py

O script irá:
1. Executar o build para a plataforma atual
2. Criar pacote com executável e documentação
3. Gerar arquivo ZIP para distribuição
4. Limpar arquivos temporários

Arquivos gerados em: ./releases/
"""
        )
        return

    builder = ReleaseBuilder()
    success = builder.build_release()

    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
