import sys
import os
from pathlib import Path
import time

try:
    # Escreve um log logo no início da execução (antes do main.py)
    log_dir = Path(getattr(sys, 'executable', sys.argv[0])).parent
    log_file = log_dir / 'runtime_boot.log'
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write('[RUNTIME HOOK] inicializado\n')
        f.write(f"[RUNTIME HOOK] sys.executable: {sys.executable}\n")
        f.write(f"[RUNTIME HOOK] cwd: {os.getcwd()}\n")
        f.write(f"[RUNTIME HOOK] frozen: {getattr(sys, 'frozen', False)}\n")
        f.flush()
    # Pequeno delay para garantir escrita em disco em alguns ambientes
    time.sleep(0.05)
except Exception:
    # Evitar qualquer falha aqui
    pass