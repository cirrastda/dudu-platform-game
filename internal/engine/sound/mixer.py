class Mixer:
    def init(pygame):
        # Sistema de música - configuração otimizada para Windows
        try:
            pygame.mixer.quit()  # Garantir que não há instância anterior
            pygame.mixer.pre_init(frequency=44100, size=-16, channels=2, buffer=1024)
            pygame.mixer.init()
        except pygame.error as e:
            print(f"Erro ao inicializar mixer: {e}")
            # Fallback para inicialização padrão
            pygame.mixer.init()
