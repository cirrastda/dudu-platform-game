import os
import pygame

from internal.resources.cache import ResourceCache
from internal.utils.functions import resource_path


class SoundEffects:
    sound_effects = {}
    sound_volume = 0.8

    def __init__(self):
        self.sound_effects = {}
        self.sound_volume = 0.8

    def load_sound_effects(self):
        """Carregar efeitos sonoros do jogo usando sistema de cache"""
        try:
            # Inicializar cache de recursos
            cache = ResourceCache()

            # Carregar som de pulo usando cache
            jump_path = "sounds/jump.mp3"
            if os.path.exists(resource_path(jump_path)):
                sound = cache.get_sound(jump_path)
                if sound:
                    self.sound_effects["jump"] = sound
                    self.sound_effects["jump"].set_volume(self.sound_volume)
                    print("Som de pulo carregado com sucesso")
            else:
                print("Aviso: Arquivo sounds/jump.mp3 não encontrado")

            # Carregar som de explosão usando cache
            explosion_path = "sounds/explosion.mp3"
            if os.path.exists(resource_path(explosion_path)):
                sound = cache.get_sound(explosion_path)
                if sound:
                    self.sound_effects["explosion"] = sound
                    self.sound_effects["explosion"].set_volume(self.sound_volume)
                    print("Som de explosão carregado com sucesso")
            else:
                print("Aviso: Arquivo sounds/explosion.mp3 não encontrado")

            # Carregar som de tiro usando cache
            shot_path = "sounds/shot.mp3"
            if os.path.exists(resource_path(shot_path)):
                sound = cache.get_sound(shot_path)
                if sound:
                    self.sound_effects["shot"] = sound
                    self.sound_effects["shot"].set_volume(self.sound_volume)
                    print("Som de tiro carregado com sucesso")
            else:
                print("Aviso: Arquivo sounds/shot.mp3 não encontrado")

            # Carregar som de vida extra usando cache
            newlife_path = "sounds/new-life.mp3"
            if os.path.exists(resource_path(newlife_path)):
                sound = cache.get_sound(newlife_path)
                if sound:
                    self.sound_effects["new-life"] = sound
                    # Volume mais alto para se sobressair sobre a música de fundo
                    self.sound_effects["new-life"].set_volume(
                        min(1.0, self.sound_volume * 1.5)
                    )
                    print("Som de vida extra carregado com sucesso")
                    # Alias para coletar powerups quando não houver som dedicado
                    # Se existir um som específico de coletar, preferir ele
                    collect_path = "sounds/collect.mp3"
                    if os.path.exists(resource_path(collect_path)):
                        collect_sound = cache.get_sound(collect_path)
                        if collect_sound:
                            self.sound_effects["collect"] = collect_sound
                            self.sound_effects["collect"].set_volume(self.sound_volume)
                            print("Som de coleta carregado com sucesso")
                    else:
                        # Mapear 'collect' para 'new-life' como fallback
                        self.sound_effects["collect"] = self.sound_effects["new-life"]
                        print("Som 'collect' não encontrado; usando fallback de 'new-life'")
            else:
                print("Aviso: Arquivo sounds/new-life.mp3 não encontrado")
                # Ainda tentar carregar um som dedicado de 'collect' se existir
                collect_path = "sounds/collect.mp3"
                if os.path.exists(resource_path(collect_path)):
                    collect_sound = cache.get_sound(collect_path)
                    if collect_sound:
                        self.sound_effects["collect"] = collect_sound
                        self.sound_effects["collect"].set_volume(self.sound_volume)
                        print("Som de coleta carregado com sucesso")

            # Carregar som de fim de fase
            level_end_path = "sounds/level-end.mp3"
            if os.path.exists(resource_path(level_end_path)):
                sound = cache.get_sound(level_end_path)
                if sound:
                    self.sound_effects["level-end"] = sound
                    # leve destaque
                    self.sound_effects["level-end"].set_volume(min(1.0, self.sound_volume * 1.2))
                    print("Som de fim de fase carregado com sucesso")
            else:
                print("Aviso: Arquivo sounds/level-end.mp3 não encontrado")

            # Carregar som de game over
            game_over_path = "sounds/game-over.mp3"
            if os.path.exists(resource_path(game_over_path)):
                sound = cache.get_sound(game_over_path)
                if sound:
                    self.sound_effects["game-over"] = sound
                    # manter volume padrão
                    self.sound_effects["game-over"].set_volume(self.sound_volume)
                    print("Som de game over carregado com sucesso")
            else:
                print("Aviso: Arquivo sounds/game-over.mp3 não encontrado")

            # Carregar som de acerto em pássaro
            bird_hit_path = "sounds/bird-hit.mp3"
            if os.path.exists(resource_path(bird_hit_path)):
                sound = cache.get_sound(bird_hit_path)
                if sound:
                    self.sound_effects["bird-hit"] = sound
                    # ligeiramente mais alto para destacar o impacto
                    self.sound_effects["bird-hit"].set_volume(min(1.0, self.sound_volume * 1.2))
                    print("Som de bird-hit carregado com sucesso")
            else:
                print("Aviso: Arquivo sounds/bird-hit.mp3 não encontrado")

            # Carregar som de acerto em gota de chuva
            water_hit_path = "sounds/water-hit.mp3"
            if os.path.exists(resource_path(water_hit_path)):
                sound = cache.get_sound(water_hit_path)
                if sound:
                    self.sound_effects["water-hit"] = sound
                    # um pouco mais alto para destacar o estouro da gota
                    self.sound_effects["water-hit"].set_volume(min(1.0, self.sound_volume * 1.2))
                    print("Som de water-hit carregado com sucesso")
            else:
                print("Aviso: Arquivo sounds/water-hit.mp3 não encontrado")

            # Carregar som de jogador atingido
            player_hit_path = "sounds/player-hit.mp3"
            if os.path.exists(resource_path(player_hit_path)):
                sound = cache.get_sound(player_hit_path)
                if sound:
                    self.sound_effects["player-hit"] = sound
                    # manter volume padrão
                    self.sound_effects["player-hit"].set_volume(self.sound_volume)
                    print("Som de player-hit carregado com sucesso")
            else:
                print("Aviso: Arquivo sounds/player-hit.mp3 não encontrado")

        except pygame.error as e:
            print(f"Erro ao carregar efeitos sonoros: {e}")

    def play_sound_effect(self, sound_name):
        """Tocar um efeito sonoro específico"""
        if sound_name in self.sound_effects:
            try:
                self.sound_effects[sound_name].play()
            except pygame.error as e:
                print(f"Erro ao tocar efeito sonoro {sound_name}: {e}")
        else:
            print(f"Efeito sonoro '{sound_name}' não encontrado")
