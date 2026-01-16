import os
import sys
import importlib.util
from pathlib import Path


class ModLoader:
    """
    Gerenciador de MODs para Jump and Hit.
    Carrega arquivos .py da pasta mods/ e executa suas funções init_mod(game).
    """
    
    def __init__(self, game):
        self.game = game
        self.loaded_mods = []
    
    def get_mods_directory(self):
        """
        Retorna o diretório onde os MODs devem estar.
        
        Durante desenvolvimento: pasta mods/ ao lado de main.py
        Em executável: pasta mods/ ao lado do .exe
        """
        if getattr(sys, 'frozen', False):
            # Executável PyInstaller
            base_dir = Path(sys.executable).parent
        else:
            # Modo desenvolvimento
            base_dir = Path(__file__).parent.parent.parent
        
        return base_dir / "mods"
    
    def load_mods(self):
        """Carrega todos os MODs da pasta mods/"""
        mods_dir = self.get_mods_directory()
        
        # Se a pasta não existe, não há MODs para carregar
        if not mods_dir.exists():
            print("[MOD LOADER] Pasta mods/ não encontrada. Nenhum MOD carregado.")
            return
        
        # Buscar todos os arquivos .py na pasta mods/
        mod_files = list(mods_dir.glob("*.py"))
        
        if not mod_files:
            print("[MOD LOADER] Nenhum arquivo .py encontrado em mods/")
            return
        
        print(f"[MOD LOADER] Encontrados {len(mod_files)} MOD(s) para carregar...")
        
        for mod_file in mod_files:
            try:
                self._load_mod(mod_file)
            except Exception as e:
                print(f"[MOD LOADER] ✗ Erro ao carregar {mod_file.name}: {e}")
    
    def _load_mod(self, mod_file):
        """Carrega um MOD específico"""
        mod_name = mod_file.stem  # Nome do arquivo sem extensão
        
        # Carregar o módulo dinamicamente
        spec = importlib.util.spec_from_file_location(mod_name, mod_file)
        if spec is None or spec.loader is None:
            raise ImportError(f"Não foi possível carregar o módulo {mod_name}")
        
        module = importlib.util.module_from_spec(spec)
        sys.modules[mod_name] = module
        spec.loader.exec_module(module)
        
        # Procurar pela função init_mod
        if not hasattr(module, 'init_mod'):
            raise AttributeError(
                f"MOD {mod_name} não possui função init_mod(game)"
            )
        
        # Executar a função init_mod passando o objeto game
        init_mod = getattr(module, 'init_mod')
        init_mod(self.game)
        
        # Registrar MOD carregado
        self.loaded_mods.append({
            'name': mod_name,
            'path': str(mod_file),
            'module': module
        })
        
        print(f"[MOD LOADER] ✓ {mod_name} carregado com sucesso")
