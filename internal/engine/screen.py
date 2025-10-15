# import platform
import pygame
from internal.utils.constants import WIDTH, HEIGHT


class Screen:
    def __init__(self):
        self.game_width = WIDTH
        self.game_height = HEIGHT
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        self.scale_x = 1.0
        self.scale_y = 1.0
        self.offset_x = 0
        self.offset_y = 0
        self.game_surface = None
    
    def init(game):
        # Criar instância do Screen se não existir
        if not hasattr(game, 'screen_manager'):
            game.screen_manager = Screen()
        
        screen_manager = game.screen_manager
        
        # Detectar se deve usar fullscreen
        use_fullscreen = (not game.is_development()) or (Screen.is_fullscreen(game))
        
        if use_fullscreen:
            # Obter informações da tela
            info = pygame.display.Info()
            screen_manager.screen_width = info.current_w
            screen_manager.screen_height = info.current_h
            
            # Criar tela real em fullscreen com resolução nativa
            screen_manager.real_screen = pygame.display.set_mode(
                (screen_manager.screen_width, screen_manager.screen_height), 
                pygame.FULLSCREEN
            )
            
            # Calcular escalonamento mantendo proporção
            scale_x = screen_manager.screen_width / screen_manager.game_width
            scale_y = screen_manager.screen_height / screen_manager.game_height
            
            # Usar o menor fator de escala para manter proporção
            screen_manager.scale_x = screen_manager.scale_y = min(scale_x, scale_y)
            
            # Calcular dimensões escaladas
            scaled_width = int(screen_manager.game_width * screen_manager.scale_x)
            scaled_height = int(screen_manager.game_height * screen_manager.scale_y)
            
            # Calcular offset para centralizar
            screen_manager.offset_x = (screen_manager.screen_width - scaled_width) // 2
            screen_manager.offset_y = (screen_manager.screen_height - scaled_height) // 2
            
            # Criar surface do jogo - esta será a "tela" que todos os objetos usam
            screen_manager.game_surface = pygame.Surface((screen_manager.game_width, screen_manager.game_height))
            
            # IMPORTANTE: fazer game.screen apontar para a surface do jogo
            # Isso mantém compatibilidade total com o código existente
            game.screen = screen_manager.game_surface
        else:
            # Modo janela - usar resolução original
            game.screen = pygame.display.set_mode((WIDTH, HEIGHT))
            screen_manager.real_screen = game.screen
            screen_manager.game_surface = game.screen
            screen_manager.scale_x = screen_manager.scale_y = 1.0
            screen_manager.offset_x = screen_manager.offset_y = 0
    
    def get_game_surface(game):
        """Retorna a surface onde o jogo deve desenhar"""
        if hasattr(game, 'screen_manager'):
            return game.screen_manager.game_surface
        return game.screen
    
    def present(game):
        """Apresenta o frame na tela, aplicando escalonamento se necessário"""
        if not hasattr(game, 'screen_manager'):
            pygame.display.flip()
            return
            
        screen_manager = game.screen_manager
        
        # Se não está em fullscreen ou escala é 1:1, apenas flip
        if screen_manager.scale_x == 1.0 and screen_manager.scale_y == 1.0:
            pygame.display.flip()
            return
        
        # Limpar tela real com preto
        screen_manager.real_screen.fill((0, 0, 0))
        
        # Escalar e desenhar a surface do jogo na tela real
        scaled_width = int(screen_manager.game_width * screen_manager.scale_x)
        scaled_height = int(screen_manager.game_height * screen_manager.scale_y)
        
        scaled_surface = pygame.transform.scale(
            screen_manager.game_surface, 
            (scaled_width, scaled_height)
        )
        
        screen_manager.real_screen.blit(scaled_surface, (screen_manager.offset_x, screen_manager.offset_y))
        pygame.display.flip()

    def is_fullscreen(game):
        env = game.env_config
        return env.get("fullscreen", False)
