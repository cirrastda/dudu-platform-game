import pygame


class Cheat:
    def __init__(self, game):
        self.g = game

    def process_cheat_token(self, token):
        g = self.g
        if not token:
            return
        g._cheat_buffer.append(token)
        if len(g._cheat_buffer) > len(g._cheat_sequence):
            g._cheat_buffer = g._cheat_buffer[-len(g._cheat_sequence) :]
        if g._cheat_buffer == g._cheat_sequence:
            g.cheat_99_lives_enabled = True
            g.max_lives = 99
            g.lives = 99
            
            # Feedback visual: mensagem no canto superior direito
            g.cheat_message = "99 VIDAS ATIVADO!"
            g.cheat_message_timer = 180  # 3 segundos a 60 FPS
            
            # Penalidade: zerar pontuação
            g.score = 0

    def map_key_to_cheat_token(self, key, unicode_val=""):
        # Direcionais
        if key == pygame.K_UP:
            return "UP"
        if key == pygame.K_DOWN:
            return "DOWN"
        if key == pygame.K_LEFT:
            return "LEFT"
        if key == pygame.K_RIGHT:
            return "RIGHT"
        
        # Pulo (múltiplas teclas possíveis)
        if key in [pygame.K_SPACE, pygame.K_w]:
            return "JUMP"
        
        # Ataque (múltiplas teclas possíveis)
        if key in [pygame.K_LCTRL, pygame.K_RCTRL, pygame.K_x]:
            return "SHOOT"
        
        # OPCIONAL: Manter B e A como aliases para compatibilidade com teclado
        if key == pygame.K_b or unicode_val.lower() == "b":
            return "JUMP"  # B = JUMP
        if key == pygame.K_a or unicode_val.lower() == "a":
            return "SHOOT"  # A = SHOOT
        
        return None

    def process_powerups_cheat_token(self, token):
        """Processa cheat de todos os power-ups"""
        g = self.g
        if not token:
            return
        
        g._cheat_powerups_buffer.append(token)
        if len(g._cheat_powerups_buffer) > len(g._cheat_powerups_sequence):
            g._cheat_powerups_buffer = g._cheat_powerups_buffer[-len(g._cheat_powerups_sequence):]
        
        if g._cheat_powerups_buffer == g._cheat_powerups_sequence:
            # Ativar todos os power-ups
            # 1. Invencibilidade (20 segundos = 1200 frames)
            g.player.is_invulnerable = True
            g.player.invulnerability_timer = 1200
            g.invincibility_active = True
            
            # 2. Pulo Duplo (70 segundos = 4200 frames)
            g.player.double_jump_enabled = True
            g.player.double_jump_timer = 4200
            
            # 3. Escudo
            g.shield_active = True
            
            # 4. Tempo/Lentidão (70 segundos = 4200 frames)
            g.tempo_active = True
            g.tempo_timer = 4200
            g.tempo_factor = 0.5
            
            # 5. Super Tiro (70 segundos = 4200 frames)
            g.super_shot_active = True
            g.super_shot_timer = 4200
            
            # Feedback visual: mensagem no canto superior direito
            g.cheat_message = "TODOS OS POWER-UPS ATIVADO!"
            g.cheat_message_timer = 180  # 3 segundos a 60 FPS
            
            # Penalidade: deduzir 2000 pontos (mínimo 0)
            g.score = max(0, g.score - 2000)
