import pygame
import sys
import math
import os
import json
from enum import Enum
import random
import math
from pathlib import Path
import time

# Logging simples para diagnosticar execução do executável (PyInstaller)
def _setup_runtime_logging():
    try:
        # Diretório para log: ao lado do executável quando congelado; caso contrário, cwd
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

        # Redirecionar stdout/stderr para arquivo também
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
            # Em ambiente congelado, aguardar um instante para garantir escrita
            if getattr(sys, "frozen", False):
                time.sleep(0.2)

        sys.excepthook = excepthook
        print("[BOOT] App iniciado")
        print("[BOOT] Python:", sys.executable)
        print("[BOOT] CWD:", os.getcwd())
        print("[BOOT] Frozen:", getattr(sys, "frozen", False))
    except Exception:
        pass

_setup_runtime_logging()

# Inicializar pygame
pygame.init()

# Importar constantes do jogo
from internal.engine.game import Game


if __name__ == "__main__":
    print("[BOOT] Criando Game...")
    game = Game()
    print("[BOOT] Carregando MODs...")
    game.load_mods()
    print("[BOOT] Iniciando loop do jogo...")
    game.run()

