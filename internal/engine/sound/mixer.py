class Mixer:
    def init(pygame):
        # Sistema de música - configuração otimizada e segura
        try:
            # Evitar reinicialização redundante
            if pygame.mixer.get_init() is None:
                try:
                    pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
                except Exception:
                    pass
                pygame.mixer.init()
        except pygame.error as e:
            print(f"Erro ao inicializar mixer: {e}")
            # Fallback para inicialização padrão
            try:
                pygame.mixer.init()
            except Exception as e2:
                print(f"Falha no fallback do mixer: {e2}")
