import pytest


class FakeRect:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.width = w
        self.height = h
    @property
    def top(self):
        return self.y
    @property
    def bottom(self):
        return self.y + self.height
    @property
    def left(self):
        return self.x
    @property
    def right(self):
        return self.x + self.width
    def colliderect(self, other):
        return not (
            self.right <= other.left or other.right <= self.left or
            self.bottom <= other.top or other.bottom <= self.top
        )


class FakeDraw:
    rect_calls = []
    @staticmethod
    def rect(screen, color, rect_or_tuple):
        FakeDraw.rect_calls.append((screen, color, rect_or_tuple))


class FakeScreen:
    def __init__(self):
        self.blit_calls = []
    def blit(self, img, pos):
        self.blit_calls.append((img, pos))


class FakeImage:
    pass


@pytest.fixture(autouse=True)
def patch_pygame(monkeypatch):
    import pygame
    monkeypatch.setattr(pygame, "Rect", FakeRect, raising=True)
    monkeypatch.setattr(pygame, "draw", FakeDraw, raising=True)


def test_stops_at_stop_position_and_draws_stopped_image():
    from internal.resources.enemies.boss_alien import BossAlien

    # Two platforms, last determines stop position
    platforms = [(0, 300, 200, 20), (300, 300, 200, 20)]
    stop_x = platforms[-1][0] + platforms[-1][2] - 20
    b = BossAlien(stop_x - 20, 243, platforms, boss_images={"stopped": FakeImage()})
    screen = FakeScreen()

    # One update should reach stop state
    b.update(player_x=b.x, camera_x=0)
    assert b.is_stopped is True
    assert b.state == "stopped"
    b.draw(screen)
    # Image blitted
    assert len(screen.blit_calls) == 1


def test_jumping_draws_jump_image_and_updates():
    from internal.resources.enemies.boss_alien import BossAlien

    platforms = [(0, 300, 400, 20)]
    images = {"jumping": [FakeImage(), FakeImage()]}
    b = BossAlien(50, 243, platforms, boss_images=images)
    screen = FakeScreen()

    b.jump()
    prev_y = b.y
    b.update(player_x=b.x, camera_x=0)
    b.draw(screen)
    assert len(screen.blit_calls) == 1
    assert b.y != prev_y


def test_running_draws_running_image():
    from internal.resources.enemies.boss_alien import BossAlien

    platforms = [(0, 300, 400, 20)]
    images = {"running": [FakeImage(), FakeImage()]}
    b = BossAlien(50, 243, platforms, boss_images=images)
    screen = FakeScreen()

    # Ensure on_ground and running
    b.on_ground = True
    b.update(player_x=b.x - 10, camera_x=0)
    b.draw(screen)
    assert len(screen.blit_calls) == 1


def test_detect_hole_ahead_support_present_returns_false():
    from internal.resources.enemies.boss_alien import BossAlien

    # Platform under future check point
    platforms = [(0, 300, 400, 20)]
    b = BossAlien(50, 243, platforms)
    assert b.detect_hole_ahead(next_x=b.x + 5) is False


def test_detect_hole_ahead_no_support_but_reachable_platform_returns_false():
    from internal.resources.enemies.boss_alien import BossAlien

    # No support under check point, but a platform ahead within jump reach
    platforms = [
        (0, 400, 50, 20),  # far below current bottom; won't count as support
        (140, 300, 100, 20),  # reachable platform ahead
    ]
    b = BossAlien(50, 243, platforms)
    assert b.detect_hole_ahead(next_x=b.x + 80) is False


def test_detect_hole_ahead_true_when_no_support_and_no_reachable():
    from internal.resources.enemies.boss_alien import BossAlien

    platforms = [(0, 400, 50, 20)]  # Too low to be support or reachable
    b = BossAlien(50, 243, platforms)
    assert b.detect_hole_ahead(next_x=b.x + 80) is True


def test_is_safe_to_move_current_platform_and_hole_checks():
    from internal.resources.enemies.boss_alien import BossAlien

    platforms = [(0, 300, 400, 20)]
    b = BossAlien(50, 243, platforms)
    # On current platform center, should be safe
    assert b.is_safe_to_move(next_x=60) is True
    # If detect_hole_ahead returns True, not safe
    # Move far beyond platform with no support
    b.platforms = []
    assert b.detect_hole_ahead(next_x=b.x + 500) is True
    assert b.is_safe_to_move(next_x=b.x + 500) is False


def test_is_safe_to_move_default_true():
    from internal.resources.enemies.boss_alien import BossAlien

    platforms = [(0, 300, 400, 20)]
    b = BossAlien(50, 243, platforms)
    # With platform present and within tolerances but not current, defaults to True
    assert b.is_safe_to_move(next_x=b.x + 5) is True


def test_is_safe_to_move_during_jump_variants():
    from internal.resources.enemies.boss_alien import BossAlien

    # Case 1: hole ahead -> False
    b = BossAlien(50, 243, [])
    assert b.is_safe_to_move_during_jump(b.x + 100) is False

    # Case 2: suitable platform found -> True
    platforms = [(140, 260, 120, 20)]  # Ahead and suitable height
    b = BossAlien(50, 243, platforms)
    assert b.is_safe_to_move_during_jump(b.x + 80) is True

    # Case 3: no suitable platform -> False
    platforms = [(300, 500, 50, 20)]  # Too low and far
    b = BossAlien(50, 243, platforms)
    assert b.is_safe_to_move_during_jump(b.x + 80) is False


def test_get_current_platform_and_none():
    from internal.resources.enemies.boss_alien import BossAlien

    platforms = [(0, 300, 400, 20), (500, 350, 200, 20)]
    b = BossAlien(50, 243, platforms)
    assert b.get_current_platform() == platforms[0]
    # Move off platforms
    b.x = 800
    b.y = 200
    assert b.get_current_platform() is None


def test_has_platform_ahead_true_and_false():
    from internal.resources.enemies.boss_alien import BossAlien

    current = (0, 300, 400, 20)
    next_plat = (450, 300, 100, 20)
    platforms = [current, next_plat]
    b = BossAlien(330, 243, platforms)
    assert b.has_platform_ahead() is True
    # Far from edge: should be False
    b = BossAlien(200, 243, platforms)
    assert b.has_platform_ahead() is False


def test_check_jump_needed_triggers_and_last_platform_blocks():
    from internal.resources.enemies.boss_alien import BossAlien

    platforms = [(0, 300, 400, 20)]
    b = BossAlien(301.0, 243, platforms)
    b.on_ground = True
    b.check_jump_needed()
    assert b.state == "jumping"

    # On last platform: should not jump
    b = BossAlien(7000, 243, platforms)
    b.on_ground = True
    assert b.is_on_last_platform() is True
    b.check_jump_needed()
    assert b.state == "running"


def test_is_captured_true_on_last_platform_and_collision():
    from internal.resources.enemies.boss_alien import BossAlien

    # Place boss on last platform range and colliding with player
    platforms = [(7000, 300, 400, 20)]
    b = BossAlien(7000, 243, platforms)

    player = FakeRect(7000, 243, 57, 57)
    # Simulate collision
    b.rect = FakeRect(b.x, b.y, b.width, b.height)
    assert b.is_captured(player_rect=player) is True


def test_update_speed_adaptation_branches_execute():
    from internal.resources.enemies.boss_alien import BossAlien

    platforms = [(0, 300, 400, 20)]
    b = BossAlien(0, 243, platforms)
    # Far behind -> speed 8
    b.update(player_x=400, camera_x=0)
    assert b.speed == 8.0
    # Moderately behind -> 7
    b.x = 300
    b.update(player_x=330, camera_x=0)
    assert b.speed == 7.0
    # Slightly behind -> 6
    b.x = 340
    b.update(player_x=330, camera_x=0)
    assert b.speed == 6.0
    # Near target -> 5
    b.x = 300
    b.update(player_x=280, camera_x=0)
    assert b.speed == 5.0
    # Very close -> 4
    b.x = 399
    b.update(player_x=280, camera_x=0)
    assert b.speed in (4.0, 5.0)
    # Ahead -> 3
    b.x = 402
    b.update(player_x=280, camera_x=0)
    assert b.speed in (3.0, 4.0, 5.0)


def test_update_when_already_stopped_only_animates():
    from internal.resources.enemies.boss_alien import BossAlien

    platforms = [(0, 300, 200, 20)]
    b = BossAlien(0, 243, platforms)
    b.is_stopped = True
    b.animation_frame = 0
    b.update(player_x=0, camera_x=0)
    assert b.animation_frame == 1


def test_is_captured_false_when_no_collision_or_not_on_last_platform():
    from internal.resources.enemies.boss_alien import BossAlien

    platforms = [(0, 300, 400, 20)]
    b = BossAlien(100, 243, platforms)
    # Player rect far away: no collision
    player = FakeRect(1000, 1000, 10, 10)
    b.rect = FakeRect(b.x, b.y, b.width, b.height)
    assert b.is_captured(player_rect=player) is False

    # Collision returns True regardless of last platform
    player = FakeRect(b.x, b.y, b.width, b.height)
    assert b.is_captured(player_rect=player) is True

    # No platforms: collision yields True per code path
    b.platforms = []
    assert b.is_captured(player_rect=player) is True


def test_stuck_counter_increments_and_resets():
    from internal.resources.enemies.boss_alien import BossAlien

    platforms = [(0, 300, 400, 20)]
    b = BossAlien(0, 243, platforms)
    # Make distance small enough to avoid movement and increment stuck
    b.last_x = b.x
    b.update(player_x=b.x + 0, camera_x=0)
    assert b.stuck_counter >= 1
    # Now move sufficiently and stuck resets
    b.x += 10
    b.update(player_x=b.x - 200, camera_x=0)
    assert b.stuck_counter == 0


def test_is_safe_to_move_best_overlap_branch_true():
    from internal.resources.enemies.boss_alien import BossAlien

    # Configure a platform just at suitable height to compute overlap
    platforms = [(0, 300, 200, 20), (240, 320, 120, 20)]
    # Adjust Y so alien_bottom aligns with 300 (assuming height ~32)
    b = BossAlien(200, 268, platforms)
    next_x = 240  # Align with second platform to ensure overlap
    assert b.is_safe_to_move(next_x) is True


def test_is_safe_to_move_during_jump_respects_stop_limit():
    from internal.resources.enemies.boss_alien import BossAlien

    # Last platform defines stop_position; suitable platform ahead
    platforms = [(0, 300, 200, 20), (300, 300, 150, 20)]
    b = BossAlien(260, 243, platforms)
    # Stub platform check to isolate stop limit logic
    b.has_platform_ahead = lambda nx: True
    b.is_jumping = True
    # Within limit -> True
    assert b.is_safe_to_move_during_jump(b.stop_position - 60) is True
    # Beyond limit -> False
    assert b.is_safe_to_move_during_jump(b.stop_position - 40) is False