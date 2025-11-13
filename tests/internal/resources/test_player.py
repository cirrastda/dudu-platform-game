import types

import internal.resources.player as player_mod
from internal.utils.constants import WIDTH, HEIGHT, GRAVITY, PLAYER_SPEED, JUMP_STRENGTH


class FakeRect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def colliderect(self, other):
        return not (
            self.x + self.w <= other.x
            or self.x >= other.x + other.w
            or self.y + self.h <= other.y
            or self.y >= other.y + other.h
        )


class FakeSurface:
    def __init__(self, w=10, h=10):
        self._w = w
        self._h = h

    def get_height(self):
        return self._h

    def copy(self):
        return FakeSurface(self._w, self._h)

    def set_alpha(self, a):
        # no-op
        pass

    def fill(self, color):
        # no-op for tests
        pass


class FakeTransform:
    @staticmethod
    def scale(img, size):
        return FakeSurface(size[0], size[1])


class FakeDraw:
    @staticmethod
    def rect(screen, color, rect):
        screen.draw_calls.append(("rect", color, rect.x, rect.y, rect.w, rect.h))


class FakeKeys:
    def __init__(self):
        self._state = {}

    def set(self, key, value):
        self._state[key] = value

    def __getitem__(self, key):
        return self._state.get(key, False)


class FakeKeyModule:
    def __init__(self, keys):
        self._keys = keys

    def get_pressed(self):
        return self._keys


class FakeScreen:
    def __init__(self):
        self.blit_calls = []
        self.draw_calls = []

    def blit(self, sprite, pos):
        self.blit_calls.append((pos[0], pos[1], getattr(sprite, "_w", None), getattr(sprite, "_h", None)))


class FakeJoystick:
    def __init__(self, axes=None, buttons=None):
        self._axes = axes or {0: 0.0, 1: 0.0}
        self._buttons = buttons or {0: 0, 1: 0}

    def get_numaxes(self):
        return len(self._axes)

    def get_axis(self, idx):
        return self._axes.get(idx, 0.0)

    def get_numbuttons(self):
        return len(self._buttons)

    def get_button(self, idx):
        return self._buttons.get(idx, 0)


class FakePlatform:
    def __init__(self, x, y, w, h, pid=1):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.id = pid
        self.rect = FakeRect(x, y, w, h)


class FakeBullet:
    def __init__(self, x, y, direction, image=None):
        self.x = x
        self.y = y
        self.direction = direction
        self.rect = FakeRect(x, y, 10, 5)

    def update(self):
        self.x += 12 * self.direction
        self.rect.x = self.x


def _install_fake_pygame(monkeypatch, keys):
    # Define key constants used in player.update
    K = types.SimpleNamespace(
        K_LEFT="K_LEFT",
        K_RIGHT="K_RIGHT",
        K_a="K_a",
        K_d="K_d",
        K_DOWN="K_DOWN",
        K_s="K_s",
        K_SPACE="K_SPACE",
        K_UP="K_UP",
        K_w="K_w",
        SRCALPHA=1,
    )

    fake_pygame = types.SimpleNamespace(
        Rect=FakeRect,
        Surface=lambda size, flags=None: FakeSurface(size[0], size[1]),
        transform=FakeTransform,
        draw=FakeDraw,
        key=FakeKeyModule(keys),
        image=types.SimpleNamespace(load=lambda p: FakeSurface(20, 20)),
        SRCALPHA=1,
        K_LEFT=K.K_LEFT,
        K_RIGHT=K.K_RIGHT,
        K_a=K.K_a,
        K_d=K.K_d,
        K_DOWN=K.K_DOWN,
        K_s=K.K_s,
        K_SPACE=K.K_SPACE,
        K_UP=K.K_UP,
        K_w=K.K_w,
        error=Exception,
    )
    monkeypatch.setattr(player_mod, "pygame", fake_pygame, raising=False)


def test_update_landing_then_jump(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(50, 40)
    platforms = [FakePlatform(0, 120, 200, 12, pid=7)]

    # First update: fall due to gravity and land on platform
    rv = p.update(platforms, bullet_image=None, camera_x=0, joystick=None, game=None)
    assert rv is True
    assert p.on_ground is True
    assert p.just_landed is True
    assert p.landed_platform_id == 7
    assert p.vel_y == 0
    assert p.y == platforms[0].y - p.height

    # Second update: press jump, should return "jump"
    keys.set(player_mod.pygame.K_UP, True)
    rv2 = p.update(platforms, bullet_image=None, camera_x=0, joystick=None, game=None)
    assert rv2 == "jump"
    assert p.on_ground is False
    assert p.vel_y == JUMP_STRENGTH


def test_shoot_cooldown_direction_and_offscreen_pool(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(100, 100)
    p.vel_x = -2  # ensure direction is -1 when shooting

    returned = []

    class Game:
        def get_pooled_bullet(self, x, y, direction, image):
            return FakeBullet(x, y, direction, image)

        def return_bullet_to_pool(self, bullet):
            returned.append(bullet)

    # First shoot should create a bullet and set cooldown
    ok = p.shoot(bullet_image=None, game=Game())
    assert ok is True
    assert len(p.bullets) == 1
    assert p.shoot_cooldown == p.max_shoot_cooldown
    assert p.bullets[0].direction == -1

    # Second shoot should fail due to cooldown
    ok2 = p.shoot(bullet_image=None, game=Game())
    assert ok2 is False

    # Add an offscreen bullet and update: should be removed and returned to pool
    off = FakeBullet(WIDTH + 400, 100, 1)
    p.bullets.append(off)
    rv = p.update([], bullet_image=None, camera_x=0, joystick=None, game=Game())
    assert rv is True
    assert off in returned
    assert off not in p.bullets


def test_crouch_toggle_and_animation_states(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)
    p.on_ground = True

    # Crouch while on ground
    keys.set(player_mod.pygame.K_DOWN, True)
    p.update([], bullet_image=None, camera_x=0, joystick=None, game=None)
    assert p.is_crouching is True
    assert p.height == p.crouched_height

    # Stand up
    keys.set(player_mod.pygame.K_DOWN, False)
    p.update([], bullet_image=None, camera_x=0, joystick=None, game=None)
    assert p.is_crouching is False
    assert p.height == p.original_height

    # Animation state selection
    p.is_hit = True
    p.hit_timer = 5
    p.on_ground = True
    p.vel_x = 0
    p.update_animation()
    assert p.current_animation == "hit"

    p.is_hit = False
    p.is_crouching = True
    p.update_animation()
    assert p.current_animation == "crouch"

    p.is_crouching = False
    p.on_ground = False
    p.vel_y = -12
    p.update_animation()
    assert p.current_animation == "jump"

    p.on_ground = True
    p.vel_x = PLAYER_SPEED
    p.update_animation()
    assert p.current_animation == "walk"

    p.vel_x = 0
    p.update_animation()
    assert p.current_animation == "idle"


def test_draw_blinking_and_fallback(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(10, 20)
    screen = FakeScreen()

    # Ensure we have a sprite to draw
    p.current_animation = "idle"
    p.sprites["idle"] = [FakeSurface(20, 30)]

    # Invulnerable blinking: one normal blit, one faded blit
    p.is_invulnerable = True
    p.blink_timer = 0
    p.draw(screen)
    p.blink_timer = 8
    p.draw(screen)
    assert len(screen.blit_calls) >= 2

    # Fallback path: empty sprites uses draw.rect
    p.sprites = {}
    p.is_invulnerable = False
    p.draw(screen)
    # One of the draw calls should be a rect
    assert any(c[0] == "rect" for c in screen.draw_calls)


def test_load_sprites_fallback_on_error(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    # Force pygame.image.load to raise error to hit fallback path in load_sprites
    def raise_error(_):
        raise player_mod.pygame.error("boom")

    monkeypatch.setattr(player_mod.pygame.image, "load", raise_error, raising=False)

    p = player_mod.Player(0, 0)
    # Fallback should populate all animations
    assert set(p.sprites.keys()) == {"idle", "walk", "jump", "crouch", "hit"}
    assert len(p.sprites["walk"]) == 4
    assert len(p.sprites["jump"]) == 5
    # Crouch sprite should use crouched height in fallback
    assert p.sprites["crouch"][0].get_height() == p.crouched_height


def test_update_animation_jump_frame_mapping(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)
    p.current_animation = "jump"
    # Make frame advance trigger every call
    p.animation_speed = 60

    p.vel_y = -11  # Subindo rápido
    p.update_animation()
    assert p.animation_frame == 0

    p.vel_y = -6  # Subindo devagar
    p.update_animation()
    assert p.animation_frame == 1

    p.vel_y = 0  # No ar
    p.update_animation()
    assert p.animation_frame == 2

    p.vel_y = 7  # Descendo
    p.update_animation()
    assert p.animation_frame == 3

    p.vel_y = 15  # Aterrissando
    p.update_animation()
    assert p.animation_frame == 4


def test_take_hit_and_invulnerability_timers(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)
    p.take_hit()
    assert p.is_hit is True
    assert p.hit_timer == 30
    assert p.is_invulnerable is True
    assert p.invulnerability_timer == 300
    assert p.blink_timer == 0

    # Progress timers via update_animation
    p.update_animation()
    assert p.invulnerability_timer == 299
    assert p.blink_timer == 1


def test_abduction_blinking_draw(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(10, 20)
    screen = FakeScreen()

    # Prepare a sprite
    p.current_animation = "idle"
    p.sprites["idle"] = [FakeSurface(20, 30)]

    # Abduction blinking: one normal blit, one faded blit
    p.start_abduction()
    p.blink_timer = 0
    p.draw(screen)
    p.blink_timer = 8
    p.draw(screen)
    assert len(screen.blit_calls) >= 2


def test_update_with_joystick_movement_and_crouch(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(50, 50)
    p.on_ground = True
    # Move left with joystick
    js = FakeJoystick(axes={0: -0.2, 1: 0.0}, buttons={0: 0, 1: 0})
    rv = p.update([], bullet_image=None, camera_x=0, joystick=js, game=None)
    assert rv is True
    assert p.vel_x == -PLAYER_SPEED
    # Crouch with joystick Y down
    js2 = FakeJoystick(axes={0: 0.0, 1: 0.6}, buttons={0: 0, 1: 0})
    # Garantir que ainda está no chão para permitir agachar
    p.on_ground = True
    rv2 = p.update([], bullet_image=None, camera_x=0, joystick=js2, game=None)
    assert rv2 is True
    assert p.is_crouching is True
    assert p.height == p.crouched_height


def test_update_returns_shot_on_space(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)

    class Game:
        def get_pooled_bullet(self, x, y, direction, image):
            return FakeBullet(x, y, direction, image)

    keys.set(player_mod.pygame.K_SPACE, True)
    rv = p.update([], bullet_image=None, camera_x=0, joystick=None, game=Game())
    assert rv == "shot"


def test_update_returns_false_on_fall_off_screen(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, HEIGHT + 5)
    rv = p.update([], bullet_image=None, camera_x=0, joystick=None, game=None)
    assert rv is False


def test_left_clamp_when_moving_left_beyond_zero(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)
    # Simulate left movement
    keys.set(player_mod.pygame.K_LEFT, True)
    p.update([], bullet_image=None, camera_x=0, joystick=None, game=None)
    assert p.x == 0


def test_bullet_removal_without_pool(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)
    # Add an offscreen bullet and update without game pool
    off = FakeBullet(WIDTH + 400, 100, 1)
    p.bullets.append(off)
    rv = p.update([], bullet_image=None, camera_x=0, joystick=None, game=None)
    assert rv is True
    assert off not in p.bullets


def test_update_animation_hit_timer_expires_clears_is_hit(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)
    p.is_hit = True
    p.hit_timer = 1
    p.update_animation()
    assert p.is_hit is False


def test_draw_crouch_offsets_y(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(10, 100)
    screen = FakeScreen()

    # Enter crouch state
    p.on_ground = True
    keys.set(player_mod.pygame.K_DOWN, True)
    p.update([], bullet_image=None, camera_x=0, joystick=None, game=None)

    # Prepare crouch sprite
    p.current_animation = "crouch"
    p.sprites["crouch"] = [FakeSurface(p.width, p.original_height)]
    pre = len(screen.blit_calls)
    p.draw(screen)
    assert len(screen.blit_calls) == pre + 1
    # Validate y offset logic applied
    last = screen.blit_calls[-1]
    expected_y = p.y + (p.height - p.sprites["crouch"][0].get_height())
    assert last[1] == expected_y


def test_joystick_jump_via_axis(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)
    p.on_ground = True
    js = FakeJoystick(axes={0: 0.0, 1: -0.6}, buttons={0: 0, 1: 0})
    rv = p.update([], bullet_image=None, camera_x=0, joystick=js, game=None)
    assert rv == "jump"


def test_joystick_shoot_button(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)

    class Game:
        def get_pooled_bullet(self, x, y, direction, image):
            return FakeBullet(x, y, direction, image)

    js = FakeJoystick(axes={0: 0.0, 1: 0.0}, buttons={0: 0, 1: 1})
    rv = p.update([], bullet_image=None, camera_x=0, joystick=js, game=Game())
    assert rv == "shot"


def test_fallback_blinking_invulnerable(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(10, 10)
    screen = FakeScreen()
    # No sprites -> fallback
    p.sprites = {}
    p.is_invulnerable = True
    p.blink_timer = 0
    p.draw(screen)
    p.blink_timer = 8
    p.draw(screen)
    # Should have both a rect draw and a blit of fade surface
    assert any(c[0] == "rect" for c in screen.draw_calls)
    assert len(screen.blit_calls) >= 1


def test_joystick_deadzone_results_no_movement(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)
    js = FakeJoystick(axes={0: 0.05, 1: 0.0}, buttons={0: 0, 1: 0})
    rv = p.update([], bullet_image=None, camera_x=0, joystick=js, game=None)
    assert rv is True
    assert p.vel_x == 0


def test_update_animation_walk_cycle_wraps(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)
    # Define a small walk animation list to test wrap
    p.sprites["walk"] = [FakeSurface(p.width, p.original_height), FakeSurface(p.width, p.original_height)]
    p.current_animation = "walk"
    p.on_ground = True
    p.vel_x = PLAYER_SPEED
    p.animation_frame = 0
    p.animation_speed = 60
    p.update_animation()
    assert p.animation_frame == 1
    p.update_animation()
    assert p.animation_frame == 0


def test_fallback_blinking_abduction(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(5, 5)
    screen = FakeScreen()
    p.sprites = {}
    p.is_being_abducted = True
    p.blink_timer = 0
    p.draw(screen)
    p.blink_timer = 8
    p.draw(screen)
    assert any(c[0] == "rect" for c in screen.draw_calls)
    assert len(screen.blit_calls) >= 1


def test_move_right_with_keyboard(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)
    keys.set(player_mod.pygame.K_RIGHT, True)
    rv = p.update([], bullet_image=None, camera_x=0, joystick=None, game=None)
    assert rv is True
    assert p.vel_x == PLAYER_SPEED


def test_shoot_without_game_instantiates_bullet(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)
    # Garantir que o caminho sem pool use um Bullet válido
    player_mod.Bullet = FakeBullet
    ok = p.shoot(bullet_image=None, game=None)
    assert ok is True
    assert len(p.bullets) == 1
    assert p.shoot_cooldown == p.max_shoot_cooldown


def test_joystick_jump_via_button(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)
    p.on_ground = True
    js = FakeJoystick(axes={0: 0.0, 1: 0.0}, buttons={0: 1, 1: 0})
    rv = p.update([], bullet_image=None, camera_x=0, joystick=js, game=None)
    assert rv == "jump"


def test_update_animation_abduction_increments_timers(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)
    p.start_abduction()
    assert p.abduction_timer == 0
    assert p.blink_timer == 0
    p.update_animation()
    assert p.abduction_timer == 1
    assert p.blink_timer == 1


def test_invulnerability_expires_resets_flag_and_blink(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)
    p.is_invulnerable = True
    p.invulnerability_timer = 1
    p.blink_timer = 0
    p.update_animation()
    assert p.is_invulnerable is False
    assert p.invulnerability_timer == 0
    assert p.blink_timer == 0


def test_bullet_removal_left_of_camera_without_pool(monkeypatch):
    keys = FakeKeys()
    _install_fake_pygame(monkeypatch, keys)

    p = player_mod.Player(0, 0)
    left = FakeBullet(-400, 50, -1)
    p.bullets.append(left)
    rv = p.update([], bullet_image=None, camera_x=0, joystick=None, game=None)
    assert rv is True
    assert left not in p.bullets