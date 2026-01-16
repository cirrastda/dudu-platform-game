#!/usr/bin/env python3
"""
Sistema de detecção de edição do jogo (Demo vs Full)
"""

import os
import sys


class GameEdition:
    """Gerencia a edição do jogo (Demo ou Full)"""
    
    # Valores padrão
    _is_demo = False
    _max_demo_levels = 10
    _demo_url = "https://v0-cirrastec.vercel.app/jogos/jump-and-hit"
    _demo_steam_url = "Steam"
    
    @classmethod
    def set_demo_mode(cls, enable=True):
        """Define se o jogo está em modo Demo"""
        cls._is_demo = enable
    
    @classmethod
    def is_demo(cls):
        """Verifica se o jogo está em modo Demo"""
        # Verificar variável de ambiente primeiro
        env_demo = os.environ.get("PLATFORM_GAME_DEMO", "").lower()
        if env_demo in ["1", "true", "yes"]:
            return True
        return cls._is_demo
    
    @classmethod
    def get_max_levels(cls):
        """Retorna o número máximo de fases permitidas"""
        if cls.is_demo():
            return cls._max_demo_levels
        return 51  # Número total de fases do jogo completo
    
    @classmethod
    def get_demo_message(cls):
        """Retorna a mensagem a ser exibida ao final da demo"""
        return (
            "Esta é uma versão de Demonstração do jogo.\n\n"
            f"Para jogar o game completo, você deve comprá-lo,\n"
            f"no site {cls._demo_url}\n"
            f"ou na página do jogo na {cls._demo_steam_url}."
        )
    
    @classmethod
    def should_show_demo_end_message(cls, current_level):
        """Verifica se deve mostrar a mensagem de fim da demo"""
        return cls.is_demo() and current_level >= cls._max_demo_levels


# Detecção automática ao importar o módulo
def _auto_detect_demo():
    """Detecta automaticamente se está em modo Demo"""
    # Verificar se foi compilado com flag de demo
    if getattr(sys, 'frozen', False):
        # Executável compilado
        exe_name = os.path.basename(sys.executable).lower()
        if 'demo' in exe_name:
            GameEdition.set_demo_mode(True)
    
    # Verificar variável de ambiente
    if os.environ.get("PLATFORM_GAME_DEMO", "").lower() in ["1", "true", "yes"]:
        GameEdition.set_demo_mode(True)


# Executar detecção ao importar
_auto_detect_demo()
