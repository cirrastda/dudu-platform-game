import math
import pygame

from internal.utils.constants import *
from internal.engine.screen import Screen
from internal.engine.state import GameState
from internal.engine.title import TitleScreen
from internal.engine.info import Info


class Draw:
    def __init__(self, game):
        self.game = game

    def draw_ocean_background(self, surface=None):
        """Desenha o fundo do mar para menus e jogo, com fallback em gradiente."""
        g = self.game
        surf = surface if surface is not None else g.screen

        # Escolher imagem de fundo conforme estado
        if g.state == GameState.PLAYING:
            background_to_use = getattr(g, "background_img", g.image.background_img)
        else:
            background_to_use = getattr(
                g, "menu_background_img", g.image.background_img
            )

        if background_to_use:
            surf.blit(background_to_use, (0, 0))
            return

        # Fallback: gradiente azul e ondas simples
        for y in range(HEIGHT):
            ratio = y / HEIGHT
            r = int(135 * (1 - ratio) + 0 * ratio)
            gg = int(206 * (1 - ratio) + 50 * ratio)
            b = int(235 * (1 - ratio) + 100 * ratio)
            pygame.draw.line(surf, (r, gg, b), (0, y), (WIDTH, y))

        wave_offset = pygame.time.get_ticks() * 0.002
        for x in range(0, WIDTH, 20):
            wave_y = HEIGHT - 50 + math.sin(x * 0.01 + wave_offset) * 10
            pygame.draw.circle(surf, (0, 80, 150), (x, int(wave_y)), 15)

    def draw(self):
        game = self.game

        if game.state == GameState.SPLASH:
            # Tela de splash com fundo preto
            game.screen.fill(BLACK)

            # Mostrar logo atual com efeito de fade
            if game.logos and game.current_logo_index < len(game.logos):
                logo = game.logos[game.current_logo_index]

                # Calcular posição no ciclo do logo atual
                logo_cycle_time = game.splash_timer % game.logo_display_time
                alpha = 255  # Opacidade padrão

                # Fade in (primeiros frames)
                if logo_cycle_time < game.fade_in_duration:
                    alpha = int((logo_cycle_time / game.fade_in_duration) * 255)
                # Fade out (últimos frames)
                elif logo_cycle_time > (
                    game.logo_display_time - game.fade_out_duration
                ):
                    fade_progress = (
                        logo_cycle_time
                        - (game.logo_display_time - game.fade_out_duration)
                    ) / game.fade_out_duration
                    alpha = int((1 - fade_progress) * 255)

                # Aplicar alpha ao logo
                if alpha < 255:
                    logo_with_alpha = logo.copy()
                    logo_with_alpha.set_alpha(alpha)
                    logo_rect = logo_with_alpha.get_rect(
                        center=(WIDTH // 2, HEIGHT // 2)
                    )
                    game.screen.blit(logo_with_alpha, logo_rect)
                else:
                    logo_rect = logo.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                    game.screen.blit(logo, logo_rect)

            # Texto de instrução com fade suave (só em modo development)
            if game.env_config.get("environment", "production") == "development":
                instruction_alpha = min(255, game.splash_timer * 3)  # Fade in gradual
                instruction_text = game.font.render(
                    "Pressione qualquer tecla para continuar", True, WHITE
                )
                if instruction_alpha < 255:
                    instruction_text.set_alpha(instruction_alpha)
                instruction_rect = instruction_text.get_rect(
                    center=(WIDTH // 2, HEIGHT - 80)
                )
                game.screen.blit(instruction_text, instruction_rect)

        elif game.state == GameState.TITLE_SCREEN:
            TitleScreen.show(game)

        elif game.state == GameState.OPENING_VIDEO:
            # Limpar a tela com fundo preto para evitar sobreposição
            game.screen.fill(BLACK)
            # Desenhar o vídeo de abertura
            game.video_player.draw(game.screen)

        elif game.state == GameState.ENDING_VIDEO:
            # Limpar a tela com fundo preto para evitar sobreposição
            game.screen.fill(BLACK)
            # Desenhar o vídeo de ending
            game.ending_video_player.draw(game.screen)

        elif game.state == GameState.MAIN_MENU:
            # Tela de menu com fundo do jogo
            self.draw_ocean_background(game.screen)

            # Logo do jogo (aumentado)
            if game.game_logo:
                # Aumentar o tamanho do logo em 50%
                logo_scaled = pygame.transform.scale(
                    game.game_logo,
                    (
                        int(game.game_logo.get_width() * 1.5),
                        int(game.game_logo.get_height() * 1.5),
                    ),
                )
                logo_rect = logo_scaled.get_rect(center=(WIDTH // 2, 120))
                game.screen.blit(logo_scaled, logo_rect)

            # Título do jogo se não houver logo
            else:
                title_text = game.menu_big_font.render("Jump & Hit", True, WHITE)
                title_rect = title_text.get_rect(center=(WIDTH // 2, 150))
                game.screen.blit(title_text, title_rect)

            # Opções do menu
            menu_start_y = 300
            for i, option in enumerate(game.menu_options):
                color = YELLOW if i == game.menu_selected else WHITE
                option_text = game.menu_font.render(option, True, color)
                option_rect = option_text.get_rect(
                    center=(WIDTH // 2, menu_start_y + i * 60)
                )

                # Destacar opção selecionada com retângulo
                if i == game.menu_selected:
                    pygame.draw.rect(
                        game.screen, DARK_BLUE, option_rect.inflate(20, 10)
                    )

                game.screen.blit(option_text, option_rect)

            # Rodapé com direitos autorais
            footer_text = "Desenvolvido por CirrasTec, Cirras RetroGames e Canal do Dudu. Todos os direitos reservados."
            footer_surface = game.menu_small_font.render(footer_text, True, LIGHT_GRAY)
            footer_rect = footer_surface.get_rect(center=(WIDTH // 2, HEIGHT - 30))
            game.screen.blit(footer_surface, footer_rect)

        elif game.state == GameState.SELECT_DIFFICULTY:
            # Tela de seleção de dificuldade com o mesmo estilo do menu
            self.draw_ocean_background(game.screen)

            # Título da tela
            title_text = game.menu_big_font.render(
                "Selecione a Dificuldade", True, YELLOW
            )
            title_rect = title_text.get_rect(center=(WIDTH // 2, 140))
            game.screen.blit(title_text, title_rect)

            # Opções de dificuldade
            start_y = 280
            for i, option in enumerate(game.difficulty_options):
                color = YELLOW if i == game.difficulty_selected else WHITE
                option_text = game.menu_font.render(option, True, color)
                option_rect = option_text.get_rect(
                    center=(WIDTH // 2, start_y + i * 60)
                )

                if i == game.difficulty_selected:
                    pygame.draw.rect(
                        game.screen, DARK_BLUE, option_rect.inflate(20, 10)
                    )

                game.screen.blit(option_text, option_rect)

            # Instruções de controle
            instructions = [
                "↑↓ para escolher, Enter/A confirma",
                "ESC/B para voltar",
            ]
            for j, line in enumerate(instructions):
                inst_text = game.menu_small_font.render(line, True, LIGHT_GRAY)
                inst_rect = inst_text.get_rect(
                    center=(WIDTH // 2, HEIGHT - 100 + j * 30)
                )
                game.screen.blit(inst_text, inst_rect)

        elif game.state == GameState.PLAYING:
            self.draw_ocean_background(game.screen)

            # Desenhar plataformas com offset da câmera
            for platform in game.platforms:
                adjusted_rect = pygame.Rect(
                    platform.rect.x - game.camera_x,
                    platform.rect.y,
                    platform.rect.width,
                    platform.rect.height,
                )
                if (
                    adjusted_rect.right > 0 and adjusted_rect.left < WIDTH
                ):  # Só desenhar se visível
                    # Salvar posição original da plataforma
                    original_x = platform.x
                    # Ajustar posição para câmera
                    platform.x = adjusted_rect.x
                    # Usar o método draw da plataforma que faz ladrilhamento correto
                    platform.draw(game.screen)
                    # Restaurar posição original
                    platform.x = original_x

            # Desenhar bandeira com offset da câmera
            if game.flag:  # Verificar se a bandeira existe
                flag_x = game.flag.x - game.camera_x
                if flag_x > -50 and flag_x < WIDTH:  # Só desenhar se visível
                    # Salvar posição original da bandeira
                    original_x = game.flag.x
                    # Ajustar posição temporariamente para o offset da câmera
                    game.flag.x = flag_x
                    # Desenhar usando o método da classe Flag
                    game.flag.draw(game.screen)
                    # Restaurar posição original
                    game.flag.x = original_x

            # Desenhar spaceship com offset da câmera (fase 50)
            if game.spaceship:  # Verificar se a spaceship existe
                spaceship_x = game.spaceship.x - game.camera_x
                if spaceship_x > -150 and spaceship_x < WIDTH:  # Só desenhar se visível
                    # Salvar posição original da spaceship
                    original_spaceship_x = game.spaceship.x
                    original_spaceship_y = game.spaceship.y
                    # Ajustar posição temporariamente para o offset da câmera usando update_position
                    game.spaceship.update_position(spaceship_x, game.spaceship.y)
                    # Desenhar usando o método da classe Spaceship
                    game.spaceship.draw(game.screen)
                    # Restaurar posição original usando update_position
                    game.spaceship.update_position(
                        original_spaceship_x, original_spaceship_y
                    )

            # Desenhar pássaros, morcegos e estrelas (1–20) com offset da câmera
            if game.current_level <= 20:
                # Pássaros (1–16)
                for bird in game.birds:
                    bird_x = bird.x - game.camera_x
                    if bird_x > -50 and bird_x < WIDTH:  # Só desenhar se visível
                        original_bird_x = bird.x
                        bird.x = bird_x
                        bird.draw(game.screen)
                        bird.x = original_bird_x
                # Gotas de chuva (7–10)
                if 7 <= game.current_level <= 10 and hasattr(game, "raindrops"):
                    for drop in game.raindrops:
                        drop_x = drop.x - game.camera_x
                        if drop_x > -30 and drop_x < WIDTH + 30:
                            original_drop_x = drop.x
                            drop.x = drop_x
                            drop.draw(game.screen, game.camera_x)
                            drop.x = original_drop_x
                # Morcegos e estrelas (17–20)
                if game.current_level >= 17:
                    # Morcegos
                    for bat in game.bats:
                        bat_x = bat.x - game.camera_x
                        if bat_x > -50 and bat_x < WIDTH:
                            original_bat_x = bat.x
                            bat.x = bat_x
                            bat.draw(game.screen)
                            bat.x = original_bat_x
                    # Estrelas cadentes
                    if hasattr(game, "shooting_stars"):
                        for star in game.shooting_stars:
                            star_x = star.x - game.camera_x
                            if star_x > -60 and star_x < WIDTH + 20:
                                original_star_x = star.x
                                star.x = star_x
                                star.draw(game.screen)
                                star.x = original_star_x
            elif game.current_level <= 30:
                for bat in game.bats:
                    bat_x = bat.x - game.camera_x
                    if bat_x > -50 and bat_x < WIDTH:  # Só desenhar se visível
                        # Salvar posição original do morcego
                        original_bat_x = bat.x
                        # Ajustar posição para câmera
                        bat.x = bat_x
                        # Chamar método draw do morcego
                        bat.draw(game.screen)
                        # Restaurar posição original
                        bat.x = original_bat_x
                if 27 <= game.current_level <= 30:
                    for drop in getattr(game, "lava_drops", []):
                        drop_x = drop.x - game.camera_x
                        if drop_x > -30 and drop_x < WIDTH + 30:
                            original_drop_x = drop.x
                            drop.x = drop_x
                            drop.draw(game.screen, game.camera_x)
                            drop.x = original_drop_x
                # Shooting stars (21-30)
                if hasattr(game, "shooting_stars"):
                    for star in game.shooting_stars:
                        star_x = star.x - game.camera_x
                        if star_x > -60 and star_x < WIDTH + 20:
                            original_star_x = star.x
                            star.x = star_x
                            star.draw(game.screen)
                            star.x = original_star_x
            elif game.current_level <= 40:
                for airplane in game.airplanes:
                    airplane_x = airplane.x - game.camera_x
                    if (
                        airplane_x > -60 and airplane_x < WIDTH
                    ):  # Só desenhar se visível
                        # Salvar posição original do avião
                        original_airplane_x = airplane.x
                        # Ajustar posição para câmera
                        airplane.x = airplane_x
                        # Chamar método draw do avião
                        airplane.draw(game.screen)
                        # Restaurar posição original
                        airplane.x = original_airplane_x
            else:
                for disk in game.flying_disks:
                    disk_x = disk.x - game.camera_x
                    if disk_x > -60 and disk_x < WIDTH:  # Só desenhar se visível
                        # Salvar posição original do disco
                        original_disk_x = disk.x
                        # Ajustar posição para câmera
                        disk.x = disk_x
                        # Chamar método draw do disco
                        disk.draw(game.screen)
                        # Restaurar posição original
                        disk.x = original_disk_x

            # Desenhar foguinhos com offset da câmera (nível 51)
            if game.current_level == 51:
                for fire in game.fires:
                    fire_x = fire.x - game.camera_x
                    if fire_x > -40 and fire_x < WIDTH:  # Só desenhar se visível
                        # Salvar posição original do foguinho
                        original_fire_x = fire.x
                        # Ajustar posição para câmera
                        fire.x = fire_x
                        # Chamar método draw do foguinho
                        fire.draw(game.screen)
                        # Restaurar posição original
                        fire.x = original_fire_x

            # Desenhar tartarugas e aranhas com offset da câmera
            if game.current_level <= 20:
                for turtle in game.turtles:
                    turtle_x = turtle.x - game.camera_x
                    if turtle_x > -50 and turtle_x < WIDTH:  # Só desenhar se visível
                        # Salvar posição original da tartaruga
                        original_turtle_x = turtle.x
                        # Ajustar posição para câmera
                        turtle.x = turtle_x
                        # Chamar método draw da tartaruga
                        turtle.draw(game.screen)
                        # Restaurar posição original
                        turtle.x = original_turtle_x
            else:
                for spider in game.spiders:
                    spider_x = spider.x - game.camera_x
                    if spider_x > -50 and spider_x < WIDTH:  # Só desenhar se visível
                        # Salvar posição original da aranha
                        original_spider_x = spider.x
                        # Ajustar posição para câmera
                        spider.x = spider_x
                        # Chamar método draw da aranha
                        spider.draw(game.screen)
                        # Restaurar posição original
                        spider.x = original_spider_x

            # Desenhar robôs e seus mísseis com offset da câmera (níveis 31-40)
            if 31 <= game.current_level <= 40 and not game.player.is_being_abducted:
                for robot in game.robots:
                    robot_x = robot.x - game.camera_x
                    if robot_x > -50 and robot_x < WIDTH:  # Só desenhar se visível
                        # Salvar posição original do robô
                        original_robot_x = robot.x
                        # Ajustar posição para câmera
                        robot.x = robot_x
                        # Chamar método draw do robô (que também desenha os mísseis)
                        robot.draw(game.screen)
                        # Restaurar posição original
                        robot.x = original_robot_x

                        # Desenhar mísseis do robô com offset da câmera
                        for missile in robot.missiles:
                            missile_x = missile.x - game.camera_x
                            if (
                                missile_x > -20 and missile_x < WIDTH + 20
                            ):  # Só visíveis
                                # Salvar posição original do míssil
                                original_missile_x = missile.x
                                # Ajustar posição para câmera
                                missile.x = missile_x
                                # Chamar método draw do míssil
                                missile.draw(game.screen)
                                # Restaurar posição original
                                missile.x = original_missile_x

                # Desenhar mísseis órfãos (de robôs mortos) com offset da câmera
                for missile in game.orphan_missiles:
                    missile_x = missile.x - game.camera_x
                    if missile_x > -20 and missile_x < WIDTH + 20:  # Só visíveis
                        # Salvar posição original do míssil
                        original_missile_x = missile.x
                        # Ajustar posição para câmera
                        missile.x = missile_x
                        # Chamar método draw do míssil
                        missile.draw(game.screen)
                        # Restaurar posição original
                        missile.x = original_missile_x

            # Desenhar aliens e seus lasers com offset da câmera (níveis 41-50)
            if 41 <= game.current_level <= 50 and not game.player.is_being_abducted:
                for alien in game.aliens:
                    alien_x = alien.x - game.camera_x
                    if alien_x > -50 and alien_x < WIDTH:  # Só desenhar se visível
                        # Salvar posição original do alien
                        original_alien_x = alien.x
                        # Ajustar posição para câmera
                        alien.x = alien_x
                        # Chamar método draw do alien
                        alien.draw(game.screen)
                        # Restaurar posição original
                        alien.x = original_alien_x

                        # Desenhar lasers do alien com offset da câmera
                        for laser in alien.lasers:
                            laser_x = laser.x - game.camera_x
                            if laser_x > -20 and laser_x < WIDTH + 20:  # Só visíveis
                                # Salvar posição original do laser
                                original_laser_x = laser.x
                                # Ajustar posição para câmera
                                laser.x = laser_x
                                # Chamar método draw do laser
                                laser.draw(game.screen)
                                # Restaurar posição original
                                laser.x = original_laser_x

                # Desenhar lasers órfãos (de aliens mortos) com offset da câmera
                for laser in game.orphan_lasers:
                    laser_x = laser.x - game.camera_x
                    if laser_x > -20 and laser_x < WIDTH + 20:  # Só visíveis
                        # Salvar posição original do laser
                        original_laser_x = laser.x
                        # Ajustar posição para câmera
                        laser.x = laser_x
                        # Chamar método draw do laser
                        laser.draw(game.screen)
                        # Restaurar posição original
                        laser.x = original_laser_x

            # Desenhar boss alien com offset da câmera (nível 51)
            if (
                game.current_level == 51
                and hasattr(game, "boss_alien")
                and game.boss_alien
                and not game.player.is_being_abducted
            ):
                boss_x = game.boss_alien.x - game.camera_x
                if boss_x > -100 and boss_x < WIDTH + 100:  # Só desenhar se visível
                    # Salvar posição original do boss
                    original_boss_x = game.boss_alien.x
                    # Ajustar posição para câmera
                    game.boss_alien.x = boss_x

                    # Desenhar boss alien com efeito de piscada durante captura
                    if game.boss_alien_captured and hasattr(
                        game, "capture_flash_state"
                    ):
                        # Só desenhar se não estiver piscando (estado False)
                        if not game.capture_flash_state:
                            game.boss_alien.draw(game.screen)
                    else:
                        # Desenhar normalmente se não foi capturado
                        game.boss_alien.draw(game.screen)

                    # Restaurar posição original
                    game.boss_alien.x = original_boss_x

            # Desenhar explosões com offset da câmera
            for explosion in game.explosions:
                explosion_x = explosion.x - game.camera_x
                if explosion_x > -50 and explosion_x < WIDTH:  # Só desenhar se visível
                    # Salvar posição original da explosão
                    original_explosion_x = explosion.x
                    # Ajustar posição para câmera
                    explosion.x = explosion_x
                    # Chamar método draw da explosão
                    explosion.draw(game.screen)
                    # Restaurar posição original
                    explosion.x = original_explosion_x

            # Desenhar vidas extras com offset da câmera
            if hasattr(game, "extra_lives") and game.extra_lives:
                for extra_life in game.extra_lives:
                    extra_life_x = extra_life.x - game.camera_x
                    if extra_life_x > -30 and extra_life_x < WIDTH + 30:  # Só visíveis
                        # Chamar método draw da vida extra com offset da câmera
                        extra_life.draw(game.screen, game.camera_x)

            # Desenhar power-ups com offset da câmera
            if hasattr(game, "powerups") and game.powerups:
                for pu in game.powerups:
                    pu_x = pu.x - game.camera_x
                    if pu_x > -30 and pu_x < WIDTH + 30:
                        pu.draw(game.screen, game.camera_x)

            # Desenhar tiros do jogador com offset da câmera
            for bullet in game.player.bullets:
                bullet_x = bullet.x - game.camera_x
                if bullet_x > -20 and bullet_x < WIDTH + 20:  # Só desenhar se visível
                    # Salvar posição original do tiro
                    original_bullet_x = bullet.x
                    # Ajustar posição para câmera
                    bullet.x = bullet_x
                    # Chamar método draw do tiro
                    bullet.draw(game.screen)
                    # Restaurar posição original
                    bullet.x = original_bullet_x

            # Desenhar jogador com offset da câmera
            original_x = game.player.x  # Salvar posição original
            game.player.x = game.player.x - game.camera_x  # Ajustar posição para câmera
            game.player.draw(game.screen)  # Desenhar jogador
            # Desenhar bolha do escudo sobre o jogador
            if getattr(game, "shield_active", False) and getattr(
                game, "shield_bubble_img", None
            ):
                try:
                    bubble_w = max(24, int(getattr(game.player, "width", 65) + 12))
                    bubble_h = max(24, int(getattr(game.player, "height", 95) + 12))
                    bubble_img = pygame.transform.smoothscale(
                        game.shield_bubble_img, (bubble_w, bubble_h)
                    )
                except Exception:
                    bubble_img = pygame.transform.scale(
                        game.shield_bubble_img, (bubble_w, bubble_h)
                    )
                bubble_x = int(
                    game.player.x - (bubble_w - getattr(game.player, "width", 65)) // 2
                )
                bubble_y = int(
                    game.player.y - (bubble_h - getattr(game.player, "height", 95)) // 2
                )
                try:
                    game.screen.blit(bubble_img, (bubble_x, bubble_y))
                except Exception:
                    pass
            game.player.x = original_x  # Restaurar posição original

            # Desenhar UI (sem offset da câmera) com fonte branca
            Info.display(game, game.screen, game.font, WHITE)

        elif game.state == GameState.GAME_OVER:
            # Usar fundo do cenário, explicitamente na surface do jogo
            self.draw_ocean_background(Screen.get_game_surface(game))

            # Usar o padrão de fontes do menu para manter consistência visual
            game_over_text = game.menu_big_font.render("GAME OVER", True, RED)
            score_text = game.menu_font.render(
                f"Pontuação Final: {game.score}", True, WHITE
            )

            # Centralizar textos principais
            game_over_rect = game_over_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 - 120)
            )
            score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 60))

            game.screen.blit(game_over_text, game_over_rect)
            game.screen.blit(score_text, score_rect)

            # Menu de opções
            for i, option in enumerate(game.game_over_options):
                color = YELLOW if i == game.game_over_selected else WHITE
                option_text = game.menu_font.render(option, True, color)
                option_rect = option_text.get_rect(
                    center=(WIDTH // 2, HEIGHT // 2 + i * 40)
                )

                if i == game.game_over_selected:
                    pygame.draw.rect(
                        game.screen, DARK_BLUE, option_rect.inflate(20, 10)
                    )

                game.screen.blit(option_text, option_rect)

            control_text = game.menu_small_font.render(
                "Use ↑↓ ou D-pad para navegar, Enter ou A para selecionar",
                True,
                LIGHT_GRAY,
            )
            control_rect = control_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 120))
            game.screen.blit(control_text, control_rect)

        elif game.state == GameState.VICTORY:
            # Desenhar troféu
            trophy_x = WIDTH // 2
            trophy_y = HEIGHT // 2 - 100
            pygame.draw.rect(game.screen, BROWN, (trophy_x - 40, trophy_y + 80, 80, 20))
            pygame.draw.rect(game.screen, BROWN, (trophy_x - 10, trophy_y + 60, 20, 40))
            pygame.draw.ellipse(game.screen, YELLOW, (trophy_x - 30, trophy_y, 60, 80))
            pygame.draw.ellipse(
                game.screen, (255, 215, 0), (trophy_x - 25, trophy_y + 5, 50, 70)
            )
            pygame.draw.arc(
                game.screen,
                YELLOW,
                (trophy_x - 50, trophy_y + 20, 20, 40),
                0,
                math.pi,
                5,
            )
            pygame.draw.arc(
                game.screen,
                YELLOW,
                (trophy_x + 30, trophy_y + 20, 20, 40),
                0,
                math.pi,
                5,
            )

            victory_text = game.big_font.render("PARABÉNS!", True, GREEN)
            complete_text = game.font.render(
                "Você completou todos os níveis!", True, WHITE
            )
            final_score_text = game.font.render(
                f"Pontuação Final: {game.score}", True, WHITE
            )
            restart_text = game.font.render(
                "Pressione R para jogar novamente", True, WHITE
            )
            game.screen.blit(victory_text, (WIDTH // 2 - 150, HEIGHT // 2 + 120))
            game.screen.blit(complete_text, (WIDTH // 2 - 200, HEIGHT // 2 + 170))
            game.screen.blit(final_score_text, (WIDTH // 2 - 120, HEIGHT // 2 + 200))
            game.screen.blit(restart_text, (WIDTH // 2 - 180, HEIGHT // 2 + 240))

        elif game.state == GameState.ENTER_NAME:
            title_text = game.big_font.render("NOVO RECORDE!", True, YELLOW)
            score_text = game.font.render(f"Pontuação: {game.score}", True, WHITE)
            prompt_text = game.font.render(
                "Digite seu nome (máximo 25 caracteres):", True, WHITE
            )
            name_display = (
                game.player_name + "_"
                if len(game.player_name) < 25
                else game.player_name
            )
            name_text = game.font.render(name_display, True, WHITE)
            instruction_text = game.font.render(
                "Pressione ENTER para confirmar", True, LIGHT_GRAY
            )
            title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
            score_rect = score_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
            prompt_rect = prompt_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            name_rect = name_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            instruction_rect = instruction_text.get_rect(
                center=(WIDTH // 2, HEIGHT // 2 + 50)
            )
            input_box = pygame.Rect(WIDTH // 2 - 200, HEIGHT // 2 - 15, 400, 30)
            pygame.draw.rect(game.screen, DARK_GRAY, input_box)
            pygame.draw.rect(game.screen, WHITE, input_box, 2)
            game.screen.blit(title_text, title_rect)
            game.screen.blit(score_text, score_rect)
            game.screen.blit(prompt_text, prompt_rect)
            game.screen.blit(name_text, name_rect)
            game.screen.blit(instruction_text, instruction_rect)

        elif game.state == GameState.SHOW_RANKING:
            self.draw_ocean_background(game.screen)
            title_text = game.menu_font.render("TOP 10 RANKING", True, YELLOW)
            rankings = game.ranking_manager.get_rankings()
            title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
            game.screen.blit(title_text, title_rect)

            table_width = 520
            pos_x = WIDTH // 2 - table_width // 2
            header_pos = game.menu_content_font.render("POS", True, WHITE)
            header_name = game.menu_content_font.render("NOME", True, WHITE)
            header_score = game.menu_content_font.render("PONTUAÇÃO", True, WHITE)
            game.screen.blit(header_pos, (pos_x, 180))
            game.screen.blit(header_name, (pos_x + 60, 180))
            header_score_rect = header_score.get_rect()
            header_score_rect.right = pos_x + table_width
            header_score_rect.y = 180
            game.screen.blit(header_score, header_score_rect)
            header_line_y = (
                180
                + max(
                    header_pos.get_height(),
                    header_name.get_height(),
                    header_score.get_height(),
                )
                + 6
            )
            pygame.draw.line(
                game.screen,
                WHITE,
                (pos_x, header_line_y),
                (pos_x + table_width, header_line_y),
                2,
            )
            y_offset = header_line_y + 30
            for i, ranking in enumerate(rankings, 1):
                color = YELLOW if ranking["name"] == game.player_name.strip() else WHITE
                pos_text = game.menu_content_font.render(f"{i:2d}.", True, color)
                game.screen.blit(pos_text, (pos_x, y_offset))
                name_display = ranking["name"]
                score_min_width = game.menu_content_font.size("888.888.888")[0]
                name_max_width = table_width - 60 - score_min_width - 20
                while (
                    len(name_display) > 0
                    and game.menu_content_font.size(
                        name_display + ("…" if name_display != ranking["name"] else "")
                    )[0]
                    > name_max_width
                ):
                    name_display = name_display[:-1]
                if name_display != ranking["name"]:
                    name_display = name_display + "…"
                name_text = game.menu_content_font.render(name_display, True, color)
                game.screen.blit(name_text, (pos_x + 60, y_offset))
                score_display = f"{int(ranking['score']):,}".replace(",", ".")
                score_text = game.menu_content_font.render(score_display, True, color)
                score_rect = score_text.get_rect()
                score_rect.right = pos_x + table_width
                score_rect.y = y_offset
                game.screen.blit(score_text, score_rect)
                y_offset += 35
            restart_text = game.menu_small_font.render(
                "Pressione R para jogar novamente", True, LIGHT_GRAY
            )
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT - 80))
            game.screen.blit(restart_text, restart_rect)
            back_text = game.menu_small_font.render(
                "Pressione ESC ou Botão B para voltar", True, LIGHT_GRAY
            )
            back_rect = back_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
            game.screen.blit(back_text, back_rect)

        elif game.state == GameState.FIM_SCREEN:
            game.screen.fill(BLACK)
            fim_text = pygame.font.Font(None, 120).render("FIM", True, WHITE)
            fim_rect = fim_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            game.screen.blit(fim_text, fim_rect)
            if game.fim_screen_timer > 60:
                skip_text = game.font.render(
                    "Pressione qualquer tecla para continuar", True, LIGHT_GRAY
                )
                skip_rect = skip_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
                game.screen.blit(skip_text, skip_rect)

        elif game.state == GameState.CREDITS:
            if game.credits_type == "menu":
                self.draw_ocean_background(game.screen)
                title_text = game.menu_font.render("CRÉDITOS", True, YELLOW)
                title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
                game.screen.blit(title_text, title_rect)
                menu_credits = [
                    "Desenvolvido por:",
                    "CirrasTec",
                    "",
                    "Em parceria com:",
                    "Cirras RetroGames",
                    "https://www.youtube.com/@cirrasretrogames",
                    "",
                    "Canal do Dudu",
                    "https://www.youtube.com/@canaldodudu14",
                    "",
                    "Obrigado por jogar!",
                ]
                y_offset = 200
                for line in menu_credits:
                    if line.startswith("https://"):
                        text_surface = game.menu_content_font.render(
                            line, True, LIGHT_BLUE
                        )
                    elif line in ["CirrasTec", "Cirras RetroGames", "Canal do Dudu"]:
                        text_surface = game.menu_content_font.render(line, True, YELLOW)
                    elif line != "":
                        text_surface = game.menu_content_font.render(line, True, WHITE)
                    else:
                        y_offset += 20
                        continue
                    text_rect = text_surface.get_rect(center=(WIDTH // 2, y_offset))
                    game.screen.blit(text_surface, text_rect)
                    y_offset += 40
                instruction_text = game.menu_small_font.render(
                    "Pressione ESC ou ENTER para voltar", True, LIGHT_GRAY
                )
                instruction_rect = instruction_text.get_rect(
                    center=(WIDTH // 2, HEIGHT - 50)
                )
                game.screen.blit(instruction_text, instruction_rect)
            else:
                game.screen.fill(BLACK)
                credits_content = [
                    "",
                    "",
                    "",
                    "JUMP & HIT",
                    "",
                    "",
                    "Um jogo de plataforma 2D",
                    "inspirado nos clássicos dos anos 80 e 90",
                    "",
                    "",
                    "═══════════════════════════════════════",
                    "",
                    "DESENVOLVIDO POR",
                    "",
                    "CirrasTec",
                    "",
                    "═══════════════════════════════════════",
                    "",
                    "EM PARCERIA COM",
                    "",
                    "Cirras RetroGames",
                    "https://www.youtube.com/@cirrasretrogames",
                    "",
                    "Canal do Dudu",
                    "https://www.youtube.com/@canaldodudu14",
                    "",
                    "═══════════════════════════════════════",
                    "",
                    "PROGRAMAÇÃO E DESIGN",
                    "",
                    "Cirras",
                    "Dudu",
                    "",
                    "═══════════════════════════════════════",
                    "",
                    "ARTE E GRÁFICOS",
                    "",
                    "Cirras",
                    "",
                    "═══════════════════════════════════════",
                    "",
                    "ÁUDIO E MÚSICA",
                    "",
                    "Cirras",
                    "",
                    "═══════════════════════════════════════",
                    "",
                    "NÍVEIS E GAMEPLAY",
                    "",
                    "Cirras",
                    "Dudu",
                    "Aline",
                    "",
                    "═══════════════════════════════════════",
                    "",
                    "TECNOLOGIAS UTILIZADAS",
                    "",
                    "Python 3.x",
                    "Pygame",
                    "Trae",
                    "Suno",
                    "Canva",
                    "",
                    "═══════════════════════════════════════",
                    "",
                    "AGRADECIMENTOS ESPECIAIS",
                    "",
                    "À comunidade retrogaming",
                    "Aos jogadores que testaram o jogo",
                    "Aos criadores dos jogos clássicos",
                    "que nos inspiraram",
                    "",
                    "═══════════════════════════════════════",
                    "",
                    "MENSAGEM FINAL",
                    "",
                    "Este jogo foi criado com paixão e dedicação,",
                    "combinando a nostalgia dos jogos clássicos",
                    "com elementos modernos de gameplay.",
                    "",
                    "Esperamos que você tenha se divertido",
                    "tanto quanto nós nos divertimos criando!",
                    "",
                    "Continue jogando, continue sonhando!",
                    "",
                    "═══════════════════════════════════════",
                    "",
                    "© 2025 CirrasTec",
                    "Todos os direitos reservados",
                    "",
                    "",
                    "Obrigado por jogar!",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                    "",
                ]
                y_start = HEIGHT - game.credits_scroll_y
                line_height = 35
                for i, line in enumerate(credits_content):
                    y_pos = y_start + (i * line_height)
                    if y_pos > -50 and y_pos < HEIGHT + 50:
                        if line == "JUMP & HIT":
                            title_font = pygame.font.Font(None, 96)
                            text_surface = title_font.render(line, True, YELLOW)
                        elif line.startswith("═══"):
                            text_surface = game.font.render(line, True, DARK_GRAY)
                        elif line.startswith("https://"):
                            text_surface = game.font.render(line, True, LIGHT_BLUE)
                        elif line in [
                            "DESENVOLVIDO POR",
                            "EM PARCERIA COM",
                            "PROGRAMAÇÃO E DESIGN",
                            "ARTE E GRÁFICOS",
                            "ÁUDIO E MÚSICA",
                            "NÍVEIS E GAMEPLAY",
                            "TECNOLOGIAS UTILIZADAS",
                            "AGRADECIMENTOS ESPECIAIS",
                            "MENSAGEM FINAL",
                        ]:
                            section_font = pygame.font.Font(None, 48)
                            text_surface = section_font.render(line, True, CYAN)
                        elif line in [
                            "CirrasTec",
                            "Cirras RetroGames",
                            "Canal do Dudu",
                        ]:
                            text_surface = game.font.render(line, True, YELLOW)
                        elif (
                            line == "© 2025 CirrasTec"
                            or line == "Todos os direitos reservados"
                        ):
                            text_surface = game.font.render(line, True, LIGHT_GRAY)
                        elif line == "Obrigado por jogar!":
                            final_font = pygame.font.Font(None, 56)
                            text_surface = final_font.render(line, True, YELLOW)
                        elif line != "":
                            text_surface = game.font.render(line, True, WHITE)
                        else:
                            continue
                        text_rect = text_surface.get_rect(center=(WIDTH // 2, y_pos))
                        game.screen.blit(text_surface, text_rect)
                total_credits_height = len(credits_content) * line_height
                if game.credits_scroll_y > total_credits_height + HEIGHT:
                    pygame.mixer.music.stop()
                    game.state = GameState.MAIN_MENU
                    game.music.play_menu_music(game)
                    game.credits_scroll_y = 0
                    game.credits_reset_timer = 0

        elif game.state == GameState.RECORDS:
            game.draw_ocean_background(game.screen)
            title_text = game.menu_font.render("RECORDES", True, YELLOW)
            rankings = game.ranking_manager.get_rankings()
            title_rect = title_text.get_rect(center=(WIDTH // 2, 100))
            game.screen.blit(title_text, title_rect)
            table_width = 520
            pos_x = WIDTH // 2 - table_width // 2
            header_pos = game.menu_content_font.render("POS", True, WHITE)
            header_name = game.menu_content_font.render("NOME", True, WHITE)
            header_score = game.menu_content_font.render("PONTUAÇÃO", True, WHITE)
            game.screen.blit(header_pos, (pos_x, 180))
            game.screen.blit(header_name, (pos_x + 60, 180))
            header_score_rect = header_score.get_rect()
            header_score_rect.right = pos_x + table_width
            header_score_rect.y = 180
            game.screen.blit(header_score, header_score_rect)
            header_line_y = (
                180
                + max(
                    header_pos.get_height(),
                    header_name.get_height(),
                    header_score.get_height(),
                )
                + 6
            )
            pygame.draw.line(
                game.screen,
                WHITE,
                (pos_x, header_line_y),
                (pos_x + table_width, header_line_y),
                2,
            )
            y_offset = header_line_y + 30
            for i, ranking in enumerate(rankings, 1):
                color = WHITE
                pos_text = game.menu_content_font.render(f"{i:2d}.", True, color)
                game.screen.blit(pos_text, (pos_x, y_offset))
                name_display = ranking["name"]
                score_min_width = game.menu_content_font.size("888.888.888")[0]
                name_max_width = table_width - 60 - score_min_width - 20
                while (
                    len(name_display) > 0
                    and game.menu_content_font.size(
                        name_display + ("…" if name_display != ranking["name"] else "")
                    )[0]
                    > name_max_width
                ):
                    name_display = name_display[:-1]
                if name_display != ranking["name"]:
                    name_display = name_display + "…"
                name_text = game.menu_content_font.render(name_display, True, color)
                game.screen.blit(name_text, (pos_x + 60, y_offset))
                score_display = f"{int(ranking['score']):,}".replace(",", ".")
                score_text = game.menu_content_font.render(score_display, True, color)
                score_rect = score_text.get_rect()
                score_rect.right = pos_x + table_width
                score_rect.y = y_offset
                game.screen.blit(score_text, score_rect)
                y_offset += 35
            instruction_text = game.menu_small_font.render(
                "Pressione ESC ou ENTER para voltar", True, LIGHT_GRAY
            )
            instruction_rect = instruction_text.get_rect(
                center=(WIDTH // 2, HEIGHT - 50)
            )
            game.screen.blit(instruction_text, instruction_rect)

        # Overlay de esmaecimento durante hold (fade progressivo)
        if getattr(game, "hold_active", False):
            try:
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.fill(BLACK)
                total = max(1, getattr(game, "hold_total_frames", 1))
                elapsed = total - max(0, game.hold_frames_left)
                progress = min(1.0, max(0.0, elapsed / float(total)))
                target_alpha = 0.6 if game.hold_type == "level_end" else 0.4
                overlay.set_alpha(int(255 * target_alpha * progress))
                game.screen.blit(overlay, (0, 0))
            except Exception:
                pass

        Screen.present(game)
