import pygame
import os
import time
import sys
from internal.utils.constants import *
from internal.utils.functions import resource_path
import threading

# Importação opcional do moviepy
try:
    from moviepy.editor import VideoFileClip
    MOVIEPY_AVAILABLE = True
except ImportError:
    MOVIEPY_AVAILABLE = False
    try:
        print(f"MoviePy não está disponível. Áudio do vídeo não será reproduzido. (Python: {sys.executable})")
        print(f"Dica: \"{sys.executable}\" -m pip install -r requirements.txt")
    except Exception:
        print("MoviePy não está disponível. Áudio do vídeo não será reproduzido.")


class VideoPlayer:
    def __init__(self):
        self.screen_width = WIDTH
        self.screen_height = HEIGHT
        self.video_clip = None
        self.current_frame = None
        self.is_playing = False
        self.finished = False
        self.start_time = 0
        self.duration = 0
        self.fps = 30
        self.video_rect = None
        
        # Áudio usando moviepy
        self.audio_clip = None
        self.audio_thread = None
        self.has_audio = False
        
        # Fallback com imagens estáticas
        self.fallback_images = []
        self.fallback_mode = False
        self.fallback_index = 0
        self.fallback_delay = 4000  # 4000ms (4s) por imagem
        self.fallback_fade = 1000   # 1000ms (1s) de transição por esmaecimento
        self.last_fallback_time = 0

        # Áudio para fallback (pygame.mixer)
        self.fallback_music_path = None
        self.has_fallback_music = False
        self.fallback_music_started = False
        # Contexto do fallback: 'opening' (padrão) ou 'ending'
        self.fallback_context = "opening"
        
    def load_video(self, video_path):
        """Carregar vídeo para reprodução usando moviepy"""
        try:
            # Verificar se o arquivo existe
            full_path = resource_path(video_path)

            # Definir contexto pelo nome do arquivo
            try:
                base = os.path.basename(video_path).lower()
                self.fallback_context = "ending" if ("ending" in base or "final" in base) else "opening"
            except Exception:
                self.fallback_context = "opening"

            if not os.path.exists(full_path):
                print(f"Arquivo de vídeo não encontrado: {full_path}")
                return self.load_fallback_video()
                
            # Tentar carregar com moviepy se disponível
            if MOVIEPY_AVAILABLE:
                try:

                    self.video_clip = VideoFileClip(full_path)
                    self.duration = self.video_clip.duration
                    self.fps = self.video_clip.fps or 30
                    
                    # Calcular posição e tamanho para manter aspect ratio
                    video_size = self.video_clip.size  # (width, height)
                    self._calculate_video_rect(video_size)
                    
                    # Carregar áudio se disponível
                    if self.video_clip.audio:
                        self.audio_clip = self.video_clip.audio
                        self.has_audio = True

                    else:
                        self.has_audio = False

                    

                    
                    return True
                    
                except Exception as e:
                    print(f"Erro ao carregar vídeo com MoviePy: {e}")
                    return self.load_fallback_video()
            else:
                print("MoviePy não disponível, usando modo fallback")
                return self.load_fallback_video()
                
        except Exception as e:
            print(f"Erro ao carregar vídeo: {e}")
            return self.load_fallback_video()
    
    def _calculate_video_rect(self, video_size):
        """Calcular posição e tamanho do vídeo para ocupar toda a tela"""
        video_width, video_height = video_size
        video_aspect = video_width / video_height
        screen_aspect = self.screen_width / self.screen_height
        
        # Fazer o vídeo ocupar toda a tela, cortando se necessário para manter aspect ratio
        if video_aspect > screen_aspect:
            # Vídeo é mais largo que a tela - ajustar pela altura
            new_height = self.screen_height
            new_width = int(self.screen_height * video_aspect)
            x = (self.screen_width - new_width) // 2
            y = 0
        else:
            # Vídeo é mais alto que a tela - ajustar pela largura
            new_width = self.screen_width
            new_height = int(self.screen_width / video_aspect)
            x = 0
            y = (self.screen_height - new_height) // 2
        
        self.video_rect = pygame.Rect(x, y, new_width, new_height)


    def _calculate_fallback_rect(self, image_size):
        """Calcular posição e tamanho para imagens de fallback (fit dentro da tela, centralizado)."""
        img_width, img_height = image_size
        img_aspect = img_width / img_height
        screen_aspect = self.screen_width / self.screen_height

        # Ajuste para ocupar o máximo sem cortar (contain)
        if img_aspect > screen_aspect:
            # Limitar pela largura da tela
            new_width = self.screen_width
            new_height = int(new_width / img_aspect)
            x = 0
            y = (self.screen_height - new_height) // 2
        else:
            # Limitar pela altura da tela
            new_height = self.screen_height
            new_width = int(new_height * img_aspect)
            x = (self.screen_width - new_width) // 2
            y = 0

        self.video_rect = pygame.Rect(x, y, new_width, new_height)
        print(f"Fallback será exibido em: {x}, {y} com tamanho {new_width}x{new_height}")
    
    def load_fallback_video(self):
        """Carregar vídeo alternativo usando imagens estáticas"""
        self.fallback_mode = True
        self.fallback_images = []

        def try_load_series(base_dir, label):
            """Tenta carregar uma série de frames (png/jpg) em base_dir.
            Suporta nomes frame_1..frame_7 e frame1..frame7.
            """
            loaded = 0
            for i in range(1, 8):  # Assumindo até 7 imagens
                candidates = [
                    os.path.join(base_dir, f"frame_{i}.png"),
                    os.path.join(base_dir, f"frame_{i}.jpg"),
                    os.path.join(base_dir, f"frame{i}.png"),
                    os.path.join(base_dir, f"frame{i}.jpg"),
                ]
                img_path = next((p for p in candidates if os.path.exists(p)), None)
                if img_path:
                    try:
                        img = pygame.image.load(img_path).convert_alpha()
                        img_rect = img.get_rect()
                        # Calcular rect de exibição para esta imagem e redimensionar
                        self._calculate_fallback_rect((img_rect.width, img_rect.height))
                        img = pygame.transform.smoothscale(
                            img, (self.video_rect.width, self.video_rect.height)
                        ).convert_alpha()
                        self.fallback_images.append(img)
                        loaded += 1
                    except Exception as e:
                        print(f"Erro ao carregar imagem fallback ({label}) {img_path}: {e}")
            if loaded:
                print(f"Fallback: carregadas {loaded} imagens de '{label}'")
            return loaded

        # Seleção de fontes de imagens conforme contexto
        try:
            if self.fallback_context == "ending":
                # Final: priorizar imagens finais
                final_dir = resource_path("imagens/final")
                if os.path.exists(final_dir):
                    try_load_series(final_dir, "imagens/final")
                # (Opcional) pastas alternativas, caso existam
                if not self.fallback_images:
                    fb_end_a = resource_path("videos/fallback_ending")
                    fb_end_b = resource_path("videos/fallback-ending")
                    if os.path.exists(fb_end_a):
                        try_load_series(fb_end_a, "videos/fallback_ending")
                    elif os.path.exists(fb_end_b):
                        try_load_series(fb_end_b, "videos/fallback-ending")
            else:
                # Abertura: manter comportamento existente
                fallback_dir = resource_path("videos/fallback")
                if os.path.exists(fallback_dir):
                    try_load_series(fallback_dir, "videos/fallback")
                if not self.fallback_images:
                    intro_dir = resource_path("imagens/intro")
                    if os.path.exists(intro_dir):
                        try_load_series(intro_dir, "imagens/intro")
        except Exception as e:
            print(f"Fallback: erro ao selecionar imagens ({self.fallback_context}): {e}")

        # Música de fallback conforme contexto
        try:
            if self.fallback_context == "ending":
                music_path = resource_path("videos/final.mp3")
            else:
                music_path = resource_path("videos/intro.mp3")
            if os.path.exists(music_path):
                self.fallback_music_path = music_path
                self.has_fallback_music = True
                print(f"Fallback: música '{os.path.relpath(music_path)}' disponível")
            else:
                print(f"Fallback: música não encontrada para contexto '{self.fallback_context}'")
        except Exception as e:
            print(f"Fallback: erro ao localizar música ({self.fallback_context}): {e}")

        # 3) Último recurso: uma tela preta centralizada
        if not self.fallback_images:
            self._calculate_fallback_rect((400, 300))
            black_surface = pygame.Surface((self.video_rect.width, self.video_rect.height), pygame.SRCALPHA)
            black_surface.fill((0, 0, 0))
            self.fallback_images.append(black_surface.convert_alpha())
            print("Fallback: nenhuma imagem encontrada; usando tela preta")

        # Duração: 5s por imagem + 1s de fade entre pares
        num_imgs = len(self.fallback_images)
        self.duration = num_imgs * (self.fallback_delay / 1000.0) + max(0, num_imgs - 1) * (self.fallback_fade / 1000.0)
        print(f"Modo fallback ativado com {len(self.fallback_images)} imagens")
        return True
    
    def start_playback(self):
        """Iniciar reprodução do vídeo"""
        if not self.is_playing:
            self.is_playing = True
            self.finished = False
            self.start_time = time.time()
            
            if self.fallback_mode:
                self.fallback_index = 0
                self.last_fallback_time = pygame.time.get_ticks()
                # Iniciar música do fallback se disponível
                if self.has_fallback_music and self.fallback_music_path:
                    try:
                        # Parar qualquer música que esteja tocando
                        pygame.mixer.music.stop()
                        pygame.mixer.music.load(self.fallback_music_path)
                        # Ajustar volume (opcional)
                        try:
                            pygame.mixer.music.set_volume(0.8)
                        except Exception:
                            pass
                        pygame.mixer.music.play()
                        self.fallback_music_started = True
                        print("Fallback: música iniciada")
                    except Exception as e:
                        print(f"Fallback: erro ao iniciar música: {e}")
                        self.fallback_music_started = False
            
            # Iniciar áudio se disponível
            if self.has_audio and self.audio_clip:
                self._play_audio()
    
    def _play_audio(self):
        """Reproduz o áudio do vídeo usando moviepy em thread separada"""
        if not MOVIEPY_AVAILABLE or not self.audio_clip or self.audio_thread:
            return
            
        try:
            def play_audio():
                try:
                    # Parar qualquer música que esteja tocando
                    pygame.mixer.music.stop()
                    
                    # Reproduzir áudio usando moviepy
                    self.audio_clip.preview()

                except Exception as e:
                    print(f"Erro ao reproduzir áudio: {e}")
            
            self.audio_thread = threading.Thread(target=play_audio, daemon=True)
            self.audio_thread.start()

        except Exception as e:
            print(f"Erro ao iniciar thread de áudio: {e}")
    
    def update(self):
        """Atualizar o estado do vídeo"""
        if not self.is_playing:
            return
        
        if self.fallback_mode:
            # Modo fallback com imagens (5s por imagem + fade de 1s)
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.last_fallback_time
            if elapsed >= self.fallback_delay + self.fallback_fade:
                self.fallback_index += 1
                self.last_fallback_time = current_time
                if self.fallback_index >= len(self.fallback_images):
                    self.finished = True
                    self.is_playing = False
                    # Parar música do fallback ao finalizar
                    try:
                        pygame.mixer.music.stop()
                        self.fallback_music_started = False
                    except Exception:
                        pass
        else:
            # Modo vídeo real com moviepy
            elapsed_time = time.time() - self.start_time
            
            if elapsed_time >= self.duration:
                self.finished = True
                self.is_playing = False
            else:
                # Obter frame atual do vídeo
                try:
                    if self.video_clip:
                        # Obter frame no tempo atual
                        frame_array = self.video_clip.get_frame(elapsed_time)
                        # Converter para surface do pygame
                        frame_surface = pygame.surfarray.make_surface(frame_array.swapaxes(0, 1))
                        # Redimensionar para o tamanho correto
                        self.current_frame = pygame.transform.scale(frame_surface, 
                                                                  (self.video_rect.width, self.video_rect.height))
                except Exception as e:
                    print(f"Erro ao obter frame do vídeo: {e}")
                    self.finished = True
                    self.is_playing = False
    
    def draw(self, screen):
        """Desenhar o frame atual do vídeo"""
        if not self.is_playing and not self.finished:
            return
        
        if self.fallback_mode:
            # Desenhar imagem fallback com transição por esmaecimento
            if self.fallback_index < len(self.fallback_images):
                elapsed = pygame.time.get_ticks() - self.last_fallback_time
                if elapsed < self.fallback_delay or self.fallback_fade <= 0:
                    # Exibir imagem atual normalmente (centralizada e ajustada)
                    screen.blit(self.fallback_images[self.fallback_index], self.video_rect)
                else:
                    # Crossfade entre imagem atual e próxima
                    fade_elapsed = min(self.fallback_fade, elapsed - self.fallback_delay)
                    t = fade_elapsed / float(self.fallback_fade) if self.fallback_fade > 0 else 1.0

                    cur_img = self.fallback_images[self.fallback_index]
                    next_index = self.fallback_index + 1
                    next_img = self.fallback_images[next_index] if next_index < len(self.fallback_images) else None

                    # Esmaecer imagem atual (fade-out)
                    alpha_cur = int(255 * (1.0 - t))
                    cur_img.set_alpha(alpha_cur)
                    screen.blit(cur_img, self.video_rect)
                    cur_img.set_alpha(255)

                    if next_img:
                        # Esmaecer imagem próxima (fade-in)
                        alpha_next = int(255 * t)
                        next_img.set_alpha(alpha_next)
                        screen.blit(next_img, self.video_rect)
                        next_img.set_alpha(255)
                    else:
                        # Sem próxima imagem: esmaecer para preto
                        black = pygame.Surface((self.video_rect.width, self.video_rect.height))
                        black.fill((0, 0, 0))
                        black.set_alpha(int(255 * t))
                        screen.blit(black, self.video_rect)
        else:
            # Desenhar frame do vídeo
            if self.current_frame and self.video_rect:
                screen.blit(self.current_frame, self.video_rect)
    
    def stop(self):
        """Parar reprodução do vídeo"""
        self.is_playing = False
        
        # Parar áudio se estiver tocando
        if self.audio_thread and self.audio_thread.is_alive():
            try:
                self.audio_thread.join(timeout=1.0)
            except:
                pass
            self.audio_thread = None

        # Parar música do fallback se estiver tocando
        if self.fallback_music_started:
            try:
                pygame.mixer.music.stop()
            except Exception:
                pass
            self.fallback_music_started = False
    
    def is_finished(self):
        """Verificar se o vídeo terminou"""
        return self.finished
    
    def cleanup(self):
        """Limpar recursos do vídeo"""
        self.stop()
        
        if self.video_clip:
            try:
                self.video_clip.close()
            except:
                pass
            self.video_clip = None
        
        if self.audio_clip:
            try:
                self.audio_clip.close()
            except:
                pass
            self.audio_clip = None
        
        if self.audio_thread and self.audio_thread.is_alive():
            try:
                self.audio_thread.join(timeout=1.0)
            except:
                pass
            self.audio_thread = None
        
        self.current_frame = None
        self.fallback_images.clear()
        self.finished = False