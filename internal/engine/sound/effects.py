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
            else:
                print("Aviso: Arquivo sounds/new-life.mp3 não encontrado")

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
