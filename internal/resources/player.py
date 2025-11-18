import pygame
from internal.utils.functions import resource_path
from internal.utils.constants import *


class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 65
        self.original_height = 95
        self.crouched_height = 47
        self.height = self.original_height
        self.vel_x = 0
        self.vel_y = 0
        self.prev_vel_y = 0  # Velocidade anterior para detectar mudança
        self.on_ground = False
        self.just_landed = False  # Flag para detectar pouso
        self.is_crouching = False
        self.is_hit = False  # Flag para quando o personagem é atingido
        self.hit_timer = 0  # Timer para controlar duração do estado de hit
        self.is_invulnerable = False  # Flag para invulnerabilidade
        self.invulnerability_timer = (
            0  # Timer para duração da invulnerabilidade (5s = 300 frames)
        )
        self.blink_timer = 0  # Timer para controlar o piscar durante invulnerabilidade
        self.is_being_abducted = False  # Flag para quando está sendo abduzido
        self.abduction_timer = 0  # Timer para controlar duração da abdução
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        # Pulo duplo (habilitado por power-up)
        self.double_jump_enabled = False
        self.double_jump_frames_left = 0
        self.remaining_jumps = 1
        # Detecção de borda de entrada para pulo (evita consumo imediato do pulo duplo)
        self.jump_was_down = False

        # Sistema de animação
        self.sprites = {}
        self.current_animation = "idle"
        self.animation_frame = 0
        self.animation_timer = 0
        self.animation_speed = 8  # Frames por segundo da animação

        # Sistema de tiro
        self.bullets = []
        self.shoot_cooldown = 0  # Cooldown entre tiros
        self.max_shoot_cooldown = 15  # 15 frames = 0.25 segundos a 60 FPS
        self.shooting_timer = 0  # Duração temporária da animação de tiro

        self.load_sprites()

    def load_sprites(self):
        """Carregar todos os sprites do personagem"""
        try:
            # Carregar diretamente com pygame.image.load para compatibilidade com testes
            def load_and_scale(path, size):
                img = pygame.image.load(resource_path(path))
                try:
                    img = img.convert_alpha()
                except Exception:
                    try:
                        img = img.convert()
                    except Exception:
                        pass
                if size:
                    img = pygame.transform.scale(img, size)
                    try:
                        img = img.convert_alpha()
                    except Exception:
                        try:
                            img = img.convert()
                        except Exception:
                            pass
                return img

            # Sprite parado (idle)
            self.sprites["idle"] = [
                load_and_scale("imagens/personagem/1.png", (self.width, self.original_height))
            ]

            # Sprites de caminhada
            self.sprites["walk"] = [
                load_and_scale("imagens/personagem/1.png", (self.width, self.original_height)),
                load_and_scale("imagens/personagem/2.png", (self.width, self.original_height)),
                load_and_scale("imagens/personagem/3.png", (self.width, self.original_height)),
                load_and_scale("imagens/personagem/4.png", (self.width, self.original_height)),
            ]

            # Sprites de pulo (inclui aterrissagem)
            self.sprites["jump"] = [
                load_and_scale("imagens/personagem/j1.png", (self.width, self.original_height)),
                load_and_scale("imagens/personagem/j2.png", (self.width, self.original_height)),
                load_and_scale("imagens/personagem/j3.png", (self.width, self.original_height)),
                load_and_scale("imagens/personagem/j4.png", (self.width, self.original_height)),
                load_and_scale("imagens/personagem/j5.png", (self.width, self.original_height)),
            ]

            # Sprite agachado (mantém altura original conforme lógica atual)
            self.sprites["crouch"] = [
                load_and_scale("imagens/personagem/dn1.png", (self.width, self.original_height))
            ]

            # Sprite quando atingido
            self.sprites["hit"] = [
                load_and_scale("imagens/personagem/d1.png", (self.width, self.original_height))
            ]

            # Sprites de tiro
            self.sprites["shoot"] = [
                load_and_scale("imagens/personagem/bow.png", (self.width, self.original_height))
            ]
            self.sprites["shoot_crouch"] = [
                load_and_scale("imagens/personagem/bowD.png", (self.width, self.original_height))
            ]

        except pygame.error as e:
            print(f"Erro ao carregar sprites do personagem: {e}")
            # Fallback: criar sprites coloridos simples
            self.sprites = {
                "idle": [pygame.Surface((self.width, self.original_height))],
                "walk": [
                    pygame.Surface((self.width, self.original_height)) for _ in range(4)
                ],
                "jump": [
                    pygame.Surface((self.width, self.original_height)) for _ in range(5)
                ],
                "crouch": [pygame.Surface((self.width, self.crouched_height))],
                "hit": [pygame.Surface((self.width, self.original_height))],
            }
            # Preencher com cores para fallback
            for animation in self.sprites:
                for sprite in self.sprites[animation]:
                    sprite.fill(BLUE)

    def update_animation(self):
        """Atualizar a animação do personagem baseada no estado atual"""
        # Determinar qual animação usar
        if self.shooting_timer > 0:
            new_animation = "shoot_crouch" if self.is_crouching else "shoot"
        elif self.is_hit and self.hit_timer > 0:
            new_animation = "hit"
        elif self.is_crouching:
            new_animation = "crouch"
        elif not self.on_ground:
            new_animation = "jump"
        elif abs(self.vel_x) > 0:
            new_animation = "walk"
        else:
            new_animation = "idle"

        # Se mudou de animação, resetar frame
        if new_animation != self.current_animation:
            self.current_animation = new_animation
            self.animation_frame = 0
            self.animation_timer = 0

        # Atualizar timer da animação
        self.animation_timer += 1

        # Avançar frame da animação
        if (
            self.animation_timer >= 60 // self.animation_speed
        ):  # 60 FPS / animation_speed
            self.animation_timer = 0

            # Lógica especial para animação de pulo
            if self.current_animation == "jump":
                if self.vel_y < -10:  # Subindo rápido
                    self.animation_frame = 0
                elif self.vel_y < -5:  # Subindo devagar
                    self.animation_frame = 1
                elif self.vel_y < 5:  # No ar
                    self.animation_frame = 2
                elif self.vel_y < 10:  # Descendo
                    self.animation_frame = 3
                else:  # Aterrissando
                    self.animation_frame = 4
            else:
                # Para outras animações, ciclar normalmente
                self.animation_frame = (self.animation_frame + 1) % len(
                    self.sprites[self.current_animation]
                )

        # Atualizar timer de hit
        if self.hit_timer > 0:
            self.hit_timer -= 1
            if self.hit_timer <= 0:
                self.is_hit = False

        # Atualizar timer de tiro (animação temporária)
        if self.shooting_timer > 0:
            self.shooting_timer -= 1

        # Atualizar timer de invulnerabilidade
        if self.invulnerability_timer > 0:
            self.invulnerability_timer -= 1
            self.blink_timer += 1
            if self.invulnerability_timer <= 0:
                self.is_invulnerable = False
                self.blink_timer = 0

        # Atualizar timer de abdução
        if self.is_being_abducted:
            self.abduction_timer += 1
            self.blink_timer += 1

    def take_hit(self):
        """Método chamado quando o personagem é atingido"""
        self.is_hit = True
        self.hit_timer = 30  # 30 frames = 0.5 segundos a 60 FPS
        self.is_invulnerable = True
        self.invulnerability_timer = 300  # 5 segundos de invulnerabilidade
        self.blink_timer = 0

    def start_abduction(self):
        """Método chamado quando o personagem entra na área de abdução"""
        self.is_being_abducted = True
        self.abduction_timer = 0
        self.blink_timer = 0

    def shoot(self, bullet_image=None, game=None):
        """Criar um novo tiro usando pool de objetos se disponível"""
        if self.shoot_cooldown <= 0:
            # Determinar direção do tiro baseado no movimento
            direction = 1 if self.vel_x >= 0 else -1

            # Posição do tiro (centro do personagem)
            bullet_x = self.x + self.width // 2
            bullet_y = self.y + self.height // 2

            # Criar tiro usando pool se disponível
            if game and hasattr(game, "get_pooled_bullet"):
                bullet = game.get_pooled_bullet(
                    bullet_x, bullet_y, direction, bullet_image
                )
            else:
                bullet = Bullet(bullet_x, bullet_y, direction, bullet_image)
            self.bullets.append(bullet)

            # Resetar cooldown
            self.shoot_cooldown = self.max_shoot_cooldown

            # Disparar animação de tiro por alguns frames
            self.shooting_timer = 10

            # Retornar sinal de que atirou
            return True
        return False

    def update(
        self, platforms, bullet_image=None, camera_x=0, joystick=None, game=None
    ):
        # Aplicar gravidade
        self.vel_y += GRAVITY

        # Movimento horizontal
        keys = pygame.key.get_pressed()
        joystick_x = 0

        # Verificar entrada do joystick
        if joystick and joystick.get_numaxes() >= 1:
            joystick_x = joystick.get_axis(0)  # Eixo X do analógico esquerdo
            # Aplicar zona morta para evitar drift
            if abs(joystick_x) < 0.1:
                joystick_x = 0

        # Movimento com teclado ou joystick
        if keys[pygame.K_LEFT] or keys[pygame.K_a] or joystick_x < -0.1:
            self.vel_x = -PLAYER_SPEED
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d] or joystick_x > 0.1:
            self.vel_x = PLAYER_SPEED
        else:
            self.vel_x = 0

        # Sistema de agachamento
        joystick_y = 0
        joystick_crouch = False

        # Verificar entrada do joystick para agachamento
        if joystick and joystick.get_numaxes() >= 2:
            joystick_y = joystick.get_axis(1)  # Eixo Y do analógico esquerdo
            if joystick_y > 0.5:  # Analógico para baixo
                joystick_crouch = True

        if keys[pygame.K_DOWN] or keys[pygame.K_s] or joystick_crouch:
            if not self.is_crouching and self.on_ground:
                # Começar a agachar
                old_y = self.y
                self.height = self.crouched_height
                self.y = old_y + (self.original_height - self.crouched_height)
                self.is_crouching = True
        else:
            if self.is_crouching:
                # Parar de agachar
                old_y = self.y
                self.height = self.original_height
                self.y = old_y - (self.original_height - self.crouched_height)
                self.is_crouching = False

        # Tiro com barra de espaço ou botão do joystick
        joystick_shoot = False
        if joystick and joystick.get_numbuttons() > 1:
            joystick_shoot = joystick.get_button(1)  # Botão B/Círculo para tiro

        shot_sound = False
        if keys[pygame.K_SPACE] or joystick_shoot:
            shot_sound = self.shoot(bullet_image, game)

        # Pulo com setas/WASD ou botão/analógico do joystick
        joystick_jump = False
        if joystick:
            # Botão A/X para pulo
            if joystick.get_numbuttons() > 0:
                joystick_jump = joystick.get_button(0)
            # Ou analógico para cima
            if joystick.get_numaxes() >= 2 and joystick_y < -0.5:
                joystick_jump = True

        jump_sound = False
        # Pulo baseado em detecção de PRESS (borda de subida) para permitir segundo salto quando desejado
        want_jump = (keys[pygame.K_UP] or keys[pygame.K_w]) or joystick_jump
        press_jump = want_jump and not self.jump_was_down
        if press_jump:
            if self.on_ground and not self.is_crouching:
                # Primeiro salto a partir do chão
                self.vel_y = JUMP_STRENGTH
                self.on_ground = False
                jump_sound = True
            elif self.double_jump_enabled and self.remaining_jumps > 0:
                # Segundo salto no ar quando habilitado
                self.vel_y = JUMP_STRENGTH
                self.remaining_jumps -= 1
                jump_sound = True

        # Atualizar posição
        self.x += self.vel_x
        self.y += self.vel_y

        # Limitar movimento horizontal apenas no lado esquerdo
        if self.x < 0:
            self.x = 0

        # Verificar se caiu da tela
        if self.y > HEIGHT:
            return False  # Game over

        # Atualizar rect
        self.rect.x = self.x
        self.rect.y = self.y

        # Verificar colisões com plataformas
        self.prev_vel_y = self.vel_y  # Salvar velocidade anterior
        self.on_ground = False

        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                # Colisão por cima (jogador pousando na plataforma) - com tolerância de 3px
                if self.vel_y > 0 and self.y <= platform.y + 3:
                    self.y = platform.y - self.height
                    # Detectar se acabou de pousar (estava caindo e agora parou)
                    if self.prev_vel_y > 0:
                        self.just_landed = True
                        self.landed_platform_id = platform.id
                    self.vel_y = 0
                    self.on_ground = True
                    self.rect.y = self.y
                    # Reset dos saltos disponíveis
                    self.remaining_jumps = 2 if self.double_jump_enabled else 1

        # Atualizar tiros e remover os que saíram da área visível
        for bullet in self.bullets[:]:
            bullet.update()
            # Remover tiro se saiu muito da área visível da câmera
            if bullet.x < camera_x - 300 or bullet.x > camera_x + WIDTH + 300:
                self.bullets.remove(bullet)
                # Retornar bala ao pool se disponível
                if game and hasattr(game, "return_bullet_to_pool"):
                    game.return_bullet_to_pool(bullet)

        # Atualizar cooldown de tiro
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

        # Atualizar animação
        self.update_animation()

        # Decaimento do power-up de pulo duplo
        if self.double_jump_frames_left > 0:
            self.double_jump_frames_left -= 1
            if self.double_jump_frames_left <= 0:
                self.double_jump_enabled = False
                # Garantir reset de saltos ao desabilitar
                self.remaining_jumps = 1

        # Atualizar estado de borda da entrada de pulo
        self.jump_was_down = want_jump

        # Retornar ação baseada nos sons
        if jump_sound:
            return "jump"
        elif shot_sound:
            return "shot"
        else:
            return True

    def draw(self, screen):
        # Desenhar o sprite atual do personagem
        if (
            self.current_animation in self.sprites
            and self.sprites[self.current_animation]
        ):
            current_sprite = self.sprites[self.current_animation][self.animation_frame]

            # Ajustar posição Y para sprites agachados (sem redimensionar)
            draw_y = self.y
            if self.current_animation == "crouch" or self.current_animation == "shoot_crouch":
                # Ajustar posição Y para que o sprite apareça na posição correta
                # quando agachado (sprite mantém tamanho original)
                draw_y = self.y + (self.height - current_sprite.get_height())

            # Efeito de piscar durante invulnerabilidade ou abdução
            if self.is_invulnerable or self.is_being_abducted:
                # Piscar a cada 8 frames entre normal e esmaecido
                if (self.blink_timer // 8) % 2 == 0:
                    # Sprite normal
                    screen.blit(current_sprite, (self.x, draw_y))
                else:
                    # Sprite esmaecido
                    faded_sprite = current_sprite.copy()
                    alpha_value = 80 if self.is_invulnerable else 120  # Menos transparente durante abdução
                    faded_sprite.set_alpha(alpha_value)
                    screen.blit(faded_sprite, (self.x, draw_y))
            else:
                # Sprite normal quando não invulnerável nem sendo abduzido
                screen.blit(current_sprite, (self.x, draw_y))
        else:
            # Fallback: desenhar retângulo colorido
            color = RED if self.is_hit else BLUE

            # Efeito de piscar durante invulnerabilidade ou abdução no fallback também
            if self.is_invulnerable or self.is_being_abducted:
                if (self.blink_timer // 8) % 2 == 0:
                    # Retângulo normal
                    pygame.draw.rect(screen, color, self.rect)
                else:
                    # Retângulo esmaecido
                    fade_surface = pygame.Surface(
                        (self.width, self.height), pygame.SRCALPHA
                    )
                    alpha_value = 80 if self.is_invulnerable else 120  # Menos transparente durante abdução
                    fade_surface.fill((*color, alpha_value))
                    screen.blit(fade_surface, (self.x, self.y))
            else:
                pygame.draw.rect(screen, color, self.rect)

        # Tiros são desenhados no método draw da classe Game com offset da câmera
