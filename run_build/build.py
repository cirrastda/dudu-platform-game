#!/usr/bin/env python3
"""
Script para criar executável do jogo de plataforma
Suporte para Windows, Linux e MacOS
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# Importar informações de versão
try:
    from version import (
        VERSION_FULL,
        GAME_NAME,
        GAME_TITLE,
        BUILD_PLATFORMS,
        get_version_info,
    )
except ImportError:
    print("⚠️  Arquivo version.py não encontrado. Usando valores padrão.")
    VERSION_FULL = "0.0.1-alpha.1"
    GAME_NAME = "Jogo de Plataforma"
    GAME_TITLE = "🎮 Jogo de Plataforma - Vista do Mar"
    BUILD_PLATFORMS = ["windows", "linux", "macos"]


class GameBuilder:
    def __init__(self):
        self.current_platform = self.detect_platform()
        self.project_root = Path.cwd()
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"

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

    def clean_build_dirs(self):
        """Limpa diretórios de build anteriores"""
        print("Limpando diretorios de build...")
        for dir_path in [self.dist_dir, self.build_dir]:
            if dir_path.exists():
                shutil.rmtree(dir_path)
                print(f"   Removido: {dir_path}")

    def check_dependencies(self):
        """Verifica se as dependências estão instaladas"""
        print("Verificando dependencias...")

        # Verificar PyInstaller
        try:
            import PyInstaller

            print(f"   PyInstaller {PyInstaller.__version__} encontrado")
        except ImportError:
            print("   PyInstaller nao encontrado")
            return False

        # Verificar Pygame
        try:
            import pygame

            print(f"   Pygame {pygame.version.ver} encontrado")
        except ImportError:
            print("   Pygame nao encontrado")
            return False

        # Verificar arquivo principal
        if not (self.project_root / "main.py").exists():
            print("   main.py nao encontrado")
            return False

        print("   Todas as dependencias verificadas")
        return True

    def install_dependencies(self):
        """Instala dependências do requirements.txt"""
        print("Instalando dependencias...")
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "-r", "requirements.txt"],
                check=True,
            )
            print("   Dependencias instaladas com sucesso!")
            return True
        except subprocess.CalledProcessError as e:
            print(f"   Erro ao instalar dependencias: {e}")
            return False
        except FileNotFoundError:
            print("   requirements.txt nao encontrado")
            return False

    def get_executable_name(self, platform_target=None):
        """Gera nome do executável baseado na plataforma"""
        target = platform_target or self.current_platform
        base_name = GAME_NAME.replace(" ", "").replace("-", "")

        if target == "windows":
            return f"{base_name}-{VERSION_FULL}-win64.exe"
        elif target == "macos":
            return f"{base_name}-{VERSION_FULL}-macos"
        elif target == "linux":
            return f"{base_name}-{VERSION_FULL}-linux64"
        else:
            return f"{base_name}-{VERSION_FULL}"

    def build_for_platform(self, target_platform=None):
        """Constrói executável para plataforma específica"""
        target = target_platform or self.current_platform
        executable_name = self.get_executable_name(target)

        print(f"Construindo para {target.upper()}...")
        print(f"   Executável: {executable_name}")

        # Criar diretório de saída específico da plataforma
        platform_dist_dir = Path("dist") / target
        platform_dist_dir.mkdir(parents=True, exist_ok=True)

        # Configurar argumentos do PyInstaller
        cmd = [
            "pyinstaller",
            "--onefile",  # Arquivo único
            "--name",
            executable_name.replace(".exe", ""),  # Nome sem extensão
            "--distpath",
            str(platform_dist_dir),
            "--workpath",
            str(self.build_dir),
            "--specpath",
            str(self.build_dir),
        ]

        # Configurações específicas por plataforma
        if target == "windows":
            cmd.extend(["--windowed", "--console"])  # Manter console para debug
        elif target == "macos":
            cmd.extend(["--windowed"])
        elif target == "linux":
            cmd.extend(["--console"])

        # Adicionar ícone se existir
        icon_files = ["icon.ico", "icon.png", "icon.icns"]
        for icon_file in icon_files:
            if (self.project_root / icon_file).exists():
                cmd.extend(["--icon", icon_file])
                break

        # Incluir recursos necessários (usando caminhos absolutos)
        resource_dirs = ["imagens", "musicas", "sounds"]
        for resource_dir in resource_dirs:
            resource_path = self.project_root / resource_dir
            if resource_path.exists():
                cmd.extend(["--add-data", f"{resource_path}{os.pathsep}{resource_dir}"])

        # Arquivo principal
        cmd.append("main.py")

        try:
            print(f"   Executando: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, cwd=self.project_root)

            # Verificar se o executável foi criado
            expected_exe = self.dist_dir / executable_name.replace(".exe", "")
            if target == "windows":
                expected_exe = (
                    self.dist_dir / f"{executable_name.replace('.exe', '')}.exe"
                )

            if expected_exe.exists():
                # Renomear para o nome correto se necessário
                final_exe = self.dist_dir / executable_name
                if expected_exe != final_exe:
                    expected_exe.rename(final_exe)

                print(f"   Executavel criado: {final_exe}")
                print(f"   Tamanho: {final_exe.stat().st_size / (1024*1024):.1f} MB")
                return True
            else:
                print(f"   Executavel nao encontrado em {expected_exe}")
                return False

        except subprocess.CalledProcessError as e:
            print(f"   Erro ao criar executavel: {e}")
            return False
        except FileNotFoundError:
            print("   PyInstaller nao encontrado. Instale com: pip install pyinstaller")
            return False

    def create_release_package(self):
        """Cria pacote de release com documentação"""
        print("Criando pacote de release...")

        release_dir = self.dist_dir / f"release-{VERSION_FULL}"
        release_dir.mkdir(exist_ok=True)

        # Copiar executáveis
        for exe_file in self.dist_dir.glob("*"):
            if exe_file.is_file() and exe_file.name != release_dir.name:
                shutil.copy2(exe_file, release_dir)

        # Copiar documentação
        docs = ["README.md", "CHANGELOG.md", "LICENSE"]
        for doc in docs:
            doc_path = self.project_root / doc
            if doc_path.exists():
                shutil.copy2(doc_path, release_dir)

        # Criar arquivo de informações da versão
        version_info = release_dir / "VERSION.txt"
        with open(version_info, "w", encoding="utf-8") as f:
            f.write(f"{GAME_TITLE}\n")
            f.write(f"Versão: {VERSION_FULL}\n")
            f.write(f"Plataforma de build: {self.current_platform}\n")
            f.write(
                f"Data de build: {subprocess.check_output(['date'], shell=True, text=True).strip()}\n"
            )

        print(f"   Pacote criado em: {release_dir}")
        return release_dir

    def build_all(self):
        """Constrói para todas as plataformas suportadas"""
        print(f"Iniciando build do {GAME_TITLE}")
        print(f"   Versão: {VERSION_FULL}")
        print(f"   Plataforma atual: {self.current_platform}")
        print()

        if not self.check_dependencies():
            print(
                "\nDependencias nao atendidas. Execute 'python build.py --install-deps' primeiro."
            )
            return False

        self.clean_build_dirs()

        # Build para plataforma atual
        success = self.build_for_platform()

        if success:
            self.create_release_package()
            print(f"\nBuild concluído com sucesso!")
            print(f"Arquivos em: {self.dist_dir}")
            print("\nPara executar o jogo:")

            if self.current_platform == "windows":
                print(f"   {self.dist_dir}\\{self.get_executable_name()}")
            else:
                print(f"   ./{self.dist_dir}/{self.get_executable_name()}")

            return True
        else:
            print("\nBuild falhou!")
            return False


def main():
    """Função principal"""
    builder = GameBuilder()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--install-deps":
            builder.install_dependencies()
        elif sys.argv[1] == "--clean":
            builder.clean_build_dirs()
        elif sys.argv[1] == "--check":
            builder.check_dependencies()
        elif sys.argv[1] == "--mobile":
            print("\n=== BUILD MÓVEL ===")
            print("Iniciando build móvel...")
            try:
                import subprocess

                subprocess.run([sys.executable, "build_mobile.py"], check=True)
            except subprocess.CalledProcessError as e:
                print(f"Erro ao executar build móvel: {e}")
            except FileNotFoundError:
                print("Arquivo build_mobile.py não encontrado!")
        elif sys.argv[1] == "--help":
            print(
                f"""{GAME_TITLE} - Build System

Uso: python build.py [opção]

Opções:
  --install-deps    Instala dependências do requirements.txt
  --clean          Limpa diretórios de build
  --check          Verifica dependências
  --mobile         Executa build para Android/iOS (requer build_mobile.py)
  --help           Mostra esta ajuda
  
Sem argumentos: Executa build completo para desktop
"""
            )
        else:
            print(f"Opção desconhecida: {sys.argv[1]}")
            print("Use --help para ver opções disponíveis")
    else:
        builder.build_all()


if __name__ == "__main__":
    main()
