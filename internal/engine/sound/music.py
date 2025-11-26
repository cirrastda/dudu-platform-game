import os
import io
import pygame
from internal.utils.functions import resource_path
from internal.engine.level.music import LevelMusic


class Music:
    INTRO = "intro"

    def start(self, game):
        game.current_music = None
        game.music_volume = 0.7

        # Volumes individuais para cada música (equalização)
        game.music_volumes = {
            self.INTRO: 0.6,  # Música do menu - geralmente mais alta
            "musicas/fundo1.mp3": 0.7,  # Volume padrão
            "musicas/fundo2.mp3": 0.8,  # Geralmente mais baixa
            "musicas/fundo3.mp3": 0.7,  # Volume padrão
            "musicas/fundo4.mp3": 0.6,  # Geralmente mais alta
        }
        self.load_music(game)

    def load_music(self, game):
        """Carregar todas as músicas do jogo"""
        game.music_files = {
            self.INTRO: "musicas/intro.mp3",  # Música do menu
        }

        level_music = LevelMusic()
        level_music_list = level_music.load_level_music_list()
        if not level_music_list:
            print("Erro: Nenhuma música de nível foi carregada.")
            return

        for level, music_file in level_music_list.items():
            game.music_files[level] = music_file

        # Verificar se os arquivos de música existem
        for level, music_file in game.music_files.items():
            if not self.check_music_exists(music_file):
                continue

    def check_music_exists(self, music_file):
        """Verificar se o arquivo de música existe"""
        full_path = resource_path(music_file)
        if not os.path.exists(full_path):
            print(f"Aviso: Arquivo de música não encontrado: {music_file}")
            return False
        return full_path

    def play_menu_music(self, game):
        """Tocar a música do menu"""
        music_file = game.music_files[self.INTRO]
        full_music_path = self.check_music_exists(music_file)
        if not full_music_path:
            return

        try:
            volume = game.music_volumes.get(self.INTRO, game.music_volume)
            self.play(game, music_file, full_music_path, volume)

            print(f"Tocando música do menu: {music_file} (volume: {volume})")
        except pygame.error as e:
            print(f"Erro ao carregar música do menu {music_file}: {e}")

    def play_level_music(self, game, level):
        """Tocar a música correspondente ao nível"""

        if level in game.music_files:
            music_file = game.music_files[level]
        else:
            print(f"Música não encontrada para o nível {level}")
            return

        if not self.check_music_exists(music_file):
            return

        full_music_path = resource_path(music_file)

        try:
            try:
                with open(full_music_path, "rb") as f:
                    normal_bytes = f.read()
            except Exception:
                normal_bytes = None
            try:
                base, ext = os.path.splitext(music_file)
                slow_file = f"{base}_slow{ext}"
            except Exception:
                slow_file = None
            slow_path = resource_path(slow_file) if slow_file else None
            try:
                if slow_path and os.path.exists(slow_path):
                    with open(slow_path, "rb") as f:
                        slow_bytes = f.read()
                else:
                    slow_bytes = None
            except Exception:
                slow_bytes = None
            game._music_cache = {
                "normal_file": music_file,
                "normal_bytes": normal_bytes,
                "slow_file": slow_file,
                "slow_bytes": slow_bytes,
            }
            volume = game.music_volumes.get(music_file, game.music_volume)
            self.play(game, music_file, full_music_path, volume)

            print(f"Tocando música do nível {level}: {music_file} (volume: {volume})")
        except pygame.error as e:
            print(f"Erro ao carregar música {music_file}: {e}")

    def play_music(self, music_type):
        """Tocar música especial (capture, credits, etc.)"""
        # Para músicas especiais, usar um volume padrão
        volume = 0.7
        
        # Mapear tipos de música para arquivos
        special_music_files = {
            "capture": "musicas/capture.mp3",
            "credits": "musicas/credits.mp3"
        }
        
        if music_type not in special_music_files:
            print(f"Tipo de música especial não encontrado: {music_type}")
            return
            
        music_file = special_music_files[music_type]
        full_music_path = self.check_music_exists(music_file)
        
        if not full_music_path:
            print(f"Arquivo de música não encontrado: {music_file}")
            return
            
        try:
            # Parar música atual se estiver tocando
            pygame.mixer.music.stop()
            # Carregar e tocar música
            pygame.mixer.music.load(full_music_path)
            # Usar volume específico para esta música
            pygame.mixer.music.set_volume(volume)
            # Para música de captura, tocar apenas uma vez; para outras, loop infinito
            if music_type == "capture":
                pygame.mixer.music.play(0)  # 0 = tocar apenas uma vez
            else:
                pygame.mixer.music.play(-1)  # -1 para loop infinito
            print(f"Tocando música especial: {music_type} ({music_file})")
        except pygame.error as e:
            print(f"Erro ao carregar música especial {music_file}: {e}")

    def play(self, game, music_file, full_music_path, volume):
        # Parar música atual se estiver tocando
        pygame.mixer.music.stop()
        # Carregar e tocar música
        pygame.mixer.music.load(full_music_path)
        # Usar volume específico para esta música
        pygame.mixer.music.set_volume(volume)
        pygame.mixer.music.play(-1)  # -1 para loop infinito
        game.current_music = music_file

    def stop_music(self):
        """Parar qualquer música em execução (compatível com chamadas do jogo)."""
        try:
            pygame.mixer.music.stop()
        except Exception:
            pass

    def enter_invincibility_music(self, game):
        """Durante invencibilidade, simula aceleração trocando para faixa mais rápida em loop."""
        try:
            # Guardar música atual para restaurar depois
            game._saved_level_music = getattr(game, "current_music", None)
            # Tocar faixa especial "capture" em loop contínuo
            special = "musicas/capture.mp3"
            full_music_path = self.check_music_exists(special)
            if not full_music_path:
                return
            pygame.mixer.music.stop()
            pygame.mixer.music.load(full_music_path)
            pygame.mixer.music.set_volume(0.8)
            pygame.mixer.music.play(-1)
        except Exception:
            pass

    def enter_tempo_music(self, game):
        try:
            game._tempo_music_active = True
            game._saved_level_music = getattr(game, "current_music", None)
            prev = getattr(game, "current_music", None)
            if not prev:
                return
            base_vol = game.music_volumes.get(prev, game.music_volume)
            slow_vol = max(0.4, base_vol * 0.85)
            try:
                slow_bytes = None
                if hasattr(game, "_music_cache") and isinstance(getattr(game, "_music_cache", None), dict):
                    slow_bytes = game._music_cache.get("slow_bytes")
                    slow_file = game._music_cache.get("slow_file")
                else:
                    slow_file = None
            except Exception:
                slow_bytes = None
                slow_file = None
            try:
                pygame.mixer.music.fadeout(400)
            except Exception:
                pass
            if slow_bytes:
                try:
                    pygame.mixer.music.load(io.BytesIO(slow_bytes))
                    pygame.mixer.music.set_volume(slow_vol)
                    try:
                        pygame.mixer.music.play(-1, fade_ms=400)
                    except TypeError:
                        pygame.mixer.music.play(-1)
                    if slow_file:
                        game.current_music = slow_file
                except Exception:
                    pass
            else:
                try:
                    base, ext = os.path.splitext(prev)
                    slow_file2 = f"{base}_slow{ext}"
                except Exception:
                    slow_file2 = None
                slow_full = self.check_music_exists(slow_file2) if slow_file2 else None
                try:
                    if slow_full:
                        pygame.mixer.music.load(slow_full)
                        pygame.mixer.music.set_volume(slow_vol)
                        try:
                            pygame.mixer.music.play(-1, fade_ms=400)
                        except TypeError:
                            pygame.mixer.music.play(-1)
                        game.current_music = slow_file2
                    else:
                        full_prev = resource_path(prev)
                        pygame.mixer.music.load(full_prev)
                        pygame.mixer.music.set_volume(slow_vol)
                        try:
                            pygame.mixer.music.play(-1, fade_ms=400)
                        except TypeError:
                            pygame.mixer.music.play(-1)
                except Exception:
                    pass
        except Exception:
            pass

    def exit_tempo_music(self, game):
        try:
            game._tempo_music_active = False
            target = getattr(game, "_saved_level_music", None) or getattr(game, "current_music", None)
            if not target:
                return
            vol = game.music_volumes.get(target, game.music_volume)
            try:
                normal_bytes = None
                normal_file = None
                if hasattr(game, "_music_cache") and isinstance(getattr(game, "_music_cache", None), dict):
                    normal_bytes = game._music_cache.get("normal_bytes")
                    normal_file = game._music_cache.get("normal_file")
            except Exception:
                normal_bytes = None
                normal_file = None
            try:
                pygame.mixer.music.fadeout(400)
            except Exception:
                pass
            if normal_bytes:
                try:
                    pygame.mixer.music.load(io.BytesIO(normal_bytes))
                    pygame.mixer.music.set_volume(vol)
                    try:
                        pygame.mixer.music.play(-1, fade_ms=400)
                    except TypeError:
                        pygame.mixer.music.play(-1)
                    if normal_file:
                        game.current_music = normal_file
                except Exception:
                    pass
            else:
                try:
                    if not self.check_music_exists(target):
                        return
                    full_music_path = resource_path(target)
                    pygame.mixer.music.load(full_music_path)
                    pygame.mixer.music.set_volume(vol)
                    try:
                        pygame.mixer.music.play(-1, fade_ms=400)
                    except TypeError:
                        pygame.mixer.music.play(-1)
                    game.current_music = target
                except Exception:
                    pass
        except Exception:
            pass
    def exit_invincibility_music(self, game):
        """Restaurar música do nível ao terminar invencibilidade."""
        try:
            prev = getattr(game, "_saved_level_music", None)
            if prev and self.check_music_exists(prev):
                full_music_path = resource_path(prev)
                volume = game.music_volumes.get(prev, game.music_volume)
                self.play(game, prev, full_music_path, volume)
        except Exception:
            pass
