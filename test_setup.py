#!/usr/bin/env python3
"""
Script de teste para verificar configurações de desenvolvimento

Este script testa se todas as configurações estão funcionando corretamente
para desenvolvimento multiplataforma.
"""

import os
import sys
import subprocess
import platform
import json
from pathlib import Path


def test_python_environment():
    """Testa o ambiente Python"""
    print("🐍 Testando ambiente Python...")

    # Versão do Python
    python_version = sys.version_info
    if python_version >= (3, 8):
        print(
            f"✅ Python {python_version.major}.{python_version.minor}.{python_version.micro}"
        )
    else:
        print(
            f"❌ Python {python_version.major}.{python_version.minor}.{python_version.micro} (requer 3.8+)"
        )
        return False

    # Pygame
    try:
        import pygame

        print(f"✅ Pygame {pygame.version.ver}")
    except ImportError:
        print("❌ Pygame não instalado")
        return False

    return True


def test_vscode_config():
    """Testa configurações do VS Code"""
    print("\n⚙️ Testando configurações VS Code...")

    vscode_dir = Path(".vscode")
    if not vscode_dir.exists():
        print("❌ Pasta .vscode não encontrada")
        return False

    # Testa arquivos de configuração
    config_files = {
        "launch.json": "Configurações de execução (F5)",
        "tasks.json": "Tarefas automatizadas",
        "settings.json": "Configurações do projeto",
        "extensions.json": "Extensões recomendadas",
    }

    all_good = True
    for file_name, description in config_files.items():
        file_path = vscode_dir / file_name
        if file_path.exists():
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    json.load(f)  # Valida JSON
                print(f"✅ {file_name} - {description}")
            except json.JSONDecodeError:
                print(f"❌ {file_name} - JSON inválido")
                all_good = False
        else:
            print(f"❌ {file_name} - Não encontrado")
            all_good = False

    return all_good


def test_android_setup():
    """Testa configuração Android"""
    print("\n🤖 Testando configuração Android...")

    # Buildozer.spec
    if not os.path.exists("buildozer.spec"):
        print("❌ buildozer.spec não encontrado")
        return False
    else:
        print("✅ buildozer.spec encontrado")

    # Buildozer instalado
    try:
        result = subprocess.run(
            ["buildozer", "--version"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            print("✅ Buildozer instalado")
        else:
            print("❌ Buildozer não funcional")
            return False
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ):
        print("❌ Buildozer não instalado")
        return False

    # Script run_android.py
    if os.path.exists("run_android.py"):
        print("✅ Script run_android.py encontrado")
    else:
        print("❌ Script run_android.py não encontrado")
        return False

    return True


def test_linux_setup():
    """Testa configuração Linux"""
    print("\n🐧 Testando configuração Linux...")

    if platform.system() != "Windows":
        print("⚠️  Teste de Linux via WSL2 disponível apenas no Windows")
        return True

    # WSL2
    try:
        result = subprocess.run(
            ["wsl", "--status"], capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            print("✅ WSL2 disponível")
        else:
            print("❌ WSL2 não configurado")
            return False
    except (
        subprocess.CalledProcessError,
        FileNotFoundError,
        subprocess.TimeoutExpired,
    ):
        print("❌ WSL2 não instalado")
        return False

    # Script run_linux.py
    if os.path.exists("run_linux.py"):
        print("✅ Script run_linux.py encontrado")
    else:
        print("❌ Script run_linux.py não encontrado")
        return False

    # Setup script
    if os.path.exists("setup_wsl2.ps1"):
        print("✅ Script setup_wsl2.ps1 encontrado")
    else:
        print("❌ Script setup_wsl2.ps1 não encontrado")
        return False

    return True


def test_game_files():
    """Testa arquivos do jogo"""
    print("\n🎮 Testando arquivos do jogo...")

    essential_files = {
        "main.py": "Arquivo principal do jogo",
        "requirements.txt": "Dependências Python",
        "requirements-mobile.txt": "Dependências mobile",
        "run_android_direct.py": "Script execução Android direta",
        "build_linux.py": "Script build Linux",
        "build_android_release.py": "Script build Android release",
    }

    essential_dirs = {
        "imagens": "Recursos gráficos",
        "musicas": "Recursos de áudio",
        "sounds": "Efeitos sonoros",
    }

    all_good = True

    # Testa arquivos
    for file_name, description in essential_files.items():
        if os.path.exists(file_name):
            print(f"✅ {file_name} - {description}")
        else:
            print(f"❌ {file_name} - {description} (não encontrado)")
            all_good = False

    # Testa diretórios
    for dir_name, description in essential_dirs.items():
        if os.path.isdir(dir_name):
            file_count = len(list(Path(dir_name).rglob("*.*")))
            print(f"✅ {dir_name}/ - {description} ({file_count} arquivos)")
        else:
            print(f"❌ {dir_name}/ - {description} (não encontrado)")
            all_good = False

    return all_good


def show_launch_configurations():
    """Mostra as configurações de execução disponíveis"""
    print("\n🚀 CONFIGURAÇÕES DE EXECUÇÃO DISPONÍVEIS (F5):")
    print("=" * 50)

    try:
        with open(".vscode/launch.json", "r", encoding="utf-8") as f:
            launch_config = json.load(f)

        for i, config in enumerate(launch_config.get("configurations", []), 1):
            name = config.get("name", "Sem nome")
            program = config.get("program", "N/A")
            program = program.replace("${workspaceFolder}/", "")
            print(f"{i}. {name}")
            print(f"   Executa: {program}")
            print()

    except (FileNotFoundError, json.JSONDecodeError):
        print("❌ Não foi possível ler as configurações de execução")


def test_video_dependencies():
    """Testa dependências de vídeo (MoviePy/FFmpeg) e o vídeo de abertura"""
    print("\n🎬 Testando player de vídeo (MoviePy/FFmpeg)...")
    ok = True

    # Verificar MoviePy
    try:
        import moviepy  # noqa: F401
        from moviepy.editor import VideoFileClip  # noqa: F401
        print(f"✅ MoviePy {getattr(moviepy, '__version__', 'desconhecida')} instalado")
    except Exception as e:
        print(f"❌ MoviePy indisponível no interpretador atual ({sys.executable}): {e}")
        print("   Dica: instale as dependências neste Python com:")
        print(f"   \"{sys.executable}\" -m pip install -r requirements.txt")
        return False

    # Verificar imageio-ffmpeg / ffmpeg
    try:
        import imageio_ffmpeg as iio_ffmpeg  # noqa: F401
        ffmpeg_path = iio_ffmpeg.get_ffmpeg_exe()
        print(f"✅ imageio-ffmpeg disponível (ffmpeg: {ffmpeg_path})")
    except Exception as e:
        print(f"❌ imageio-ffmpeg/ffmpeg indisponível: {e}")
        print(f"   Dica: \"{sys.executable}\" -m pip install imageio-ffmpeg")
        ok = False

    # Verificar arquivo de vídeo de abertura
    video_path = os.path.join(".", "videos", "opening.mp4")
    abs_video = os.path.abspath(video_path)
    if not os.path.exists(video_path):
        print(f"❌ Vídeo de abertura não encontrado: {abs_video}")
        ok = False
    else:
        print(f"➡️  Testando leitura de: {abs_video}")
        try:
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(abs_video)
            # Força leitura de um frame inicial
            _ = clip.get_frame(0.0)
            print(f"✅ Abriu vídeo de abertura (dur: {clip.duration:.2f}s, fps: {clip.fps})")
            clip.close()
        except Exception as e:
            print(f"❌ Erro ao abrir/ler vídeo de abertura com MoviePy: {e}")
            ok = False

    # Verificar arquivo de vídeo final
    end_path = os.path.join(".", "videos", "ending.mp4")
    abs_end = os.path.abspath(end_path)
    if not os.path.exists(end_path):
        print(f"❌ Vídeo final não encontrado: {abs_end}")
        ok = False
    else:
        print(f"➡️  Testando leitura de: {abs_end}")
        try:
            from moviepy.editor import VideoFileClip
            clip = VideoFileClip(abs_end)
            _ = clip.get_frame(0.0)
            print(f"✅ Abriu vídeo final (dur: {clip.duration:.2f}s, fps: {clip.fps})")
            clip.close()
        except Exception as e:
            print(f"❌ Erro ao abrir/ler vídeo final com MoviePy: {e}")
            ok = False

    return ok


def main():
    """Função principal"""
    print("🧪 TESTE DE CONFIGURAÇÃO DE DESENVOLVIMENTO")
    print("=" * 50)

    tests = [
        ("Ambiente Python", test_python_environment),
        ("Player de Vídeo (MoviePy/FFmpeg)", test_video_dependencies),
        ("Configurações VS Code", test_vscode_config),
        ("Configuração Android", test_android_setup),
        ("Configuração Linux", test_linux_setup),
        ("Arquivos do Jogo", test_game_files),
    ]

    results = []

    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ Erro no teste {test_name}: {e}")
            results.append((test_name, False))

    # Resumo
    print("\n📊 RESUMO DOS TESTES:")
    print("=" * 30)

    passed = 0
    for test_name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{test_name}: {status}")
        if result:
            passed += 1

    print(f"\n🎯 Resultado: {passed}/{len(results)} testes passaram")

    if passed == len(results):
        print("\n🎉 Todas as configurações estão funcionando!")
        print("Você pode usar F5 para executar o jogo em diferentes plataformas.")
    else:
        print("\n⚠️  Algumas configurações precisam de atenção.")
        print("Consulte o arquivo DESENVOLVIMENTO.md para mais informações.")

    # Mostra configurações disponíveis
    show_launch_configurations()

    return passed == len(results)


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
