import pygame
from internal.utils.constants import *
from internal.resources.cache import ResourceCache


class TitleScreen:
    def show(game):
        # Tela de título com imagem cover
        game.screen.fill(BLACK)  # Fundo preto

        # Carregar e exibir a imagem de capa
        try:
            cache = ResourceCache()
            cover_image = cache.get_image(
                "imagens/cover/cover_wide.png", (WIDTH, HEIGHT)
            )
            game.screen.blit(cover_image, (0, 0))
        except:
            # Fallback caso a imagem não carregue
            game.screen.fill(BLACK)
            title_text = game.big_font.render("JOGO DE PLATAFORMA", True, WHITE)
            title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            game.screen.blit(title_text, title_rect)

        # Mensagem de instrução
        if game.joystick_connected:
            instruction_text = "Pressione um botão para iniciar"
        else:
            instruction_text = "Pressione uma tecla para iniciar"

        instruction_surface = game.font.render(instruction_text, True, WHITE)
        instruction_rect = instruction_surface.get_rect(
            center=(WIDTH // 2, HEIGHT - 80)
        )

        # Efeito de piscar na mensagem
        blink_timer = pygame.time.get_ticks() // 500  # Pisca a cada 500ms
        if blink_timer % 2 == 0:
            game.screen.blit(instruction_surface, instruction_rect)
