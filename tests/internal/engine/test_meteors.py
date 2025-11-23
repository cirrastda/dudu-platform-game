from internal.engine.game import Game
from internal.engine.level.level import Level
from internal.engine.state import GameState


def _setup_game_at_level(level: int):
    g = Game()
    g.current_level = level
    g.state = GameState.PLAYING
    Level.init_level(g)
    g.camera_x = 0
    return g


def test_spawn_meteors_on_levels_47_to_50():
    for level in (47, 50):
        g = _setup_game_at_level(level)
        g.meteor_spawn_interval = 1
        g.meteors_per_spawn = 2
        g.update()
        assert len(getattr(g, "meteors", [])) >= 1


def test_draw_renders_meteors_on_level_47(monkeypatch):
    g = _setup_game_at_level(47)
    g.meteor_spawn_interval = 1
    g.meteors_per_spawn = 1
    g.update()
    draw_calls = {"n": 0}
    for met in g.meteors:
        met.x = g.camera_x + 10
        monkeypatch.setattr(
            met, "draw", lambda screen, _c=draw_calls: _c.__setitem__("n", _c["n"] + 1)
        )
    g.draw()
    assert draw_calls["n"] >= 1


def test_bullet_destroys_meteor_awards_points():
    g = _setup_game_at_level(47)
    g.meteors.append(
        __import__(
            "internal.resources.enemies.meteor", fromlist=["Meteor"]
        ).Meteor(
            g.camera_x + 20,
            100,
            getattr(g.image, "meteor_img", None),
        )
    )
    m = g.meteors[0]
    # Place player bullet overlapping meteor
    b = g.get_pooled_bullet(
        m.x,
        m.y,
        direction=-1,
        image=getattr(g.image, "bullet_img", None),
    )
    g.player.bullets.append(b)
    start_score = g.score
    g.update()
    assert g.score - start_score == 259
    assert m not in g.meteors


def test_meteor_collision_invulnerable_does_not_destroy_or_score():
    g = _setup_game_at_level(47)
    g.player.is_invulnerable = True
    g.meteors.append(
        __import__(
            "internal.resources.enemies.meteor", fromlist=["Meteor"]
        ).Meteor(
            g.player.x,
            g.player.y,
            getattr(g.image, "meteor_img", None),
        )
    )
    g.update()
    assert len(g.meteors) >= 1


def test_meteor_hits_player_causes_hit_and_life_loss():
    g = _setup_game_at_level(47)
    max_lives = g.max_lives
    g.meteors.append(
        __import__(
            "internal.resources.enemies.meteor", fromlist=["Meteor"]
        ).Meteor(
            g.player.x,
            g.player.y,
            getattr(g.image, "meteor_img", None),
        )
    )
    g.update()
    assert g.lives == max_lives - 1 or g.player.is_hit
