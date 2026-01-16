#!/usr/bin/env python3
"""
Script para criar um executável da versão DEMO do jogo.
A versão Demo tem apenas as 10 primeiras fases.
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# Importar informações de versão (precisa estar no sys.path da raiz)
_root_path = Path(__file__).parent.parent
if str(_root_path) not in sys.path:
    sys.path.insert(0, str(_root_path))

try:
    from version import VERSION_FULL, GAME_NAME, GAME_TITLE
except ImportError:
    print("[AVISO] version.py nao encontrado. Usando valores padrao.")
    VERSION_FULL = "0.0.1-alpha.1"
    GAME_NAME = "JumpAndHit"
    GAME_TITLE = "Jump and Hit"


class DemoBuilder:
    def __init__(self):
        self.current_platform = self._detect_platform()
        self.project_root = Path.cwd()
        self.dist_dir = self.project_root / "dist"
        self.build_dir = self.project_root / "build"

    def _detect_platform(self):
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

    def _clean_build_dirs(self):
        """Limpa diretórios de build anteriores"""
        import stat
        
        def _handle_remove_readonly(func, path, exc_info):
            """Callback para remover arquivos somente leitura."""
            try:
                os.chmod(path, stat.S_IWRITE)
                func(path)
            except Exception:
                pass

        print("[CLEAN] Limpando diretorios de build...")
        for dir_path in [self.dist_dir, self.build_dir]:
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path, onerror=_handle_remove_readonly)
                    print(f"   OK: {dir_path}")
                except Exception as e:
                    print(f"   AVISO: Nao foi possivel limpar {dir_path}: {e}")

    def _check_dependencies(self):
        """Verifica se as dependências estão instaladas"""
        print("[CHECK] Verificando dependencias...")

        required = {
            "PyInstaller": "PyInstaller",
            "pygame": "pygame",
            "moviepy": "moviepy",
            "imageio_ffmpeg": "imageio_ffmpeg",
        }

        all_found = True
        for name, module in required.items():
            try:
                mod = __import__(module)
                version = getattr(mod, "__version__", "instalado")
                print(f"   OK: {name} ({version})")
            except ImportError:
                print(f"   ERRO: {name} NAO ENCONTRADO")
                all_found = False

        # Verificar arquivo principal
        if not (self.project_root / "bootstrap.py").exists():
            print("   ERRO: bootstrap.py nao encontrado")
            all_found = False
        else:
            print("   OK: bootstrap.py encontrado")

        if all_found:
            print("   OK: Todas as dependencias OK")
        return all_found

    def _get_executable_name(self):
        """Gera nome do executável baseado na plataforma"""
        base = GAME_NAME.replace(" ", "")
        demo_suffix = "Demo"
        if self.current_platform == "windows":
            return f"{base}-{VERSION_FULL}-{demo_suffix}-win64.exe"
        elif self.current_platform == "macos":
            return f"{base}-{VERSION_FULL}-{demo_suffix}-macos"
        else:  # linux
            return f"{base}-{VERSION_FULL}-{demo_suffix}-linux64"

    def build(self):
        """Cria o executável único da versão DEMO do jogo"""
        exe_name = self._get_executable_name()
        print(f"\n{'='*60}")
        print(f"[BUILD DEMO] {GAME_TITLE} - Versão Demo")
        print(f"   Versao: {VERSION_FULL}")
        print(f"   Plataforma: {self.current_platform.upper()}")
        print(f"   Executavel: {exe_name}")
        print(f"   Fases: 10 (Demo)")
        print(f"{'='*60}\n")

        # 1. Limpar builds anteriores
        self._clean_build_dirs()
        print()

        # 2. Verificar dependências
        if not self._check_dependencies():
            print("\n[ERRO] Dependencias nao atendidas!")
            return False
        print()

        # 3. Criar diretório de saída
        self.dist_dir.mkdir(parents=True, exist_ok=True)

        # 4. Configurar comando PyInstaller
        cmd = [
            sys.executable,
            "-m", "PyInstaller",
            "--onefile",  # Executável ÚNICO
            "--name", exe_name.replace(".exe", ""),
            "--distpath", str(self.dist_dir),
            "--workpath", str(self.build_dir),
            "--specpath", str(self.build_dir),
            "--console",  # Manter console para debug/logs
        ]

        # Adicionar hook de runtime para logging
        if (self.project_root / "run_build" / "runtime_hook_logging.py").exists():
            cmd.extend(["--runtime-hook", str(self.project_root / "run_build" / "runtime_hook_logging.py")])

        # Buscar ícone
        icon_candidates = [
            "imagens/icones/icon_desktop_new.ico",
            "imagens/icones/icon_desktop_new.png",
            "imagens/icones/icon_minimal.png",
            "icon.ico",
        ]
        for icon_file in icon_candidates:
            icon_path = self.project_root / icon_file
            if icon_path.exists():
                print(f"[ICON] Icone encontrado: {icon_file}")
                cmd.extend(["--icon", str(icon_path)])
                break

        # Adicionar recursos (imagens, sons, vídeos)
        resource_dirs = ["imagens", "musicas", "sounds", "videos"]
        for res_dir in resource_dirs:
            res_path = self.project_root / res_dir
            if res_path.exists():
                cmd.append(f"--add-data={res_path}{os.pathsep}{res_dir}")

        # Excluir pasta mods/ do executável
        # MODs são carregados dinamicamente da pasta ao lado do .exe
        if (self.project_root / "mods").exists():
            cmd.extend(["--exclude-module", "mods"])


        # Coletar todos os submódulos e dependências necessárias
        cmd.extend([
            # Coletar tudo dos pacotes críticos
            "--collect-all", "imageio_ffmpeg",
            "--collect-all", "moviepy",
            "--collect-submodules", "moviepy",
            "--collect-submodules", "imageio",
            "--collect-submodules", "numpy",
            "--collect-submodules", "pygame",
            "--collect-submodules", "proglog",
            "--collect-submodules", "tqdm",
            "--collect-submodules", "decorator",
            "--collect-submodules", "internal",
            
            # Copias de metadados
            "--copy-metadata", "imageio",
            "--copy-metadata", "moviepy",
            "--copy-metadata", "numpy",
            "--copy-metadata", "proglog",
            "--copy-metadata", "tqdm",
            
            # Hidden imports
            "--hidden-import", "moviepy",
            "--hidden-import", "moviepy.editor",
            "--hidden-import", "numpy",
            "--hidden-import", "requests",
            "--hidden-import", "imageio",
            "--hidden-import", "imageio_ffmpeg",
            "--hidden-import", "pygame.freetype",
            "--hidden-import", "proglog",
            "--hidden-import", "tqdm",
            "--hidden-import", "decorator",
            "--hidden-import", "internal.engine.ranking",
            "--hidden-import", "internal.engine.game.life",
            "--hidden-import", "internal.engine.game.score",
            "--hidden-import", "internal.engine.game.events",
            "--hidden-import", "internal.engine.game.draw",
            "--hidden-import", "internal.engine.game.update",
            "--hidden-import", "internal.engine.game.difficulty",
            "--hidden-import", "internal.engine.game.pool",
            "--hidden-import", "internal.engine.game.cheat",
            "--hidden-import", "internal.engine.game.menu",
            "--hidden-import", "internal.engine.game.system",
            "--hidden-import", "internal.engine.level.level",
            "--hidden-import", "internal.utils.functions",
            "--hidden-import", "internal.utils.edition",
        ])

        # IMPORTANTE: Definir variável de ambiente para modo DEMO
        # Isso será lido pelo módulo edition.py
        print("[DEMO] Configurando modo DEMO...")
        os.environ["PLATFORM_GAME_DEMO"] = "1"

        # Tentar incluir ffmpeg diretamente se disponível
        try:
            import imageio_ffmpeg
            ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
            if os.path.exists(ffmpeg_exe):
                print(f"[BUILD] ffmpeg incluido: {ffmpeg_exe}")
                cmd.append(f"--add-binary={ffmpeg_exe}{os.pathsep}imageio_ffmpeg")
        except Exception:
            pass

        # Arquivo de entrada (bootstrap)
        cmd.append("bootstrap.py")

        # 5. Executar PyInstaller
        print(f"[BUILD] Compilando executavel DEMO...")
        try:
            # Passar variável de ambiente para o subprocess
            env = os.environ.copy()
            env["PLATFORM_GAME_DEMO"] = "1"
            subprocess.run(cmd, check=True, cwd=self.project_root, env=env)
        except subprocess.CalledProcessError as e:
            print(f"\n[ERRO] Erro ao compilar: {e}")
            return False

        # 6. Verificar se o executável foi criado
        exe_path = self.dist_dir / exe_name if self.current_platform == "windows" else self.dist_dir / exe_name.replace(".exe", "")
        
        # PyInstaller as vezes coloca em um subdiretorio com o mesmo nome
        if not exe_path.exists():
            alt_path = self.dist_dir / exe_name.replace(".exe", "") / exe_name
            if alt_path.exists():
                exe_path = alt_path
            else:
                print(f"\n[ERRO] Executavel nao encontrado em {exe_path}")
                print(f"Conteudo de dist:")
                for item in self.dist_dir.rglob("*"):
                    print(f"  {item}")
                return False

        # 7. Exibir resultado
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"\n{'='*60}")
        print(f"[OK] SUCESSO! Executavel DEMO criado:")
        print(f"   {exe_path}")
        print(f"   Tamanho: {size_mb:.1f} MB")
        print(f"   Fases: 10 (Demo)")
        print(f"{'='*60}\n")
        
        print("[INFO] Versão Demo:")
        print("   - Apenas 10 primeiras fases disponíveis")
        print("   - Ao completar a fase 10, exibe mensagem de compra")
        print("   - Retorna automaticamente ao menu principal")
        print()
        
        print("[OK] Para executar o jogo:")
        if self.current_platform == "windows":
            print(f"   .\\dist\\{exe_name}")
        else:
            print(f"   ./dist/{exe_name.replace('.exe', '')}")
        print()

        return True


def main():
    """Funcao principal - build da versão Demo"""
    print("""
╔════════════════════════════════════════════════════════════╗
║         JUMP AND HIT - BUILD VERSÃO DEMO                   ║
║  Este script cria uma versão de demonstração com apenas    ║
║  as 10 primeiras fases do jogo.                            ║
╚════════════════════════════════════════════════════════════╝
""")
    
    builder = DemoBuilder()
    success = builder.build()
    
    if success:
        print("\n[OK] Build da versão Demo concluído com sucesso!")
    else:
        print("\n[ERRO] Falha ao criar build da versão Demo")
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
