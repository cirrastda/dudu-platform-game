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

    def _handle_remove_readonly(self, func, path, exc_info):
        """Callback para remover arquivos somente leitura ou contornar PermissionError."""
        import stat
        try:
            # Tentar alterar permissões e remover novamente
            os.chmod(path, stat.S_IWRITE)
            func(path)
        except Exception:
            # Como último recurso, apenas ignore o erro
            pass

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
                try:
                    shutil.rmtree(dir_path, onerror=self._handle_remove_readonly)
                    print(f"   Removido: {dir_path}")
                except Exception as e:
                    print(f"   Aviso: nao foi possivel remover {dir_path}: {e}")

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

        # Verificar MoviePy
        try:
            import moviepy
            print(f"   MoviePy {getattr(moviepy, '__version__', 'desconhecida')} encontrado")
        except ImportError:
            print("   MoviePy nao encontrado")
            return False

        # Verificar imageio-ffmpeg
        try:
            import imageio_ffmpeg
            print(f"   imageio-ffmpeg {getattr(imageio_ffmpeg, '__version__', 'desconhecida')} encontrado")
        except ImportError:
            print("   imageio-ffmpeg nao encontrado")
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
            "--onedir",  # Pasta (mais estável para diagnosticar)
            "--name",
            executable_name.replace(".exe", ""),  # Nome sem extensão
            "--distpath",
            str(platform_dist_dir),
            "--workpath",
            str(self.build_dir),
            "--specpath",
            str(self.build_dir),
            "--runtime-hook",
            str(self.project_root / "run_build" / "runtime_hook_logging.py"),
            "--debug",
            "all",
        ]

        # Configurações específicas por plataforma
        if target == "windows":
            # Usar apenas console para garantir logs visíveis
            cmd.extend(["--console"])  # Manter console para debug
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
        resource_dirs = ["imagens", "musicas", "sounds", "videos"]
        for resource_dir in resource_dirs:
            resource_path = self.project_root / resource_dir
            if resource_path.exists():
                cmd.extend(["--add-data", f"{resource_path}{os.pathsep}{resource_dir}"])

        # Incluir .env se existir (para configurar ambiente em runtime)
        env_file = self.project_root / ".env"
        if env_file.exists():
            cmd.extend(["--add-data", f"{env_file}{os.pathsep}."])

        # Garantir coleta de dados/submódulos para vídeo (ffmpeg + moviepy + imageio + numpy + pygame)
        # Coleta todo conteúdo do pacote imageio_ffmpeg (inclui binários ffmpeg por plataforma)
        cmd.extend([
            "--collect-all", "imageio_ffmpeg",
            "--collect-submodules", "moviepy",
            "--collect-submodules", "imageio",
            "--collect-submodules", "numpy",
            "--collect-submodules", "pygame",
            # Hidden imports comuns
            "--hidden-import", "moviepy.editor",
            "--hidden-import", "imageio",
            "--hidden-import", "imageio_ffmpeg",
            "--hidden-import", "pygame.freetype",
        ])

        # Adicionar binário do ffmpeg diretamente se disponível localmente
        try:
            import imageio_ffmpeg
            ffmpeg_path = imageio_ffmpeg.get_ffmpeg_exe()
            if os.path.exists(ffmpeg_path):
                # Colocar sob o pacote imageio_ffmpeg para facilitar descoberta em runtime
                cmd.extend(["--add-binary", f"{ffmpeg_path}{os.pathsep}imageio_ffmpeg"])
                print(f"   ffmpeg detectado e incluído: {ffmpeg_path}")
            else:
                print(f"   Aviso: ffmpeg não encontrado em {ffmpeg_path}; confiando em --collect-all imageio_ffmpeg")
        except Exception as e:
            print(f"   Aviso: não foi possível resolver ffmpeg via imageio_ffmpeg ({e}). PyInstaller coletará dados do pacote.")

        # Arquivo principal (usar bootstrap para melhor logging de arranque)
        cmd.append("bootstrap.py")

        try:
            print(f"   Executando: {' '.join(cmd)}")
            subprocess.run(cmd, check=True, cwd=self.project_root)

            # Verificar se o executável foi criado no diretório da plataforma
            base_name = executable_name.replace(".exe", "")
            windows_ext = ".exe" if target == "windows" else ""
            expected_onefile = platform_dist_dir / f"{base_name}{windows_ext}"
            expected_onedir = platform_dist_dir / base_name / f"{base_name}{windows_ext}"

            exe_found = None
            is_onedir = False
            if expected_onefile.exists():
                exe_found = expected_onefile
                is_onedir = False
            elif expected_onedir.exists():
                exe_found = expected_onedir
                is_onedir = True

            if exe_found:
                # Em onedir não mover o executável (depende de DLLs do diretório)
                if is_onedir:
                    exe_to_report = exe_found
                else:
                    final_exe = self.dist_dir / executable_name
                    if exe_found != final_exe:
                        try:
                            if final_exe.exists():
                                final_exe.unlink()
                            exe_found.rename(final_exe)
                            exe_to_report = final_exe
                        except Exception as e:
                            print(f"   Aviso: nao foi possivel mover executavel: {e}")
                            exe_to_report = exe_found
                    else:
                        exe_to_report = final_exe

                print(f"   Executavel criado: {exe_to_report}")
                try:
                    print(f"   Tamanho: {exe_to_report.stat().st_size / (1024*1024):.1f} MB")
                except Exception:
                    pass
                return True
            else:
                print("   Executavel nao encontrado nas seguintes localizacoes:")
                print(f"     - {expected_onefile}")
                print(f"     - {expected_onedir}")
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
            print("\nDependencias nao atendidas. Instalando automaticamente...")
            if not self.install_dependencies():
                print("   Falha ao instalar dependencias.")
                return False
            # Revalidar após instalação
            if not self.check_dependencies():
                print("   Dependencias ainda não atendidas após instalação.")
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
