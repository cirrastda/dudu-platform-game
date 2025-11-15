import pygame
from internal.utils.functions import resource_path


class ResourceCache:
    """Sistema de cache para imagens e sons para otimizar uso de memória"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResourceCache, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self.image_cache = {}
        self.sound_cache = {}
        self.music_cache = {}
        self.cache_hits = 0
        self.cache_misses = 0

    def get_image(self, path, scale=None):
        """Carrega uma imagem do cache ou do disco"""
        cache_key = f"{path}_{scale}" if scale else path

        if cache_key in self.image_cache:
            self.cache_hits += 1
            return self.image_cache[cache_key]

        try:
            # Carregar imagem do disco usando caminho correto
            full_path = resource_path(path)
            image = pygame.image.load(full_path)
            # Converter para formato otimizado de exibição (com alpha)
            try:
                image = image.convert_alpha()
            except Exception:
                try:
                    image = image.convert()
                except Exception:
                    pass
            if scale:
                image = pygame.transform.scale(image, scale)
                # Garantir que a surface escalada também esteja convertida
                try:
                    image = image.convert_alpha()
                except Exception:
                    try:
                        image = image.convert()
                    except Exception:
                        pass

            # Armazenar no cache
            self.image_cache[cache_key] = image
            self.cache_misses += 1
            return image
        except pygame.error as e:
            print(f"Erro ao carregar imagem {path}: {e}")
            return None

    def get_sound(self, path):
        """Carrega um som do cache ou do disco"""
        if path in self.sound_cache:
            self.cache_hits += 1
            return self.sound_cache[path]

        try:
            # Carregar som usando caminho correto
            full_path = resource_path(path)
            sound = pygame.mixer.Sound(full_path)
            self.sound_cache[path] = sound
            self.cache_misses += 1
            return sound
        except pygame.error as e:
            print(f"Erro ao carregar som {path}: {e}")
            return None

    def preload_images(self, image_paths):
        """Pré-carrega uma lista de imagens"""
        for path_info in image_paths:
            if isinstance(path_info, tuple):
                path, scale = path_info
                self.get_image(path, scale)
            else:
                self.get_image(path_info)

    def preload_sounds(self, sound_paths):
        """Pré-carrega uma lista de sons"""
        for path in sound_paths:
            self.get_sound(path)

    def clear_cache(self):
        """Limpa o cache para liberar memória"""
        self.image_cache.clear()
        self.sound_cache.clear()
        self.music_cache.clear()

    def get_cache_stats(self):
        """Retorna estatísticas do cache"""
        total_requests = self.cache_hits + self.cache_misses
        hit_rate = (self.cache_hits / total_requests * 100) if total_requests > 0 else 0
        return {
            "hits": self.cache_hits,
            "misses": self.cache_misses,
            "hit_rate": hit_rate,
            "images_cached": len(self.image_cache),
            "sounds_cached": len(self.sound_cache),
        }
