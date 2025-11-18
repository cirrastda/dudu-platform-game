from internal.engine.difficulty import Difficulty
from internal.utils.constants import WIDTH, HEIGHT
import pygame


class Info:
    def display(game, screen, font, color):
        margin = 10
        spacing = 8

        # Aplicar negrito na fonte quando suportado
        try:
            if hasattr(font, "set_bold"):
                font.set_bold(True)
        except Exception:
            pass

        # Calcular tamanho da fonte superior (menor que a do rodapé)
        try:
            base_h = int(getattr(font, "get_height", lambda: 40)())
        except Exception:
            base_h = 40
        # Reduzir mais a fonte do topo para ficar mais discreta
        top_h = max(24, int(base_h * 0.65))
        # Criar fonte do topo com fallback seguro
        try:
            top_font = pygame.font.SysFont("Segoe UI", top_h, bold=True)
        except Exception:
            try:
                top_font = pygame.font.SysFont("Arial", top_h, bold=True)
            except Exception:
                top_font = pygame.font.Font(None, top_h)
                try:
                    if hasattr(top_font, "set_bold"):
                        top_font.set_bold(True)
                except Exception:
                    pass

        # Topo Esquerdo: Fase atual
        level_text = top_font.render(f"Fase: {game.current_level}", True, color)
        screen.blit(level_text, (margin, margin))

        # Em modo development, exibir a dificuldade logo abaixo
        show_difficulty = False
        try:
            show_difficulty = bool(getattr(game, "is_development", lambda: False)())
        except Exception:
            try:
                show_difficulty = getattr(game, "env_config", {}).get("environment") == "development"
            except Exception:
                show_difficulty = False

        if show_difficulty:
            diff = getattr(game, "difficulty", Difficulty.NORMAL)
            if diff == Difficulty.EASY:
                diff_label = "Fácil"
            elif diff == Difficulty.HARD:
                diff_label = "Difícil"
            else:
                diff_label = "Normal"
            diff_text = top_font.render(f"Dificuldade: {diff_label}", True, color)
            screen.blit(diff_text, (margin, margin + level_text.get_height() + spacing))

        # Topo Direito: Pontos atuais (rótulo atualizado)
        score_text = top_font.render(f"Pontos: {game.score}", True, color)
        score_pos_x = WIDTH - margin - score_text.get_width()
        screen.blit(score_text, (score_pos_x, margin))

        # Inferior Esquerdo: Ícone de vida + número de vidas
        life_icon = getattr(game, "extra_life_img", None)
        lives_value_text = font.render(f"x {getattr(game, 'lives', 0)}", True, color)
        # Tamanho de ícones do HUD proporcional à altura da fonte
        hud_icon_size = max(32, base_h)

        # Base vertical alinhada pela maior altura entre ícone e texto
        def _transparent_background(surf):
            try:
                w, h = surf.get_width(), surf.get_height()
                c_tl = surf.get_at((0, 0))
                c_tr = surf.get_at((w - 1, 0))
                c_bl = surf.get_at((0, h - 1))
                c_br = surf.get_at((w - 1, h - 1))
                # Se os 4 cantos têm a mesma cor opaca, assumir cor de fundo
                same_corners = (c_tl == c_tr == c_bl == c_br)
                if same_corners and getattr(c_tl, "a", 255) >= 250:
                    try:
                        surf = surf.convert()
                    except Exception:
                        pass
                    try:
                        surf.set_colorkey((c_tl.r, c_tl.g, c_tl.b))
                    except Exception:
                        pass
                else:
                    # Manter per-pixel alpha quando disponível
                    try:
                        surf = surf.convert_alpha()
                    except Exception:
                        pass
            except Exception:
                # Fallback: manter como está
                pass
            return surf

        if isinstance(life_icon, pygame.Surface):
            try:
                scaled_life = pygame.transform.smoothscale(life_icon, (hud_icon_size, hud_icon_size))
            except Exception:
                scaled_life = pygame.transform.scale(life_icon, (hud_icon_size, hud_icon_size))
            # Garantir que o fundo do ícone no HUD seja transparente
            scaled_life = _transparent_background(scaled_life)
            icon_w = scaled_life.get_width()
            icon_h = scaled_life.get_height()
        else:
            icon_w = 0
            icon_h = lives_value_text.get_height()

        base_y = HEIGHT - margin - max(icon_h, lives_value_text.get_height())
        if isinstance(life_icon, pygame.Surface):
            screen.blit(scaled_life, (margin, base_y))
            screen.blit(lives_value_text, (margin + icon_w + spacing, base_y))
        else:
            # Fallback: apenas texto se ícone indisponível
            screen.blit(lives_value_text, (margin, base_y))

        # Inferior Direito: Ícones dos power-ups ativos (direita para esquerda)
        powerup_icons = []
        if getattr(game, "invincibility_active", False):
            img = getattr(game, "powerup_invincibility_img", None)
            if isinstance(img, pygame.Surface):
                powerup_icons.append(img)
        # Double jump habilitado no player
        try:
            if getattr(getattr(game, "player", None), "double_jump_enabled", False):
                img = getattr(game, "powerup_double_jump_img", None)
                if isinstance(img, pygame.Surface):
                    powerup_icons.append(img)
        except Exception:
            pass
        # Escudo ativo
        if getattr(game, "shield_active", False):
            img = getattr(game, "powerup_shield_img", None)
            if isinstance(img, pygame.Surface):
                powerup_icons.append(img)

        if powerup_icons:
            # Escalar ícones para tamanho do HUD
            y = HEIGHT - margin - hud_icon_size
            x = WIDTH - margin
            # Renderizar da direita para a esquerda
            for img in reversed(powerup_icons):
                try:
                    scaled = pygame.transform.smoothscale(img, (hud_icon_size, hud_icon_size))
                except Exception:
                    scaled = pygame.transform.scale(img, (hud_icon_size, hud_icon_size))
                # Garantir fundo transparente também nos ícones de power-up
                scaled = _transparent_background(scaled)
                w = scaled.get_width()
                x -= w
                screen.blit(scaled, (x, y))
                x -= spacing
