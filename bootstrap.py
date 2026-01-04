import os
import sys
from pathlib import Path
import time

# Tentar minimizar problemas de audio/display no boot
os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")
if sys.platform.startswith("win"):
    # Forçar driver de áudio do SDL mais estável em Windows
    os.environ.setdefault("SDL_AUDIODRIVER", "directsound")


def _setup_runtime_logging():
    try:
        if getattr(sys, "frozen", False):
            log_dir = Path(sys.executable).parent
        else:
            log_dir = Path.cwd()
        log_file = log_dir / "runtime.log"

        class Tee:
            def __init__(self, stream, file_path):
                self.stream = stream
                self.file = open(file_path, "a", encoding="utf-8")

            def write(self, data):
                try:
                    self.stream.write(data)
                except Exception:
                    pass
                try:
                    self.file.write(data)
                    self.file.flush()
                except Exception:
                    pass

            def flush(self):
                try:
                    self.stream.flush()
                except Exception:
                    pass
                try:
                    self.file.flush()
                except Exception:
                    pass

        try:
            sys.stdout = Tee(sys.stdout, log_file)
        except Exception:
            pass
        try:
            sys.stderr = Tee(sys.stderr, log_file)
        except Exception:
            pass

        def excepthook(exc_type, exc_value, exc_traceback):
            try:
                print("[EXCEPTION]", exc_type.__name__, exc_value)
                import traceback
                traceback.print_tb(exc_traceback)
            except Exception:
                pass
            if getattr(sys, "frozen", False):
                time.sleep(0.2)

        sys.excepthook = excepthook
        print("[BOOT] Bootstrap iniciado")
        print("[BOOT] Executable:", sys.executable)
        print("[BOOT] Frozen:", getattr(sys, "frozen", False))
        print("[BOOT] CWD:", os.getcwd())
        print("[BOOT] SDL_AUDIODRIVER:", os.environ.get("SDL_AUDIODRIVER"))
    except Exception:
        pass


def main():
    _setup_runtime_logging()
    print("[BOOT] Importando jogo...")
    import pygame
    pygame.init()
    try:
        # Importar Game diretamente do módulo game.py (não do package game/)
        from internal.engine.game import Game
        print("[BOOT] Criando Game...")
        game = Game()
        print("[BOOT] Iniciando loop do jogo...")
        game.run()
    except Exception as e:
        print("[BOOT] Falha ao iniciar jogo:", e)
        raise


if __name__ == "__main__":
    main()
