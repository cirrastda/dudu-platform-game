import pygame
from internal.utils.constants import *
from internal.engine.state import GameState
from internal.engine.level.level import Level
from internal.resources.explosion import Explosion
from internal.resources.enemies.bird import Bird
from internal.resources.enemies.bat import Bat
from internal.resources.enemies.airplane import Airplane
from internal.resources.enemies.flying_disk import FlyingDisk
from internal.resources.enemies.fire import Fire
from internal.resources.enemies.shooting_star import ShootingStar
from internal.resources.enemies.raindrop import Raindrop
from internal.resources.enemies.lava_drop import LavaDrop


class Update:
    def __init__(self, game):
        self.game = game

    def update(self):
        g = self.game

        # Se estamos em hold, gerenciar contagem.
        if getattr(g, "hold_active", False):
            if g.hold_frames_left > 0:
                g.hold_frames_left -= 1
            else:
                # fim do hold
                g.hold_active = False
                # Restaurar volume da música se foi reduzido
                try:
                    if g._music_duck_original_volume is not None:
                        pygame.mixer.music.set_volume(g._music_duck_original_volume)
                        g._music_duck_original_volume = None
                except Exception:
                    pass
                if g.hold_type == "level_end":
                    # Agora avançamos de fase somente após o hold terminar
                    try:
                        if getattr(g, "_next_level_after_hold", False):
                            if g.current_level < g.max_levels:
                                g.current_level += 1
                                Level.init_level(g)
                                # Tocar música do novo nível
                                g.music.play_level_music(g, g.current_level)
                            else:
                                # Vitória - verificar se entra no ranking
                                if g.ranking_manager.is_high_score(g.score):
                                    g.state = GameState.ENTER_NAME
                                else:
                                    g.state = GameState.VICTORY
                    except Exception:
                        pass
                    finally:
                        g._next_level_after_hold = False
                    g.hold_type = None
                elif g.hold_type == "game_over":
                    # Para game over, não bloqueamos atualização; apenas removemos o esmaecimento
                    g.hold_type = None

        if g.state == GameState.SPLASH:
            # Atualizar timer do splash screen
            g.splash_timer += 1

            # Calcular qual logo mostrar baseado no tempo com fade
            if g.logos:
                g.current_logo_index = (g.splash_timer // g.logo_display_time) % len(
                    g.logos
                )

            # Após o tempo total, ir para a tela de título
            if g.splash_timer >= g.splash_duration:
                g.state = GameState.TITLE_SCREEN

        elif g.state == GameState.OPENING_VIDEO:
            # Atualizar reprodução do vídeo
            g.video_player.update()

            # Verificar se o vídeo terminou
            if g.video_player.is_finished():
                g.video_player.cleanup()
                g.state = GameState.MAIN_MENU
                # Iniciar música do menu
                if not g.music_started:
                    g.music.play_menu_music(g)
                    g.music_started = True

        elif g.state == GameState.ENDING_VIDEO:
            # Carregar vídeo de ending se ainda não foi carregado
            if not hasattr(g, "ending_video_loaded"):
                if g.ending_video_player.load_video("videos/ending.mp4"):
                    g.ending_video_loaded = True
                    # Iniciar reprodução do vídeo
                    g.ending_video_player.start_playback()
                else:
                    # Se não conseguir carregar o vídeo, ir direto para tela FIM
                    g.state = GameState.FIM_SCREEN
                    g.fim_screen_timer = 0

            # Atualizar reprodução do vídeo de ending
            if hasattr(g, "ending_video_loaded") and g.ending_video_loaded:
                g.ending_video_player.update()

                # Verificar se o vídeo terminou
                if g.ending_video_player.is_finished():
                    g.ending_video_player.cleanup()
                    g.state = GameState.FIM_SCREEN
                    # Inicializar timer para a tela FIM
                    g.fim_screen_timer = 0

        elif g.state == GameState.FIM_SCREEN:
            # Atualizar timer da tela FIM
            g.fim_screen_timer += 1

            # Após 3 segundos (180 frames a 60 FPS), ir para os créditos
            if g.fim_screen_timer >= 180:
                g.state = GameState.CREDITS
                g.credits_type = "ending"
                g.music.play_music("credits")
                # Resetar rolagem dos créditos
                g.credits_scroll_y = 0
                g.credits_reset_timer = 0

        elif g.state == GameState.CREDITS:
            # Atualizar rolagem dos créditos
            g.credits_scroll_y += g.credits_scroll_speed
            g.credits_reset_timer += 1

            # Resetar rolagem apenas para créditos do menu (loop contínuo)
            if (
                g.credits_type == "menu" and g.credits_reset_timer >= 1800
            ):  # 30 segundos a 60 FPS
                g.credits_scroll_y = 0
                g.credits_reset_timer = 0

        elif g.state == GameState.PLAYING:
            # Congelar toda a jogabilidade durante holds de transição (fim de fase / game over)
            if getattr(g, "hold_active", False) and g.hold_type in (
                "level_end",
                "game_over",
            ):
                return

            # Atualizar jogador
            player_action = g.player.update(
                g.platforms,
                g.image.bullet_image,
                g.camera_x,
                g.joystick if g.joystick_connected else None,
                g,
            )

            # Verificar ações do jogador e tocar sons
            if player_action == "jump":
                g.sound_effects.play_sound_effect("jump")
            elif player_action == "shot":
                g.sound_effects.play_sound_effect("shot")

            # Verificar se jogador morreu (retorno False)
            if player_action is False:
                # Jogador morreu (caiu da tela) - decrementar vida
                g.lives -= 1
                if g.lives <= 0:
                    # Disparar rotina de game over imediatamente e esmaecer enquanto o som toca
                    if g.ranking_manager.is_high_score(g.score):
                        g.state = GameState.ENTER_NAME
                    else:
                        g.state = GameState.GAME_OVER
                    g.start_game_over_hold()
                else:
                    # Ainda tem vidas, reiniciar nível atual
                    Level.init_level(g)
                    # Tocar música do nível atual
                    g.music.play_level_music(g, g.current_level)

            # Restaurar música quando a invencibilidade terminar
            if (
                getattr(g, "invincibility_active", False)
                and not g.player.is_invulnerable
            ):
                g.invincibility_active = False
                try:
                    g.music.exit_invincibility_music(g)
                except Exception:
                    pass

            # Atualizar câmera para seguir o jogador
            target_camera_x = g.player.x - CAMERA_OFFSET_X
            if target_camera_x > g.camera_x:
                g.camera_x = target_camera_x

            # Sistema de pontuação - verificar se jogador pousou em nova plataforma
            if g.player.just_landed and hasattr(g.player, "landed_platform_id"):
                if g.player.landed_platform_id not in g.platforms_jumped:
                    g.platforms_jumped.add(g.player.landed_platform_id)
                    g.add_score(10)
                # Reset da flag após verificar pontuação
                g.player.just_landed = False

            # Atualizar e verificar coleta de itens de vida
            if hasattr(g, "extra_lives") and g.extra_lives:
                remaining_items = []
                for item in g.extra_lives:
                    item.update()
                    if g.player.rect.colliderect(item.rect):
                        # Jogador coletou vida extra
                        g.lives += 1
                        # Marcar vida extra como coletada neste nível
                        if hasattr(g, "collected_extra_life_levels"):
                            g.collected_extra_life_levels.add(g.current_level)
                        if hasattr(g, "sound_effects"):
                            try:
                                g.sound_effects.play_sound_effect("new-life")
                            except Exception:
                                pass
                    else:
                        remaining_items.append(item)
                g.extra_lives = remaining_items
                # Remover atributo de plataforma pousada se existir, para evitar recontagem
                if hasattr(g.player, "landed_platform_id"):
                    delattr(g.player, "landed_platform_id")

            # Atualizar e verificar coleta de power-ups
            if hasattr(g, "powerups") and g.powerups:
                remaining_powerups = []
                for pu in g.powerups:
                    pu.update()
                    if g.player.rect.colliderect(pu.rect):
                        kind = pu.spec.kind
                        if kind == "invencibilidade":
                            # 20 segundos de invencibilidade
                            g.player.is_invulnerable = True
                            g.player.invulnerability_timer = 20 * FPS
                            g.invincibility_active = True
                            # Música acelerada simulada: trocar para faixa rápida
                            try:
                                g.music.enter_invincibility_music(g)
                            except Exception:
                                pass
                        elif kind == "pulo_duplo":
                            # 70 segundos de pulo duplo
                            g.player.double_jump_enabled = True
                            g.player.double_jump_frames_left = 70 * FPS
                            # Reset dos saltos disponíveis no próximo pouso
                        elif kind == "escudo":
                            # Ativar escudo até ser consumido
                            g.shield_active = True
                        # Efeito sonoro de coleta
                        if hasattr(g, "sound_effects"):
                            try:
                                g.sound_effects.play_sound_effect("collect")
                            except Exception:
                                pass
                    else:
                        remaining_powerups.append(pu)
                g.powerups = remaining_powerups

            # Sistema de pássaros, chuva, morcegos e estrelas
            if g.current_level <= 20:
                if g.current_level <= 16:
                    # Spawn de pássaros (níveis 1-16)
                    g.bird_spawn_timer += 1
                    if g.bird_spawn_timer >= g.bird_spawn_interval:
                        import random

                        for i in range(g.birds_per_spawn):
                            bird_y = random.randint(HEIGHT // 4, HEIGHT - 150)
                            bird_x = g.camera_x + WIDTH + 50 + (i * 100)
                            bird_images = (
                                (g.image.bird_img1, g.image.bird_img2)
                                if hasattr(g.image, "bird_img1")
                                else None
                            )
                            g.birds.append(Bird(bird_x, bird_y, bird_images))
                        g.bird_spawn_timer = 0
                    # Spawn de gotas de chuva nas fases 7-10
                    if 7 <= g.current_level <= 10:
                        g.raindrop_spawn_timer += 1
                        if g.raindrop_spawn_timer >= g.raindrop_spawn_interval:
                            import random

                            for i in range(getattr(g, "raindrops_per_spawn", 1)):
                                drop_x = g.camera_x + random.randint(0, WIDTH)
                                drop_y = -20 - (i * 15)
                                drop_img = (
                                    g.image.raindrop_img
                                    if hasattr(g.image, "raindrop_img")
                                    else None
                                )
                                g.raindrops.append(Raindrop(drop_x, drop_y, drop_img))
                            g.raindrop_spawn_timer = 0
                else:
                    # Níveis 17-20: spawn de morcegos e estrelas cadentes
                    # Morcegos
                    g.bat_spawn_timer += 1
                    if g.bat_spawn_timer >= getattr(g, "bat_spawn_interval", 999999):
                        import random
                        # Verificar limite de morcegos visíveis para evitar acumulação excessiva
                        visible_count = 0
                        for bat in getattr(g, "bats", []):
                            if (
                                bat.x > g.camera_x - 200
                                and bat.x < g.camera_x + WIDTH + 200
                            ):
                                visible_count += 1

                        max_visible = getattr(g, "max_bats_visible", None)
                        if max_visible is None or visible_count < max_visible:
                            for i in range(getattr(g, "bats_per_spawn", 0)):
                                bat_y = random.randint(HEIGHT // 4, HEIGHT - 150)
                                bat_x = g.camera_x + WIDTH + 50 + (i * 100)
                                bat_images = (
                                    (g.image.bat_img1, g.image.bat_img2, g.image.bat_img3)
                                    if hasattr(g.image, "bat_img1")
                                    else None
                                )
                                g.bats.append(Bat(bat_x, bat_y, bat_images))
                            g.bat_spawn_timer = 0
                    # Estrelas cadentes
                    g.shooting_star_spawn_timer += 1
                    if g.shooting_star_spawn_timer >= getattr(
                        g, "shooting_star_spawn_interval", 999999
                    ):
                        import random

                        for i in range(getattr(g, "shooting_stars_per_spawn", 0)):
                            star_y = random.randint(HEIGHT // 6, HEIGHT // 2)
                            star_x = g.camera_x + WIDTH + 50 + (i * 90)
                            star_img = (
                                getattr(g.image, "shooting_star_img", None)
                                if hasattr(g, "image")
                                else None
                            )
                            g.shooting_stars.append(
                                ShootingStar(star_x, star_y, star_img)
                            )
                        g.shooting_star_spawn_timer = 0
            elif g.current_level <= 30:
                # Spawn de novos morcegos (níveis 21-30)
                g.bat_spawn_timer += 1
                if g.bat_spawn_timer >= g.bat_spawn_interval:
                    import random

                    for i in range(g.bats_per_spawn):
                        bat_y = random.randint(HEIGHT // 4, HEIGHT - 150)
                        bat_x = g.camera_x + WIDTH + 50 + (i * 100)
                        bat_images = (
                            (g.image.bat_img1, g.image.bat_img2, g.image.bat_img3)
                            if hasattr(g.image, "bat_img1")
                            else None
                        )
                        g.bats.append(Bat(bat_x, bat_y, bat_images))
                    g.bat_spawn_timer = 0
                if 27 <= g.current_level <= 30:
                    g.lavadrop_spawn_timer += 1
                    if g.lavadrop_spawn_timer >= getattr(g, "lavadrop_spawn_interval", 999999):
                        import random

                        for i in range(getattr(g, "lavadrops_per_spawn", 0)):
                            drop_x = g.camera_x + random.randint(0, WIDTH)
                            drop_y = -20 - (i * 15)
                            drop_img = (
                                getattr(g.image, "lava_drop_img", None)
                                if hasattr(g, "image")
                                else None
                            )
                            g.lava_drops.append(LavaDrop(drop_x, drop_y, drop_img))
                        g.lavadrop_spawn_timer = 0
                g.shooting_star_spawn_timer += 1
                if g.shooting_star_spawn_timer >= getattr(
                    g, "shooting_star_spawn_interval", 999999
                ):
                    import random

                    for i in range(getattr(g, "shooting_stars_per_spawn", 0)):
                        star_y = random.randint(HEIGHT // 6, HEIGHT // 2)
                        star_x = g.camera_x + WIDTH + 50 + (i * 90)
                        star_img = (
                            getattr(g.image, "shooting_star_img", None)
                            if hasattr(g, "image")
                            else None
                        )
                        g.shooting_stars.append(ShootingStar(star_x, star_y, star_img))
                    g.shooting_star_spawn_timer = 0
            elif g.current_level <= 40:
                # Spawn de novos aviões (níveis 31-40)
                g.airplane_spawn_timer += 1
                if g.airplane_spawn_timer >= g.airplane_spawn_interval:
                    import random

                    for i in range(g.airplanes_per_spawn):
                        airplane_y = random.randint(HEIGHT // 4, HEIGHT - 150)
                        airplane_x = g.camera_x + WIDTH + 50 + (i * 120)
                        airplane_images = (
                            (g.airplane_img1, g.airplane_img2, g.airplane_img3)
                            if hasattr(g, "airplane_img1")
                            else None
                        )
                        g.airplanes.append(
                            Airplane(airplane_x, airplane_y, airplane_images)
                        )
                    g.airplane_spawn_timer = 0
            elif g.current_level <= 50:
                # Spawn de novos flying-disks (níveis 41-50)
                g.flying_disk_spawn_timer += 1
                if g.flying_disk_spawn_timer >= g.flying_disk_spawn_interval:
                    import random

                    for i in range(g.flying_disks_per_spawn):
                        disk_y = random.randint(HEIGHT // 4, HEIGHT - 150)
                        disk_x = g.camera_x + WIDTH + 50 + (i * 120)
                        disk_images = (
                            g.flying_disk_images
                            if hasattr(g, "flying_disk_images")
                            else None
                        )
                        g.flying_disks.append(FlyingDisk(disk_x, disk_y, disk_images))
                    g.flying_disk_spawn_timer = 0
            else:
                # Spawn de novos foguinhos (nível 51)
                if g.current_level == 51:
                    g.fire_spawn_timer += 1
                    if g.fire_spawn_timer >= g.fire_spawn_interval:
                        import random

                        for i in range(g.fires_per_spawn):
                            fire_y = random.randint(HEIGHT // 4, HEIGHT - 150)
                            fire_x = g.camera_x + WIDTH + 50 + (i * 80)
                            fire_image = (
                                g.image.fire_image
                                if hasattr(g.image, "fire_image")
                                else None
                            )
                            g.fires.append(Fire(fire_x, fire_y, fire_image))
                        g.fire_spawn_timer = 0

            # Atualizar inimigos com culling
            if g.current_level <= 20:
                if g.current_level <= 16:
                    visible_birds = []
                    for bird in g.birds:
                        if bird.update():
                            if (
                                bird.x > g.camera_x - 200
                                and bird.x < g.camera_x + WIDTH + 200
                            ):
                                visible_birds.append(bird)
                    g.birds = visible_birds
                    # Atualizar gotas de chuva (7-10)
                    if 7 <= g.current_level <= 10:
                        visible_drops = []
                        for drop in getattr(g, "raindrops", []):
                            if drop.update():
                                if (
                                    drop.x > g.camera_x - 100
                                    and drop.x < g.camera_x + WIDTH + 100
                                ):
                                    visible_drops.append(drop)
                        g.raindrops = visible_drops
                else:
                    # Morcegos e estrelas (17-20)
                    visible_bats = []
                    for bat in g.bats:
                        if bat.update(g.camera_x):
                            if (
                                bat.x > g.camera_x - 200
                                and bat.x < g.camera_x + WIDTH + 200
                            ):
                                visible_bats.append(bat)
                    g.bats = visible_bats

                    visible_stars = []
                    for star in getattr(g, "shooting_stars", []):
                        if star.update(g.camera_x):
                            if (
                                star.x > g.camera_x - 200
                                and star.x < g.camera_x + WIDTH + 200
                            ):
                                visible_stars.append(star)
                    g.shooting_stars = visible_stars
            elif g.current_level <= 30:
                visible_bats = []
                for bat in g.bats:
                    if bat.update(g.camera_x):
                        if (
                            bat.x > g.camera_x - 200
                            and bat.x < g.camera_x + WIDTH + 200
                        ):
                            visible_bats.append(bat)
                g.bats = visible_bats
                if 27 <= g.current_level <= 30:
                    visible_lava = []
                    for drop in getattr(g, "lava_drops", []):
                        if drop.update():
                            if (
                                drop.x > g.camera_x - 100
                                and drop.x < g.camera_x + WIDTH + 100
                            ):
                                visible_lava.append(drop)
                    g.lava_drops = visible_lava
                visible_stars = []
                for star in getattr(g, "shooting_stars", []):
                    if star.update(g.camera_x):
                        if (
                            star.x > g.camera_x - 200
                            and star.x < g.camera_x + WIDTH + 200
                        ):
                            visible_stars.append(star)
                g.shooting_stars = visible_stars
            elif g.current_level <= 40:
                visible_airplanes = []
                for airplane in g.airplanes:
                    if airplane.update(g.camera_x):
                        if (
                            airplane.x > g.camera_x - 200
                            and airplane.x < g.camera_x + WIDTH + 200
                        ):
                            visible_airplanes.append(airplane)
                g.airplanes = visible_airplanes
            elif g.current_level <= 50:
                visible_disks = []
                for disk in g.flying_disks:
                    if disk.update(g.camera_x):
                        if (
                            disk.x > g.camera_x - 200
                            and disk.x < g.camera_x + WIDTH + 200
                        ):
                            visible_disks.append(disk)
                g.flying_disks = visible_disks
            else:
                if g.current_level == 51:
                    visible_fires = []
                    for fire in g.fires:
                        if fire.update(g.camera_x):
                            if (
                                fire.x > g.camera_x - 200
                                and fire.x < g.camera_x + WIDTH + 200
                            ):
                                visible_fires.append(fire)
                    g.fires = visible_fires

            # Atualizar tartarugas/aranhas
            if g.current_level <= 20:
                active_turtles = []
                for turtle in g.turtles:
                    if turtle.update():
                        active_turtles.append(turtle)
                g.turtles = active_turtles
            else:
                active_spiders = []
                for spider in g.spiders:
                    if spider.update(g.camera_x):
                        active_spiders.append(spider)
                g.spiders = active_spiders

            # Atualizar robôs (31-40)
            if 31 <= g.current_level <= 40:
                active_robots = []
                for robot in g.robots:
                    if robot.update(g.camera_x):
                        active_robots.append(robot)
                g.robots = active_robots

            # Atualizar aliens (41-50)
            if 41 <= g.current_level <= 50:
                active_aliens = []
                for alien in g.aliens:
                    if alien.update(g.camera_x):
                        active_aliens.append(alien)
                g.aliens = active_aliens

            # Atualizar boss alien (51)
            if g.current_level == 51 and hasattr(g, "boss_alien") and g.boss_alien:
                g.boss_alien.update(g.player.x, g.camera_x)

                if not g.boss_alien_captured and g.boss_alien.is_captured(
                    g.player.rect
                ):
                    g.boss_alien_captured = True
                    g.capture_sequence_timer = 0
                    g.capture_flash_timer = 0
                    g.capture_flash_state = False
                    g.music.play_music("capture")

                if g.boss_alien_captured:
                    g.capture_sequence_timer += 1
                    g.capture_flash_timer += 1
                    if g.capture_flash_timer >= 30:
                        g.capture_flash_timer = 0
                        g.capture_flash_state = not g.capture_flash_state
                    if g.capture_sequence_timer >= 300:
                        g.state = GameState.ENDING_VIDEO

            # Atualizar explosões com pool
            active_explosions = []
            for explosion in g.explosions:
                if explosion.update():
                    active_explosions.append(explosion)
                else:
                    g.return_explosion_to_pool(explosion)
            g.explosions = active_explosions

            # Colisões tiros vs aves/morcegos/aviões/discos
            if g.current_level <= 20:
                if g.current_level <= 16:
                    for bullet in g.player.bullets[:]:
                        for bird in g.birds[:]:
                            if getattr(bird, "is_dead", False):
                                continue
                            if bullet.rect.colliderect(bird.rect):
                                g.player.bullets.remove(bullet)
                                g.return_bullet_to_pool(bullet)
                                if hasattr(bird, "die"):
                                    bird.die()
                                g.sound_effects.play_sound_effect("bird-hit")
                                g.add_score(100)
                                break
                        # Colisões com gotas de chuva (7-10)
                        if 7 <= g.current_level <= 10:
                            for drop in g.raindrops[:]:
                                if getattr(drop, "is_dead", False):
                                    continue
                                if bullet.rect.colliderect(drop.rect):
                                    g.player.bullets.remove(bullet)
                                    g.return_bullet_to_pool(bullet)
                                    drop.die()
                                    g.sound_effects.play_sound_effect("water-hit")
                                    g.add_score(100)
                                    break
                else:
                    # Compatibilidade de testes: se pássaros forem injetados manualmente,
                    # ainda processar colisões com tiros nas fases 17-20.
                    for bullet in g.player.bullets[:]:
                        for bird in g.birds[:]:
                            if getattr(bird, "is_dead", False):
                                continue
                            if bullet.rect.colliderect(bird.rect):
                                g.player.bullets.remove(bullet)
                                g.return_bullet_to_pool(bullet)
                                if hasattr(bird, "die"):
                                    bird.die()
                                g.sound_effects.play_sound_effect("bird-hit")
                                g.add_score(100)
                                break
                    for bullet in g.player.bullets[:]:
                        for bat in g.bats[:]:
                            if getattr(bat, "is_dead", False):
                                continue
                            if bullet.rect.colliderect(bat.rect):
                                g.player.bullets.remove(bullet)
                                g.return_bullet_to_pool(bullet)
                                if hasattr(bat, "die"):
                                    bat.die()
                                g.sound_effects.play_sound_effect("bird-hit")
                                g.add_score(75)
                                break
                        # Estrelas cadentes
                        for star in getattr(g, "shooting_stars", [])[:]:
                            if getattr(star, "is_dead", False):
                                continue
                            if bullet.rect.colliderect(star.rect):
                                if bullet in g.player.bullets:
                                    g.player.bullets.remove(bullet)
                                g.return_bullet_to_pool(bullet)
                                star.die()
                                explosion = g.get_pooled_explosion(
                                    star.x, star.y, g.image.explosion_image
                                )
                                g.explosions.append(explosion)
                                g.sound_effects.play_sound_effect("explosion")
                                g.add_score(225)
                                break
            elif g.current_level <= 30:
                for bullet in g.player.bullets[:]:
                    for bat in g.bats[:]:
                        if getattr(bat, "is_dead", False):
                            continue
                        if bullet.rect.colliderect(bat.rect):
                            g.player.bullets.remove(bullet)
                            g.return_bullet_to_pool(bullet)
                            if hasattr(bat, "die"):
                                bat.die()
                            g.sound_effects.play_sound_effect("bird-hit")
                            g.add_score(75)
                            break
                    # Shooting stars bullet collisions
                    for star in getattr(g, "shooting_stars", [])[:]:
                        if getattr(star, "is_dead", False):
                            continue
                        if bullet.rect.colliderect(star.rect):
                            if bullet in g.player.bullets:
                                g.player.bullets.remove(bullet)
                            g.return_bullet_to_pool(bullet)
                            star.die()
                            explosion = g.get_pooled_explosion(
                                star.x, star.y, g.image.explosion_image
                            )
                            g.explosions.append(explosion)
                            g.sound_effects.play_sound_effect("explosion")
                            g.add_score(225)
                            break
            elif g.current_level <= 40:
                for bullet in g.player.bullets[:]:
                    for airplane in g.airplanes[:]:
                        if bullet.rect.colliderect(airplane.rect):
                            g.player.bullets.remove(bullet)
                            g.airplanes.remove(airplane)
                            explosion = g.get_pooled_explosion(
                                airplane.x, airplane.y, g.image.explosion_image
                            )
                            g.explosions.append(explosion)
                            g.return_bullet_to_pool(bullet)
                            g.sound_effects.play_sound_effect("explosion")
                            g.add_score(50)
                            break
            else:
                for bullet in g.player.bullets[:]:
                    for disk in g.flying_disks[:]:
                        if bullet.rect.colliderect(disk.rect):
                            g.player.bullets.remove(bullet)
                            g.flying_disks.remove(disk)
                            explosion = g.get_pooled_explosion(
                                disk.x, disk.y, g.image.explosion_image
                            )
                            g.explosions.append(explosion)
                            g.return_bullet_to_pool(bullet)
                            g.sound_effects.play_sound_effect("explosion")
                            g.add_score(90)
                            break

            # Colisões tiros vs tartarugas/aranhas
            if g.current_level <= 20:
                for bullet in g.player.bullets[:]:
                    for turtle in g.turtles[:]:
                        if getattr(turtle, "is_dead", False):
                            continue
                        if bullet.rect.colliderect(turtle.rect):
                            g.player.bullets.remove(bullet)
                            g.return_bullet_to_pool(bullet)
                            if hasattr(turtle, "die"):
                                turtle.die()
                            g.sound_effects.play_sound_effect("bird-hit")
                            g.add_score(70)
                            break
            else:
                for bullet in g.player.bullets[:]:
                    for spider in g.spiders[:]:
                        if getattr(spider, "is_dead", False):
                            continue
                        if bullet.rect.colliderect(spider.rect):
                            g.player.bullets.remove(bullet)
                            g.return_bullet_to_pool(bullet)
                            if hasattr(spider, "die"):
                                spider.die()
                            g.sound_effects.play_sound_effect("bird-hit")
                            g.add_score(120)
                            break

            # Colisões tiros do jogador vs robôs (31-40)
            if 31 <= g.current_level <= 40:
                for bullet in g.player.bullets[:]:
                    for robot in g.robots[:]:
                        if bullet.rect.colliderect(robot.rect):
                            if bullet in g.player.bullets:
                                g.player.bullets.remove(bullet)
                            g.return_bullet_to_pool(bullet)
                            explosion = g.get_pooled_explosion(
                                robot.x, robot.y, g.image.explosion_image
                            )
                            g.explosions.append(explosion)
                            g.sound_effects.play_sound_effect("explosion")
                            for missile in getattr(robot, "missiles", []):
                                g.orphan_missiles.append(missile)
                            if robot in g.robots:
                                g.robots.remove(robot)
                            g.add_score(100)
                            break

            # Colisões mísseis dos robôs vs jogador (31-40)
            if 31 <= g.current_level <= 40 and not g.player.is_being_abducted:
                for robot in g.robots[:]:
                    for missile in robot.missiles[:]:
                        if g.player.rect.colliderect(missile.rect):
                            if g.player.is_invulnerable:
                                explosion = g.get_pooled_explosion(
                                    missile.x, missile.y, g.image.explosion_image
                                )
                                g.explosions.append(explosion)
                                robot.missiles.remove(missile)
                                g.add_score(15)
                            else:
                                if not g.player.is_hit:
                                    if getattr(g, "shield_active", False):
                                        g.shield_active = False
                                        explosion = g.get_pooled_explosion(
                                            missile.x,
                                            missile.y,
                                            g.image.explosion_image,
                                        )
                                        g.explosions.append(explosion)
                                        if missile in robot.missiles:
                                            robot.missiles.remove(missile)
                                    else:
                                        g.player.take_hit()
                                        g.sound_effects.play_sound_effect("player-hit")
                                        explosion = g.get_pooled_explosion(
                                            missile.x,
                                            missile.y,
                                            g.image.explosion_image,
                                        )
                                        g.explosions.append(explosion)
                                        robot.missiles.remove(missile)
                                        g.lives -= 1
                                        if g.lives <= 0:
                                            if g.ranking_manager.is_high_score(g.score):
                                                g.state = GameState.ENTER_NAME
                                            else:
                                                g.state = GameState.GAME_OVER
                                            g.start_game_over_hold()
                            break

            # Colisões lasers dos aliens vs jogador (41-50)
            if 41 <= g.current_level <= 50 and not g.player.is_being_abducted:
                for alien in g.aliens[:]:
                    if hasattr(alien, "is_dead") and alien.is_dead:
                        continue
                    for laser in alien.lasers[:]:
                        if not getattr(laser, "collision_enabled", True):
                            continue
                        if g.player.rect.colliderect(laser.rect):
                            if g.player.is_invulnerable:
                                explosion = g.get_pooled_explosion(
                                    laser.x, laser.y, g.image.explosion_image
                                )
                                g.explosions.append(explosion)
                                alien.lasers.remove(laser)
                                g.add_score(15)
                            else:
                                if not g.player.is_hit:
                                    if getattr(g, "shield_active", False):
                                        g.shield_active = False
                                        explosion = g.get_pooled_explosion(
                                            laser.x, laser.y, g.image.explosion_image
                                        )
                                        g.explosions.append(explosion)
                                        if laser in alien.lasers:
                                            alien.lasers.remove(laser)
                                    else:
                                        g.player.take_hit()
                                        g.sound_effects.play_sound_effect("player-hit")
                                        explosion = g.get_pooled_explosion(
                                            laser.x, laser.y, g.image.explosion_image
                                        )
                                        g.explosions.append(explosion)
                                        alien.lasers.remove(laser)
                                        g.lives -= 1
                                        if g.lives <= 0:
                                            if g.ranking_manager.is_high_score(g.score):
                                                g.state = GameState.ENTER_NAME
                                            else:
                                                g.state = GameState.GAME_OVER
                                            g.start_game_over_hold()
                            break

            # Colisões tiros vs aliens (41-50)
            if 41 <= g.current_level <= 50:
                for bullet in g.player.bullets[:]:
                    for alien in g.aliens[:]:
                        if bullet.rect.colliderect(alien.rect):
                            if hasattr(alien, "is_dead") and alien.is_dead:
                                if bullet in g.player.bullets:
                                    g.player.bullets.remove(bullet)
                                g.return_bullet_to_pool(bullet)
                                break
                            if hasattr(alien, "die"):
                                alien.die()
                                g.sound_effects.play_sound_effect("bird-hit")
                            if bullet in g.player.bullets:
                                g.player.bullets.remove(bullet)
                            g.return_bullet_to_pool(bullet)
                            for laser in getattr(alien, "lasers", []):
                                g.orphan_lasers.append(laser)
                            g.add_score(60)
                            break

            # Atualizar mísseis/lases órfãos
            if 31 <= g.current_level <= 40:
                active_orphan_missiles = []
                for missile in g.orphan_missiles:
                    if missile.update(g.camera_x):
                        active_orphan_missiles.append(missile)
                g.orphan_missiles = active_orphan_missiles

            if 41 <= g.current_level <= 50:
                active_orphan_lasers = []
                for laser in g.orphan_lasers:
                    if laser.update(g.camera_x):
                        active_orphan_lasers.append(laser)
                g.orphan_lasers = active_orphan_lasers

            # Colisão/esquiva aves/morcegos/aviões/discos
            if g.current_level <= 20:
                if g.current_level <= 16:
                    for bird in g.birds[:]:
                        distance_x = abs(bird.x - g.player.x)
                        distance_y = abs(bird.y - g.player.y)
                        if (
                            distance_x < 40
                            and distance_y < 50
                            and bird.x < g.player.x
                            and bird.id not in g.birds_dodged
                        ):
                            g.birds_dodged.add(bird.id)
                            g.add_score(10)
                        # Usar hitbox efetiva quando abaixado para inimigos voadores
                        player_rect = g.player.get_airborne_collision_rect()
                        if player_rect.colliderect(bird.rect):
                            if hasattr(bird, "is_dead") and bird.is_dead:
                                continue
                            if g.player.is_invulnerable:
                                g.explosions.append(
                                    Explosion(bird.x, bird.y, g.image.explosion_image)
                                )
                                g.birds.remove(bird)
                                g.add_score(20)
                            else:
                                if not g.player.is_hit:
                                    if getattr(g, "shield_active", False):
                                        g.shield_active = False
                                        g.explosions.append(
                                            Explosion(
                                                bird.x, bird.y, g.image.explosion_image
                                            )
                                        )
                                        if bird in g.birds:
                                            g.birds.remove(bird)
                                    else:
                                        g.player.take_hit()
                                        g.sound_effects.play_sound_effect("player-hit")
                                        g.explosions.append(
                                            Explosion(
                                                bird.x, bird.y, g.image.explosion_image
                                            )
                                        )
                                        g.birds.remove(bird)
                                        g.lives -= 1
                                        if g.lives <= 0:
                                            if g.ranking_manager.is_high_score(g.score):
                                                g.state = GameState.ENTER_NAME
                                            else:
                                                g.state = GameState.GAME_OVER
                                            g.start_game_over_hold()
                            break
                    # Colisão com gotas de chuva (fases 7-10)
                    if 7 <= g.current_level <= 10:
                        for drop in g.raindrops[:]:
                            if g.player.rect.colliderect(drop.rect):
                                if getattr(drop, "is_dead", False):
                                    continue
                                # Pulo destrói a gota; invulnerável também destrói
                                if g.player.is_invulnerable or not getattr(
                                    g.player, "on_ground", True
                                ):
                                    drop.die()
                                    g.sound_effects.play_sound_effect("water-hit")
                                    g.add_score(20)
                                else:
                                    if not g.player.is_hit:
                                        if getattr(g, "shield_active", False):
                                            g.shield_active = False
                                            drop.die()
                                            g.sound_effects.play_sound_effect(
                                                "water-hit"
                                            )
                                        else:
                                            g.player.take_hit()
                                            g.sound_effects.play_sound_effect(
                                                "player-hit"
                                            )
                                            drop.die()
                                            g.lives -= 1
                                            if g.lives <= 0:
                                                if g.ranking_manager.is_high_score(
                                                    g.score
                                                ):
                                                    g.state = GameState.ENTER_NAME
                                                else:
                                                    g.state = GameState.GAME_OVER
                                                g.start_game_over_hold()
                                break
                else:
                    # Compatibilidade de testes: processar colisões com pássaros se existirem nas fases 17-20
                    for bird in g.birds[:]:
                        distance_x = abs(bird.x - g.player.x)
                        distance_y = abs(bird.y - g.player.y)
                        if (
                            distance_x < 40
                            and distance_y < 50
                            and bird.x < g.player.x
                            and bird.id not in g.birds_dodged
                        ):
                            g.birds_dodged.add(bird.id)
                            g.add_score(10)
                        player_rect = g.player.get_airborne_collision_rect()
                        if player_rect.colliderect(bird.rect):
                            if hasattr(bird, "is_dead") and bird.is_dead:
                                continue
                            if g.player.is_invulnerable:
                                g.explosions.append(
                                    Explosion(bird.x, bird.y, g.image.explosion_image)
                                )
                                g.birds.remove(bird)
                                g.add_score(20)
                            else:
                                if not g.player.is_hit:
                                    if getattr(g, "shield_active", False):
                                        g.shield_active = False
                                        g.explosions.append(
                                            Explosion(
                                                bird.x, bird.y, g.image.explosion_image
                                            )
                                        )
                                        if bird in g.birds:
                                            g.birds.remove(bird)
                                    else:
                                        g.player.take_hit()
                                        g.sound_effects.play_sound_effect("player-hit")
                                        g.explosions.append(
                                            Explosion(
                                                bird.x, bird.y, g.image.explosion_image
                                            )
                                        )
                                        g.birds.remove(bird)
                                        g.lives -= 1
                                        if g.lives <= 0:
                                            if g.ranking_manager.is_high_score(g.score):
                                                g.state = GameState.ENTER_NAME
                                            else:
                                                g.state = GameState.GAME_OVER
                                            g.start_game_over_hold()
                            break
                    # Morcegos
                    for bat in g.bats[:]:
                        distance_x = abs(bat.x - g.player.x)
                        distance_y = abs(bat.y - g.player.y)
                        if (
                            distance_x < 40
                            and distance_y < 50
                            and bat.x < g.player.x
                            and bat.id not in g.birds_dodged
                        ):
                            g.birds_dodged.add(bat.id)
                            g.add_score(15)
                        player_rect = g.player.get_airborne_collision_rect()
                        if player_rect.colliderect(bat.rect):
                            if hasattr(bat, "is_dead") and bat.is_dead:
                                continue
                            if g.player.is_invulnerable:
                                g.explosions.append(
                                    Explosion(bat.x, bat.y, g.image.explosion_image)
                                )
                                g.bats.remove(bat)
                                g.add_score(25)
                            else:
                                if not g.player.is_hit:
                                    if getattr(g, "shield_active", False):
                                        g.shield_active = False
                                        g.explosions.append(
                                            Explosion(
                                                bat.x, bat.y, g.image.explosion_image
                                            )
                                        )
                                        if bat in g.bats:
                                            g.bats.remove(bat)
                                    else:
                                        g.player.take_hit()
                                        g.sound_effects.play_sound_effect("player-hit")
                                        g.explosions.append(
                                            Explosion(
                                                bat.x, bat.y, g.image.explosion_image
                                            )
                                        )
                                        g.bats.remove(bat)
                                        g.lives -= 1
                                        if g.lives <= 0:
                                            if g.ranking_manager.is_high_score(g.score):
                                                g.state = GameState.ENTER_NAME
                                            else:
                                                g.state = GameState.GAME_OVER
                                            g.start_game_over_hold()
                            break
                    # Estrelas cadentes
                    for star in getattr(g, "shooting_stars", [])[:]:
                        distance_x = abs(star.x - g.player.x)
                        distance_y = abs(star.y - g.player.y)
                        if (
                            distance_x < 45
                            and distance_y < 55
                            and star.x < g.player.x
                            and star.id not in g.birds_dodged
                        ):
                            g.birds_dodged.add(star.id)
                            g.add_score(45)
                        player_rect = g.player.get_airborne_collision_rect()
                        if player_rect.colliderect(star.rect):
                            if hasattr(star, "is_dead") and star.is_dead:
                                continue
                            if g.player.is_invulnerable:
                                explosion = g.get_pooled_explosion(
                                    star.x, star.y, g.image.explosion_image
                                )
                                g.explosions.append(explosion)
                                if star in g.shooting_stars:
                                    g.shooting_stars.remove(star)
                                g.add_score(75)
                            else:
                                if not g.player.is_hit:
                                    if getattr(g, "shield_active", False):
                                        g.shield_active = False
                                        explosion = g.get_pooled_explosion(
                                            star.x, star.y, g.image.explosion_image
                                        )
                                        g.explosions.append(explosion)
                                        if star in g.shooting_stars:
                                            g.shooting_stars.remove(star)
                                    else:
                                        g.player.take_hit()
                                        g.sound_effects.play_sound_effect("player-hit")
                                        explosion = g.get_pooled_explosion(
                                            star.x, star.y, g.image.explosion_image
                                        )
                                        g.explosions.append(explosion)
                                        if star in g.shooting_stars:
                                            g.shooting_stars.remove(star)
                                        g.lives -= 1
                                        if g.lives <= 0:
                                            if g.ranking_manager.is_high_score(g.score):
                                                g.state = GameState.ENTER_NAME
                                            else:
                                                g.state = GameState.GAME_OVER
                                            g.start_game_over_hold()
                            break
            elif g.current_level <= 30:
                for bat in g.bats[:]:
                    distance_x = abs(bat.x - g.player.x)
                    distance_y = abs(bat.y - g.player.y)
                    if (
                        distance_x < 40
                        and distance_y < 50
                        and bat.x < g.player.x
                        and bat.id not in g.birds_dodged
                    ):
                        g.birds_dodged.add(bat.id)
                        g.add_score(15)
                    if g.player.rect.colliderect(bat.rect):
                        if hasattr(bat, "is_dead") and bat.is_dead:
                            continue
                        if g.player.is_invulnerable:
                            g.explosions.append(
                                Explosion(bat.x, bat.y, g.image.explosion_image)
                            )
                            g.bats.remove(bat)
                            g.add_score(25)
                        else:
                            if not g.player.is_hit:
                                if getattr(g, "shield_active", False):
                                    g.shield_active = False
                                    g.explosions.append(
                                        Explosion(bat.x, bat.y, g.image.explosion_image)
                                    )
                                    if bat in g.bats:
                                        g.bats.remove(bat)
                                else:
                                    g.player.take_hit()
                                    g.sound_effects.play_sound_effect("player-hit")
                                    g.explosions.append(
                                        Explosion(bat.x, bat.y, g.image.explosion_image)
                                    )
                                    g.bats.remove(bat)
                                    g.lives -= 1
                                    if g.lives <= 0:
                                        if g.ranking_manager.is_high_score(g.score):
                                            g.state = GameState.ENTER_NAME
                                        else:
                                            g.state = GameState.GAME_OVER
                                    g.start_game_over_hold()
                        break
                if 27 <= g.current_level <= 30:
                    for drop in getattr(g, "lava_drops", [])[:]:
                        if g.player.rect.colliderect(drop.rect):
                            if g.player.is_invulnerable:
                                pass
                            else:
                                if not g.player.is_hit:
                                    if getattr(g, "shield_active", False):
                                        g.shield_active = False
                                        g.player.take_hit()
                                        g.sound_effects.play_sound_effect("player-hit")
                                    else:
                                        g.player.take_hit()
                                        g.sound_effects.play_sound_effect("player-hit")
                                        g.lives -= 1
                                        if g.lives <= 0:
                                            if g.ranking_manager.is_high_score(g.score):
                                                g.state = GameState.ENTER_NAME
                                            else:
                                                g.state = GameState.GAME_OVER
                                            g.start_game_over_hold()
                # Shooting stars dodge/collision
                for star in getattr(g, "shooting_stars", [])[:]:
                    distance_x = abs(star.x - g.player.x)
                    distance_y = abs(star.y - g.player.y)
                    if (
                        distance_x < 45
                        and distance_y < 55
                        and star.x < g.player.x
                        and star.id not in g.birds_dodged
                    ):
                        g.birds_dodged.add(star.id)
                        g.add_score(45)
                    if g.player.rect.colliderect(star.rect):
                        if hasattr(star, "is_dead") and star.is_dead:
                            continue
                        if g.player.is_invulnerable:
                            explosion = g.get_pooled_explosion(
                                star.x, star.y, g.image.explosion_image
                            )
                            g.explosions.append(explosion)
                            if star in g.shooting_stars:
                                g.shooting_stars.remove(star)
                            g.add_score(75)
                        else:
                            if not g.player.is_hit:
                                if getattr(g, "shield_active", False):
                                    g.shield_active = False
                                    explosion = g.get_pooled_explosion(
                                        star.x, star.y, g.image.explosion_image
                                    )
                                    g.explosions.append(explosion)
                                    if star in g.shooting_stars:
                                        g.shooting_stars.remove(star)
                                else:
                                    g.player.take_hit()
                                    g.sound_effects.play_sound_effect("player-hit")
                                    explosion = g.get_pooled_explosion(
                                        star.x, star.y, g.image.explosion_image
                                    )
                                    g.explosions.append(explosion)
                                    if star in g.shooting_stars:
                                        g.shooting_stars.remove(star)
                                    g.lives -= 1
                                    if g.lives <= 0:
                                        if g.ranking_manager.is_high_score(g.score):
                                            g.state = GameState.ENTER_NAME
                                        else:
                                            g.state = GameState.GAME_OVER
                                        g.start_game_over_hold()
                        break
            elif g.current_level <= 40:
                for airplane in g.airplanes[:]:
                    distance_x = abs(airplane.x - g.player.x)
                    distance_y = abs(airplane.y - g.player.y)
                    if (
                        distance_x < 50
                        and distance_y < 60
                        and airplane.x < g.player.x
                        and airplane.id not in g.birds_dodged
                    ):
                        g.birds_dodged.add(airplane.id)
                        g.add_score(20)
                    player_rect = g.player.get_airborne_collision_rect()
                    if player_rect.colliderect(airplane.rect):
                        if hasattr(airplane, "is_dead") and airplane.is_dead:
                            continue
                        if g.player.is_invulnerable:
                            g.explosions.append(
                                Explosion(
                                    airplane.x, airplane.y, g.image.explosion_image
                                )
                            )
                            g.airplanes.remove(airplane)
                            g.add_score(30)
                        else:
                            if not g.player.is_hit:
                                if getattr(g, "shield_active", False):
                                    g.shield_active = False
                                    g.explosions.append(
                                        Explosion(
                                            airplane.x,
                                            airplane.y,
                                            g.image.explosion_image,
                                        )
                                    )
                                    if airplane in g.airplanes:
                                        g.airplanes.remove(airplane)
                                else:
                                    g.player.take_hit()
                                    g.explosions.append(
                                        Explosion(
                                            airplane.x,
                                            airplane.y,
                                            g.image.explosion_image,
                                        )
                                    )
                                    g.airplanes.remove(airplane)
                                    g.lives -= 1
                                    if g.lives <= 0:
                                        if g.ranking_manager.is_high_score(g.score):
                                            g.state = GameState.ENTER_NAME
                                        else:
                                            g.state = GameState.GAME_OVER
                                        g.start_game_over_hold()
                        break
            else:
                for disk in g.flying_disks[:]:
                    distance_x = abs(disk.x - g.player.x)
                    distance_y = abs(disk.y - g.player.y)
                    if (
                        distance_x < 55
                        and distance_y < 65
                        and disk.x < g.player.x
                        and disk.id not in g.birds_dodged
                    ):
                        g.birds_dodged.add(disk.id)
                        g.add_score(25)
                    player_rect = g.player.get_airborne_collision_rect()
                    if player_rect.colliderect(disk.rect):
                        if hasattr(disk, "is_dead") and disk.is_dead:
                            continue
                        if g.player.is_invulnerable:
                            g.explosions.append(
                                Explosion(disk.x, disk.y, g.image.explosion_image)
                            )
                            g.flying_disks.remove(disk)
                            g.add_score(40)
                        else:
                            if not g.player.is_hit:
                                if getattr(g, "shield_active", False):
                                    g.shield_active = False
                                    g.explosions.append(
                                        Explosion(
                                            disk.x, disk.y, g.image.explosion_image
                                        )
                                    )
                                    if disk in g.flying_disks:
                                        g.flying_disks.remove(disk)
                                else:
                                    g.player.take_hit()
                                    g.sound_effects.play_sound_effect("player-hit")
                                    g.explosions.append(
                                        Explosion(
                                            disk.x, disk.y, g.image.explosion_image
                                        )
                                    )
                                    g.flying_disks.remove(disk)
                                    g.lives -= 1
                                    if g.lives <= 0:
                                        if g.ranking_manager.is_high_score(g.score):
                                            g.state = GameState.ENTER_NAME
                                        else:
                                            g.state = GameState.GAME_OVER
                        break

            # Colisão com foguinhos (51)
            if g.current_level == 51:
                for fire in g.fires[:]:
                    if g.player.rect.colliderect(fire.rect):
                        if not g.player.is_invulnerable and not g.player.is_hit:
                            if getattr(g, "shield_active", False):
                                g.shield_active = False
                            else:
                                g.player.take_hit()
                                g.sound_effects.play_sound_effect("player-hit")
                                g.lives -= 1
                                if g.lives <= 0:
                                    if g.ranking_manager.is_high_score(g.score):
                                        g.state = GameState.ENTER_NAME
                                    else:
                                        g.state = GameState.GAME_OVER
                                    g.start_game_over_hold()
                        break

            # Colisão com tartarugas/aranhas
            if g.current_level <= 20:
                for turtle in g.turtles[:]:
                    if g.player.rect.colliderect(turtle.rect):
                        if hasattr(turtle, "is_dead") and turtle.is_dead:
                            continue
                        if g.player.is_invulnerable:
                            if hasattr(turtle, "die"):
                                turtle.die()
                            g.sound_effects.play_sound_effect("bird-hit")
                            g.add_score(20)
                        else:
                            if not g.player.is_hit:
                                if getattr(g, "shield_active", False):
                                    g.shield_active = False
                                    if hasattr(turtle, "die"):
                                        turtle.die()
                                    g.sound_effects.play_sound_effect("bird-hit")
                                else:
                                    g.player.take_hit()
                                    g.sound_effects.play_sound_effect("player-hit")
                                    if hasattr(turtle, "die"):
                                        turtle.die()
                                    g.sound_effects.play_sound_effect("bird-hit")
                                    g.lives -= 1
                                    if g.lives <= 0:
                                        if g.ranking_manager.is_high_score(g.score):
                                            g.state = GameState.ENTER_NAME
                                        else:
                                            g.state = GameState.GAME_OVER
                                        g.start_game_over_hold()
                        break
            else:
                for spider in g.spiders[:]:
                    if g.player.rect.colliderect(spider.rect):
                        if hasattr(spider, "is_dead") and spider.is_dead:
                            continue
                        if g.player.is_invulnerable:
                            if hasattr(spider, "die"):
                                spider.die()
                            g.sound_effects.play_sound_effect("bird-hit")
                            g.add_score(35)
                        else:
                            if not g.player.is_hit:
                                if getattr(g, "shield_active", False):
                                    g.shield_active = False
                                    if hasattr(spider, "die"):
                                        spider.die()
                                    g.sound_effects.play_sound_effect("bird-hit")
                                else:
                                    g.player.take_hit()
                                    g.sound_effects.play_sound_effect("player-hit")
                                    if hasattr(spider, "die"):
                                        spider.die()
                                    g.sound_effects.play_sound_effect("bird-hit")
                                    g.lives -= 1
                                    if g.lives <= 0:
                                        if g.ranking_manager.is_high_score(g.score):
                                            g.state = GameState.ENTER_NAME
                                        else:
                                            g.state = GameState.GAME_OVER
                                        g.start_game_over_hold()
                        break

            # Colisão com robôs (31-40)
            if 31 <= g.current_level <= 40 and not g.player.is_being_abducted:
                for robot in g.robots[:]:
                    if g.player.rect.colliderect(robot.rect):
                        if g.player.is_invulnerable:
                            explosion = g.get_pooled_explosion(
                                robot.x, robot.y, g.image.explosion_image
                            )
                            g.explosions.append(explosion)
                            g.sound_effects.play_sound_effect("explosion")
                            for missile in getattr(robot, "missiles", []):
                                g.orphan_missiles.append(missile)
                            if robot in g.robots:
                                g.robots.remove(robot)
                            g.add_score(50)
                        else:
                            if not g.player.is_hit:
                                if getattr(g, "shield_active", False):
                                    g.shield_active = False
                                    explosion = g.get_pooled_explosion(
                                        robot.x, robot.y, g.image.explosion_image
                                    )
                                    g.explosions.append(explosion)
                                    g.sound_effects.play_sound_effect("explosion")
                                    for missile in getattr(robot, "missiles", []):
                                        g.orphan_missiles.append(missile)
                                    if robot in g.robots:
                                        g.robots.remove(robot)
                                else:
                                    g.player.take_hit()
                                    g.sound_effects.play_sound_effect("player-hit")
                                    explosion = g.get_pooled_explosion(
                                        robot.x, robot.y, g.image.explosion_image
                                    )
                                    g.explosions.append(explosion)
                                    g.sound_effects.play_sound_effect("explosion")
                                    for missile in getattr(robot, "missiles", []):
                                        g.orphan_missiles.append(missile)
                                    if robot in g.robots:
                                        g.robots.remove(robot)
                                    g.lives -= 1
                                    if g.lives <= 0:
                                        if g.ranking_manager.is_high_score(g.score):
                                            g.state = GameState.ENTER_NAME
                                        else:
                                            g.state = GameState.GAME_OVER
                                        g.start_game_over_hold()
                        break

            # Colisão com aliens (41-50)
            if 41 <= g.current_level <= 50 and not g.player.is_being_abducted:
                for alien in g.aliens[:]:
                    if g.player.rect.colliderect(alien.rect):
                        if hasattr(alien, "is_dead") and alien.is_dead:
                            continue
                        if g.player.is_invulnerable:
                            if hasattr(alien, "die"):
                                alien.die()
                                g.sound_effects.play_sound_effect("bird-hit")
                            for laser in alien.lasers:
                                g.orphan_lasers.append(laser)
                            g.add_score(60)
                        else:
                            if not g.player.is_hit:
                                if getattr(g, "shield_active", False):
                                    g.shield_active = False
                                    if hasattr(alien, "die"):
                                        alien.die()
                                        g.sound_effects.play_sound_effect("bird-hit")
                                    for laser in getattr(alien, "lasers", []):
                                        g.orphan_lasers.append(laser)
                                else:
                                    g.player.take_hit()
                                    g.sound_effects.play_sound_effect("player-hit")
                                    if hasattr(alien, "die"):
                                        alien.die()
                                        g.sound_effects.play_sound_effect("bird-hit")
                                for laser in alien.lasers:
                                    g.orphan_lasers.append(laser)
                                g.lives -= 1
                                if g.lives <= 0:
                                    if g.ranking_manager.is_high_score(g.score):
                                        g.state = GameState.ENTER_NAME
                                    else:
                                        g.state = GameState.GAME_OVER
                        break

            # Verificar bandeira
            if g.flag and g.player.rect.colliderect(g.flag.rect):
                if not getattr(g, "hold_active", False):
                    g.start_level_end_hold(g.current_level >= g.max_levels)
                    g._next_level_after_hold = True

            # Verificar abdução (fase 50)
            if g.spaceship and g.player.rect.colliderect(g.spaceship.abduction_rect):
                if not g.player.is_being_abducted:
                    g.player.start_abduction()
                if g.player.abduction_timer >= 600:
                    if not getattr(g, "hold_active", False):
                        g.start_level_end_hold(g.current_level >= g.max_levels)
                        g._next_level_after_hold = True
